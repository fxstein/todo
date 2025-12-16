#!/bin/zsh

# Intelligent release script for todo.ai
# Automatically determines version bump, generates release notes, and creates release

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Release log file
RELEASE_LOG="${RELEASE_LOG:-$(pwd)/release/RELEASE_LOG.log}"

# Get GitHub user ID
get_github_user() {
    gh api user --jq .login 2>/dev/null || git config user.email 2>/dev/null | cut -d'@' -f1 || echo "unknown"
}

# Log release step with timestamp (newest entries on top)
log_release_step() {
    local step="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local user_id=$(get_github_user)

    # Create header if file doesn't exist
    if [[ ! -f "$RELEASE_LOG" ]]; then
        local generated_date=$(date)
        cat > "$RELEASE_LOG" << EOF
# Release Log File
# Format: TIMESTAMP | USER | STEP | MESSAGE
# Generated: ${generated_date}
#
EOF
    fi

    # Create log entry (flatten multi-line messages to single line)
    local flat_message=$(echo "$message" | tr '\n' ' ' | sed 's/  */ /g' | sed 's/^ *//;s/ *$//')
    local log_entry="${timestamp} | ${user_id} | ${step} | ${flat_message}"

    # Find where header ends (before the first log entry - the empty line separator)
    # Find first timestamp line (log entry), then use the line before it as header end
    local first_log_line=$(awk '/^[0-9]/ {print NR; exit}' "$RELEASE_LOG" 2>/dev/null || echo 0)

    # If no log entries found, header is entire file
    if [[ -z "$first_log_line" ]] || [[ "$first_log_line" -eq 0 ]]; then
        first_log_line=$(wc -l < "$RELEASE_LOG" 2>/dev/null || echo 4)
    fi

    # Header ends at the line before first log entry (the empty line separator)
    local header_end=$((first_log_line - 1))

    # Ensure header_end is at least the header lines (3 comment lines + empty line = 4)
    if [[ $header_end -lt 4 ]]; then
        header_end=4
    fi

    # Create new log: header + new entry + old entries
    local temp_log=$(mktemp)

    # Copy header (includes empty line separator, stops before first log entry)
    head -n "$header_end" "$RELEASE_LOG" > "$temp_log" 2>/dev/null

    # Add new entry (prepend - newest on top)
    echo "$log_entry" >> "$temp_log"

    # Append existing log entries (skip header, start from first log entry)
    if [[ $first_log_line -gt 0 ]]; then
        tail -n +$first_log_line "$RELEASE_LOG" 2>/dev/null >> "$temp_log" || true
    fi

    mv "$temp_log" "$RELEASE_LOG"
}

# Get version from todo.ai file (secondary source - for validation only)
get_file_version() {
    grep '^VERSION=' todo.ai | sed 's/VERSION="\([^"]*\)"/\1/'
}

# Get latest release version from GitHub (PRIMARY source of truth)
get_github_version() {
    # Query GitHub for the latest release tag
    local latest_tag=$(gh release list --limit 1 --json tagName --jq '.[0].tagName' 2>/dev/null || echo "")

    if [[ -z "$latest_tag" ]]; then
        # No releases found on GitHub
        echo ""
        return 1
    fi

    # Remove 'v' prefix from tag (e.g., v2.5.0 -> 2.5.0)
    echo "${latest_tag#v}"
}

# Get current version (PRIMARY: from GitHub, FALLBACK: from file if no GitHub releases)
get_current_version() {
    local github_version=$(get_github_version 2>/dev/null)

    if [[ -n "$github_version" ]]; then
        # GitHub version exists - use it as source of truth
        echo "$github_version"
    else
        # No GitHub releases yet - fall back to file version
        # This only happens for the very first release
        local file_version=$(get_file_version)
        if [[ -z "$file_version" ]]; then
            # No version in file either - default to 0.0.0
            echo "0.0.0"
        else
            echo "$file_version"
        fi
    fi
}

# Validate that file version matches GitHub version
validate_version_consistency() {
    local github_version=$(get_github_version 2>/dev/null)
    local file_version=$(get_file_version)

    # If no GitHub releases exist yet, skip validation
    if [[ -z "$github_version" ]]; then
        return 0
    fi

    # Compare versions
    if [[ "$file_version" != "$github_version" ]]; then
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${YELLOW}⚠️  VERSION MISMATCH DETECTED${NC}"
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        echo -e "${YELLOW}The VERSION variable in todo.ai does not match the latest GitHub release:${NC}"
        echo -e "  ${RED}File version (todo.ai):    ${file_version}${NC}"
        echo -e "  ${GREEN}GitHub version (releases): ${github_version}${NC}"
        echo ""
        echo -e "${YELLOW}GitHub releases are the source of truth for versioning.${NC}"
        echo -e "${YELLOW}The file version will be updated during the release process.${NC}"
        echo ""
        log_release_step "VERSION MISMATCH" "File version (${file_version}) does not match GitHub version (${github_version})"
    fi
}

# Get last tag or initial commit
get_last_tag() {
    local last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
    if [[ -z "$last_tag" ]]; then
        # No tags exist, use initial commit
        git rev-list --max-parents=0 HEAD 2>/dev/null || git log --reverse --pretty=format:%H | head -1
    else
        echo "$last_tag"
    fi
}

