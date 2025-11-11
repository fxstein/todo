# Bug Reporting Feature Design

## Overview

The bug reporting feature enables `todo.ai` to detect errors and suggest reporting bugs to GitHub Issues. The system always requires explicit user confirmation before sending any reports. This allows users to create detailed bug reports with logs, context, and relevant data, improving the feedback loop between users and developers while maintaining full user control.

## Problem Statement

Currently, when `todo.ai` encounters errors or unexpected behavior, users must manually:
1. Identify that something went wrong
2. Gather relevant logs and context
3. Navigate to GitHub Issues
4. Create a bug report with all necessary information
5. Check if a similar issue already exists

This process is time-consuming and often results in incomplete bug reports or duplicate issues. The bug reporting feature suggests creating bug reports and assists with the process while ensuring quality reports and preventing duplicates, but always requires user confirmation before any action.

## Goals

1. **Error Detection**: Detect errors and unexpected behavior during script execution
2. **Reporting Suggestion**: Suggest creating GitHub Issues when errors occur (never automatic)
3. **User Control**: Always require explicit user confirmation before any GitHub API calls
4. **Duplicate Prevention**: Check for existing similar issues before creating new ones (with user confirmation)
5. **Context Preservation**: Include logs, error details, and relevant data in reports
6. **Privacy Protection**: For private repos, hide repository identifiers, only include todo.ai-specific info

## Architecture

### Components

1. **Error Detection System**: Catches errors, exceptions, and unexpected behavior
2. **Bug Report Generator**: Creates formatted bug reports with templates
3. **Duplicate Detection Engine**: Searches for similar issues using GitHub API
4. **GitHub CLI Integration**: Uses `gh` CLI to create issues and comments
5. **Log Collector**: Gathers relevant logs and error context
6. **Issue Reporter**: Orchestrates the reporting workflow

### Workflow

```
┌─────────────────┐
│  Error Detected │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Collect Error Context   │
│ - Error message         │
│ - Stack trace           │
│ - Relevant logs         │
│ - System information    │
│ - Version info          │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Check for Duplicates    │
│ - Search GitHub Issues  │
│ - Compare titles/bodies │
│ - Calculate similarity  │
└────────┬────────────────┘
         │
         ▼
    ┌────┴────┐
    │ Similar │
    │ Issue   │
    │ Found?  │
    └────┬────┘
         │
    ┌────┴────┐
    │          │
   YES         NO
    │          │
    ▼          ▼
┌──────────────────┐  ┌─────────────────┐
│ Reply to Issue   │  │ Create New Issue│
│ - "Me too" msg  │  │ - Full report   │
│ - Attach logs    │  │ - All context   │
└──────────────────┘  └─────────────────┘
```

## Bug Detection

### Error Types to Report

1. **Fatal Errors**: Script crashes or exits unexpectedly
2. **Unexpected Behavior**: Function returns incorrect results
3. **File System Errors**: Cannot read/write files
4. **Data Corruption**: TODO.md structure becomes invalid
5. **Migration Failures**: Migration system errors
6. **Permission Errors**: Cannot access required files/directories

### Detection Mechanism

```zsh
# Wrapper function to catch errors
report_bug_on_error() {
    local command="$@"
    if ! eval "$command" 2>&1; then
        local exit_code=$?
        # Collect error context and report
        collect_error_context "$exit_code" "$command"
        return $exit_code
    fi
}
```

### Error Context Collection

- **Error Message**: Captured from stderr/stdout
- **Command**: What was being executed
- **Exit Code**: Process exit status
- **Stack Trace**: Function call stack (if available)
- **Log Files**: Recent entries from `.todo.ai/.todo.ai.log`
- **System Info**: OS version, shell version, script version
- **TODO.md State**: Recent changes, structure validation
- **File Permissions**: Relevant file permissions
- **Disk Space**: Available disk space

**Private Repository Considerations**:
- **Exclude**: Repository name, URL, commit hashes, branch names
- **Include**: Only todo.ai-specific information (version, logs, errors)
- **Sanitize**: Remove any paths or identifiers that reveal repository structure

