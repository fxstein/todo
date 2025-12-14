#!/bin/zsh
# Setup git hooks for todo.ai repository
# Uses pre-commit framework for modern Python development

set -e

# Check if .git directory exists
if [[ ! -d ".git" ]]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check if pre-commit is available
if command -v uv &> /dev/null; then
    echo "🔧 Installing pre-commit hooks via uv..."
    uv run pre-commit install
    echo "✅ Pre-commit hooks installed"
elif command -v pre-commit &> /dev/null; then
    echo "🔧 Installing pre-commit hooks..."
    pre-commit install
    echo "✅ Pre-commit hooks installed"
else
    echo "⚠️  Warning: pre-commit not found"
    echo "   Install it with: uv sync --all-extras"
    echo "   Or run: ./setup.sh"
    exit 1
fi

echo ""
echo "✅ Git hooks setup complete!"
echo ""
echo "To test hooks, run:"
if command -v uv &> /dev/null; then
    echo "  uv run pre-commit run --all-files"
else
    echo "  pre-commit run --all-files"
fi
