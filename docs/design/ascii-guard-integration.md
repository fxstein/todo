# ASCII-Guard Integration Design

**Status:** Design
**Created:** 2026-01-31
**Task:** #272.1 ([AIT-9](https://linear.app/fxstein/issue/AIT-9))

## Why

AI-generated ASCII diagrams in our documentation (17+ files) often have subtle alignment errors that break visual integrity. We need automated validation to ensure consistency without manual review overhead.

## What

Integrate `ascii-guard` (our own linting tool for ASCII box-drawing characters) into:

- Pre-commit hooks - catch issues before commit
- CI/CD workflows - block merges with malformed diagrams
- Documentation - 17+ files need initial cleanup

## How

### 1. Add Dependency

```toml
# pyproject.toml
[project.optional-dependencies]
dev = [
    "ascii-guard>=1.5.0",  # Add to existing dev dependencies
]
```

### 2. Enable Pre-commit Hook

```yaml
# .pre-commit-config.yaml (uncomment and fix existing hook)
- id: ascii-guard
  name: ascii-guard
  entry: uv run ascii-guard lint  # Changed from plain 'ascii-guard lint'
  language: system
  types: [markdown]
  pass_filenames: true
  files: \.(md|mdc)$
  exclude: ^\.ai-todo/
```

### 3. Add to CI/CD

```yaml
# .github/workflows/ci-cd.yml (add to docs-quality job after markdownlint)
- name: Lint ASCII art boxes
  run: uv run ascii-guard lint '**/*.md' '**/*.mdc'
```

### 4. Clean Existing Docs

```bash
# Run once to fix existing 17+ files
uv run ascii-guard fix docs/
```

### 5. Add Validation Test

```python
# tests/validation/test_ascii_art_validation.py (new file)
def test_ascii_guard_passes_on_all_docs():
    """Verify all documentation passes ascii-guard linting."""
    result = subprocess.run(["uv", "run", "ascii-guard", "lint", "docs/"], ...)
    assert result.returncode == 0
```

## Rollout Order

1. Add dependency to `pyproject.toml`
2. Clean existing docs (`ascii-guard fix docs/`)
3. Enable pre-commit hook (uncomment + fix entry point)
4. Add CI/CD step to `docs-quality` job
5. Add validation test

## Rollback

Comment out pre-commit hook and CI/CD step. Remove from `pyproject.toml`.
