# ASCII-Guard Integration Design

**Status:** Design
**Created:** 2026-01-31
**Task:** #272.1 ([AIT-9](https://linear.app/fxstein/issue/AIT-9))

## Executive Summary

This document outlines the integration of `ascii-guard` into the ai-todo project to ensure consistent formatting of ASCII art diagrams in documentation. The tool will be integrated into both pre-commit hooks and CI/CD workflows to automatically detect and fix misaligned ASCII box-drawing characters.

## Background

### What is ascii-guard?

**ascii-guard** is a zero-dependency Python linter developed by fxstein that detects and fixes misaligned ASCII art boxes in documentation. AI-generated ASCII flowcharts and diagrams often have subtle formatting errors where box borders are misaligned by 1-2 characters, breaking visual integrity.

**Key Features:**

- Minimal dependencies (zero for Python 3.11+, one tiny dependency for 3.10)
- Tiny footprint and fast execution
- Type-safe with full mypy strict mode support
- Python API for programmatic integration
- Supports Unicode box-drawing characters: `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼`

**Links:**

- Repository: <https://github.com/fxstein/ascii-guard>
- PyPI: <https://pypi.org/project/ascii-guard/>
- Latest version: 1.5.0 (as of 2026-01-31)

### Why Integrate ascii-guard?

The ai-todo project contains extensive documentation with ASCII art diagrams for:

- Architecture flowcharts
- State machine diagrams
- Process flows
- Visual structure representations

**Current Situation:**

- 17+ markdown files contain ASCII box-drawing characters
- No automated validation ensures ASCII art alignment
- Manual review is error-prone and time-consuming
- AI-generated diagrams may have subtle misalignments

**Benefits of Integration:**

1. **Consistency** - All ASCII art maintained to the same visual standard
2. **Automation** - Catch issues early in pre-commit and CI/CD
3. **Documentation Quality** - Professional, readable diagrams
4. **Developer Experience** - Auto-fix capability reduces manual corrections

## Integration Points

### 1. Pre-commit Hook

**Location:** `.pre-commit-config.yaml`

**Current Status:**

The repository already has a commented-out ascii-guard hook (lines 64-71) with a note about "pipx environment issues":

```yaml
# Temporarily disabled due to pipx environment issues
# - id: ascii-guard
#   name: ascii-guard
#   entry: ascii-guard lint
#   language: system
#   types: [markdown]
#   pass_filenames: true
#   files: \.(md|mdc)$
```

**Proposed Configuration:**

```yaml
- repo: local
  hooks:
    - id: ascii-guard
      name: ascii-guard
      entry: uv run ascii-guard lint
      language: system
      types: [markdown]
      pass_filenames: true
      files: \.(md|mdc)$
      exclude: ^(\.ai-todo/|\.git/|node_modules/)
```

**Key Changes:**

1. **Use `uv run`** - Consistent with other Python tools in the pre-commit config (pytest, ai-todo lint)
2. **Include `.mdc` files** - Cursor rule files also contain documentation
3. **Exclude patterns** - Skip `.ai-todo/` state files and infrastructure directories

### 2. CI/CD Workflow

**Location:** `.github/workflows/ci-cd.yml`

**Target Job:** `docs-quality` (lines 104-161)

**Current Docs Quality Checks:**

1. Forbidden flags check
2. Markdownlint validation
3. TODO.md linting with ai-todo

**Proposed Addition:**

Add ascii-guard linting step after markdownlint:

```yaml
- name: Lint ASCII art boxes
  run: uv run ascii-guard lint '**/*.md' '**/*.mdc'
```

**Integration Strategy:**

- Run after markdownlint (both check markdown quality)
- Run before TODO.md linting (TODO.md may contain ASCII art)
- Use `uv run` for consistency with other Python tools
- Exit with non-zero status on errors (fail the CI job)

### 3. Configuration File

**Location:** `.ascii-guard.toml` (new file at repository root)

**Proposed Configuration:**

```toml
# .ascii-guard.toml
# Configuration for ascii-guard linter

[files]
# Scan all text files (empty = all)
extensions = []

# Exclude patterns (gitignore-style)
exclude = [
    ".git/",
    "node_modules/",
    "__pycache__/",
    ".venv/",
    "venv/",
    ".tox/",
    "build/",
    "dist/",
    ".mypy_cache/",
    ".pytest_cache/",
    ".ruff_cache/",
    "*.egg-info/",
    # Project-specific excludes:
    ".ai-todo/",           # ai-todo state directory
    ".cursor/",            # Cursor IDE files (skip if no docs)
    "htmlcov/",
    ".coverage",
    "uv.lock",
]

# Follow symbolic links when scanning
follow_symlinks = false

# Maximum file size to scan in MB
max_file_size = 10

[rules]
# Phase 2: Enable/disable specific validation rules (future)
# check_alignment = true
# check_corners = true
# check_width = true

[output]
# Phase 2: Output customization (future)
# color = "auto"
# verbose = false
```

**Configuration Rationale:**