# Check if release is backend-only (infrastructure only, no user-facing changes)
is_backend_only_release() {
    local commit_range="$1"

    # Get list of changed files
    local changed_files
    if [[ "$commit_range" == "HEAD" ]]; then
        # HEAD only - compare to initial commit or all files
        changed_files=$(git diff --name-only "$commit_range" 2>/dev/null || echo "")
    elif [[ ! "$commit_range" =~ \.\. ]]; then
        # Single commit - use diff-tree
        changed_files=$(git diff-tree --no-commit-id --name-only -r "$commit_range" 2>/dev/null || echo "")
    else
        # Range of commits (e.g., v1.1.0..HEAD) - use diff
        changed_files=$(git diff --name-only "$commit_range" 2>/dev/null || echo "")
    fi

    if [[ -z "$changed_files" ]]; then
        return 1  # Can't determine, use normal logic
    fi

    # Backend file patterns (infrastructure only)
    local backend_patterns=(
        "^release/release\.sh$"
        "^\.cursor/rules/"
        "^\.todo\.ai/"
        "^tests/"
        "^release/RELEASE_SUMMARY\.md$"
        "^release/RELEASE_LOG\.log$"
        "^release/RELEASE_PROCESS\.md$"
        "^docs/TEST_PLAN\.md$"
        "^release/RELEASE_NUMBERING_ANALYSIS\.md$"
    )

    # Frontend file patterns (user-facing)
    local frontend_patterns=(
        "^README\.md$"
        "^docs/[^/]+\.md$"  # General docs (excluding RELEASE_PROCESS, TEST_PLAN)
        "^todo\.ai$"  # Only count if functional changes (handled separately)
    )

    local has_frontend=false
    local has_backend=false

    while IFS= read -r file; do
        [[ -z "$file" ]] && continue

        # Skip version bump commits
        if [[ "$file" == "todo.ai" ]]; then
            # Check if todo.ai changes are functional or just version bumps
            # This is handled by commit message analysis below
            continue
        fi

        # Check if frontend (user-facing docs)
        if [[ "$file" == "README.md" ]] || [[ "$file" =~ ^docs/[^/]+\.md$ ]]; then
            if [[ "$file" != "docs/TEST_PLAN.md" ]]; then
                has_frontend=true
            fi
        fi

        # Check if backend (infrastructure)
        if [[ "$file" =~ ^(release/release\.sh|\.cursor/rules/|\.todo\.ai/|tests/|release/RELEASE_SUMMARY\.md|release/RELEASE_LOG\.log|release/RELEASE_PROCESS\.md|docs/TEST_PLAN\.md|release/RELEASE_NUMBERING_ANALYSIS\.md)$ ]] ||
           [[ "$file" =~ ^release/ ]] || [[ "$file" =~ ^\.cursor/rules/ ]] ||
           [[ "$file" =~ ^\.todo\.ai/ ]] || [[ "$file" =~ ^tests/ ]]; then
            has_backend=true
        fi
    done <<< "$changed_files"

    # Return true if only backend files changed
    if [[ "$has_backend" == true ]] && [[ "$has_frontend" == false ]]; then
        return 0  # Backend-only
    else
        return 1  # Mixed or frontend
    fi
}

# Analyze commits to determine version bump (major/minor/patch)
analyze_commits() {
    local commit_range="$1"

    # If commit_range is empty, use HEAD (all commits)
    # If it doesn't contain ".." (range separator), convert to tag..HEAD
    if [[ -z "$commit_range" ]]; then
        commit_range="HEAD"
    elif [[ "$commit_range" != *".."* ]]; then
        # Tag provided without range separator - analyze commits since that tag
        commit_range="${commit_range}..HEAD"
    fi

    local highest_level="patch"

    # Get individual commit hashes to check per-commit file changes
    local commit_hashes
    if [[ "$commit_range" == "HEAD" ]]; then
        commit_hashes=$(git log "$commit_range" --pretty=format:"%H" --no-merges 2>/dev/null || echo "")
    elif [[ ! "$commit_range" =~ \.\. ]]; then
        commit_hashes="$commit_range"
    else
        commit_hashes=$(git log "$commit_range" --pretty=format:"%H" --no-merges 2>/dev/null || echo "")
    fi

    # Process each commit individually
    while IFS= read -r commit_hash || [[ -n "$commit_hash" ]]; do
        [[ -z "$commit_hash" ]] && continue

        # Get commit message for this specific commit
        local commit=$(git log -1 --pretty=format:"%s" "$commit_hash" 2>/dev/null || echo "")
        [[ -z "$commit" ]] && continue

        local lower_commit=$(echo "$commit" | tr '[:upper:]' '[:lower:]' 2>/dev/null || echo "$commit")
        local commit_level="patch"

        # Get files changed in this specific commit
        local commit_files=$(git diff-tree --no-commit-id --name-only -r "$commit_hash" 2>/dev/null || echo "")

        # Classify this commit by stepping down from highest to lowest level
        # Default is PATCH - we only need to check for MAJOR and MINOR

        # Check for MAJOR - Breaking changes (highest priority)
        # Check for explicit MAJOR tag in commit message (must contain #MAJOR as a tag, not as part of "tag" or "detection")
        if (echo "$commit" | grep -qi "#MAJOR" && ! echo "$commit" | grep -qiE "MAJOR tag|tag.*MAJOR|MAJOR.*detection|detection.*MAJOR") ||
           [[ "$lower_commit" =~ (breaking|break|!:) ]] ||
           [[ "$lower_commit" =~ ^(feat|fix|refactor|perf)!: ]]; then
            commit_level="major"
        # Check for MINOR - User-facing features
        elif [[ "$lower_commit" =~ ^(feat|feature): ]]; then
            # Check if this is a user-facing feature based on files changed in this commit
            local todo_ai_changed=false
            local cursor_rules_changed=false

            # Skip if explicitly marked as backend
            if echo "$commit" | grep -qiE "(backend|infra|release|internal|refactor|developer)"; then
                # Explicitly backend - stays PATCH (default)
                commit_level="patch"
            elif echo "$commit_files" | grep -q "^todo\.ai$"; then
                # todo.ai changed - assume user-facing unless explicitly backend
                commit_level="minor"
            elif echo "$commit_files" | grep -q "^\.cursor/rules/"; then
                # .cursor/rules/ changed - assume user-facing unless explicitly backend
                commit_level="minor"
            else
                # feat: prefix but no specific file checks - assume user-facing
                commit_level="minor"
            fi
        # Check for explicit PATCH prefixes (docs:, chore:) - these should never be MINOR
        elif [[ "$lower_commit" =~ ^(docs|chore): ]]; then
            # Explicitly PATCH - documentation and maintenance tasks are always PATCH
            commit_level="patch"
        # Check for MINOR - Feature keywords (if not backend-only)
        elif [[ "$lower_commit" =~ (add|new|implement|create|support) ]]; then
            # Check if this commit only changed backend files
            local has_frontend=false
            local has_backend=false

            while IFS= read -r file || [[ -n "$file" ]]; do
                [[ -z "$file" ]] && continue

                # Check if frontend (user-facing docs or todo.ai)
                if [[ "$file" == "README.md" ]] || [[ "$file" == "todo.ai" ]] ||
                   [[ "$file" =~ ^docs/[^/]+\.md$ ]]; then
                    if [[ "$file" != "docs/TEST_PLAN.md" ]]; then
                        has_frontend=true
                    fi
                fi

                # Check if backend (infrastructure)
                if [[ "$file" =~ ^(release/release\.sh|\.cursor/rules/|\.todo\.ai/|tests/|release/RELEASE_SUMMARY\.md|release/RELEASE_LOG\.log|release/RELEASE_PROCESS\.md|docs/TEST_PLAN\.md|release/RELEASE_NUMBERING_ANALYSIS\.md)$ ]] ||
                   [[ "$file" =~ ^release/ ]] || [[ "$file" =~ ^\.cursor/rules/ ]] ||
                   [[ "$file" =~ ^\.todo\.ai/ ]] || [[ "$file" =~ ^tests/ ]]; then
                    has_backend=true
                fi
            done <<< "$commit_files"

            # If only backend files changed in this commit, it stays PATCH (default)
            # Otherwise, it's MINOR
            if [[ "$has_backend" == true ]] && [[ "$has_frontend" == false ]]; then
                # Backend-only - stays PATCH (default)
                commit_level="patch"
            else
                commit_level="minor"
            fi
        fi
        # Everything else defaults to PATCH (commit_level="patch" already set above)

        # Update highest level if this commit has a higher priority
        case "$commit_level" in
            major)
                # MAJOR is highest possible, no need to check other commits
                echo "major"
                return
                ;;
            minor)
                # Only upgrade to minor if we haven't found a major yet
                if [[ "$highest_level" != "major" ]]; then
                    highest_level="minor"
                fi
                ;;
            patch)
                # Keep patch as lowest level (default)
                ;;
        esac
    done <<< "$commit_hashes"

    # If highest level is still patch, check if entire release is backend-only
    if [[ "$highest_level" == "patch" ]] && is_backend_only_release "$commit_range"; then
        echo "patch"
        return
    fi

    # Return the highest level found
    echo "$highest_level"
}

