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
echo ""
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