1. **Empty extensions list** - Scan all text files (ascii-guard auto-detects)
2. **Exclude `.ai-todo/`** - State files, not documentation
3. **Exclude build artifacts** - Standard Python exclusions
4. **10MB file size limit** - Prevent processing large binaries/logs

## Document Cleanup Strategy

### Phase 1: Discovery

**Objective:** Identify all files with ASCII art and assess their current state.

**Method:**

```bash
# Find all files with box-drawing characters
rg '[┌┐└┘├┤┬┴┼─│]' --type md --files-with-matches

# Run ascii-guard lint to identify issues
uv run ascii-guard lint '**/*.md' '**/*.mdc'
```

**Expected Results:**

- List of 17+ files containing ASCII art (already identified)
- Count of alignment errors per file
- Severity assessment (cosmetic vs. structural)

### Phase 2: Auto-Fix

**Objective:** Use ascii-guard's auto-fix capability to correct alignment issues.

**Method:**

```bash
# Dry-run to preview changes
uv run ascii-guard fix --dry-run '**/*.md' '**/*.mdc'

# Apply fixes
uv run ascii-guard fix '**/*.md' '**/*.mdc'
```

**Files to Clean:**

Based on grep results, these files contain ASCII art:

- `docs/design/` (13 files)
- `docs/guides/` (2 files)
- `docs/archive/` (1 file)
- `docs/analysis/` (2 files)
- `docs/STRUCTURE.md` (1 file)

**Verification:**

1. Visual review of fixed diagrams (git diff)
2. Re-run ascii-guard lint (should pass with 0 errors)
3. Ensure diagrams render correctly in markdown viewers

### Phase 3: Documentation Update

**Files to Update:**

1. **README.md** - Add ascii-guard badge or mention
2. **CONTRIBUTING.md** - Document ascii-guard pre-commit hook
3. **docs/development/DEVELOPMENT_GUIDELINES.md** - Add ASCII art formatting guidelines

**Content to Add:**

```markdown
## ASCII Art Guidelines

This project uses [ascii-guard](https://github.com/fxstein/ascii-guard) to ensure consistent formatting of ASCII diagrams.

### Pre-commit Hook

ascii-guard runs automatically on commit via pre-commit hooks:

```bash
# Manual check
uv run ascii-guard lint docs/

# Auto-fix alignment issues
uv run ascii-guard fix docs/
```

### Creating ASCII Art

When creating new diagrams:

1. Use Unicode box-drawing characters: `─ │ ┌ ┐ └ ┘`
2. Ensure all borders align properly
3. Run `ascii-guard fix` before committing
4. Use ignore markers for intentionally broken examples (see ascii-guard docs)
```

## Testing Strategy

### Unit Tests

**Not Applicable** - ascii-guard is an external tool with its own test suite. No unit tests needed in ai-todo.

### Integration Tests

**Objective:** Verify ascii-guard integration works correctly in ai-todo workflows.

**Test Cases:**

1. **Pre-commit Hook Test**

   ```bash
   # Create a test file with misaligned ASCII art
   echo '┌─────┐\n│ Box │\n└────┘' > test_box.md

   # Stage file and attempt commit
   git add test_box.md
   git commit -m "test: ascii-guard integration"

   # Expected: Pre-commit hook catches misalignment
   ```

1. **CI/CD Test**

   - Create PR with misaligned ASCII art in docs/
   - Expected: `docs-quality` job fails with ascii-guard error
   - Fix alignment and push
   - Expected: `docs-quality` job passes

1. **Auto-fix Test**

   ```bash
   # Create misaligned box
   echo '┌─────┐\n│ Box │\n└────┘' > test_box.md

   # Run auto-fix
   uv run ascii-guard fix test_box.md

   # Verify fix
   uv run ascii-guard lint test_box.md
   # Expected: No errors
   ```

### Validation Tests

**Objective:** Ensure existing ASCII art in documentation is valid.

**Method:**

```bash
# Run ascii-guard on all documentation
uv run ascii-guard lint docs/

# Expected result after cleanup:
# ✅ All ASCII art boxes validated
# 0 errors found
```

**Test File:** `tests/validation/test_ascii_art_validation.py` (new)

```python
"""Validation tests for ASCII art formatting."""

import subprocess
from pathlib import Path


def test_ascii_guard_passes_on_all_docs():
    """Verify all documentation passes ascii-guard linting."""
    result = subprocess.run(
        ["uv", "run", "ascii-guard", "lint", "docs/"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"ascii-guard found errors in documentation:\n{result.stdout}\n{result.stderr}"
    )


def test_ascii_guard_installed():
    """Verify ascii-guard is installed and executable."""
    result = subprocess.run(
        ["uv", "run", "ascii-guard", "--version"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, "ascii-guard not installed or not executable"
    assert "ascii-guard" in result.stdout.lower(), "Unexpected version output"
```

## Implementation Plan

### Dependencies

**Add to `pyproject.toml`:**

```toml
[project.optional-dependencies]
dev = [
    # ... existing dev dependencies ...
    "ascii-guard>=1.5.0",
]
```

