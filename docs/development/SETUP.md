# Development Environment Setup

This guide explains how to set up the todo.ai development environment using modern Python tooling.

## Prerequisites

- Python 3.10 or higher
- Git
- (Optional) `uv` - will be installed automatically if missing

## Quick Start

Run the one-step setup script:

```bash
./setup.sh
```

This script will:
1. Install `uv` if not present
2. Install all dependencies (including dev dependencies)
3. Set up pre-commit hooks

## Manual Setup

If you prefer to set up manually:

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

The installer places `uv` in `~/.local/bin` by default. Make sure this is in your PATH.

### 2. Install Dependencies

```bash
uv sync --all-extras
```

This installs both runtime and development dependencies based on `pyproject.toml` and `uv.lock`.

### 3. Install Pre-commit Hooks

```bash
uv run pre-commit install
```

## Development Workflow

### Running Tests

```bash
uv run pytest
```

### Running Linting

```bash
uv run ruff check .
```

### Running Type Checking

```bash
uv run mypy todo_ai
```

### Running All Pre-commit Checks

```bash
uv run pre-commit run --all-files
```

### Running Individual Commands

All development commands should be run through `uv run` to ensure they use the correct environment:

```bash
uv run pytest tests/unit/test_task.py
uv run ruff check todo_ai/core/task.py
uv run mypy todo_ai/core/task.py
```

## Dependencies

### Runtime Dependencies

Defined in `pyproject.toml` under `[project]` dependencies:
- `mcp>=0.1.0` - Model Context Protocol
- `click>=8.0.0` - CLI framework
- `pyyaml>=6.0` - YAML parsing
- `requests>=2.28.0` - HTTP client
- `pygithub>=1.59.0` - GitHub API client

### Development Dependencies

Defined in `pyproject.toml` under `[project.optional-dependencies]` dev:
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `ruff>=0.1.0` - Linting and formatting
- `mypy>=1.0.0` - Type checking
- `pre-commit>=3.0.0` - Git hooks framework
- `types-requests>=2.28.0` - Type stubs for requests
- `types-pyyaml>=6.0` - Type stubs for pyyaml

## Lock File

The `uv.lock` file ensures reproducible builds. It should be committed to version control.

To update dependencies:

```bash
# Update a specific package
uv add package-name

# Update all dependencies
uv lock --upgrade

# Sync after updating lock file
uv sync --all-extras
```

## Troubleshooting

### uv not found after installation

The installer places `uv` in `~/.local/bin`. Make sure this is in your PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Add this to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.) to make it permanent.

### Pre-commit hooks not running

Make sure hooks are installed:

```bash
uv run pre-commit install
```

You can also run hooks manually:

```bash
uv run pre-commit run --all-files
```

### Dependencies out of sync

If you see dependency errors, sync the environment:

```bash
uv sync --all-extras
```

## See Also

- [Development Guidelines](DEVELOPMENT_GUIDELINES.md)
- [Contributing Guide](../CONTRIBUTING.md) (if exists)
- [uv Documentation](https://github.com/astral-sh/uv)
- [pre-commit Documentation](https://pre-commit.com/)
