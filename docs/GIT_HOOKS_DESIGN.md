# Git Hooks Design

## Overview

Git hooks will automatically validate code quality and consistency before commits are allowed. This ensures that linting errors, formatting issues, and TODO.md problems are caught before they enter the repository.

## Problem Statement

Currently, there are no automated checks before commits. This can lead to:
- Committing files with linting errors (Markdown, YAML, JSON)
- Committing TODO.md with formatting issues or broken structure
- Inconsistent code quality across commits
- Manual review required for catchable issues

## Goals

1. **Automated Validation**: Run linting checks automatically before commits
2. **Fast Execution**: Hooks should complete quickly (< 2 seconds)
3. **Clear Feedback**: Provide actionable error messages
4. **Bypass Option**: Allow `--no-verify` for emergency bypasses (logged)
5. **Comprehensive Coverage**: Validate Markdown, YAML, JSON, and TODO.md files

## Architecture

### Components

1. **Pre-commit Hook**: Main entry point for validation
2. **File Detection**: Identify changed files by type
3. **Linting Engine**: Run appropriate linter for each file type
4. **Error Aggregation**: Collect all errors and present together
5. **Exit Handling**: Block commit on errors, allow on success

### Workflow

```
┌─────────────────┐
│ git commit      │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Pre-commit Hook    │
│ Triggered          │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Get Staged Files    │
│ - Detect file types │
│ - Filter relevant  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Run Validators     │
│ ├─ Markdown linter │
│ ├─ YAML linter     │
│ ├─ JSON linter     │
│ └─ TODO.md lint    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Check Results      │
│ - Any errors?      │
└────────┬────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌──────┐  ┌──────────┐
│ Pass │  │ Fail     │
└──┬───┘  └──┬───────┘
   │         │
   ▼         ▼
Allow     Block
commit    commit
```

## Implementation Details

### Hook Structure

The pre-commit hook will be located at `.git/hooks/pre-commit`:

```zsh
#!/bin/zsh
# Pre-commit hook for todo.ai repository
# Validates Markdown, YAML, JSON, and TODO.md files before commit

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track if any errors occurred
errors=0

echo "🔍 Running pre-commit validations..."

# Get staged files
staged_files=$(git diff --cached --name-only --diff-filter=ACM)

if [[ -z "$staged_files" ]]; then
    echo "✅ No staged files to validate"
    exit 0
fi

# Validate TODO.md if it's in staged files
if echo "$staged_files" | grep -q "TODO.md"; then
    echo "📋 Validating TODO.md..."
    if ! ./todo.ai --lint 2>/dev/null; then
        echo -e "${RED}❌ TODO.md validation failed${NC}"
        echo "   Run './todo.ai --lint' to see details"
        errors=$((errors + 1))
    else
        echo -e "${GREEN}✅ TODO.md validation passed${NC}"
    fi
fi

# Validate Markdown files
md_files=$(echo "$staged_files" | grep -E '\.(md|mdc)$' || true)
if [[ -n "$md_files" ]]; then
    echo "📝 Validating Markdown files..."
    # Markdown linting implementation
    # ... (see Markdown Linting section)
fi

# Validate YAML files
yaml_files=$(echo "$staged_files" | grep -E '\.(yml|yaml)$' || true)
if [[ -n "$yaml_files" ]]; then
    echo "📄 Validating YAML files..."
    # YAML linting implementation
    # ... (see YAML Linting section)
fi

# Validate JSON files
json_files=$(echo "$staged_files" | grep -E '\.json$' || true)
if [[ -n "$json_files" ]]; then
    echo "📊 Validating JSON files..."
    # JSON linting implementation
    # ... (see JSON Linting section)
fi

# Exit with error if any validations failed
if [[ $errors -gt 0 ]]; then
    echo ""
    echo -e "${RED}❌ Pre-commit validation failed${NC}"
    echo "   Fix errors above and try again"
    echo "   Use 'git commit --no-verify' to bypass (not recommended)"
    exit 1
fi

echo -e "${GREEN}✅ All validations passed${NC}"
exit 0
```

### File Type Detection

The hook will identify files to validate based on extensions:

- **Markdown**: `.md`, `.mdc` files
- **YAML**: `.yml`, `.yaml` files
- **JSON**: `.json` files
- **TODO.md**: Special handling for `TODO.md` using `todo.ai --lint`

### Markdown Linting (Task #15.1)

