# ai-todo Test Strategy

## Purpose

- Establish a repeatable, automated test framework that validates all behavior exposed by `ai-todo`
- Catch regressions quickly while supporting rapid iteration by AI agents and humans alike
- Provide guidance for contributors on how to extend coverage when new commands or features are introduced

## Scope Overview

- **System under test:** `ai-todo` Python package (CLI and MCP server)
- **Primary artifacts:** `TODO.md`, `.ai-todo/` directory (config, serial, log, state)
- **Out of scope:** Legacy shell scripts (frozen as of 2026-01-27, see `legacy/todo.ai`)

## Guiding Principles

- Tests must be deterministic, hermetic, and executable without network access (where possible)
- Every test runs in a temporary workspace; never mutate the developer's real `TODO.md`
- Prefer testing through the public API (CLI commands, MCP tools) over internal implementation details
- Use fixtures for complex state setup; avoid brittle sequential dependencies between tests

## Test Architecture

- **Runner:** pytest with coverage reporting via pytest-cov
- **Framework:** Standard pytest fixtures, parametrization, and markers
- **Layout:**
  - `tests/unit/` → Unit tests for individual modules and functions
  - `tests/integration/` → Integration tests for CLI commands and MCP tools
  - `tests/e2e/` → End-to-end workflow tests
  - `tests/validation/` → Validation tests (complete parity audit, show command tests)
  - `tests/conftest.py` → Shared fixtures and test configuration
  - `tests/integration/test_data/` → Fixture data for integration tests

## Environment & Tooling Requirements

- Python 3.10+ (development uses 3.14)
- `uv` for dependency management
- `pytest` with `pytest-cov` for test execution and coverage
- `ruff` for linting and formatting
- `mypy` for type checking

## Test Fixture Strategy

- Use `conftest.py` fixtures for common setup (isolated TODO directories, CLI runners)
- The `test_data/` directory contains baseline TODO.md and `.ai-todo/` configuration
- Tests use `tmp_path` fixture for isolated temporary directories
- Use `reset_test_data.py` to restore test fixtures to known state

## Coverage Matrix

| Area | Key Behaviors | Test Location |
|------|---------------|---------------|
| CLI Commands | add-task, complete, list, modify-task, delete, archive, restore, etc. | `tests/integration/test_cli.py` |
| MCP Tools | All MCP tools match CLI behavior | `tests/integration/test_mcp_cli_parity.py` |
| Task Lifecycle | Creation, completion, archival, deletion, restoration | `tests/e2e/test_workflows.py` |
| Subtasks | Parent-child relationships, cascade operations | `tests/integration/test_subtask_ordering.py` |
| Notes/Description | set-description, notes management | `tests/integration/test_cli.py` |
| Tags | set-tags, tag filtering | `tests/integration/test_cli.py` |
| Task Relationships | Dependencies, relates-to | `tests/integration/test_cli.py` |
| File Operations | TODO.md parsing, writing, integrity | `tests/unit/test_file_ops.py` |
| Configuration | Config loading, validation | `tests/unit/test_config.py` |
| Coordination | Serial number management, GitHub coordination | `tests/unit/test_coordination.py` |
| Tamper Detection | Checksum validation, tamper modes | `tests/unit/test_tamper_detection.py` |
| Migrations | Version migrations | `tests/unit/test_migrations.py` |

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=ai_todo --cov-report=term

# Run specific test categories
uv run pytest tests/unit          # Unit tests only
uv run pytest tests/integration   # Integration tests only
uv run pytest tests/e2e           # End-to-end tests only

# Run specific test file
uv run pytest tests/unit/test_task.py

# Run tests matching a pattern
uv run pytest -k "test_add"
```

## CI/CD Integration

- Tests run automatically on push to `main` and on pull requests
- Full test matrix: Python 3.10-3.14 on Linux, macOS, and Windows
- Coverage reports uploaded to Codecov
- Pre-commit hooks run quality checks before commit

## Historical Note

Prior to v3.1, this project maintained shell/Python parity tests comparing the legacy
shell script output to Python CLI output. After the API terminology standardization
(task#253), Python and shell implementations intentionally diverged. The shell scripts
are now frozen (task#254) and parity tests have been removed. The legacy shell scripts
(`legacy/todo.ai`, `todo.bash`) are still distributed for backward compatibility but
receive no feature updates.