## Duplicate Detection

### Similarity Matching

**Strategy**: Use multiple heuristics to detect similar issues:

1. **Title Similarity**: 
   - Exact match on error message keywords
   - Fuzzy matching on error descriptions
   - Pattern matching on error types

2. **Body Similarity**:
   - Compare error messages
   - Match stack traces
   - Similar error codes/patterns

3. **Recent Issues**: Check issues from last 30 days first (most relevant)

### Implementation

```zsh
check_for_duplicate_issues() {
    local title="$1"
    local body="$2"
    
    # Search for issues with similar titles
    # Note: This only searches, doesn't automatically reply
    local similar_issues=$(gh issue list \
        --repo "$REPO" \
        --search "in:title $title" \
        --limit 10 \
        --json number,title,body,state)
    
    # Check each issue for similarity
    local duplicates=()
    for issue in "$similar_issues"; do
        local similarity=$(calculate_similarity "$title" "$body" "$issue")
        if [[ $similarity -ge 75 ]]; then
            duplicates+=("$issue")  # Potential duplicate
        fi
    done
    
    # Return duplicates found (user will confirm)
    echo "${duplicates[@]}"
}
```

### Duplicate Detection with User Confirmation

```zsh
handle_duplicate_detection() {
    local title="$1"
    local body="$2"
    
    local duplicates=$(check_for_duplicate_issues "$title" "$body")
    
    if [[ -n "$duplicates" ]]; then
        echo "Similar issues found:"
        # Show similar issues
        # ...
        echo ""
        printf "Would you like to add a 'me too' comment to an existing issue? (y/N) "
        read -r reply
        if [[ "$reply" =~ ^[Yy]$ ]]; then
            # User selects which issue to reply to
            reply_to_existing_issue "$selected_issue" "$body"
        else
            printf "Create a new issue instead? (y/N) "
            read -r reply
            if [[ "$reply" =~ ^[Yy]$ ]]; then
                create_new_issue "$title" "$body"
            fi
        fi
    else
        # No duplicates, ask to create new issue
        printf "Would you like to create a new issue? (y/N) "
        read -r reply
        if [[ "$reply" =~ ^[Yy]$ ]]; then
            create_new_issue "$title" "$body"
        fi
    fi
}
```

### Similarity Threshold

**Starting Point**: 75% similarity threshold
- **75%+ similarity**: Likely duplicate - suggest replying to existing issue (with user confirmation)
- **50-74% similarity**: Possible duplicate - show similar issues to user for confirmation
- **<50% similarity**: Different issue - suggest creating new one

**Note**: Threshold will be tested and adjusted based on real-world usage. The goal is to catch obvious duplicates while avoiding false positives.

## Bug Report Template

### Format

```markdown
## Bug Report

**Version**: 1.4.3
**Date**: 2025-11-01 12:15:00
**OS**: macOS 24.6.0
**Shell**: zsh 5.9

### Error
```
[Error message here]
```

### Command
```bash
./todo.ai [command]
```

### Stack Trace
```
[Stack trace if available]
```

### Recent Logs
```
[Last 20 log entries from .todo.ai/.todo.ai.log]
```

### System Information
- OS: macOS 24.6.0
- Shell: zsh 5.9
- Script Version: 1.4.3
- Git Repository: [if available]

### Additional Context
[Any additional relevant information]

---
*Reported automatically by todo.ai*
```

## GitHub CLI Integration

### Prerequisites

1. **GitHub CLI installed**: `command -v gh`
2. **Authenticated**: `gh auth status`
3. **Repository access**: User has permissions to create issues

### Commands

```zsh
# Create new issue
gh issue create \
    --repo "$REPO" \
    --title "Bug: [error summary]" \
    --body-file "$BUG_REPORT_FILE" \
    --label "bug,auto-reported"

# Search for similar issues
gh issue list \
    --repo "$REPO" \
    --search "in:title [keywords]" \
    --limit 10

# Add comment to existing issue
gh issue comment [ISSUE_NUMBER] \
    --repo "$REPO" \
    --body "$ME_TOO_MESSAGE"

# Attach file/logs to comment
gh issue comment [ISSUE_NUMBER] \
    --repo "$REPO" \
    --body-file "$COMMENT_FILE"
```