**Tool Options:**
- `markdownlint` (markdownlint-cli2) - Recommended
- `mdl` (Markdownlint) - Alternative
- Custom validation script - Fallback

**Implementation:**

```zsh
validate_markdown() {
    local files="$1"
    local errors=0
    
    # Check if markdownlint-cli2 is available
    if command -v markdownlint-cli2 >/dev/null 2>&1; then
        for file in $files; do
            if ! markdownlint-cli2 "$file" 2>/dev/null; then
                errors=$((errors + 1))
            fi
        done
    elif command -v mdl >/dev/null 2>&1; then
        # Fallback to mdl
        for file in $files; do
            if ! mdl "$file" 2>/dev/null; then
                errors=$((errors + 1))
            fi
        done
    else
        # Basic validation: check for common issues
        echo "⚠️  No Markdown linter found, skipping Markdown validation"
        echo "   Install 'markdownlint-cli2' or 'mdl' for Markdown linting"
    fi
    
    return $errors
}
```

**Configuration:**
- Create `.markdownlint.json` or `.markdownlint.yaml` for repository-specific rules
- Exclude auto-generated files (e.g., `release/RELEASE_LOG.log`)

### YAML Linting (Task #15.2)

**Tool Options:**
- `yamllint` (Python-based) - Recommended
- `yq` validation - Alternative
- Custom validation script - Fallback

**Implementation:**

```zsh
validate_yaml() {
    local files="$1"
    local errors=0
    
    # Check if yamllint is available
    if command -v yamllint >/dev/null 2>&1; then
        for file in $files; do
            if ! yamllint -d relaxed "$file" 2>/dev/null; then
                errors=$((errors + 1))
            fi
        done
    elif command -v yq >/dev/null 2>&1; then
        # Fallback to yq validation
        for file in $files; do
            if ! yq eval '.' "$file" >/dev/null 2>&1; then
                echo "❌ Invalid YAML: $file"
                errors=$((errors + 1))
            fi
        done
    else
        # Basic validation: check syntax
        echo "⚠️  No YAML linter found, skipping YAML validation"
        echo "   Install 'yamllint' or 'yq' for YAML linting"
    fi
    
    return $errors
}
```

**Configuration:**
- Create `.yamllint` configuration file
- Set relaxed rules for YAML front matter in `.mdc` files

### JSON Linting (Task #15.3)

**Tool Options:**
- `jq` - Recommended (validates JSON syntax)
- `jsonlint` - Alternative
- Custom validation script - Fallback

**Implementation:**

```zsh
validate_json() {
    local files="$1"
    local errors=0
    
    # Check if jq is available
    if command -v jq >/dev/null 2>&1; then
        for file in $files; do
            if ! jq empty "$file" 2>/dev/null; then
                echo "❌ Invalid JSON: $file"
                errors=$((errors + 1))
            fi
        done
    elif command -v jsonlint >/dev/null 2>&1; then
        # Fallback to jsonlint
        for file in $files; do
            if ! jsonlint "$file" 2>/dev/null; then
                errors=$((errors + 1))
            fi
        done
    else
        # Basic validation: check syntax with Python
        for file in $files; do
            if ! python3 -m json.tool "$file" >/dev/null 2>&1; then
                echo "❌ Invalid JSON: $file"
                errors=$((errors + 1))
            fi
        done
    fi
    
    return $errors
}
```

### TODO.md Linting (Task #15.4)

**Tool:** Use existing `todo.ai --lint` command

**Implementation:**

```zsh
validate_todo() {
    local errors=0
    
    # Check if TODO.md exists
    if [[ ! -f "TODO.md" ]]; then
        echo "⚠️  TODO.md not found, skipping validation"
        return 0
    fi
    
    # Check if todo.ai exists and is executable
    if [[ ! -x "./todo.ai" ]]; then
        echo "⚠️  todo.ai not found or not executable, skipping TODO validation"
        return 0
    fi
    
    # Run todo.ai --lint
    if ! ./todo.ai --lint 2>/dev/null; then
        echo "❌ TODO.md validation failed"
        echo "   Run './todo.ai --lint' to see details"
        errors=$((errors + 1))
    fi
    
    return $errors
}
```

**What it validates:**
- Task ID format and uniqueness
- Subtask parent relationships
- Formatting issues (indentation, checkboxes)
- Tag format
- Section structure

## Installation

### Setup Script

Create a setup script at `scripts/setup-git-hooks.sh`:

