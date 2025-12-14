# CI/CD and Release Process Parity Assessment

**Created:** 2025-12-14
**Status:** Implementation Complete (Phase 1)
**Related:** ascii-guard reference implementation

## Document Purpose

This document assesses the gap between **ascii-guard**'s modern Python development workflow and **todo.ai**'s current setup. ascii-guard uses modern tooling (uv, pre-commit framework, GitHub Actions CI/CD) while todo.ai previously relied on manual scripts and traditional approaches. This assessment identifies gaps and provides a roadmap to achieve process parity.

**Note:** Phase 1 (Foundation) has been implemented. See implementation status in section 9.

## Executive Summary

This document assesses the gap between **ascii-guard**'s modern Python development workflow and **todo.ai**'s current setup. ascii-guard uses modern tooling (uv, pre-commit framework, GitHub Actions CI/CD) while todo.ai previously relied on manual scripts and traditional approaches. This assessment identifies gaps and provides a roadmap to achieve process parity.

**Status:** Phase 1 (Foundation) implementation is complete. The project now has modern CI/CD infrastructure matching ascii-guard's setup.

## 1. ascii-guard Setup Analysis

### 1.1 Dependency Management with `uv`

**Current Implementation:**

- Uses `uv` as the primary package manager
- Has `uv.lock` file for reproducible builds
- One-step setup: `./setup.sh` creates venv, installs deps, configures hooks
- Fast dependency resolution and installation
- Zero-dependency Python 3.11+, minimal deps for 3.10

**Key Features:**

- `uv tool install` for global tool installation
- `uv add --dev` for development dependencies
- Automatic lock file generation
- Fast, reliable dependency resolution

### 1.2 Pre-commit Framework Integration

**Current Implementation:**

- Uses `.pre-commit-config.yaml` for hook configuration
- Integrates with pre-commit framework (not custom scripts)
- Hooks run automatically on commit
- Can run manually: `pre-commit run --all-files`
- Supports local hooks and remote repositories

**Typical Setup:**

```yaml
repos:
 - repo: local
    hooks:
   - id: ruff
        name: ruff
        entry: ruff check
        language: python
        types: [python]
 - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
   - id: trailing-whitespace
   - id: end-of-file-fixer
```

### 1.3 CI/CD with GitHub Actions

**Current Implementation:**

- GitHub Actions workflows in `.github/workflows/`
- Automated testing on push/PR
- Multiple Python versions tested
- Automated releases
- Code coverage reporting
- Type checking (mypy)
- Linting (ruff)

**Typical Workflow Structure:**

- Test matrix across Python versions
- Lint and type check steps
- Test execution with coverage
- Artifact uploads
- Release automation

### 1.4 Testing Infrastructure

**Current Implementation:**

- pytest for test framework
- Comprehensive test coverage
- Test fixtures and helpers
- Integration and unit tests
- Coverage reporting (codecov)

### 1.5 Release Process

**Current Implementation:**

- Automated version bumping
- GitHub Actions for release creation
- PyPI publishing automation
- Release notes generation
- Tag management

## 2. todo.ai Current State

### 2.1 Dependency Management

**Current State:**

- `pyproject.toml` exists with dependencies
- **No `uv.lock` file** - missing lock file for reproducibility
- **No `uv` integration** - uses traditional pip/venv
- Manual dependency installation required
- No one-step setup script

**Gap:** Missing modern dependency management with uv

### 2.2 Pre-commit Setup

**Current State:**

- Custom shell script: `scripts/pre-commit-hook.sh`
- Manual installation via `scripts/setup-git-hooks.sh`
- **Not using pre-commit framework**
- Checks for Python tests but requires manual venv setup
- Checks for markdownlint, yamllint, jq but no automatic installation

**Gap:** Not using pre-commit framework, manual hook management

### 2.3 CI/CD

**Current State:**

- **No GitHub Actions workflows** - `.github/workflows/` directory missing
- No automated testing in CI
- No automated linting/type checking in CI
- No automated releases
- Manual release process via `release/release.sh`

**Gap:** Complete absence of CI/CD automation

### 2.4 Testing Infrastructure

**Current State:**

- pytest configured in `pyproject.toml`
- Test files exist: `tests/unit/`, `tests/integration/`, `tests/e2e/`
- `conftest.py` with fixtures
- **No automated test execution in CI**
- Manual test execution only

**Gap:** Tests exist but not automated in CI

### 2.5 Release Process

**Current State:**

- Manual release script: `release/release.sh`
- Manual PyPI publishing: `release/publish_pypi.sh`
- Requires manual execution
- No automated version bumping
- No automated GitHub release creation

**Gap:** Manual process, not automated

## 3. Gap Analysis

### 3.1 Critical Gaps (Must Fix)