## "Me Too" Reply

### Message Template

```markdown
## Me Too - Same Issue Encountered

**Version**: 1.4.3
**Date**: 2025-11-01 12:15:00
**OS**: macOS 24.6.0

I'm experiencing the same error. Here's my context:

### Error
```
[Error message]
```

### Command
```bash
./todo.ai [command]
```

### Logs
[Attached log file or relevant excerpts]

---
*Reported automatically by todo.ai*
```

### Attachment Strategy

- **Small logs (< 10KB)**: Include directly in comment body
- **Large logs (> 10KB)**: Create gist and link to it
- **Multiple files**: Create gist with all files

## Log Collection

### Log Files to Include

1. **`.todo.ai/.todo.ai.log`**: Recent entries (last 50 lines)
2. **`release/RELEASE_LOG.log`**: If release-related error
3. **Error-specific logs**: Migration logs, backup logs, etc.

### Filtering

- Remove sensitive information (passwords, tokens, personal data)
- Truncate very long logs (keep last N lines)
- Include timestamp range in log excerpts

## Implementation Details

### Configuration

```zsh
# Bug reporting configuration
BUG_REPORT_ENABLED="${BUG_REPORT_ENABLED:-true}"
BUG_REPORT_REPO="${BUG_REPORT_REPO:-$(git remote get-url origin 2>/dev/null | sed 's/\.git$//' | sed 's/git@github\.com:/https:\/\/github.com\//' || echo '')}"
BUG_REPORT_THRESHOLD="${BUG_REPORT_THRESHOLD:-75}"  # Similarity threshold (%) - will be tested and adjusted
```

### Function Structure

```zsh
# Main entry point - ALWAYS requires user confirmation
suggest_bug_report() {
    local error_message="$1"
    local error_context="$2"
    
    # Collect full context
    local bug_report=$(generate_bug_report "$error_message" "$error_context")
    
    # Show error and suggest reporting
    echo "⚠️  An error occurred: $error_message"
    echo ""
    echo "Would you like to report this bug to GitHub Issues?"
    echo ""
    echo "Preview of bug report:"
    echo "---"
    echo "$bug_report" | head -30
    echo "---"
    echo ""
    
    # Always require confirmation
    printf "Report this bug? (y/N) "
    read -r reply
    
    if [[ ! "$reply" =~ ^[Yy]$ ]]; then
        echo "Bug report cancelled by user"
        return 0
    fi
    
    # User confirmed - proceed with duplicate check and reporting
    handle_duplicate_detection "$error_message" "$bug_report"
}

# Helper functions
collect_error_context() { ... }
generate_bug_report() { ... }
check_for_duplicate_issues() { ... }
calculate_similarity() { ... }
create_new_issue() { ... }
reply_to_existing_issue() { ... }
collect_logs() { ... }
```

### Error Handler Integration

```zsh
# Wrap commands with error handling
safe_execute() {
    local command="$@"
    if ! eval "$command" 2>&1; then
        local exit_code=$?
        local error_output=$(eval "$command" 2>&1)
        report_bug "Command failed: $command" "$error_output"
        return $exit_code
    fi
}
```

## User Control

### Manual Confirmation Required

**CRITICAL**: Bug reporting is NEVER automatic. The system will:
1. Detect errors and suggest reporting
2. Prepare bug report with all context
3. **Always ask user for confirmation before sending**
4. Show preview of what will be sent
5. Require explicit user approval (cannot be skipped)

This ensures:
- Users maintain full control
- No unexpected API calls
- Rate limits are not an issue
- Privacy is protected

### Confirmation Flow