```zsh
#!/bin/zsh
# Setup git hooks for todo.ai repository

set -e

HOOKS_DIR=".git/hooks"
PRE_COMMIT_HOOK="$HOOKS_DIR/pre-commit"

# Check if .git directory exists
if [[ ! -d ".git" ]]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Create hooks directory if it doesn't exist
mkdir -p "$HOOKS_DIR"

# Copy pre-commit hook
if [[ -f "scripts/pre-commit-hook.sh" ]]; then
    cp "scripts/pre-commit-hook.sh" "$PRE_COMMIT_HOOK"
    chmod +x "$PRE_COMMIT_HOOK"
    echo "✅ Pre-commit hook installed"
else
    echo "❌ Error: scripts/pre-commit-hook.sh not found"
    exit 1
fi

# Check for required tools
echo "🔍 Checking for required linting tools..."

missing_tools=()

if ! command -v markdownlint-cli2 >/dev/null 2>&1 && ! command -v mdl >/dev/null 2>&1; then
    missing_tools+=("Markdown linter (markdownlint-cli2 or mdl)")
fi

if ! command -v yamllint >/dev/null 2>&1 && ! command -v yq >/dev/null 2>&1; then
    missing_tools+=("YAML linter (yamllint or yq)")
fi

if ! command -v jq >/dev/null 2>&1 && ! command -v jsonlint >/dev/null 2>&1; then
    missing_tools+=("JSON linter (jq or jsonlint)")
fi

if [[ ${#missing_tools[@]} -gt 0 ]]; then
    echo "⚠️  Missing recommended tools:"
    for tool in "${missing_tools[@]}"; do
        echo "   - $tool"
    done
    echo ""
    echo "Hooks will use basic validation or skip checks if tools are missing"
else
    echo "✅ All recommended tools are installed"
fi

echo ""
echo "✅ Git hooks setup complete!"
```

## Configuration Files

### Markdown Lint Configuration

Create `.markdownlint.yaml`:

```yaml
default: true
extends: default
rules:
  line-length: false  # Allow long lines
  no-duplicate-heading: false  # Allow duplicate headings
  no-trailing-punctuation: false  # Allow trailing punctuation
```

### YAML Lint Configuration

Create `.yamllint`:

```yaml
extends: default

rules:
  line-length: disable
  comments: disable
  comments-indentation: disable
  
# Allow relaxed rules for front matter
yaml-files:
  - '*.yml'
  - '*.yaml'
  - '*.mdc'
```

## Testing Strategy

### Unit Tests

1. **Test each validator independently:**
   - Markdown validator with valid/invalid files
   - YAML validator with valid/invalid files
   - JSON validator with valid/invalid files
   - TODO.md validator with valid/invalid TODO.md

2. **Test hook integration:**
   - Hook blocks commit on errors
   - Hook allows commit on success
   - Hook handles missing tools gracefully
   - Hook handles no staged files

### Integration Tests

1. **Test full workflow:**
   - Stage files with linting errors → commit should fail
   - Stage files without errors → commit should succeed
   - Test `--no-verify` bypass option

2. **Test with real files:**
   - Valid Markdown files
   - Invalid Markdown files
   - Invalid YAML
   - Invalid JSON
   - Valid/invalid TODO.md

## Error Handling

### Missing Tools

If required linting tools are not installed:
- Show warning message
- Use basic validation if available
- Skip validation if no fallback exists
- Do not block commits (warn only)

### Performance

- Hooks should complete in < 2 seconds
- Only validate staged files (not entire repository)
- Use parallel execution where possible
- Cache results for unchanged files if needed

### Bypass Option

Users can bypass hooks with:
```bash
git commit --no-verify -m "message"
```

**Note:** This should be logged and used sparingly. Document when bypass is acceptable.

## Future Enhancements

1. **Auto-fix Mode**: Automatically fix simple linting errors before commit
2. **Configuration Management**: Allow per-user or per-branch hook configurations
3. **Performance Optimization**: Cache validation results for unchanged files
4. **Additional Validators**: Add more file type validators (Shell script linting, etc.)
5. **Pre-push Hook**: Validate remote branch state before push

## Dependencies

### Required Tools

- `git` - Already available
- `zsh` - Already available

### Recommended Tools

- `markdownlint-cli2` - Markdown linting (or `mdl` as fallback)
- `yamllint` - YAML linting (or `yq` as fallback)
- `jq` - JSON validation (or `jsonlint`/Python as fallback)
- `todo.ai` - TODO.md validation (already in repo)

### Installation Instructions

#### Direct Installation Methods