1. **No CI/CD Pipeline**

   - Missing GitHub Actions workflows
   - No automated testing on commits/PRs
   - No automated linting/type checking
   - No automated releases

2. **No uv Integration**

   - Missing `uv.lock` file
   - No `uv` usage for dependency management
   - No one-step setup script
   - Manual dependency management

3. **Pre-commit Framework Not Used**

   - Custom shell script instead of framework
   - Manual hook installation
   - No automatic tool installation
   - Inconsistent developer experience

### 3.2 Important Gaps (Should Fix)

1. **No Development Dependencies in pyproject.toml**

   - Missing dev dependencies (pytest, ruff, mypy, etc.)
   - Tools must be installed manually
   - No standardized development environment

2. **No Automated Release Process**

   - Manual release execution
   - No automated version bumping
   - No automated PyPI publishing
   - No automated GitHub release creation

3. **No Code Quality Automation**

   - No automated ruff/mypy in CI
   - No coverage reporting
   - No automated code quality checks

### 3.3 Nice-to-Have Gaps (Could Fix)

1. **No Test Coverage Reporting**

   - No codecov integration
   - No coverage badges
   - No coverage thresholds

2. **No Multi-Python Version Testing**

   - Only tests current Python version
   - No matrix testing across Python versions

3. **No Automated Documentation**

   - No automated doc generation
   - No automated API docs

## 4. Implementation Roadmap

### Phase 1: Foundation (Critical)

#### 1.1 Add uv Dependency Management

- Install `uv` (if not present)
- Create `uv.lock` file: `uv lock`
- Update `pyproject.toml` with dev dependencies
- Create one-step setup script: `setup.sh`
- Document uv usage in README

**Files to Create/Modify:**

- `pyproject.toml` - Add `[project.optional-dependencies]` for dev deps
- `uv.lock` - Generate via `uv lock`
- `setup.sh` - One-step setup script
- `docs/development/SETUP.md` - Setup documentation

#### 1.2 Migrate to Pre-commit Framework

- Create `.pre-commit-config.yaml`
- Configure hooks: ruff, mypy, trailing-whitespace, end-of-file-fixer
- Remove custom `scripts/pre-commit-hook.sh` (or keep as fallback)
- Update `scripts/setup-git-hooks.sh` to use pre-commit
- Document migration

**Files to Create/Modify:**

- `.pre-commit-config.yaml` - New pre-commit config
- `scripts/setup-git-hooks.sh` - Update to use pre-commit
- `docs/development/CONTRIBUTING.md` - Update setup instructions

#### 1.3 Create GitHub Actions CI/CD

- Create `.github/workflows/ci.yml` for continuous integration
- Create `.github/workflows/release.yml` for automated releases
- Configure test matrix (Python 3.8-3.12)
- Add linting and type checking steps
- Add test execution with coverage

**Files to Create:**

- `.github/workflows/ci.yml` - CI workflow
- `.github/workflows/release.yml` - Release workflow
- `.github/workflows/test.yml` - Test workflow (optional, can be in ci.yml)

### Phase 2: Enhancement (Important)

#### 2.1 Add Development Dependencies

- Add to `pyproject.toml`:
  ```toml
  [project.optional-dependencies]
  dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
  ]
  ```


#### 2.2 Configure Code Quality Tools

- Add `[tool.ruff]` section to `pyproject.toml`
- Add `[tool.mypy]` section to `pyproject.toml`
- Add `[tool.pytest.ini_options]` (already exists, enhance)
- Configure coverage settings

**Files to Modify:**

- `pyproject.toml` - Add tool configurations

#### 2.3 Automated Release Process

- Enhance `release/release.sh` or create GitHub Actions workflow
- Automate version bumping
- Automate PyPI publishing
- Automate GitHub release creation
- Add release notes generation

**Files to Create/Modify:**

- `.github/workflows/release.yml` - Automated release workflow
- `release/release.sh` - Enhance or replace with workflow

### Phase 3: Polish (Nice-to-Have)

#### 3.1 Code Coverage

- Add codecov integration
- Add coverage badges to README
- Set coverage thresholds

#### 3.2 Multi-Python Testing

- Expand test matrix to all supported Python versions
- Test on multiple OS (Ubuntu, macOS, Windows)

#### 3.3 Documentation Automation

- Automated API documentation generation
- Automated example updates

## 5. Detailed Implementation Steps

### Step 1: Setup uv and Lock File

```bash
# Install uv (if not present)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create lock file
uv lock

# Install dependencies
uv sync
```

### Step 2: Create .pre-commit-config.yaml

```yaml
repos:
 - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
   - id: trailing-whitespace
   - id: end-of-file-fixer
   - id: check-yaml
   - id: check-json
   - id: check-added-large-files

 - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
   - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

 - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
   - id: mypy
        additional_dependencies: [types-all]

 - repo: local
    hooks:
   - id: pytest
        name: pytest
        entry: uv run pytest
        language: system
        types: [python]
        pass_filenames: false
        always_run: true
```

