#!/bin/bash
set -e

echo "🚀 Setting up todo.ai development environment..."

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add uv to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Sync dependencies
echo "📦 Installing dependencies..."
uv sync --all-extras

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
uv run pre-commit install

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  - Run tests: uv run pytest"
echo "  - Run linting: uv run ruff check ."
echo "  - Run type checking: uv run mypy todo_ai"
echo "  - Run pre-commit on all files: uv run pre-commit run --all-files"