# Calculate next version
calculate_next_version() {
    local current_version="$1"
    local bump_type="$2"

    IFS='.' read -r major minor patch <<< "$current_version"

    case "$bump_type" in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
    esac

    echo "${major}.${minor}.${patch}"
}

# Determine next beta version by querying GitHub releases
# Returns version like "1.0.0b1", "1.0.0b2", etc.
determine_beta_version() {
    local base_version="$1"  # e.g., "1.0.0"

    # Query GitHub for existing beta releases matching this base version
    # Format: v1.0.0b1, v1.0.0b2, etc.
    local existing_betas=$(gh release list --limit 100 --json tagName --jq '.[].tagName' 2>/dev/null | grep "^v${base_version}b[0-9]\+$" || echo "")

    if [[ -z "$existing_betas" ]]; then
        # No betas found for this version - use b1
        echo "${base_version}b1"
        log_release_step "BETA VERSION" "No existing betas found for ${base_version}, using b1"
        return 0
    fi

    # Find highest beta number
    local highest_beta=0
    while IFS= read -r tag; do
        # Extract beta number from tag (e.g., v1.0.0b2 -> 2)
        local beta_num=$(echo "$tag" | sed -E "s/^v${base_version}b([0-9]+)$/\1/")
        if [[ "$beta_num" =~ ^[0-9]+$ ]] && [[ $beta_num -gt $highest_beta ]]; then
            highest_beta=$beta_num
        fi
    done <<< "$existing_betas"

    # Increment for next beta
    local next_beta=$((highest_beta + 1))
    echo "${base_version}b${next_beta}"
    log_release_step "BETA VERSION" "Found existing betas up to b${highest_beta} for ${base_version}, using b${next_beta}"
}

# Detect and enforce beta requirement for major releases
# Returns 0 if OK to proceed, 1 if blocked
detect_and_enforce_beta_requirement() {
    local current_version="$1"
    local new_version="$2"
    local is_beta_release="$3"  # "true" or "false"

    # Extract major version numbers
    local current_major=$(echo "$current_version" | cut -d'.' -f1)
    local new_major=$(echo "$new_version" | cut -d'.' -f1)

    # Check if this is a major version bump
    if [[ "$new_major" -le "$current_major" ]]; then
        # Not a major bump - no beta required
        return 0
    fi

    # This is a major bump
    log_release_step "MAJOR RELEASE DETECTED" "Major version bump: ${current_version} → ${new_version}"

    # If creating a beta release, always allow
    if [[ "$is_beta_release" == "true" ]]; then
        log_release_step "BETA RELEASE" "Creating beta for major version ${new_version}"
        return 0
    fi

    # If creating stable release, check if beta exists
    echo -e "${BLUE}🔍 Checking for existing beta releases for v${new_version}...${NC}"
    local existing_betas=$(gh release list --limit 100 --json tagName --jq '.[].tagName' 2>/dev/null | grep "^v${new_version}b[0-9]\+$" || echo "")

    if [[ -z "$existing_betas" ]]; then
        # No beta found - BLOCK release
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${RED}❌ ERROR: Major release requires beta testing first${NC}"
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        echo -e "${YELLOW}This is a major version bump (${current_version} → ${new_version}).${NC}"
        echo -e "${YELLOW}Major releases MUST have at least one beta release.${NC}"
        echo ""
        echo -e "${GREEN}To create a beta:${NC}"
        echo -e "${GREEN}  ./release/release.sh --prepare --beta${NC}"
        echo ""
        echo -e "${YELLOW}After beta testing, run prepare again for stable release.${NC}"
        echo ""
        log_release_step "BETA REQUIRED ERROR" "Major release ${new_version} blocked - no beta exists. User must create beta first."
        return 1
    fi

    # Beta exists - allow proceed
    echo -e "${GREEN}✓ Found existing beta release(s) for v${new_version}${NC}"
    log_release_step "BETA VERIFIED" "Beta exists for major version ${new_version}, proceeding with stable release"
    return 0
}

# Get GitHub repository URL
get_repo_url() {
    local remote_url=$(git remote get-url origin 2>/dev/null || echo "")
    if [[ -z "$remote_url" ]]; then
        echo "https://github.com/fxstein/todo.ai"
        return
    fi

    # Convert SSH URL to HTTPS if needed
    if [[ "$remote_url" =~ git@github.com: ]]; then
        remote_url=$(echo "$remote_url" | sed 's/git@github.com:/https:\/\/github.com\//')
    fi

    # Remove .git suffix if present
    remote_url=$(echo "$remote_url" | sed 's/\.git$//')

    echo "$remote_url"
}