### Step 3: Create GitHub Actions Workflows

**`.github/workflows/ci.yml`:**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]

    steps:
   - uses: actions/checkout@v4
   - uses: astral-sh/setup-uv@v3
   - name: Install dependencies
        run: uv sync
   - name: Run tests
        run: uv run pytest
   - name: Run linting
        run: uv run ruff check .
   - name: Run type checking
        run: uv run mypy todo_ai
```

### Step 4: Create setup.sh

```bash
#!/bin/bash
set -e

echo "🚀 Setting up todo.ai development environment..."

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Sync dependencies
echo "📦 Installing dependencies..."
uv sync

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
uv run pre-commit install

echo "✅ Setup complete!"
```

## 6. Success Criteria

### Phase 1 Complete When:

- ✅ `uv.lock` file exists and is committed
- ✅ `.pre-commit-config.yaml` exists and hooks work
- ✅ GitHub Actions CI runs on every push/PR
- ✅ Tests pass in CI
- ✅ Linting and type checking run in CI

### Phase 2 Complete When:

- ✅ Dev dependencies in `pyproject.toml`
- ✅ Code quality tools configured
- ✅ Automated releases work
- ✅ PyPI publishing automated

### Phase 3 Complete When:

- ✅ Code coverage reporting active
- ✅ Multi-Python version testing
- ✅ Documentation automation

## 7. Migration Notes

### Breaking Changes

- Developers must install `uv` (or use provided setup script)
- Pre-commit hooks will run automatically (can be skipped with `--no-verify`)
- CI will block PRs if tests/linting fail

### Backward Compatibility

- Existing manual processes can remain as fallback
- Shell script hooks can be kept for reference
- Manual release process can coexist with automated

### Developer Experience

- One-step setup: `./setup.sh`
- Consistent environment via `uv.lock`
- Automatic quality checks via pre-commit
- Fast feedback via CI

## 8. Estimated Effort

- **Phase 1 (Foundation):** 4-6 hours
                                                                - uv setup: 1 hour
                                                                - Pre-commit migration: 2 hours
                                                                - CI/CD setup: 2-3 hours

- **Phase 2 (Enhancement):** 3-4 hours
                                                                - Dev dependencies: 1 hour
                                                                - Code quality config: 1 hour
                                                                - Release automation: 2 hours

- **Phase 3 (Polish):** 2-3 hours
                                                                - Coverage setup: 1 hour
                                                                - Multi-version testing: 1 hour
                                                                - Documentation: 1 hour

**Total:** 9-13 hours for complete parity

## 9. Implementation Status

### Phase 1: Foundation ✅ COMPLETE

**Completed:** 2025-12-14

All Phase 1 requirements have been implemented:

- ✅ **1.1 Add uv Dependency Management**
  - `uv.lock` file created and committed
  - `pyproject.toml` updated with dev dependencies (including build, twine)
  - `setup.sh` script created with correct PATH handling (`$HOME/.local/bin`)
  - Documentation created in `docs/development/SETUP.md`

- ✅ **1.2 Migrate to Pre-commit Framework**
  - `.pre-commit-config.yaml` created with ruff, mypy, and standard hooks
  - `scripts/setup-git-hooks.sh` updated to use pre-commit framework
  - Hooks configured and tested

- ✅ **1.3 Create GitHub Actions CI/CD**
  - `.github/workflows/ci.yml` created (tests on Python 3.10, 3.11, 3.12)
  - `.github/workflows/release.yml` created (automated PyPI publishing)
  - Both workflows use uv for dependency management

### Phase 2: Enhancement (Partially Complete)

- ✅ **2.1 Add Development Dependencies** - Complete (done in Phase 1)
- ✅ **2.2 Configure Code Quality Tools** - Complete (ruff, mypy configured in Phase 1)
- ⏳ **2.3 Automated Release Process** - Workflow created, needs integration with existing `release/release.sh`

### Phase 3: Polish (Pending)

- ⏳ Code coverage reporting (codecov integration)
- ⏳ Multi-OS testing (macOS, Windows)
- ⏳ Documentation automation

## 10. Next Steps

1. ✅ Phase 1 complete - CI/CD infrastructure in place
2. Integrate automated release workflow with existing `release/release.sh` process
3. Add code coverage reporting (codecov integration)
4. Expand test matrix to include macOS and Windows
5. Consider Phase 3 enhancements as needed

## 11. References

- [uv documentation](https://github.com/astral-sh/uv)
- [pre-commit documentation](https://pre-commit.com/)
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [ascii-guard repository](https://github.com/fxstein/ascii-guard) (reference implementation)
