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
        cat > "$RELEASE_LOG" << 'EOF'
# Release Log
# This file contains a chronological log of all release operations performed by the release script.
# Format: TIMESTAMP USER_ID STEP - MESSAGE
# Newest entries appear at the top of the file.
#
EOF
    fi
    
    # Create log entry
    local log_entry="${timestamp} ${user_id} ${step} - ${message}"
    
    # Find where header ends (first non-comment line)
    local header_end=$(awk '/^[^#]/ {print NR; exit}' "$RELEASE_LOG" 2>/dev/null || echo 0)
    
    # If no non-comment lines, header is entire file
    if [[ -z "$header_end" ]] || [[ "$header_end" -eq 0 ]]; then
        header_end=$(wc -l < "$RELEASE_LOG" 2>/dev/null || echo 5)
    fi
    
    # Create new log: header + new entry + old entries
    local temp_log=$(mktemp)
    
    # Copy header
    head -n "$header_end" "$RELEASE_LOG" > "$temp_log" 2>/dev/null
    
    # Add new entry
    echo "$log_entry" >> "$temp_log"
    
    # Append existing log entries (skip header)
    if [[ $header_end -gt 0 ]]; then
        tail -n +$((header_end + 1)) "$RELEASE_LOG" 2>/dev/null >> "$temp_log" || true
    fi
    
    mv "$temp_log" "$RELEASE_LOG"
}

# Get current version from todo.ai
get_current_version() {
    grep '^VERSION=' todo.ai | sed 's/VERSION="\([^"]*\)"/\1/'
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
        "^\.cursorrules$"
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
            # Exclude backend docs
            if [[ "$file" != "docs/TEST_PLAN.md" ]]; then
                has_frontend=true
            fi
        fi
        
        # Check if backend
        for pattern in "${backend_patterns[@]}"; do
            if [[ "$file" =~ $pattern ]]; then
                has_backend=true
                break
            fi
        done
    done <<< "$changed_files"
    
    # If only backend files changed (no frontend), it's a backend-only release
    if [[ "$has_backend" == true ]] && [[ "$has_frontend" == false ]]; then
        return 0  # Backend only
    fi
    
    return 1  # Has frontend or mixed
}