**Rationale:**

- Use `dev` optional dependency group (developer tooling)
- Minimum version 1.5.0 (latest stable as of 2026-01-31)
- Already using `uv` for dependency management

### Installation

**For Developers:**

```bash
# Install dev dependencies (includes ascii-guard)
uv sync --all-extras

# Or install ascii-guard separately
uv pip install ascii-guard
```

**For CI/CD:**

Already handled by `uv sync --all-extras` in workflow.

### Rollout Sequence

1. **Add Configuration** (`.ascii-guard.toml`)
2. **Add Dependency** (`pyproject.toml`)
3. **Clean Existing Docs** (run `ascii-guard fix`)
4. **Enable Pre-commit Hook** (`.pre-commit-config.yaml`)
5. **Enable CI/CD Check** (`.github/workflows/ci-cd.yml`)
6. **Update Documentation** (README, CONTRIBUTING, dev guides)
7. **Add Validation Tests** (`tests/validation/test_ascii_art_validation.py`)

### Rollback Plan

If ascii-guard causes issues:

1. **Immediate:** Comment out pre-commit hook (revert `.pre-commit-config.yaml`)
2. **CI/CD:** Comment out docs-quality step (revert `.github/workflows/ci-cd.yml`)
3. **Cleanup:** Remove `.ascii-guard.toml` and dependency from `pyproject.toml`
4. **Communicate:** Document reason in commit message and Linear issue

**No data loss risk** - ascii-guard only lints/fixes text files, all changes are in git.

## Considerations and Trade-offs

### Pros

1. **Automated Quality** - Catch ASCII art issues automatically
2. **Consistency** - Uniform formatting across all documentation
3. **Developer-Friendly** - Auto-fix reduces manual corrections
4. **Minimal Overhead** - Lightweight tool, fast execution
5. **Same Author** - fxstein maintains both ascii-guard and ai-todo

### Cons

1. **New Dependency** - Adds another tool to the stack
2. **Pre-commit Latency** - Slight delay on commits touching markdown
3. **False Positives** - May flag intentionally broken examples (use ignore markers)
4. **Learning Curve** - Developers need to understand ignore marker syntax

### Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Pre-commit failures block work | Medium | Document fix command: `uv run ascii-guard fix` |
| CI/CD failures on valid ASCII | Low | Use ignore markers for intentional examples |
| Performance impact on large docs | Low | 10MB file size limit in config |
| Tool compatibility issues | Medium | Pin version in pyproject.toml |
| Developer confusion | Low | Update CONTRIBUTING.md with guidelines |

### Alternative Approaches Considered

1. **Manual Review**

   - Pros: No new tooling
   - Cons: Error-prone, inconsistent, time-consuming
   - **Rejected:** Does not scale

2. **Custom Linter**

   - Pros: Full control, tailored to ai-todo needs
   - Cons: Maintenance burden, duplicates effort
   - **Rejected:** ascii-guard already solves this problem

3. **Ignore ASCII Art Issues**

   - Pros: No effort required
   - Cons: Documentation quality degrades over time
   - **Rejected:** Undermines project professionalism

## Success Criteria

1. **Pre-commit Integration**

   - ascii-guard runs automatically on markdown commits
   - Developers can run `uv run ascii-guard fix` to resolve issues
   - Zero pre-commit failures on correctly formatted ASCII art

2. **CI/CD Integration**

   - `docs-quality` job includes ascii-guard linting
   - Fails on misaligned ASCII art
   - Passes on clean documentation

3. **Documentation Cleanup**

   - All 17+ files with ASCII art pass ascii-guard linting
   - Visual review confirms diagrams render correctly
   - Git history shows ascii-guard fixes applied

4. **Developer Experience**

   - Documentation clearly explains ascii-guard usage
   - Developers understand how to fix linting errors
   - Ignore markers used for intentional examples

5. **Testing**

   - Validation test passes on all documentation
   - Integration tests verify pre-commit and CI/CD behavior
   - Zero false positives reported

## Next Steps

1. **Human Review** - Get approval on this design document (task #272.2)
2. **Implementation** - Execute rollout sequence (tasks #272.3-#272.4)
3. **Testing** - Create validation tests (task #272.5)
4. **Cleanup** - Fix existing documentation (task #272.6)
5. **Verification** - Final validation and documentation update (task #272.7)

## References

- ascii-guard Repository: <https://github.com/fxstein/ascii-guard>
- ascii-guard PyPI: <https://pypi.org/project/ascii-guard/>
- ascii-guard Usage Guide: <https://github.com/fxstein/ascii-guard/blob/main/docs/USAGE.md>
- ascii-guard API Reference: <https://github.com/fxstein/ascii-guard/blob/main/docs/API_REFERENCE.md>
- Pre-commit Framework: <https://pre-commit.com/>
- ai-todo Pre-commit Config: `.pre-commit-config.yaml`
- ai-todo CI/CD Workflow: `.github/workflows/ci-cd.yml`