# Generate release notes from commits
generate_release_notes() {
    local last_tag="$1"
    local new_version="$2"
    local summary_file="${3:-}"
    local commit_range

    if [[ -z "$last_tag" ]] || [[ ! "$last_tag" =~ ^v ]]; then
        # No previous tag or not a version tag - use all commits
        commit_range="HEAD"
    else
        # Previous tag exists - use commits since that tag
        commit_range="${last_tag}..HEAD"
    fi

    local repo_url=$(get_repo_url)
    local temp_notes=$(mktemp)

    echo "## Release ${new_version}" > "$temp_notes"
    echo "" >> "$temp_notes"

    # Add AI-generated summary if provided
    if [[ -n "$summary_file" ]] && [[ -f "$summary_file" ]]; then
        echo "$(cat "$summary_file")" >> "$temp_notes"
        echo "" >> "$temp_notes"
        echo "---" >> "$temp_notes"
        echo "" >> "$temp_notes"
    fi

    # Categorize commits
    local breaking_commits=()
    local feature_commits=()
    local fix_commits=()
    local other_commits=()

    local commits
    if [[ "$commit_range" == "HEAD" ]]; then
        commits=$(git log "$commit_range" --pretty=format:"%H|%s" --no-merges 2>/dev/null || echo "")
    else
        commits=$(git log "$commit_range" --pretty=format:"%H|%s" --no-merges 2>/dev/null || echo "")
    fi

    while IFS='|' read -r hash message || [[ -n "$message" ]]; do
        [[ -z "$message" ]] && continue

        # Skip version bump commits
        if [[ "$message" =~ ^(release:|Bump version to) ]]; then
            continue
        fi

        # Skip release log commits
        if [[ "$message" =~ ^(Add release log for) ]]; then
            continue
        fi

        # Create commit link
        local commit_link="([${hash:0:7}](${repo_url}/commit/${hash}))"

        # Categorize
        if [[ "$message" =~ ^(feat|fix|refactor|perf)!: ]] || [[ "$message" =~ (breaking|BREAKING) ]]; then
            breaking_commits+=("- ${message} ${commit_link}")
        elif [[ "$message" =~ ^feat: ]] || [[ "$message" =~ ^feature: ]]; then
            feature_commits+=("- ${message#feat: } ${commit_link}")
        elif [[ "$message" =~ ^fix: ]]; then
            fix_commits+=("- ${message#fix: } ${commit_link}")
        else
            other_commits+=("- ${message} ${commit_link}")
        fi
    done <<< "$commits"

    # Write categorized commits
    if [[ ${#breaking_commits[@]} -gt 0 ]]; then
        echo "### 🔴 Breaking Changes" >> "$temp_notes"
        echo "" >> "$temp_notes"
        printf '%s\n' "${breaking_commits[@]}" >> "$temp_notes"
        echo "" >> "$temp_notes"
    fi

    if [[ ${#feature_commits[@]} -gt 0 ]]; then
        echo "### ✨ Features" >> "$temp_notes"
        echo "" >> "$temp_notes"
        printf '%s\n' "${feature_commits[@]}" >> "$temp_notes"
        echo "" >> "$temp_notes"
    fi

    if [[ ${#fix_commits[@]} -gt 0 ]]; then
        echo "### 🐛 Bug Fixes" >> "$temp_notes"
        echo "" >> "$temp_notes"
        printf '%s\n' "${fix_commits[@]}" >> "$temp_notes"
        echo "" >> "$temp_notes"
    fi

    if [[ ${#other_commits[@]} -gt 0 ]]; then
        echo "### 🔧 Other Changes" >> "$temp_notes"
        echo "" >> "$temp_notes"
        printf '%s\n' "${other_commits[@]}" >> "$temp_notes"
        echo "" >> "$temp_notes"
    fi

    echo "$temp_notes"
}

# Update version in todo.ai, pyproject.toml, and todo_ai/__init__.py
update_version() {
    local new_version="$1"

    # Use sed_inplace function if available, otherwise use direct sed
    if command -v sed_inplace &> /dev/null; then
        sed_inplace "s/^VERSION=\".*\"/VERSION=\"${new_version}\"/" todo.ai
        sed_inplace "s/^# Version: .*/# Version: ${new_version}/" todo.ai
        # Update version in pyproject.toml
        sed_inplace "s/^version = \".*\"/version = \"${new_version}\"/" pyproject.toml
        # Update version in todo_ai/__init__.py
        sed_inplace "s/^__version__ = \".*\"/__version__ = \"${new_version}\"/" todo_ai/__init__.py
    else
        # macOS or Linux compatible
        if [[ "$(uname)" == "Darwin" ]]; then
            sed -i '' "s/^VERSION=\".*\"/VERSION=\"${new_version}\"/" todo.ai
            sed -i '' "s/^# Version: .*/# Version: ${new_version}/" todo.ai
            # Update version in pyproject.toml
            sed -i '' "s/^version = \".*\"/version = \"${new_version}\"/" pyproject.toml
            # Update version in todo_ai/__init__.py
            sed -i '' "s/^__version__ = \".*\"/__version__ = \"${new_version}\"/" todo_ai/__init__.py
        else
            sed -i "s/^VERSION=\".*\"/VERSION=\"${new_version}\"/" todo.ai
            sed -i "s/^# Version: .*/# Version: ${new_version}/" todo.ai
            # Update version in pyproject.toml
            sed -i "s/^version = \".*\"/version = \"${new_version}\"/" pyproject.toml
            # Update version in todo_ai/__init__.py
            sed -i "s/^__version__ = \".*\"/__version__ = \"${new_version}\"/" todo_ai/__init__.py
        fi
    fi
}

# Convert zsh version to bash version
convert_to_bash() {
    local converter_script="release/convert_zsh_to_bash.sh"

    if [[ ! -f "$converter_script" ]]; then
        echo -e "${RED}❌ Error: Converter script not found: $converter_script${NC}"
        return 1
    fi

    # Run converter
    if ! bash "$converter_script"; then
        echo -e "${RED}❌ Error: Conversion failed${NC}"
        return 1
    fi

    return 0
}

# Main function
main() {
    local MODE="prepare"  # Default to prepare mode
    local SUMMARY_FILE=""
    local PREPARE_STATE_FILE="release/.prepare_state"
    local BETA_RELEASE=false  # Default to stable release

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --summary)
                if [[ -z "$2" ]] || [[ "$2" == --* ]]; then
                    echo -e "${RED}Error: --summary requires a file path${NC}"
                    exit 1
                fi
                SUMMARY_FILE="$2"
                shift 2
                ;;
            --prepare)
                MODE="prepare"
                shift
                ;;
            --execute)
                MODE="execute"
                shift
                ;;
            --beta)
                BETA_RELEASE=true
                shift
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                echo "Usage: $0 [--prepare|--execute] [--summary <file>] [--beta]"
                echo ""
                echo "Modes:"
                echo "  --prepare  Analyze commits and generate release preview (default)"
                echo "  --execute  Execute prepared release (no prompts)"
                echo ""
                echo "Options:"
                echo "  --beta     Create beta/pre-release (e.g., v1.0.0b1)"
                echo "  --summary  Include AI-generated summary from file"
                exit 1
                ;;
        esac
    done

    # Execute mode: load state and perform release
    if [[ "$MODE" == "execute" ]]; then
        execute_release
        return $?
    fi

    # Prepare mode (default): analyze and preview
    echo -e "${BLUE}🚀 Preparing release preview...${NC}"
    echo ""

    # Check if summary file exists if provided (no prompt, just warn)
    if [[ -n "$SUMMARY_FILE" ]] && [[ ! -f "$SUMMARY_FILE" ]]; then
        echo -e "${YELLOW}⚠️  Warning: Summary file not found: $SUMMARY_FILE (continuing without it)${NC}"
        SUMMARY_FILE=""
    fi

    # Validate summary file is not stale (newer than last release)
    if [[ -n "$SUMMARY_FILE" ]] && [[ -f "$SUMMARY_FILE" ]]; then
        # Get the last release tag
        local last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

        if [[ -n "$last_tag" ]]; then
            # Get timestamp of last release tag (seconds since epoch)
            local tag_timestamp=$(git log -1 --format=%ct "$last_tag" 2>/dev/null || echo "0")

            # Get modification time of summary file (seconds since epoch)
            if [[ "$(uname)" == "Darwin" ]]; then
                # macOS stat command
                local summary_mtime=$(stat -f %m "$SUMMARY_FILE" 2>/dev/null || echo "0")
            else
                # Linux stat command
                local summary_mtime=$(stat -c %Y "$SUMMARY_FILE" 2>/dev/null || echo "0")
            fi

            # Compare timestamps
            if [[ "$summary_mtime" -lt "$tag_timestamp" ]]; then
                echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
                echo -e "${RED}⚠️  STALE SUMMARY FILE DETECTED${NC}"
                echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
                echo ""
                echo -e "${YELLOW}The release summary file is older than the last release:${NC}"
                echo -e "  Summary file: ${SUMMARY_FILE}"
                echo -e "  Last release: ${last_tag} ($(git log -1 --format=%cd --date=format:'%Y-%m-%d %H:%M:%S' "$last_tag"))"
                echo -e "  File modified: $(date -r "$summary_mtime" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || date -d "@$summary_mtime" '+%Y-%m-%d %H:%M:%S')"
                echo ""
                echo -e "${YELLOW}This suggests the summary may be from a previous release.${NC}"
                echo -e "${YELLOW}You should update the summary file for this release.${NC}"
                echo ""

                # Check if we're in interactive mode
                if [[ -t 0 ]]; then
                    read -p "Continue anyway? (y/N): " -n 1 -r
                    echo
                    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                        echo -e "${BLUE}Release aborted. Please update the summary file.${NC}"
                        exit 1
                    fi
                    echo -e "${YELLOW}⚠️  Proceeding with potentially stale summary...${NC}"
                    echo ""
                else
                    # Non-interactive mode: abort by default
                    echo -e "${RED}Running in non-interactive mode - aborting.${NC}"
                    echo -e "${BLUE}Please update the summary file and try again.${NC}"
                    exit 1
                fi
            fi
        fi
    fi

    # Verify prerequisites
    if ! command -v gh &> /dev/null; then
        echo -e "${RED}❌ Error: GitHub CLI (gh) is not installed${NC}"
        echo "Install it with: brew install gh"
        exit 1
    fi

    # Verify we're on main branch (no prompt, just warn)
    CURRENT_BRANCH=$(git branch --show-current)
    if [[ "$CURRENT_BRANCH" != "main" ]]; then
        echo -e "${YELLOW}⚠️  Warning: Not on main branch (current: $CURRENT_BRANCH)${NC}"
        echo -e "${YELLOW}   Releases should be created from main branch${NC}"
        echo ""
    fi

    # Check for uncommitted changes (filter out weird backup files)
    local status_output=$(git status -s)
    local uncommitted=""

    # Filter out files that should be ignored during release
    while IFS= read -r line; do
        # Skip weird backup files like "todo.ai ''"
        if [[ "$line" =~ ^[?]{2}[[:space:]]+\"todo\.ai ]]; then
            continue
        fi
        # Skip RELEASE_LOG.log - it will be committed at the end after all release operations
        if echo "$line" | grep -qE "release/RELEASE_LOG\.log|^RELEASE_LOG\.log"; then
            continue
        fi
        # Skip .todo.ai/.todo.ai.serial and .todo.ai/.todo.ai.log - these are normal operational files
        # They change whenever tasks are added/completed, which is expected behavior
        # Excluding them prevents blocking releases due to normal task management activity
        if echo "$line" | grep -qE "\.todo\.ai/\.todo\.ai\.(serial|log)"; then
            continue
        fi
        # All other files are uncommitted
        if [[ -n "$line" ]]; then
            if [[ -n "$uncommitted" ]]; then
                uncommitted="${uncommitted}\n${line}"
            else
                uncommitted="$line"
            fi
        fi
    done <<< "$status_output"

    # If RELEASE_SUMMARY.md exists and is uncommitted, we'll commit it as part of the release
    local summary_needs_commit=false
    if [[ -n "$SUMMARY_FILE" ]] && [[ -f "$SUMMARY_FILE" ]]; then
        # Check if file appears in status output (untracked or modified)
        if echo "$status_output" | grep -qF "$SUMMARY_FILE"; then
            summary_needs_commit=true
            log_release_step "SUMMARY DETECTED" "Found uncommitted summary file: ${SUMMARY_FILE} - will commit as part of release"
            # Remove it from uncommitted list so it doesn't block the release
            # Use fixed string matching (F flag) instead of regex
            uncommitted=$(echo -e "$uncommitted" | grep -vF "$SUMMARY_FILE" || true)
        fi
    fi

    # Auto-commit any remaining uncommitted changes (except those already handled)
    if [[ -n "$uncommitted" ]]; then
        echo -e "${YELLOW}⚠️  Auto-committing uncommitted changes before release...${NC}"
        echo "Uncommitted files:"
        echo -e "$uncommitted"
        echo ""

        # Add all remaining uncommitted files
        local uncommitted_files=$(echo -e "$uncommitted" | sed 's/^[?AM] */ /' | sed 's/^ //' | grep -v "^$" || true)
        for file in ${uncommitted_files[@]}; do
            if [[ -f "$file" ]]; then
                echo "Adding: $file"
                git add "$file"
            fi
        done

        # Commit with a generic message
        local auto_commit_msg="chore: Auto-commit changes before release"
        git commit -m "$auto_commit_msg" || {
            echo -e "${RED}❌ Error: Failed to auto-commit changes${NC}"
            echo "Please commit or stash changes manually before releasing"
            log_release_step "ERROR - Auto-Commit Failed" "Failed to auto-commit uncommitted changes"
            exit 1
        }
        log_release_step "AUTO-COMMIT" "Auto-committed uncommitted changes: $uncommitted"
        echo -e "${GREEN}✓ Changes auto-committed${NC}"
        echo ""
    fi

    # Validate version consistency between file and GitHub
    validate_version_consistency

    # Get current version from GitHub (source of truth)
    CURRENT_VERSION=$(get_current_version)
    local file_version=$(get_file_version)

    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}📌 Version Information${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}Current version (GitHub):  ${CURRENT_VERSION} ✓${NC}"
    echo -e "${BLUE}File version (todo.ai):     ${file_version}${NC}"
    echo ""

    # Get last tag
    LAST_TAG=$(get_last_tag)
    if [[ "$LAST_TAG" =~ ^v ]]; then
        echo -e "${GREEN}📌 Last release: ${LAST_TAG}${NC}"
    else
        echo -e "${YELLOW}📌 No previous release found (using initial commit)${NC}"
    fi

    # Analyze commits to determine bump type
    echo ""
    echo -e "${BLUE}📊 Analyzing commits since last release...${NC}"
    BUMP_TYPE=$(analyze_commits "$LAST_TAG")

    case "$BUMP_TYPE" in
        major)
            echo -e "${RED}🔴 Major release detected (breaking changes)${NC}"
            ;;
        minor)
            echo -e "${YELLOW}🟡 Minor release detected (new features)${NC}"
            ;;
        patch)
            echo -e "${GREEN}🟢 Patch release detected (bug fixes)${NC}"
            ;;
    esac

    # Calculate next version
    local BASE_VERSION=$(calculate_next_version "$CURRENT_VERSION" "$BUMP_TYPE")

    # Determine if this is a beta or stable release
    local RELEASE_TYPE="stable"
    if [[ "$BETA_RELEASE" == true ]]; then
        RELEASE_TYPE="beta"
        NEW_VERSION=$(determine_beta_version "$BASE_VERSION")
        echo -e "${YELLOW}📌 Beta release: ${NEW_VERSION}${NC}"
    else
        NEW_VERSION="$BASE_VERSION"
        echo -e "${GREEN}📌 Proposed new version: ${NEW_VERSION}${NC}"

        # Enforce beta requirement for major releases
        if ! detect_and_enforce_beta_requirement "$CURRENT_VERSION" "$NEW_VERSION" "false"; then
            exit 1
        fi
    fi
    echo ""

    # Log release start with all details
    log_release_step "RELEASE START" "Starting release process:
- Current version (GitHub): ${CURRENT_VERSION}
- File version (todo.ai): ${file_version}
- Proposed version: ${NEW_VERSION}
- Release type: ${RELEASE_TYPE}
- Bump type: ${BUMP_TYPE}
- Last tag: ${LAST_TAG}
- Summary file: ${SUMMARY_FILE:-none}"

    # Generate release notes for preview
    echo -e "${BLUE}📝 Generating release notes preview...${NC}"
    if [[ -n "$SUMMARY_FILE" ]] && [[ -f "$SUMMARY_FILE" ]]; then
        echo -e "${GREEN}📄 Including AI-generated summary from: $SUMMARY_FILE${NC}"
    fi
    local preview_notes_file=$(generate_release_notes "$LAST_TAG" "$NEW_VERSION" "$SUMMARY_FILE")

    # Show release notes preview
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    cat "$preview_notes_file"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # Clean up preview file
    rm -f "$preview_notes_file"

    # Show review recommendation if major or large release
    local last_tag_for_count=$(get_last_tag)
    local commit_range_for_count
    if [[ -z "$last_tag_for_count" ]] || [[ ! "$last_tag_for_count" =~ ^v ]]; then
        commit_range_for_count="HEAD"
    else
        commit_range_for_count="${last_tag_for_count}..HEAD"
    fi
    local commit_count=$(git log "$commit_range_for_count" --oneline --no-merges 2>/dev/null | wc -l | tr -d ' ')

    if [[ "$BUMP_TYPE" == "major" ]]; then
        echo -e "${YELLOW}⚠️  Major release detected - please review carefully before executing${NC}"
        echo ""
    elif [[ $commit_count -gt 10 ]]; then
        echo -e "${YELLOW}⚠️  Large release ($commit_count commits) - please review carefully before executing${NC}"
        echo ""
    fi

    # Convert to bash version
    if ! convert_to_bash; then
        echo -e "${RED}❌ Error: Bash conversion failed${NC}"
        log_release_step "ERROR - Bash Conversion Failed" "Failed to convert zsh version to bash"
        exit 1
    fi
    log_release_step "BASH CONVERSION" "Successfully converted todo.ai to todo.bash"

    # Determine if this is a major release
    local current_major=$(echo "$CURRENT_VERSION" | cut -d'.' -f1)
    local new_major=$(echo "$BASE_VERSION" | cut -d'.' -f1)
    local IS_MAJOR="false"
    if [[ "$new_major" -gt "$current_major" ]]; then
        IS_MAJOR="true"
    fi

    # Get prepared_at timestamp
    local PREPARED_AT=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

    # Get prepared_by user
    local PREPARED_BY=$(get_github_user)

    # Save prepare state for execute mode
    # Note: RELEASE_NOTES_FILE is NOT saved - it will be regenerated during execute
    # to ensure RELEASE_SUMMARY.md is the single source of truth
    cat > "$PREPARE_STATE_FILE" << EOF
NEW_VERSION=$NEW_VERSION
BUMP_TYPE=$BUMP_TYPE
CURRENT_VERSION=$CURRENT_VERSION
LAST_TAG=$LAST_TAG
SUMMARY_FILE=$SUMMARY_FILE
summary_needs_commit=$summary_needs_commit
RELEASE_TYPE=$RELEASE_TYPE
BASE_VERSION=$BASE_VERSION
IS_MAJOR=$IS_MAJOR
PREPARED_AT=$PREPARED_AT
PREPARED_BY=$PREPARED_BY
GIT_TAG=v${NEW_VERSION}
EOF
    log_release_step "PREPARE" "Release preview prepared for v${NEW_VERSION} (${RELEASE_TYPE})"

    # Display execution command
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ Release preview prepared successfully!${NC}"
    echo ""
    echo -e "${GREEN}📋 Version: ${CURRENT_VERSION} → ${NEW_VERSION}${NC}"
    if [[ "$RELEASE_TYPE" == "beta" ]]; then
        echo -e "${YELLOW}📋 Type: Beta pre-release (${BUMP_TYPE})${NC}"
        echo -e "${YELLOW}📋 Base version: ${BASE_VERSION}${NC}"
    else
        echo -e "${GREEN}📋 Type: Stable ${BUMP_TYPE} release${NC}"
    fi
    echo -e "${GREEN}📋 Commits: ${commit_count}${NC}"
    echo ""
    echo -e "${GREEN}To execute this release, run:${NC}"
    echo -e "${GREEN}  ./release/release.sh --execute${NC}"
    if [[ "$RELEASE_TYPE" == "beta" ]]; then
        echo ""
        echo -e "${YELLOW}After beta testing, create stable release with:${NC}"
        echo -e "${YELLOW}  ./release/release.sh --prepare${NC}"
    fi
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    return 0
}

# Execute prepared release
execute_release() {
    local PREPARE_STATE_FILE="release/.prepare_state"

    # Check if prepare was run
    if [[ ! -f "$PREPARE_STATE_FILE" ]]; then
        echo -e "${RED}❌ Error: Release not prepared${NC}"
        echo "Please run: ./release/release.sh --prepare [--summary <file>]"
        exit 1
    fi

    # Load prepared state
    source "$PREPARE_STATE_FILE"

    echo -e "${BLUE}🚀 Executing release ${NEW_VERSION}...${NC}"
    echo ""

    # Regenerate release notes from RELEASE_SUMMARY.md (single source of truth)
    # This ensures any updates to the summary after prepare are included
    echo -e "${BLUE}📝 Generating release notes from ${SUMMARY_FILE:-commits}...${NC}"
    RELEASE_NOTES_FILE=$(generate_release_notes "$LAST_TAG" "$NEW_VERSION" "$SUMMARY_FILE")
    echo -e "${GREEN}✓ Release notes generated${NC}"
    echo ""

    # Update version
    echo -e "${BLUE}📝 Updating version in todo.ai, pyproject.toml, and todo_ai/__init__.py...${NC}"
    log_release_step "UPDATE VERSION" "Updating version in todo.ai, pyproject.toml, and todo_ai/__init__.py from ${CURRENT_VERSION} to ${NEW_VERSION}"
    update_version "$NEW_VERSION"

    # Verify all files were updated correctly
    if ! grep -q "^VERSION=\"${NEW_VERSION}\"" todo.ai 2>/dev/null; then
        echo -e "${RED}❌ Error: Version update failed in todo.ai${NC}"
        log_release_step "VERSION UPDATE ERROR" "Failed to update version in todo.ai to ${NEW_VERSION}"
        exit 1
    fi
    if ! grep -q "^version = \"${NEW_VERSION}\"" pyproject.toml 2>/dev/null; then
        echo -e "${RED}❌ Error: Version update failed in pyproject.toml${NC}"
        log_release_step "VERSION UPDATE ERROR" "Failed to update version in pyproject.toml to ${NEW_VERSION}"
        exit 1
    fi
    if ! grep -q "^__version__ = \"${NEW_VERSION}\"" todo_ai/__init__.py 2>/dev/null; then
        echo -e "${RED}❌ Error: Version update failed in todo_ai/__init__.py${NC}"
        log_release_step "VERSION UPDATE ERROR" "Failed to update version in todo_ai/__init__.py to ${NEW_VERSION}"
        exit 1
    fi
    echo -e "${GREEN}✓ Verified version updated in todo.ai, pyproject.toml, and todo_ai/__init__.py${NC}"
    log_release_step "VERSION UPDATED" "Version updated successfully in todo.ai, pyproject.toml, and todo_ai/__init__.py"

    # Commit version change and summary file
    echo -e "${BLUE}💾 Committing version change and release summary...${NC}"
    log_release_step "COMMIT VERSION" "Committing version change to git"
    git add todo.ai pyproject.toml todo_ai/__init__.py

    # Commit summary file if it exists and is uncommitted
    if [[ "$summary_needs_commit" == true ]] && [[ -n "$SUMMARY_FILE" ]] && [[ -f "$SUMMARY_FILE" ]]; then
        log_release_step "COMMIT SUMMARY" "Adding release summary file to commit: ${SUMMARY_FILE}"
        git add "$SUMMARY_FILE"
    fi

    # Commit TODO.md and .todo.ai files if they're uncommitted (they should always be committed together)
    local todo_status=$(git status -s | grep -E "(TODO\.md|\.todo\.ai/)" || echo "")
    if [[ -n "$todo_status" ]]; then
        if echo "$todo_status" | grep -q "TODO.md"; then
            log_release_step "COMMIT TODO" "Adding TODO.md to commit"
            git add TODO.md
        fi
        if echo "$todo_status" | grep -qE "\.todo\.ai/"; then
            log_release_step "COMMIT TODO_DATA" "Adding .todo.ai/ files to commit"
            git add .todo.ai/.todo.ai.serial .todo.ai/.todo.ai.log 2>/dev/null || true
        fi
    fi

    # Add todo.bash if it was converted (should always be the case after prepare)
    if [[ -f "todo.bash" ]]; then
        git add todo.bash
    fi

    # Create version commit message
    local commit_message="release: Version ${NEW_VERSION}"
    if [[ -n "$SUMMARY_FILE" ]] && [[ -f "$SUMMARY_FILE" ]] && [[ "$summary_needs_commit" == true ]]; then
        commit_message="${commit_message}

Includes release summary from ${SUMMARY_FILE}"
    fi

    # Commit the version change
    local commit_output=$(git commit -m "$commit_message" 2>&1 || echo "no commit needed")
    log_release_step "VERSION COMMITTED" "Version change committed: ${commit_output}"

    # Get the commit hash for the version change
    local version_commit_hash=$(git rev-parse HEAD 2>/dev/null || echo "")

    # Verify version was actually updated in the commit
    if [[ -n "$version_commit_hash" ]]; then
        if ! git show "$version_commit_hash":todo.ai 2>/dev/null | grep -q "^VERSION=\"${NEW_VERSION}\""; then
            echo -e "${YELLOW}⚠️  Note: Version in working directory but not yet committed${NC}"
            echo -e "${YELLOW}   This is expected if version was updated in a previous failed attempt${NC}"
        fi
    fi

    # Create and push tag
    TAG="v${NEW_VERSION}"
    echo -e "${BLUE}🏷️  Creating tag ${TAG}...${NC}"
    log_release_step "CREATE TAG" "Creating git tag: ${TAG} pointing to commit ${version_commit_hash}"
    # Explicitly tag the commit hash to ensure we're tagging the right commit
    git tag -a "$TAG" -m "Release version $NEW_VERSION" "$version_commit_hash" > /dev/null 2>&1
    log_release_step "TAG CREATED" "Git tag ${TAG} created successfully at commit ${version_commit_hash}"

    # Verify tag points to commit with correct version
    if ! git show "$TAG":todo.ai 2>/dev/null | grep -q "^VERSION=\"${NEW_VERSION}\""; then
        echo -e "${RED}❌ Error: Tag verification failed${NC}"
        echo "Tag does not point to commit with correct version in todo.ai or pyproject.toml"
        log_release_step "TAG VERIFY ERROR" "Tag ${TAG} verification failed - tag doesn't point to commit with VERSION=${NEW_VERSION} in todo.ai or pyproject.toml"
        exit 1
    fi

    echo -e "${BLUE}📤 Pushing to remote...${NC}"
    log_release_step "PUSH MAIN" "Pushing main branch to origin"
    git push origin main > /dev/null 2>&1 || log_release_step "PUSH ERROR" "Failed to push main branch"

    log_release_step "PUSH TAG" "Pushing tag ${TAG} to origin"
    git push origin "$TAG" > /dev/null 2>&1 || log_release_step "PUSH ERROR" "Failed to push tag ${TAG}"

    # Create GitHub release with assets
    echo -e "${BLUE}📦 Creating GitHub release with assets...${NC}"
    log_release_step "CREATE GITHUB RELEASE" "Creating GitHub release for tag ${TAG} with assets: todo.ai, todo.bash, install.sh"

    # Verify assets exist
    if [[ ! -f "todo.ai" ]]; then
        echo -e "${RED}❌ Error: todo.ai not found${NC}"
        exit 1
    fi
    if [[ ! -f "todo.bash" ]]; then
        echo -e "${RED}❌ Error: todo.bash not found (should have been created by prepare step)${NC}"
        exit 1
    fi
    if [[ ! -f "install.sh" ]]; then
        echo -e "${RED}❌ Error: install.sh not found${NC}"
        exit 1
    fi

    echo -e "  ${GREEN}✓ todo.ai (zsh version)${NC}"
    echo -e "  ${GREEN}✓ todo.bash (bash version)${NC}"
    echo -e "  ${GREEN}✓ install.sh (smart installer)${NC}"

    # Temporarily disable set -e to capture error
    set +e
    # Check if release already exists (shouldn't happen, but handle gracefully)
    if gh release view "$TAG" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Release ${TAG} already exists, attaching assets...${NC}"
        log_release_step "GITHUB RELEASE EXISTS" "Release ${TAG} already exists, attaching shell script assets"
        local release_output=$(gh release upload "$TAG" \
            todo.ai \
            todo.bash \
            install.sh \
            --clobber 2>&1)
        local release_status=$?
    else
        # Create new release with shell script assets
        # Note: GitHub Actions workflow will attach Python package (dist/*) after PyPI publish
        local release_output=$(gh release create "$TAG" \
            --title "$NEW_VERSION" \
            --notes-file "$RELEASE_NOTES_FILE" \
            todo.ai \
            todo.bash \
            install.sh 2>&1)
        local release_status=$?
    fi
    set -e

    if [[ $release_status -eq 0 ]]; then
        log_release_step "GITHUB RELEASE CREATED" "GitHub release created/updated successfully for ${TAG}\nOutput: ${release_output}\nNote: Python package will be attached by GitHub Actions workflow"
        echo -e "${GREEN}✓ GitHub release created/updated${NC}"
        echo -e "${BLUE}  Note: Python package (dist/*) will be automatically attached by CI/CD workflow${NC}"
    else
        log_release_step "GITHUB RELEASE ERROR" "Failed to create/update GitHub release for ${TAG}\nError: ${release_output}\nExit code: ${release_status}"
        echo -e "${RED}⚠️  Warning: GitHub release creation failed${NC}"
        echo "Error: ${release_output}"
        echo "Check the release log: ${RELEASE_LOG}"
        echo "Try manually: gh release view ${TAG} || gh release create ${TAG} --title ${NEW_VERSION} --notes-file <file>"
    fi

    # Cleanup
    rm -f "$RELEASE_NOTES_FILE"

    local repo_url=$(get_repo_url)
    log_release_step "RELEASE COMPLETE" "Release ${NEW_VERSION} published successfully!
- Tag: ${TAG}
- URL: ${repo_url}/releases/tag/${TAG}
- Release log: ${RELEASE_LOG}"

    # Commit and push RELEASE_LOG.log at the very end to capture all release operations
    # Note: We don't log these operations since they happen after the log is committed
    if [[ -f "$RELEASE_LOG" ]]; then
        echo -e "${BLUE}📋 Committing release log...${NC}"
        git add "$RELEASE_LOG"
        local log_commit=$(git commit -m "Add release log for ${NEW_VERSION}" 2>&1 || echo "no commit needed")

        if [[ "$log_commit" != "no commit needed" ]]; then
            echo -e "${GREEN}✓ Release log committed${NC}"
            echo -e "${BLUE}📤 Pushing release log...${NC}"
            git push origin main > /dev/null 2>&1 && echo -e "${GREEN}✓ Release log pushed${NC}" || echo -e "${YELLOW}⚠️  Release log push may have failed${NC}"
        else
            echo -e "${GREEN}✓ Release log already committed${NC}"
        fi
    fi

    echo ""
    echo -e "${GREEN}✅ Release ${NEW_VERSION} published successfully!${NC}"
    echo -e "${GREEN}🔗 View release: ${repo_url}/releases/tag/${TAG}${NC}"
    echo -e "${GREEN}📋 Release log: ${RELEASE_LOG}${NC}"
}

# Run main function
main "$@"