# Analyze commits to determine version bump type
analyze_commits() {
    local last_tag="$1"
    local commit_range
    
    if [[ -z "$last_tag" ]] || [[ ! "$last_tag" =~ ^v ]]; then
        # No previous tag or not a version tag - analyze all commits
        commit_range="HEAD"
    else
        # Previous tag exists - analyze commits since that tag
        commit_range="${last_tag}..HEAD"
    fi
    
    local commits
    commits=$(git log "$commit_range" --pretty=format:"%s" --no-merges 2>/dev/null) || commits=""
    
    if [[ -z "$commits" ]]; then
        echo "patch"
        return
    fi
    
    # Priority 1: Check for explicit backend prefixes (fastest, explicit)
    if echo "$commits" | grep -qiE "^(backend|infra|release|internal):"; then
        echo "patch"
        return
    fi
    
    # Priority 2: Check for backend-only file changes (catches forgotten prefixes)
    if is_backend_only_release "$commit_range"; then
        echo "patch"
        return
    fi
    
    # Priority 3: Continue with existing keyword analysis (frontend/mixed releases)
    local breaking_count=0
    local feature_count=0
    local fix_count=0
    local other_count=0
    
    while IFS= read -r commit || [[ -n "$commit" ]]; do
        [[ -z "$commit" ]] && continue
        local lower_commit=$(echo "$commit" | tr '[:upper:]' '[:lower:]' 2>/dev/null || echo "$commit")
        
        # Check for breaking changes
        if [[ "$lower_commit" =~ (breaking|break|major|!:) ]] || 
           [[ "$lower_commit" =~ ^(feat|fix|refactor|perf)!: ]]; then
            breaking_count=$((breaking_count + 1))
        # Check for features
        elif [[ "$lower_commit" =~ ^(feat|feature): ]] || 
             [[ "$lower_commit" =~ (add|new|implement|create|support) ]]; then
            feature_count=$((feature_count + 1))
        # Check for fixes
        elif [[ "$lower_commit" =~ ^(fix|bugfix|patch): ]] || 
             [[ "$lower_commit" =~ (fix|bug|patch|hotfix|correct) ]]; then
            fix_count=$((fix_count + 1))
        else
            other_count=$((other_count + 1))
        fi
    done <<< "$commits"
    
    # Determine bump type
    if [[ $breaking_count -gt 0 ]]; then
        echo "major"
    elif [[ $feature_count -gt 0 ]]; then
        echo "minor"
    elif [[ $fix_count -gt 0 ]] || [[ $other_count -gt 0 ]]; then
        echo "patch"
    else
        echo "patch"
    fi
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
    local added_commits=()
    local changed_commits=()
    local fixed_commits=()
    local other_commits=()
    
    while IFS= read -r commit; do
        local commit_short=$(echo "$commit" | cut -d'|' -f1)
        local commit_full=$(git rev-parse "$commit_short" 2>/dev/null || echo "$commit_short")
        local commit_msg=$(echo "$commit" | cut -d'|' -f2- | sed 's/^ *//')
        local lower_msg=$(echo "$commit_msg" | tr '[:upper:]' '[:lower:]')
        local commit_link="([${commit_short}](${repo_url}/commit/${commit_full}))"
        
        # Skip version bumps
        if [[ "$lower_msg" =~ ^bump.*version ]]; then
            continue
        fi
        
        if [[ "$lower_msg" =~ (breaking|break|major|!:) ]] || 
           [[ "$lower_msg" =~ ^(feat|fix|refactor|perf)!: ]]; then
            breaking_commits+=("- ${commit_msg} ${commit_link}")
        elif [[ "$lower_msg" =~ ^(feat|feature): ]] || 
             [[ "$lower_msg" =~ (add|new|implement|create|support) ]]; then
            added_commits+=("- ${commit_msg} ${commit_link}")
        elif [[ "$lower_msg" =~ (change|update|refactor|improve|enhance|modify) ]]; then
            changed_commits+=("- ${commit_msg} ${commit_link}")
        elif [[ "$lower_msg" =~ ^(fix|bugfix|patch): ]] || 
             [[ "$lower_msg" =~ (fix|bug|patch|hotfix|correct) ]]; then
            fixed_commits+=("- ${commit_msg} ${commit_link}")
        else
            other_commits+=("- ${commit_msg} ${commit_link}")
        fi
    done < <(git log "$commit_range" --pretty=format:"%h|%s" --no-merges 2>/dev/null || echo "")
    
    # Write sections
    if [[ ${#breaking_commits[@]} -gt 0 ]]; then
        echo "### Breaking Changes" >> "$temp_notes"
        printf '%s\n' "${breaking_commits[@]}" >> "$temp_notes"
        echo "" >> "$temp_notes"
    fi
    
    if [[ ${#added_commits[@]} -gt 0 ]]; then
        echo "### Added" >> "$temp_notes"
        printf '%s\n' "${added_commits[@]}" >> "$temp_notes"
        echo "" >> "$temp_notes"
    fi
    
    if [[ ${#changed_commits[@]} -gt 0 ]]; then
        echo "### Changed" >> "$temp_notes"
        printf '%s\n' "${changed_commits[@]}" >> "$temp_notes"
        echo "" >> "$temp_notes"
    fi
    
    if [[ ${#fixed_commits[@]} -gt 0 ]]; then
        echo "### Fixed" >> "$temp_notes"
        printf '%s\n' "${fixed_commits[@]}" >> "$temp_notes"
        echo "" >> "$temp_notes"
    fi
    
    if [[ ${#other_commits[@]} -gt 0 ]]; then
        echo "### Other" >> "$temp_notes"
        printf '%s\n' "${other_commits[@]}" >> "$temp_notes"
        echo "" >> "$temp_notes"
    fi
    
    # Count commits
    local total_commits=$(git log "$commit_range" --oneline --no-merges 2>/dev/null | wc -l | tr -d ' ')
    echo "*Total commits: ${total_commits}*" >> "$temp_notes"
    
    echo "$temp_notes"
}

# Update version in todo.ai
update_version() {
    local new_version="$1"
    local sed_flag
    if [[ "$(uname)" == "Darwin" ]]; then
        sed_flag="-i ''"
    else
        sed_flag="-i"
    fi
    
    # Update VERSION variable (line starting with VERSION=)
    sed $sed_flag "s/^VERSION=\"[^\"]*\"/VERSION=\"$new_version\"/" todo.ai
    # Update Version comment (line starting with # Version:)
    sed $sed_flag "s/^# Version: [0-9.]*/# Version: $new_version/" todo.ai
    
    # Verify
    if ! grep -q "^VERSION=\"$new_version\"" todo.ai; then
        echo -e "${RED}❌ Error: Version update failed${NC}"
        exit 1
    fi
}

# Main release process
main() {
    local SUMMARY_FILE=""
    
    # Parse command-line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --summary|-s)
                SUMMARY_FILE="$2"
                shift 2
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                echo "Usage: $0 [--summary <file>]"
                exit 1
                ;;
        esac
    done
    
    echo -e "${BLUE}🚀 Starting intelligent release process...${NC}"
    echo ""
    
    # Check if summary file exists if provided
    if [[ -n "$SUMMARY_FILE" ]] && [[ ! -f "$SUMMARY_FILE" ]]; then
        echo -e "${YELLOW}⚠️  Warning: Summary file not found: $SUMMARY_FILE${NC}"
        printf "Continue without summary? (y/N) "
        read -r reply
        if [[ ! "$reply" =~ ^[Yy]$ ]]; then
            exit 0
        fi
        SUMMARY_FILE=""
    fi
    
    # Verify prerequisites
    if ! command -v gh &> /dev/null; then
        echo -e "${RED}❌ Error: GitHub CLI (gh) is not installed${NC}"
        echo "Install it with: brew install gh"
        exit 1
    fi
    
    # Verify we're on main branch
    CURRENT_BRANCH=$(git branch --show-current)
    if [[ "$CURRENT_BRANCH" != "main" ]]; then
        echo -e "${YELLOW}⚠️  Warning: Not on main branch (current: $CURRENT_BRANCH)${NC}"
        read "?Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
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
        # Check if file is untracked (starts with ??)
        if echo "$status_output" | grep -qE "^[?]{2}[[:space:]]+.*${SUMMARY_FILE}$"; then
            summary_needs_commit=true
            log_release_step "SUMMARY DETECTED" "Found uncommitted summary file: ${SUMMARY_FILE} - will commit as part of release"
            # Remove it from uncommitted list so it doesn't block the release
            uncommitted=$(echo -e "$uncommitted" | grep -vE ".*${SUMMARY_FILE}$" || true)
        # Check if file is modified (starts with M or A)
        elif echo "$status_output" | grep -qE "^[MA ][[:space:]]+.*${SUMMARY_FILE}$"; then
            summary_needs_commit=true
            log_release_step "SUMMARY DETECTED" "Found modified summary file: ${SUMMARY_FILE} - will commit as part of release"
            # Remove it from uncommitted list so it doesn't block the release
            uncommitted=$(echo -e "$uncommitted" | grep -vE ".*${SUMMARY_FILE}$" || true)
        fi
    fi
    
    if [[ -n "$uncommitted" ]]; then
        echo -e "${RED}❌ Error: Uncommitted changes detected${NC}"
        echo "Uncommitted files:"
        echo -e "$uncommitted"
        echo ""
        echo "Please commit or stash changes before releasing"
        log_release_step "ERROR - Uncommitted Changes" "Release aborted due to uncommitted changes:\n\n$uncommitted"
        exit 1
    fi
    
    # Get current version
    CURRENT_VERSION=$(get_current_version)
    echo -e "${GREEN}📌 Current version: ${CURRENT_VERSION}${NC}"
    
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
    NEW_VERSION=$(calculate_next_version "$CURRENT_VERSION" "$BUMP_TYPE")
    echo -e "${GREEN}📌 Proposed new version: ${NEW_VERSION}${NC}"
    echo ""
    
    # Log release start with all details
    log_release_step "RELEASE START" "Starting release process:
- Current version: ${CURRENT_VERSION}
- Proposed version: ${NEW_VERSION}
- Bump type: ${BUMP_TYPE}
- Last tag: ${LAST_TAG}
- Summary file: ${SUMMARY_FILE:-none}"
    
    # Generate release notes
    echo -e "${BLUE}📝 Generating release notes...${NC}"
    if [[ -n "$SUMMARY_FILE" ]] && [[ -f "$SUMMARY_FILE" ]]; then
        echo -e "${GREEN}📄 Including AI-generated summary from: $SUMMARY_FILE${NC}"
    fi
    RELEASE_NOTES_FILE=$(generate_release_notes "$LAST_TAG" "$NEW_VERSION" "$SUMMARY_FILE")
    
    # Show release notes preview
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    cat "$RELEASE_NOTES_FILE"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    # Ask for human review if major release or many commits
    local last_tag_for_count=$(get_last_tag)
    local commit_range_for_count
    if [[ -z "$last_tag_for_count" ]] || [[ ! "$last_tag_for_count" =~ ^v ]]; then
        commit_range_for_count="HEAD"
    else
        commit_range_for_count="${last_tag_for_count}..HEAD"
    fi
    local commit_count=$(git log "$commit_range_for_count" --oneline --no-merges 2>/dev/null | wc -l | tr -d ' ')
    local needs_review=false
    
    if [[ "$BUMP_TYPE" == "major" ]]; then
        echo -e "${YELLOW}⚠️  Major release detected - human review recommended${NC}"
        needs_review=true
    elif [[ $commit_count -gt 10 ]]; then
        echo -e "${YELLOW}⚠️  Large release ($commit_count commits) - human review recommended${NC}"
        needs_review=true
    fi
    
    if [[ "$needs_review" == true ]]; then
        echo ""
        echo "Please review the release notes above."
        printf "Proceed with release? (y/N) "
        read -r reply
        if [[ ! "$reply" =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Release cancelled by user${NC}"
            log_release_step "CANCELLED" "Release cancelled by user at review stage"
            rm -f "$RELEASE_NOTES_FILE"
            exit 0
        fi
        log_release_step "REVIEW" "Human review requested and approved for ${NEW_VERSION}"
    else
        printf "Proceed with release? (y/N) "
        read -r reply
        if [[ ! "$reply" =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Release cancelled by user${NC}"
            log_release_step "CANCELLED" "Release cancelled by user at confirmation stage"
            rm -f "$RELEASE_NOTES_FILE"
            exit 0
        fi
        log_release_step "CONFIRMED" "Release confirmed by user"
    fi
    
    # Update version
    echo ""
    echo -e "${BLUE}📝 Updating version in todo.ai...${NC}"
    log_release_step "UPDATE VERSION" "Updating version in todo.ai from ${CURRENT_VERSION} to ${NEW_VERSION}"
    update_version "$NEW_VERSION"
    log_release_step "VERSION UPDATED" "Version updated successfully in todo.ai"
    
    # Commit version change and summary file
    echo -e "${BLUE}💾 Committing version change and release summary...${NC}"
    log_release_step "COMMIT VERSION" "Committing version change to git"
    git add todo.ai
    
    # Commit summary file if it exists and is uncommitted
    if [[ "$summary_needs_commit" == true ]] && [[ -n "$SUMMARY_FILE" ]] && [[ -f "$SUMMARY_FILE" ]]; then
        log_release_step "COMMIT SUMMARY" "Adding release summary file to commit: ${SUMMARY_FILE}"
        git add "$SUMMARY_FILE"
    fi
    
    local commit_msg="Bump version to $NEW_VERSION"
    if [[ "$summary_needs_commit" == true ]]; then
        commit_msg="${commit_msg}

Includes release summary from ${SUMMARY_FILE}"
    fi
    
    local version_commit=$(git commit -m "$commit_msg" 2>&1 || echo "no commit needed")
    log_release_step "VERSION COMMITTED" "Version change committed: ${version_commit}"
    
    # Create and push tag
    TAG="v${NEW_VERSION}"
    echo -e "${BLUE}🏷️  Creating tag ${TAG}...${NC}"
    log_release_step "CREATE TAG" "Creating git tag: ${TAG}"
    git tag -a "$TAG" -m "Release version $NEW_VERSION" > /dev/null 2>&1
    log_release_step "TAG CREATED" "Git tag ${TAG} created successfully"
    
    echo -e "${BLUE}📤 Pushing to remote...${NC}"
    log_release_step "PUSH MAIN" "Pushing main branch to origin"
    git push origin main > /dev/null 2>&1 || log_release_step "PUSH ERROR" "Failed to push main branch"
    
    log_release_step "PUSH TAG" "Pushing tag ${TAG} to origin"
    git push origin "$TAG" > /dev/null 2>&1 || log_release_step "PUSH ERROR" "Failed to push tag ${TAG}"
    
    # Create GitHub release
    echo -e "${BLUE}📦 Creating GitHub release...${NC}"
    log_release_step "CREATE GITHUB RELEASE" "Creating GitHub release for tag ${TAG}"
    
    # Temporarily disable set -e to capture error
    set +e
    local release_output=$(gh release create "$TAG" \
        --title "$NEW_VERSION" \
        --notes-file "$RELEASE_NOTES_FILE" 2>&1)
    local release_status=$?
    set -e
    
    if [[ $release_status -eq 0 ]]; then
        log_release_step "GITHUB RELEASE CREATED" "GitHub release created successfully for ${TAG}\nOutput: ${release_output}"
    else
        log_release_step "GITHUB RELEASE ERROR" "Failed to create GitHub release for ${TAG}\nError: ${release_output}\nExit code: ${release_status}"
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
