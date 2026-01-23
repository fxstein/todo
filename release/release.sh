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

# Version helpers (supports X.Y.Z and X.Y.ZbN)
is_valid_version() {
    [[ "$1" =~ ^[0-9]+\.[0-9]+\.[0-9]+(b[0-9]+)?$ ]]
}

is_beta_version() {
    [[ "$1" =~ ^[0-9]+\.[0-9]+\.[0-9]+b[0-9]+$ ]]
}

get_base_version() {
    echo "$1" | sed -E 's/^([0-9]+\.[0-9]+\.[0-9]+)b[0-9]+$/\1/'
}

get_beta_number() {
    echo "$1" | sed -nE 's/^.*b([0-9]+)$/\1/p'
}

compare_versions() {
    local a="$1"
    local b="$2"

    IFS='.' read -r a_major a_minor a_patch <<< "$(get_base_version "$a")"
    IFS='.' read -r b_major b_minor b_patch <<< "$(get_base_version "$b")"

    if [[ $a_major -ne $b_major ]]; then
        [[ $a_major -gt $b_major ]] && echo 1 || echo -1
        return
    fi
    if [[ $a_minor -ne $b_minor ]]; then
        [[ $a_minor -gt $b_minor ]] && echo 1 || echo -1
        return
    fi
    if [[ $a_patch -ne $b_patch ]]; then
        [[ $a_patch -gt $b_patch ]] && echo 1 || echo -1
        return
    fi

    local a_beta=$(get_beta_number "$a")
    local b_beta=$(get_beta_number "$b")

    if [[ -z "$a_beta" ]] && [[ -z "$b_beta" ]]; then
        echo 0
        return
    fi
    if [[ -z "$a_beta" ]] && [[ -n "$b_beta" ]]; then
        echo 1
        return
    fi
    if [[ -n "$a_beta" ]] && [[ -z "$b_beta" ]]; then
        echo -1
        return
    fi

    if [[ "$a_beta" -gt "$b_beta" ]]; then
        echo 1
    elif [[ "$a_beta" -lt "$b_beta" ]]; then
        echo -1
    else
        echo 0
    fi
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

# Validate beta maturity before stable release (warning only, never blocks)
# Returns 0 (always succeeds, just warns)
validate_beta_maturity() {
    local new_version="$1"
    local bump_type="$2"

    # Find latest beta for this version from GitHub releases
    local latest_beta=$(gh release list --limit 100 --json tagName,publishedAt --jq '.[] | select(.tagName | test("^v'"${new_version}"'b[0-9]+$")) | {tagName, publishedAt}' 2>/dev/null | head -1)

    if [[ -z "$latest_beta" ]]; then
        # No beta found - this shouldn't happen if enforcement worked, but don't block
        log_release_step "BETA MATURITY" "No beta found for ${new_version}, skipping maturity check"
        return 0
    fi

    # Extract published date
    local beta_published=$(echo "$latest_beta" | grep -o '"publishedAt":"[^"]*"' | cut -d'"' -f4)
    if [[ -z "$beta_published" ]]; then
        log_release_step "BETA MATURITY" "Could not determine beta publish date, skipping maturity check"
        return 0
    fi

    # Calculate days since beta was published
    local beta_timestamp=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$beta_published" "+%s" 2>/dev/null || date -d "$beta_published" "+%s" 2>/dev/null || echo "0")
    local now_timestamp=$(date "+%s")
    local days_since_beta=$(( (now_timestamp - beta_timestamp) / 86400 ))

    # Determine recommended duration based on bump type
    local recommended_days=7
    if [[ "$bump_type" == "minor" ]]; then
        recommended_days=2
    fi

    # Extract beta tag name
    local beta_tag=$(echo "$latest_beta" | grep -o '"tagName":"[^"]*"' | cut -d'"' -f4)

    # Warn if under recommended duration (but never block)
    if [[ $days_since_beta -lt $recommended_days ]]; then
        local days_remaining=$((recommended_days - days_since_beta))
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${YELLOW}⚠️  WARNING: Beta released only ${days_since_beta} day(s) ago${NC}"
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        echo -e "${YELLOW}Last beta: ${beta_tag}${NC}"
        echo -e "${YELLOW}Published: ${beta_published}${NC}"
        echo -e "${YELLOW}Recommended wait: ${days_remaining} more day(s) for feedback${NC}"
        echo ""
        echo -e "${BLUE}Proceeding with release...${NC}"
        echo ""
        log_release_step "BETA MATURITY WARNING" "Beta ${beta_tag} only ${days_since_beta} days old (recommended: ${recommended_days}), but proceeding"
    else
        echo -e "${GREEN}✓ Beta testing period met (${days_since_beta} days)${NC}"
        log_release_step "BETA MATURITY OK" "Beta ${beta_tag} is ${days_since_beta} days old (recommended: ${recommended_days})"
    fi

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
generate_release_summary() {
    local ai_summary_file="${1:-}"
    local summary_file="release/RELEASE_SUMMARY.md"

    if [[ -n "$ai_summary_file" ]] && [[ -f "$ai_summary_file" ]]; then
        cat "$ai_summary_file" > "$summary_file"
        echo "" >> "$summary_file"
        echo "$summary_file"
        return 0
    fi

    return 1
}

# Generate release notes from commits
generate_release_notes() {
    local last_tag="$1"
    local new_version="$2"
    local summary_file="${3:-}"
    local commit_range
    local is_beta=false

    if [[ "$new_version" =~ ^[0-9]+\.[0-9]+\.[0-9]+b[0-9]+$ ]]; then
        is_beta=true
    fi

    if [[ -z "$last_tag" ]] || [[ ! "$last_tag" =~ ^v ]]; then
        # No previous tag or not a version tag - use all commits
        commit_range="HEAD"
    else
        # Previous tag exists - use commits since that tag
        commit_range="${last_tag}..HEAD"
    fi

    local repo_url=$(get_repo_url)
    local notes_file="release/RELEASE_NOTES.md"

    echo "## Release ${new_version}" > "$notes_file"
    echo "" >> "$notes_file"

    # Add AI-generated summary if provided
    if [[ -n "$summary_file" ]] && [[ -f "$summary_file" ]]; then
        echo "$(cat "$summary_file")" >> "$notes_file"
        echo "" >> "$notes_file"
        echo "---" >> "$notes_file"
        echo "" >> "$notes_file"
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
        echo "### 🔴 Breaking Changes" >> "$notes_file"
        echo "" >> "$notes_file"
        printf '%s\n' "${breaking_commits[@]}" >> "$notes_file"
        echo "" >> "$notes_file"
    fi

    if [[ ${#feature_commits[@]} -gt 0 ]]; then
        echo "### ✨ Features" >> "$notes_file"
        echo "" >> "$notes_file"
        printf '%s\n' "${feature_commits[@]}" >> "$notes_file"
        echo "" >> "$notes_file"
    fi

    if [[ ${#fix_commits[@]} -gt 0 ]]; then
        echo "### 🐛 Bug Fixes" >> "$notes_file"
        echo "" >> "$notes_file"
        printf '%s\n' "${fix_commits[@]}" >> "$notes_file"
        echo "" >> "$notes_file"
    fi

    if [[ ${#other_commits[@]} -gt 0 ]]; then
        echo "### 🔧 Other Changes" >> "$notes_file"
        echo "" >> "$notes_file"
        printf '%s\n' "${other_commits[@]}" >> "$notes_file"
        echo "" >> "$notes_file"
    fi

    if [[ "$is_beta" == true ]] && [[ -n "$last_tag" ]] && [[ "$last_tag" =~ ^v ]]; then
        local previous_notes
        previous_notes=$(git show "${last_tag}:release/RELEASE_NOTES.md" 2>/dev/null || echo "")
        if [[ -n "$previous_notes" ]]; then
            echo "## Previous Beta Release Notes" >> "$notes_file"
            echo "" >> "$notes_file"
            echo "$previous_notes" >> "$notes_file"
            echo "" >> "$notes_file"
        fi
    fi

    echo "$notes_file"
}

# Commit and push release notes preview to avoid uncommitted files between prepare/execute
commit_prepare_artifacts() {
    local notes_file="release/RELEASE_NOTES.md"
    local log_file="release/RELEASE_LOG.log"
    local summary_file="release/RELEASE_SUMMARY.md"

    if [[ ! -f "$notes_file" ]] && [[ ! -f "$log_file" ]] && [[ ! -f "$summary_file" ]]; then
        return 0
    fi

    # Only commit if either file has changes
    local has_changes=$(git status -s -- "$notes_file" "$log_file" "$summary_file" 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$has_changes" -eq 0 ]]; then
        return 0
    fi

    echo -e "${BLUE}💾 Committing release notes preview...${NC}"
    git add "$notes_file" "$log_file" "$summary_file" 2>/dev/null || true

    local commit_message="release: Update release notes preview"

    if ! git commit -m "$commit_message" > /dev/null 2>&1; then
        local unstaged=$(git diff --name-only 2>/dev/null || echo "")
        if [[ -n "$unstaged" ]]; then
            while IFS= read -r file; do
                [[ -n "$file" ]] && git add "$file"
            done <<< "$unstaged"
            if ! git commit -m "$commit_message" > /dev/null 2>&1; then
                echo -e "${RED}❌ Error: Failed to commit release notes preview${NC}"
                echo -e "${RED}   → Run: git status to see uncommitted changes${NC}"
                exit 1
            fi
        else
            echo -e "${RED}❌ Error: Failed to commit release notes preview${NC}"
            echo -e "${RED}   → Run: git status to see uncommitted changes${NC}"
            exit 1
        fi
    fi

    echo -e "${GREEN}✓ Release notes preview committed${NC}"
    echo -e "${BLUE}📤 Pushing release notes preview...${NC}"
    if ! git push origin main > /dev/null 2>&1; then
        echo -e "${RED}❌ Error: Failed to push release notes preview commit${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Release notes preview pushed${NC}"
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
        echo -e "${RED}   → The bash conversion script is missing${NC}"
        echo -e "${RED}   → Check that release/convert_zsh_to_bash.sh exists${NC}"
        return 1
    fi

    # Run converter
    if ! bash "$converter_script"; then
        echo -e "${RED}❌ Error: Conversion failed${NC}"
        echo -e "${RED}   → The zsh to bash conversion encountered errors${NC}"
        echo -e "${RED}   → Check release/convert_zsh_to_bash.sh for syntax errors${NC}"
        return 1
    fi

    return 0
}

# Main function
main() {
    local MODE="prepare"  # Default to prepare mode
    local SUMMARY_FILE=""
    local AI_SUMMARY_FILE=""
    local DRY_RUN=false
    local PREPARE_STATE_FILE="release/.prepare_state"
    local BETA_RELEASE=false  # Default to stable release
    local ABORT_VERSION=""  # Version to abort (optional)
    local OVERRIDE_VERSION=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --summary)
                if [[ -z "$2" ]] || [[ "$2" == --* ]]; then
                    echo -e "${RED}Error: --summary requires a file path${NC}"
                    exit 1
                fi
                AI_SUMMARY_FILE="$2"
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
            --abort)
                MODE="abort"
                # Check if next arg is a version
                if [[ -n "$2" ]] && [[ "$2" != --* ]]; then
                    ABORT_VERSION="$2"
                    shift 2
                else
                    shift
                fi
                ;;
            --beta)
                BETA_RELEASE=true
                shift
                ;;
            --set-version)
                if [[ -z "$2" ]] || [[ "$2" == --* ]]; then
                    echo -e "${RED}Error: --set-version requires a version (e.g., 3.0.0b3)${NC}"
                    exit 1
                fi
                OVERRIDE_VERSION="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                echo "Usage: $0 [--prepare|--execute|--abort [version]] [--summary <file>] [--beta] [--set-version <version>]"
                echo ""
                echo "Modes:"
                echo "  --prepare  Analyze commits and generate release preview (default)"
                echo "  --execute  Execute prepared release (no prompts)"
                echo "  --abort    Abort failed release and clean up artifacts"
                echo ""
                echo "Options:"
                echo "  --beta     Create beta/pre-release (e.g., v1.0.0b1)"
                echo "  --summary  Include AI-generated summary from file"
                echo "  --set-version  Override proposed version (e.g., 3.0.0b3)"
                echo "  --dry-run  Generate preview without committing"
                echo ""
                echo "Abort usage:"
                echo "  $0 --abort           Auto-detect and abort latest failed release"
                echo "  $0 --abort v3.0.0b2  Abort specific release version"
                exit 1
                ;;
        esac
    done

    # Abort mode: clean up failed release
    if [[ "$MODE" == "abort" ]]; then
        abort_release "$ABORT_VERSION"
        return $?
    fi

    # Execute mode: load state and perform release
    if [[ "$MODE" == "execute" ]]; then
        execute_release
        return $?
    fi

    # Prepare mode (default): analyze and preview
    echo -e "${BLUE}🚀 Preparing release preview...${NC}"
    echo ""

    # Auto-detect AI_RELEASE_SUMMARY.md if --summary not provided
    if [[ -z "$AI_SUMMARY_FILE" ]] && [[ -f "release/AI_RELEASE_SUMMARY.md" ]]; then
        AI_SUMMARY_FILE="release/AI_RELEASE_SUMMARY.md"
        echo -e "${BLUE}📄 Auto-detected AI release summary: $AI_SUMMARY_FILE${NC}"
    fi

    # Clean up artifacts from previous prepare attempts to ensure idempotency
    if [[ -f "todo.bash" ]]; then
        # Check if todo.bash is uncommitted (indicates it's from a failed prepare)
        if git status --porcelain 2>/dev/null | grep -q "todo.bash"; then
            echo -e "${BLUE}🧹 Cleaning up uncommitted todo.bash from previous prepare attempt...${NC}"
            rm -f todo.bash
        fi
    fi

    # Check if AI summary file exists if provided (no prompt, just warn)
    if [[ -n "$AI_SUMMARY_FILE" ]] && [[ ! -f "$AI_SUMMARY_FILE" ]]; then
        echo -e "${YELLOW}⚠️  Warning: Summary file not found: $AI_SUMMARY_FILE (continuing without it)${NC}"
        AI_SUMMARY_FILE=""
    fi

    # Validate AI summary file is not stale (newer than last release)
    if [[ -n "$AI_SUMMARY_FILE" ]] && [[ -f "$AI_SUMMARY_FILE" ]]; then
        # Get the last release tag
        local last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

        if [[ -n "$last_tag" ]]; then
            # Get timestamp of last release tag (seconds since epoch)
            local tag_timestamp=$(git log -1 --format=%ct "$last_tag" 2>/dev/null || echo "0")

            # Get modification time of summary file (seconds since epoch)
            if [[ "$(uname)" == "Darwin" ]]; then
                # macOS stat command
                local summary_mtime=$(stat -f %m "$AI_SUMMARY_FILE" 2>/dev/null || echo "0")
            else
                # Linux stat command
                local summary_mtime=$(stat -c %Y "$AI_SUMMARY_FILE" 2>/dev/null || echo "0")
            fi

            # Compare timestamps
            if [[ "$summary_mtime" -lt "$tag_timestamp" ]]; then
                echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
                echo -e "${RED}⚠️  STALE SUMMARY FILE DETECTED${NC}"
                echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
                echo ""
                echo -e "${YELLOW}The release summary file is older than the last release:${NC}"
                echo -e "  Summary file: ${AI_SUMMARY_FILE}"
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
        if [[ "$DRY_RUN" == true ]]; then
            echo -e "${YELLOW}⚠️  Dry-run: Uncommitted changes detected; skipping auto-commit${NC}"
            echo -e "$uncommitted"
            echo ""
        else
        echo -e "${YELLOW}⚠️  Auto-committing uncommitted changes before release...${NC}"
        echo "Uncommitted files:"
        echo -e "$uncommitted"
        echo ""

        # Add all remaining uncommitted files (robust parsing for porcelain output)
        local uncommitted_files=()
        while IFS= read -r line; do
            [[ -z "$line" ]] && continue
            # Strip the 2-char status + space prefix (e.g., " M file" or "A  file")
            local file=$(echo "$line" | cut -c4-)
            # Handle renames (format: "old -> new")
            if [[ "$file" == *" -> "* ]]; then
                file="${file##* -> }"
            fi
            [[ -n "$file" ]] && uncommitted_files+=("$file")
        done <<< "$uncommitted"

        for file in "${uncommitted_files[@]}"; do
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

    # Check if current version is a beta (e.g., 3.0.0b1)
    # If so, we're in a beta cycle and must stay at the same base version
    local IN_BETA_CYCLE=false
    local BETA_BASE_VERSION=""
    if [[ "$CURRENT_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+b[0-9]+$ ]]; then
        IN_BETA_CYCLE=true
        # Extract base version using sed (works in both bash and zsh)
        BETA_BASE_VERSION=$(echo "$CURRENT_VERSION" | sed -E 's/^([0-9]+\.[0-9]+\.[0-9]+)b[0-9]+$/\1/')
        echo -e "${BLUE}🔄 In beta cycle for version ${BETA_BASE_VERSION}${NC}"
        echo -e "${BLUE}   Next beta will use base version ${BETA_BASE_VERSION} (ignoring commit-based bump)${NC}"
    fi

    case "$BUMP_TYPE" in
        major)
            if [[ "$IN_BETA_CYCLE" == true ]]; then
                echo -e "${BLUE}🔴 Major changes detected (will apply after ${BETA_BASE_VERSION} stable release)${NC}"
            else
                echo -e "${RED}🔴 Major release detected (breaking changes)${NC}"
            fi
            ;;
        minor)
            if [[ "$IN_BETA_CYCLE" == true ]]; then
                echo -e "${BLUE}🟡 Minor changes detected (will apply after ${BETA_BASE_VERSION} stable release)${NC}"
            else
                echo -e "${YELLOW}🟡 Minor release detected (new features)${NC}"
            fi
            ;;
        patch)
            if [[ "$IN_BETA_CYCLE" == true ]]; then
                echo -e "${BLUE}🟢 Patch changes detected (will apply after ${BETA_BASE_VERSION} stable release)${NC}"
            else
                echo -e "${GREEN}🟢 Patch release detected (bug fixes)${NC}"
            fi
            ;;
    esac

    # Calculate next version
    # If in beta cycle, use the beta base version instead of calculating a new one
    local BASE_VERSION
    if [[ "$IN_BETA_CYCLE" == true ]]; then
        BASE_VERSION="$BETA_BASE_VERSION"
        log_release_step "BETA CYCLE" "In beta cycle for ${BETA_BASE_VERSION}, next beta will use same base version"
    else
        BASE_VERSION=$(calculate_next_version "$CURRENT_VERSION" "$BUMP_TYPE")
    fi

    # Determine if this is a beta or stable release
    local RELEASE_TYPE="stable"
    if [[ "$BETA_RELEASE" == true ]]; then
        RELEASE_TYPE="beta"
        NEW_VERSION=$(determine_beta_version "$BASE_VERSION")
        echo -e "${YELLOW}📌 Beta release: ${NEW_VERSION}${NC}"
    else
        NEW_VERSION="$BASE_VERSION"
        echo -e "${GREEN}📌 Proposed new version: ${NEW_VERSION}${NC}"
    fi

    # Apply explicit version override if provided
    if [[ -n "$OVERRIDE_VERSION" ]]; then
        if ! is_valid_version "$OVERRIDE_VERSION"; then
            echo -e "${RED}❌ Error: Invalid version format for --set-version${NC}"
            echo -e "${RED}   → Expected X.Y.Z or X.Y.ZbN (e.g., 3.0.0b3)${NC}"
            exit 1
        fi

        # Ensure override is greater than current version
        local version_cmp=$(compare_versions "$OVERRIDE_VERSION" "$CURRENT_VERSION")
        if [[ "$version_cmp" -le 0 ]]; then
            echo -e "${RED}❌ Error: Override version must be greater than current version${NC}"
            echo -e "${RED}   → Current: ${CURRENT_VERSION}${NC}"
            echo -e "${RED}   → Override: ${OVERRIDE_VERSION}${NC}"
            exit 1
        fi

        local override_is_beta=false
        if is_beta_version "$OVERRIDE_VERSION"; then
            override_is_beta=true
        fi

        if [[ "$override_is_beta" == true ]]; then
            local override_base=$(get_base_version "$OVERRIDE_VERSION")
            if [[ "$IN_BETA_CYCLE" == true ]] && [[ "$override_base" != "$BETA_BASE_VERSION" ]]; then
                echo -e "${RED}❌ Error: Override beta base must match current beta cycle${NC}"
                echo -e "${RED}   → Current beta base: ${BETA_BASE_VERSION}${NC}"
                echo -e "${RED}   → Override base: ${override_base}${NC}"
                exit 1
            fi
            RELEASE_TYPE="beta"
            BETA_RELEASE=true
            BASE_VERSION="$override_base"
        else
            RELEASE_TYPE="stable"
            BETA_RELEASE=false
            BASE_VERSION="$OVERRIDE_VERSION"
        fi

        NEW_VERSION="$OVERRIDE_VERSION"
        echo -e "${YELLOW}📌 Override version: ${NEW_VERSION}${NC}"
        log_release_step "VERSION OVERRIDE" "Using override version ${NEW_VERSION} instead of proposed version"
    fi

    # Enforce beta requirement and maturity checks for stable releases
    if [[ "$RELEASE_TYPE" == "stable" ]]; then
        if ! detect_and_enforce_beta_requirement "$CURRENT_VERSION" "$NEW_VERSION" "false"; then
            exit 1
        fi

        local current_major=$(echo "$CURRENT_VERSION" | cut -d'.' -f1)
        local new_major=$(echo "$NEW_VERSION" | cut -d'.' -f1)
        local current_minor=$(echo "$CURRENT_VERSION" | cut -d'.' -f2)
        local new_minor=$(echo "$NEW_VERSION" | cut -d'.' -f2)

        if [[ "$new_major" -gt "$current_major" ]] || [[ "$new_minor" -gt "$current_minor" ]]; then
            validate_beta_maturity "$NEW_VERSION" "$BUMP_TYPE"
        fi
    fi
    echo ""

    if [[ -n "$AI_SUMMARY_FILE" ]] && [[ -f "$AI_SUMMARY_FILE" ]]; then
        SUMMARY_FILE=$(generate_release_summary "$AI_SUMMARY_FILE")
        summary_needs_commit=true
        log_release_step "SUMMARY GENERATED" "Generated release summary from ${AI_SUMMARY_FILE} into ${SUMMARY_FILE}"
    fi

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

    # Keep release notes file for human review (used between prepare and execute)
    echo -e "${GREEN}📄 Release notes saved to: ${preview_notes_file}${NC}"
    echo ""

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

    # Note: Bash conversion moved to execute phase to avoid uncommitted files after prepare

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

    # Commit release notes preview and release log to keep working tree clean
    if [[ "$DRY_RUN" == true ]]; then
        echo -e "${YELLOW}⚠️  Dry-run: Skipping prepare artifact commit${NC}"
    else
        commit_prepare_artifacts
    fi

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

# Abort a failed release and clean up all artifacts
# Usage: abort_release [version]
abort_release() {
    local abort_version="$1"

    echo -e "${BLUE}🛑 Abort Release Process${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # Auto-detect failed release if no version specified
    if [[ -z "$abort_version" ]]; then
        echo -e "${BLUE}🔍 Detecting failed release...${NC}"

        # Check last 10 workflow runs for failures
        local failed_release=$(gh run list --limit 10 --json name,conclusion,headBranch,event \
            --jq '.[] | select(.conclusion == "failure" and .event == "push" and (.headBranch | startswith("v"))) | .headBranch' \
            | head -1)

        if [[ -z "$failed_release" ]]; then
            echo -e "${YELLOW}⚠️  No failed release detected in recent workflow history${NC}"
            echo ""
            echo "To abort a specific release, provide the version:"
            echo -e "${GREEN}  ./release/release.sh --abort v3.0.0b2${NC}"
            exit 1
        fi

        abort_version="$failed_release"
        echo -e "${YELLOW}   Found failed release: ${abort_version}${NC}"
    fi

    # Remove 'v' prefix if present for version strings
    local version_number="${abort_version#v}"
    local tag_name="v${version_number}"

    echo ""
    echo -e "${YELLOW}About to abort release: ${abort_version}${NC}"
    echo -e "${YELLOW}This will:${NC}"
    echo -e "${YELLOW}  - Delete tag ${tag_name} (local + remote)${NC}"
    echo -e "${YELLOW}  - Delete GitHub release (if exists)${NC}"
    echo -e "${YELLOW}  - Revert version files to previous version${NC}"
    echo -e "${YELLOW}  - Clean up release artifacts${NC}"
    echo -e "${YELLOW}  - Create abort commit${NC}"
    echo ""

    log_release_step "ABORT START" "Aborting release ${abort_version}"

    # Step 1: Get the previous version (from file, before abort)
    local current_file_version=$(get_file_version)
    local previous_version=""

    # Try to get previous version from git tags
    local all_tags=$(git tag --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+(b[0-9]+)?$' || echo "")
    if [[ -n "$all_tags" ]]; then
        # Find the tag before the one we're aborting
        previous_version=$(echo "$all_tags" | grep -v "^${tag_name}$" | head -1 | sed 's/^v//')
    fi

    if [[ -z "$previous_version" ]]; then
        echo -e "${RED}❌ Error: Cannot determine previous version${NC}"
        echo -e "${RED}   → No previous tags found${NC}"
        log_release_step "ABORT ERROR" "Cannot determine previous version for abort"
        exit 1
    fi

    echo -e "${BLUE}📊 Version rollback: ${version_number} → ${previous_version}${NC}"
    echo ""

    # Step 2: Delete local tag
    echo -e "${BLUE}🗑️  Deleting local tag ${tag_name}...${NC}"
    if git tag -d "$tag_name" 2>/dev/null; then
        echo -e "${GREEN}   ✓ Local tag deleted${NC}"
        log_release_step "ABORT TAG LOCAL" "Deleted local tag ${tag_name}"
    else
        echo -e "${YELLOW}   ⚠️  Local tag not found (may already be deleted)${NC}"
    fi

    # Step 3: Delete remote tag
    echo -e "${BLUE}🗑️  Deleting remote tag ${tag_name}...${NC}"
    if git push origin ":refs/tags/${tag_name}" 2>/dev/null; then
        echo -e "${GREEN}   ✓ Remote tag deleted${NC}"
        log_release_step "ABORT TAG REMOTE" "Deleted remote tag ${tag_name}"
    else
        echo -e "${YELLOW}   ⚠️  Remote tag not found (may already be deleted)${NC}"
    fi

    # Step 4: Delete GitHub release (if exists)
    echo -e "${BLUE}🗑️  Deleting GitHub release ${abort_version}...${NC}"
    if gh release delete "$abort_version" --yes 2>/dev/null; then
        echo -e "${GREEN}   ✓ GitHub release deleted${NC}"
        log_release_step "ABORT RELEASE" "Deleted GitHub release ${abort_version}"
    else
        echo -e "${YELLOW}   ⚠️  GitHub release not found (may not have been created)${NC}"
    fi

    # Step 5: Revert version files
    echo -e "${BLUE}⏪ Reverting version files to ${previous_version}...${NC}"

    # Update pyproject.toml
    if [[ -f "pyproject.toml" ]]; then
        sed -i.bak "s/^version = \".*\"/version = \"${previous_version}\"/" pyproject.toml
        rm pyproject.toml.bak
        echo -e "${GREEN}   ✓ pyproject.toml${NC}"
    fi

    # Update todo.ai
    if [[ -f "todo.ai" ]]; then
        sed -i.bak "s/^VERSION=\".*\"/VERSION=\"${previous_version}\"/" todo.ai
        rm todo.ai.bak
        echo -e "${GREEN}   ✓ todo.ai${NC}"
    fi

    # Update todo_ai/__init__.py
    if [[ -f "todo_ai/__init__.py" ]]; then
        sed -i.bak "s/^__version__ = \".*\"/__version__ = \"${previous_version}\"/" todo_ai/__init__.py
        rm todo_ai/__init__.py.bak
        echo -e "${GREEN}   ✓ todo_ai/__init__.py${NC}"
    fi

    log_release_step "ABORT REVERT" "Reverted version files to ${previous_version}"

    # Step 6: Clean up release artifacts
    echo -e "${BLUE}🧹 Cleaning up release artifacts...${NC}"
    rm -f release/.prepare_state
    rm -f release/RELEASE_NOTES.md
    rm -f todo.bash
    echo -e "${GREEN}   ✓ Artifacts cleaned${NC}"
    log_release_step "ABORT CLEANUP" "Cleaned release artifacts"

    # Step 7: Stage changes
    echo -e "${BLUE}📝 Staging changes...${NC}"
    git add pyproject.toml todo.ai todo_ai/__init__.py release/RELEASE_LOG.log

    # Add uv.lock if it changed (pytest may have updated it)
    if [[ -f "uv.lock" ]] && git diff --quiet uv.lock 2>/dev/null; then
        : # No changes to uv.lock
    elif [[ -f "uv.lock" ]]; then
        git add uv.lock
    fi

    # Step 8: Create abort commit
    echo -e "${BLUE}💾 Creating abort commit...${NC}"
    local commit_message="release: Abort failed ${abort_version} release for retry

- Deleted tag ${tag_name} (local + remote)
- Deleted GitHub release (if existed)
- Reverted version files: ${version_number} → ${previous_version}
- Cleaned up release artifacts

Ready for retry after fixes applied."

    git commit -m "$commit_message"
    log_release_step "ABORT COMMIT" "Created abort commit for ${abort_version}"

    # Step 9: Push abort commit
    echo -e "${BLUE}📤 Pushing abort commit...${NC}"
    git push
    log_release_step "ABORT PUSH" "Pushed abort commit to remote"

    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ Release ${abort_version} aborted successfully!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${GREEN}Reverted to version: ${previous_version}${NC}"
    echo -e "${GREEN}Ready for retry: ./release/release.sh --prepare [--beta]${NC}"
    echo ""

    log_release_step "ABORT COMPLETE" "Release ${abort_version} aborted, reverted to ${previous_version}"

    return 0
}

# Pre-flight validation checks before execute
# Returns 0 if all checks pass, 1 if critical check fails
preflight_validation() {
    local release_type="$1"
    local new_version="$2"
    local bump_type="$3"

    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🔍 Pre-Flight Validation${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    local checks_passed=0
    local checks_failed=0
    local checks_warned=0

    # Check 1: Prepare state exists
    echo -n "1. Checking prepare state... "
    if [[ -f "release/.prepare_state" ]]; then
        echo -e "${GREEN}✅ OK${NC}"
        ((checks_passed++))
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo -e "${RED}   → Prepare state not found${NC}"
        echo -e "${RED}   → Run: ./release/release.sh --prepare${NC}"
        ((checks_failed++))
    fi

    # Check 2: CI/CD passing
    echo -n "2. Checking CI/CD status... "
    if command -v ./scripts/wait-for-ci.sh &> /dev/null && ./scripts/wait-for-ci.sh &> /dev/null; then
        echo -e "${GREEN}✅ OK${NC}"
        ((checks_passed++))
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo -e "${RED}   → CI/CD workflows failing or not found${NC}"
        echo -e "${RED}   → Fix errors before releasing${NC}"
        ((checks_failed++))
    fi

    # Check 3: No uncommitted changes (exclude release working files)
    echo -n "3. Checking for uncommitted changes... "
    local uncommitted=$(git status -s || echo "")
    if [[ -z "$uncommitted" ]]; then
        echo -e "${GREEN}✅ OK${NC}"
        ((checks_passed++))
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo -e "${RED}   → Uncommitted changes detected${NC}"
        echo -e "${RED}   → Commit or stash changes first${NC}"
        ((checks_failed++))
    fi

    # Check 4: GitHub authenticated
    echo -n "4. Checking GitHub authentication... "
    if gh auth status &> /dev/null; then
        echo -e "${GREEN}✅ OK${NC}"
        ((checks_passed++))
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo -e "${RED}   → GitHub CLI not authenticated${NC}"
        echo -e "${RED}   → Run: gh auth login${NC}"
        ((checks_failed++))
    fi

    # Check 5: Build dependencies available
    echo -n "5. Checking build dependencies... "
    if command -v uv &> /dev/null && uv run python -m build --version &> /dev/null; then
        echo -e "${GREEN}✅ OK${NC}"
        ((checks_passed++))
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo -e "${RED}   → Build dependencies missing${NC}"
        echo -e "${RED}   → Run: uv sync --extra dev${NC}"
        ((checks_failed++))
    fi

    # Check 6: Beta maturity (warning only for stable releases)
    if [[ "$release_type" == "stable" ]] && [[ "$bump_type" != "patch" ]]; then
        echo -n "6. Checking beta maturity... "
        # This is a warning-only check, so it never fails
        # The actual validation was done in prepare, just note it here
        echo -e "${GREEN}✅ OK${NC} ${YELLOW}(checked in prepare)${NC}"
        ((checks_passed++))
    else
        echo -n "6. Checking beta maturity... "
        echo -e "${BLUE}⊘ SKIP${NC} (not applicable)"
    fi

    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "Checks passed: ${GREEN}${checks_passed}${NC}"
    if [[ $checks_failed -gt 0 ]]; then
        echo -e "Checks failed: ${RED}${checks_failed}${NC}"
    fi
    if [[ $checks_warned -gt 0 ]]; then
        echo -e "Warnings: ${YELLOW}${checks_warned}${NC}"
    fi
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    if [[ $checks_failed -gt 0 ]]; then
        log_release_step "PREFLIGHT FAILED" "${checks_failed} pre-flight check(s) failed"
        return 1
    fi

    log_release_step "PREFLIGHT PASSED" "All ${checks_passed} pre-flight checks passed"
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

    # Run pre-flight validation
    if ! preflight_validation "$RELEASE_TYPE" "$NEW_VERSION" "$BUMP_TYPE"; then
        echo -e "${RED}❌ Pre-flight validation failed${NC}"
        echo ""
        echo "Fix the issues above and try again."
        exit 1
    fi

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
        echo -e "${RED}   → The VERSION variable was not updated correctly${NC}"
        echo -e "${RED}   → Check todo.ai file for sed errors or file permissions${NC}"
        log_release_step "VERSION UPDATE ERROR" "Failed to update version in todo.ai to ${NEW_VERSION}"
        exit 1
    fi
    if ! grep -q "^version = \"${NEW_VERSION}\"" pyproject.toml 2>/dev/null; then
        echo -e "${RED}❌ Error: Version update failed in pyproject.toml${NC}"
        echo -e "${RED}   → The version field was not updated correctly${NC}"
        echo -e "${RED}   → Check pyproject.toml file for sed errors or file permissions${NC}"
        log_release_step "VERSION UPDATE ERROR" "Failed to update version in pyproject.toml to ${NEW_VERSION}"
        exit 1
    fi
    if ! grep -q "^__version__ = \"${NEW_VERSION}\"" todo_ai/__init__.py 2>/dev/null; then
        echo -e "${RED}❌ Error: Version update failed in todo_ai/__init__.py${NC}"
        echo -e "${RED}   → The __version__ variable was not updated correctly${NC}"
        echo -e "${RED}   → Check todo_ai/__init__.py file for sed errors or file permissions${NC}"
        log_release_step "VERSION UPDATE ERROR" "Failed to update version in todo_ai/__init__.py to ${NEW_VERSION}"
        exit 1
    fi
    echo -e "${GREEN}✓ Verified version updated in todo.ai, pyproject.toml, and todo_ai/__init__.py${NC}"
    log_release_step "VERSION UPDATED" "Version updated successfully in todo.ai, pyproject.toml, and todo_ai/__init__.py"

    # Convert to bash version (now that version is updated)
    echo -e "${BLUE}🔄 Converting to bash version...${NC}"
    if ! convert_to_bash; then
        echo -e "${RED}❌ Error: Bash conversion failed${NC}"
        echo -e "${RED}   → See error details above for specifics${NC}"
        echo -e "${RED}   → Check release/convert_zsh_to_bash.sh for issues${NC}"
        log_release_step "ERROR - Bash Conversion Failed" "Failed to convert zsh version to bash"
        exit 1
    fi
    log_release_step "BASH CONVERSION" "Successfully converted todo.ai to todo.bash with version ${NEW_VERSION}"
    echo -e "${GREEN}✓ Bash version created${NC}"

    # Run pre-commit hooks on generated files to fix formatting before staging
    # This prevents the complex retry logic from needing to handle formatting fixes
    echo -e "${BLUE}🔍 Running pre-commit hooks on generated files...${NC}"
    if command -v pre-commit &> /dev/null; then
        if uv run pre-commit run --files todo.bash 2>&1 | grep -q "Passed\|Skipped"; then
            log_release_step "PRE-COMMIT" "Pre-commit hooks passed for todo.bash"
        else
            # Hooks may have fixed files - this is expected
            log_release_step "PRE-COMMIT" "Pre-commit hooks fixed formatting in todo.bash"
        fi
    fi
    echo -e "${GREEN}✓ Files ready for commit${NC}"

    # Commit version change and summary file
    echo -e "${BLUE}💾 Committing version change and release summary...${NC}"
    log_release_step "COMMIT VERSION" "Committing version change to git"
    git add todo.ai pyproject.toml todo_ai/__init__.py

    # Commit summary file if it exists and is uncommitted
    if [[ "$summary_needs_commit" == true ]] && [[ -n "$SUMMARY_FILE" ]] && [[ -f "$SUMMARY_FILE" ]]; then
        log_release_step "COMMIT SUMMARY" "Adding release summary file to commit: ${SUMMARY_FILE}"
        git add "$SUMMARY_FILE"
    fi

    # Commit release notes file (generated from summary + commits)
    # This file will be used by CI/CD workflow to create the GitHub release
    if [[ -f "release/RELEASE_NOTES.md" ]]; then
        log_release_step "COMMIT RELEASE_NOTES" "Adding release notes file to commit: release/RELEASE_NOTES.md"
        git add release/RELEASE_NOTES.md
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

    # Add uv.lock if it exists (may be modified by pre-commit hooks when version changes)
    if [[ -f "uv.lock" ]]; then
        local lock_status=$(git status -s uv.lock 2>/dev/null || echo "")
        if [[ -n "$lock_status" ]]; then
            log_release_step "COMMIT UV_LOCK" "Adding uv.lock to commit (modified by version change)"
            git add uv.lock
        fi
    fi

    # Create version commit message
    local commit_message="chore: Bump version to ${NEW_VERSION}"
    if [[ -n "$SUMMARY_FILE" ]] && [[ -f "$SUMMARY_FILE" ]] && [[ "$summary_needs_commit" == true ]]; then
        commit_message="${commit_message}

Includes release summary from ${SUMMARY_FILE}"
    fi

    # Commit the version change
    # Pre-commit hooks may modify files (e.g., uv run pytest updates uv.lock, ruff --fix formats code)
    # Strategy: Try commit, if it fails due to hook modifications, re-stage and retry
    echo -e "${BLUE}💾 Committing version change (running pre-commit hooks)...${NC}"

    # First attempt: let hooks run and potentially modify files
    if git commit -m "$commit_message" > /dev/null 2>&1; then
        log_release_step "VERSION COMMITTED" "Version change committed successfully"
    else
        # Commit failed - likely due to hook modifications
        # Check if there are unstaged changes (hooks modified files after staging)
        local unstaged=$(git diff --name-only 2>/dev/null || echo "")
        if [[ -n "$unstaged" ]]; then
            echo -e "${YELLOW}⚠️  Pre-commit hooks modified files: ${unstaged}${NC}"
            echo -e "${BLUE}   Re-staging modified files and retrying commit...${NC}"
            log_release_step "HOOK MODIFICATIONS" "Pre-commit hooks modified: ${unstaged}"

            # Re-stage files that hooks modified (properly handle newlines)
            # Use while loop to read each file and add it individually
            while IFS= read -r file; do
                [[ -n "$file" ]] && git add "$file"
            done <<< "$unstaged"

            # Retry commit - hooks will run again, which is correct
            # If hooks modify files again, we'll fail and require manual intervention
            if ! git commit -m "$commit_message" > /dev/null 2>&1; then
                echo -e "${RED}❌ Error: Failed to commit version changes${NC}"
                echo -e "${RED}   → Git commit failed even after re-staging${NC}"
                echo -e "${RED}   → Pre-commit hooks may still be modifying files${NC}"
                echo -e "${RED}   → Run: git status to see uncommitted changes${NC}"
                echo -e "${RED}   → This indicates a deeper issue that needs investigation${NC}"
                log_release_step "COMMIT ERROR" "Failed to commit version changes after re-staging - hooks may still be modifying files"
                exit 1
            fi
            log_release_step "VERSION COMMITTED" "Version change committed successfully (retried with hook modifications)"
        else
            # Commit failed for another reason
            echo -e "${RED}❌ Error: Failed to commit version changes${NC}"
            echo -e "${RED}   → Git commit failed${NC}"
            echo -e "${RED}   → Run: git status to see uncommitted changes${NC}"
            log_release_step "COMMIT ERROR" "Failed to commit version changes"
            exit 1
        fi
    fi

    # Get the commit hash for the version change
    local version_commit_hash=$(git rev-parse HEAD 2>/dev/null)

    # Verify we got a commit hash
    if [[ -z "$version_commit_hash" ]]; then
        echo -e "${RED}❌ Error: Failed to get commit hash${NC}"
        echo -e "${RED}   → git rev-parse HEAD failed${NC}"
        echo -e "${RED}   → Repository may be in an inconsistent state${NC}"
        log_release_step "COMMIT VERIFY ERROR" "Failed to get commit hash after version commit"
        exit 1
    fi

    log_release_step "COMMIT HASH" "Version commit hash: ${version_commit_hash}"

    # Create and push tag
    TAG="v${NEW_VERSION}"
    echo -e "${BLUE}🏷️  Creating tag ${TAG}...${NC}"
    log_release_step "CREATE TAG" "Creating git tag: ${TAG} pointing to commit ${version_commit_hash}"
    # Explicitly tag the commit hash to ensure we're tagging the right commit
    git tag -a "$TAG" -m "Release version $NEW_VERSION" "$version_commit_hash" > /dev/null 2>&1
    log_release_step "TAG CREATED" "Git tag ${TAG} created successfully at commit ${version_commit_hash}"

    # Verify tag points to commit with correct version (with improved checking)
    echo -e "${BLUE}🔍 Verifying tag points to correct version...${NC}"
    local verification_failed=false
    local verification_errors=""

    # Check todo.ai
    if ! git show "$TAG":todo.ai 2>/dev/null | grep -q "^VERSION=\"${NEW_VERSION}\""; then
        verification_failed=true
        verification_errors="${verification_errors}\n   ❌ todo.ai: VERSION not found or incorrect"
    fi

    # Check pyproject.toml
    if ! git show "$TAG":pyproject.toml 2>/dev/null | grep -q "^version = \"${NEW_VERSION}\""; then
        verification_failed=true
        verification_errors="${verification_errors}\n   ❌ pyproject.toml: version not found or incorrect"
    fi

    # Check todo_ai/__init__.py
    if ! git show "$TAG":todo_ai/__init__.py 2>/dev/null | grep -q "^__version__ = \"${NEW_VERSION}\""; then
        verification_failed=true
        verification_errors="${verification_errors}\n   ❌ todo_ai/__init__.py: __version__ not found or incorrect"
    fi

    if [[ "$verification_failed" == true ]]; then
        echo -e "${RED}❌ Error: Tag verification failed${NC}"
        echo -e "${RED}   → Tag $TAG does not point to commit with correct version${NC}"
        echo -e "${RED}   → Expected version: ${NEW_VERSION}${NC}"
        echo -e "${RED}${verification_errors}${NC}"
        echo -e "${RED}   → This indicates version files were not committed correctly${NC}"
        echo -e "${RED}   → Run: git tag -d $TAG && git reset --soft HEAD~1 && retry release${NC}"
        log_release_step "TAG VERIFY ERROR" "Tag ${TAG} verification failed - version ${NEW_VERSION} not found in all files"
        exit 1
    fi
    echo -e "${GREEN}✓ Tag verified - points to commit with version ${NEW_VERSION}${NC}"
    log_release_step "TAG VERIFIED" "Tag ${TAG} successfully verified - all version files match ${NEW_VERSION}"

    echo -e "${BLUE}📤 Pushing version commit to remote...${NC}"
    log_release_step "PUSH MAIN" "Pushing main branch to origin"
    git push origin main > /dev/null 2>&1 || log_release_step "PUSH ERROR" "Failed to push main branch"

    # Wait for CI to pass on the version commit before pushing tag
    # This ensures the release workflow has a validated commit to work with
    echo -e "${BLUE}⏳ Waiting for CI to pass on version commit...${NC}"
    log_release_step "WAIT CI" "Waiting for CI workflow to pass on version commit"

    local commit_sha=$(git rev-parse HEAD)
    local wait_start=$(date +%s)
    local timeout=600  # 10 minutes
    local ci_status=""

    while true; do
        # Check if we've exceeded timeout
        local elapsed=$(($(date +%s) - wait_start))
        if [ $elapsed -ge $timeout ]; then
            echo -e "${RED}❌ Timeout waiting for CI${NC}"
            log_release_step "CI TIMEOUT" "CI did not complete within ${timeout} seconds"
            exit 1
        fi

        # Check CI status for this commit on main branch
        # Query ALL workflows (not just ci-cd.yml) and check if ANY failed
        # If all are success/skipped, we're good. If any failed, abort.
        local all_runs=$(gh run list \
            --commit "$commit_sha" \
            --branch main \
            --json conclusion,status \
            --jq '.[]' 2>/dev/null || echo '{"conclusion":"pending","status":"in_progress"}')

        # Check if any runs are still in progress
        local has_pending=$(echo "$all_runs" | jq -r 'select(.status == "in_progress" or .status == "queued") | .status' | head -1)
        # Check if any runs failed
        local has_failure=$(echo "$all_runs" | jq -r 'select(.conclusion == "failure" or .conclusion == "cancelled") | .conclusion' | head -1)
        # Count total completed runs
        local completed_count=$(echo "$all_runs" | jq -r 'select(.status == "completed") | .status' | wc -l | tr -d ' ')

        if [[ -n "$has_failure" ]]; then
            ci_status="failure"
        elif [[ -z "$has_pending" ]] && [[ "$completed_count" -gt 0 ]]; then
            ci_status="success"
        else
            ci_status="pending"
        fi

        if [[ "$ci_status" == "success" ]]; then
            echo -e "${GREEN}✓ CI passed for version commit${NC}"
            log_release_step "CI SUCCESS" "CI workflow passed for version commit"
            break
        elif [[ "$ci_status" == "failure" ]] || [[ "$ci_status" == "cancelled" ]]; then
            echo -e "${RED}❌ CI failed for version commit: ${ci_status}${NC}"
            echo -e "${RED}   → Check: gh run list --commit ${commit_sha}${NC}"
            log_release_step "CI FAILED" "CI workflow failed for version commit: ${ci_status}"
            exit 1
        else
            echo -e "${BLUE}   CI status: ${ci_status} (${elapsed}s elapsed)${NC}"
            sleep 10
        fi
    done

    echo -e "${BLUE}📤 Pushing tag to remote...${NC}"
    log_release_step "PUSH TAG" "Pushing tag ${TAG} to origin"
    git push origin "$TAG" > /dev/null 2>&1 || log_release_step "PUSH ERROR" "Failed to push tag ${TAG}"

    # Note: GitHub release creation has been moved to CI/CD workflow
    # This ensures the release is only created AFTER successful PyPI publication
    # The workflow will create the release and attach all assets (shell scripts + Python dist)
    # The release notes file (release/RELEASE_NOTES.md) is committed so the workflow can use it
    echo -e "${BLUE}📦 GitHub release will be created by CI/CD workflow after successful PyPI publish${NC}"
    log_release_step "GITHUB RELEASE" "GitHub release creation delegated to CI/CD workflow (after PyPI success)"

    # Wait for the release workflow to complete
    echo -e "${BLUE}⏳ Waiting for release workflow to complete...${NC}"
    log_release_step "WAIT WORKFLOW" "Waiting for GitHub Actions release workflow to complete"

    # Give GitHub a moment to register the workflow run
    sleep 5

    # Wait for the workflow triggered by this tag
    local wait_start=$(date +%s)
    local timeout=600  # 10 minutes
    local workflow_status=""

    while true; do
        # Check if we've exceeded timeout
        local elapsed=$(($(date +%s) - wait_start))
        if [ $elapsed -ge $timeout ]; then
            echo -e "${RED}❌ Timeout waiting for release workflow${NC}"
            log_release_step "WORKFLOW TIMEOUT" "Release workflow did not complete within ${timeout} seconds"
            exit 1
        fi

        # Get the release workflow status for this tag
        workflow_status=$(gh run list --branch "${TAG}" --workflow ci-cd.yml --limit 1 --json conclusion --jq '.[0].conclusion // "pending"' 2>/dev/null || echo "pending")

        if [[ "$workflow_status" == "success" ]]; then
            echo -e "${GREEN}✓ Release workflow completed successfully${NC}"
            log_release_step "WORKFLOW SUCCESS" "GitHub Actions release workflow completed successfully"
            break
        elif [[ "$workflow_status" == "failure" ]] || [[ "$workflow_status" == "cancelled" ]]; then
            echo -e "${RED}❌ Release workflow failed: ${workflow_status}${NC}"
            echo -e "${RED}   → Check: gh run list --branch ${TAG}${NC}"
            log_release_step "WORKFLOW FAILED" "GitHub Actions release workflow failed: ${workflow_status}"
            exit 1
        else
            echo -e "${BLUE}   Status: ${workflow_status} (${elapsed}s elapsed)${NC}"
            sleep 10
        fi
    done

    local repo_url=$(get_repo_url)
    log_release_step "RELEASE COMPLETE" "Release ${NEW_VERSION} published successfully!
- Tag: ${TAG}
- URL: ${repo_url}/releases/tag/${TAG}
- Release log: ${RELEASE_LOG}"

    # Commit and push RELEASE_LOG.log at the very end to capture all release operations
    # This happens AFTER the release workflow succeeds
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
