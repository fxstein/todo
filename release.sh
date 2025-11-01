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
    
    # Check for uncommitted changes
    if [[ -n $(git status -s) ]]; then
        echo -e "${RED}❌ Error: Uncommitted changes detected${NC}"
        echo "Please commit or stash changes before releasing"
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
            rm -f "$RELEASE_NOTES_FILE"
            exit 0
        fi
    else
        printf "Proceed with release? (y/N) "
        read -r reply
        if [[ ! "$reply" =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Release cancelled by user${NC}"
            rm -f "$RELEASE_NOTES_FILE"
            exit 0
        fi
    fi
    
    # Update version
    echo ""
    echo -e "${BLUE}📝 Updating version in todo.ai...${NC}"
    update_version "$NEW_VERSION"
    
    # Commit version change
    echo -e "${BLUE}💾 Committing version change...${NC}"
    git add todo.ai
    git commit -m "Bump version to $NEW_VERSION" > /dev/null 2>&1 || true
    
    # Create and push tag
    TAG="v${NEW_VERSION}"
    echo -e "${BLUE}🏷️  Creating tag ${TAG}...${NC}"
    git tag -a "$TAG" -m "Release version $NEW_VERSION" > /dev/null 2>&1
    git push origin main > /dev/null 2>&1
    git push origin "$TAG" > /dev/null 2>&1
    
    # Create GitHub release
    echo -e "${BLUE}📦 Creating GitHub release...${NC}"
    gh release create "$TAG" \
        --title "$NEW_VERSION" \
        --notes-file "$RELEASE_NOTES_FILE" > /dev/null 2>&1
    
    # Cleanup
    rm -f "$RELEASE_NOTES_FILE"
    
    echo ""
    echo -e "${GREEN}✅ Release ${NEW_VERSION} published successfully!${NC}"
    echo -e "${GREEN}🔗 View release: https://github.com/fxstein/todo.ai/releases/tag/${TAG}${NC}"
}

# Run main function
main "$@"