**For Markdown Linting (markdownlint-cli2 or mdl):**

```bash
# Option 1: markdownlint-cli2 (Recommended - npm/Node.js)
npm install -g markdownlint-cli2

# Verify installation
markdownlint-cli2 --version

# Option 2: mdl (Alternative - Ruby gem)
gem install mdl

# Verify installation
mdl --version
```

**For YAML Linting (yamllint or yq):**

```bash
# Option 1: yamllint (Recommended - Python)
pip install yamllint

# Or with pip3
pip3 install yamllint

# Verify installation
yamllint --version

# Option 2: yq (Alternative - YAML processor with validation)
# macOS
brew install yq

# Linux (Ubuntu/Debian)
sudo apt-get install yq

# Linux (Other distributions)
# Download from https://github.com/mikefarah/yq/releases

# Verify installation
yq --version
```

**For JSON Linting (jq or jsonlint):**

```bash
# Option 1: jq (Recommended - JSON processor)
# macOS
brew install jq

# Linux (Ubuntu/Debian)
sudo apt-get install jq

# Linux (Fedora/RHEL)
sudo dnf install jq

# Linux (Arch)
sudo pacman -S jq

# Verify installation
jq --version

# Option 2: jsonlint (Alternative - npm/Node.js)
npm install -g jsonlint

# Verify installation
jsonlint --version

# Option 3: Python json.tool (Built-in fallback)
# No installation needed - included with Python 3
python3 -m json.tool --help
```

#### Automated Setup Script

After forking the `todo.ai` repository, developers can use the automated setup script to install all required linting tools:

```bash
# Run the setup script
./developer/setup-linters.sh
```

**What the script does:**
1. **Detects available package managers** (npm, pip3, brew, apt-get, etc.)
2. **Installs missing tools** automatically based on detected package managers
3. **Installs git hooks** by running `scripts/setup-git-hooks.sh`
4. **Provides installation summary** showing which tools were installed or skipped

**For AI Agents (Copy-paste these to your agent):**

```
Install the required linting tools for git hooks by running the automated setup script:

./developer/setup-linters.sh

The script will:
- Detect available package managers
- Install markdownlint-cli2 (via npm) or mdl (via gem)
- Install yamllint (via pip3) or yq (via brew/apt-get)
- Install jq (via brew/apt-get/dnf/pacman) or jsonlint (via npm) or use python3 json.tool
- Install git hooks via scripts/setup-git-hooks.sh
- Show installation summary

If manual installation is needed, see docs/GIT_HOOKS_DESIGN.md for detailed instructions.
```

**Manual Installation (Alternative):**

If the automated script doesn't work or you prefer manual installation:

**Agent Installation Workflow:**

1. **Detect platform and package managers:**
   ```zsh
   # Check available package managers
   command -v npm >/dev/null && echo "npm available"
   command -v pip3 >/dev/null && echo "pip3 available"
   command -v brew >/dev/null && echo "brew available (macOS)"
   command -v apt-get >/dev/null && echo "apt-get available (Linux)"
   ```

2. **Install tools based on availability:**
   - Prefer npm for markdownlint-cli2
   - Prefer pip3 for yamllint
   - Prefer brew on macOS, apt-get on Linux for jq
   - Use fallbacks (mdl, yq, jsonlint, python3) if primary tools aren't available

3. **Run automated setup script:**
   ```bash
   ./developer/setup-linters.sh
   ```
   
   This script will install all tools and then run `./scripts/setup-git-hooks.sh` automatically.

4. **Verify installation:**
   The setup script will automatically check for all tools and report any missing ones.

#### Installation Notes

- **Tool Availability**: The git hooks will work even if some tools are missing. They will show warnings but won't block commits.
- **Fallback Support**: Each validator has multiple fallback options, so partial installation is acceptable.
- **Recommended Setup**: For full validation support, install all recommended tools (markdownlint-cli2, yamllint, jq).
- **Development Setup**: After forking, developers should install tools to get full validation benefits, but the hooks will still work with basic validation or skipped checks.

## Decisions Made

1. **Use Pre-commit Hook**: Validate before commit, not after
2. **Allow Missing Tools**: Don't block commits if tools are missing (warn only)
3. **Fast Execution**: Only validate staged files, not entire repository
4. **Clear Error Messages**: Provide actionable feedback to fix issues
5. **Bypass Option**: Allow `--no-verify` for emergency situations
6. **Tool Flexibility**: Support multiple tools for each file type (fallback chain)