```zsh
report_bug() {
    local error_message="$1"
    local error_context="$2"
    
    # Generate bug report
    local bug_report=$(generate_bug_report "$error_message" "$error_context")
    
    # Show error and suggestion
    echo "⚠️  An error occurred: $error_message"
    echo ""
    echo "Would you like to report this bug to GitHub Issues?"
    echo ""
    echo "Preview of bug report:"
    echo "---"
    echo "$bug_report" | head -20
    echo "---"
    echo ""
    printf "Report this bug? (y/N) "
    read -r reply
    
    if [[ ! "$reply" =~ ^[Yy]$ ]]; then
        echo "Bug report cancelled by user"
        return 0
    fi
    
    # Proceed with reporting
    # ... (rest of reporting logic)
}
```

### Manual Reporting Command

```bash
./todo.ai report-bug "Error description" --logs --context
```

### Cursor Rules Integration

Each installation will automatically add cursor rules that remind AI agents:
- **Always suggest** bug reporting when errors occur
- **Never automatically** send bug reports
- **Always require** user confirmation before any GitHub API calls

## Testing Strategy

### Unit Tests

1. **Bug Report Generation**: Verify template formatting
2. **Duplicate Detection**: Test similarity matching algorithms with different thresholds
3. **Log Collection**: Ensure correct log extraction
4. **Context Collection**: Verify all relevant data gathered
5. **Similarity Threshold Testing**: Test various thresholds (50%, 60%, 70%, 75%, 80%, 90%) to find optimal balance

### Integration Tests

1. **GitHub CLI Integration**: Test issue creation (use test repo)
2. **Duplicate Detection**: Test against real GitHub Issues
3. **"Me Too" Flow**: Test replying to existing issues
4. **Error Handling**: Test behavior when GitHub CLI unavailable
5. **Manual Confirmation**: Verify confirmation is always required and cannot be bypassed

### Manual Testing

1. Trigger intentional errors and verify reporting suggestion (not automatic)
2. Test duplicate detection with known similar issues
3. Verify logs are correctly attached
4. Test manual confirmation flow
5. Test similarity threshold effectiveness with real issues

## Security and Privacy

### Data Sanitization

- Remove sensitive information from logs
- Filter out passwords, tokens, API keys
- Sanitize file paths (remove user-specific paths if needed)
- Review collected data before sending
- **Private Repository Protection**: For private repos, remove all repository identifiers
  - No repository name
  - No repository URL
  - No commit hashes that reveal repo
  - Only include: todo.ai version, OS, shell, error details, logs (sanitized)

### User Consent

- **Always ask before sending bug reports** (mandatory confirmation)
- Show preview of what will be sent
- Allow editing before submission
- User can cancel at any time
- Never send automatically, even if user previously approved similar reports

## Future Enhancements

1. **Issue Updates**: Optionally update existing issues when bugs are fixed (with user confirmation)
2. **Issue Linking**: Suggest linking related issues (manual only)
3. **Crash Reports**: Enhanced crash dumps for fatal errors
4. **Analytics**: Track common error patterns (anonymized, opt-in)
5. **User Feedback Loop**: Optionally notify users when their reported bugs are fixed

## Cursor Rules Integration

The bug reporting system will automatically add cursor rules to `.cursor/rules/` on each installation to ensure AI agents follow the correct behavior:

```markdown
## Bug Reporting

When todo.ai encounters errors or unexpected behavior:

1. **Always suggest** bug reporting to the user
2. **Never automatically** send bug reports to GitHub
3. **Always require** explicit user confirmation before any GitHub API calls
4. **Show preview** of bug report before asking for confirmation
5. **Respect privacy**: For private repositories, remove all repo identifiers

Example:
- ✅ "An error occurred. Would you like me to prepare a bug report for GitHub?"
- ❌ "Error occurred. Automatically reporting to GitHub..." (NEVER DO THIS)
```

## Decisions Made

1. **Manual Confirmation Required**: Always ask before sending, never automatic
2. **GitHub Only**: This project is on GitHub, no other trackers needed
3. **Similarity Threshold**: Starting at 75%, will be tested and adjusted
4. **Rate Limits**: Not an issue since all reporting requires manual confirmation
5. **Private Repos**: Hide all repository identifiers, only include todo.ai-specific information

