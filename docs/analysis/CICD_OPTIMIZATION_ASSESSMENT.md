# CI/CD and Testing Optimization Assessment

## Executive Summary
This document outlines the current state of the `todo.ai` CI/CD pipeline and provides recommendations to improve performance, reduce resource usage, and accelerate developer feedback loops.

The analysis identified three primary bottlenecks:

1. **Redundant Test Execution**: The full test matrix (9 jobs) runs on every PR.
2. **Sequential Job Execution**: Linting and testing run in a single serial flow.
3. **Aggressive Local Hooks**: Local pre-commit hooks run the entire test suite, slowing down the commit process.

## Current State Analysis

### 1. CI Workflow (`.github/workflows/ci.yml`)
* **Heavy Matrix**: Runs on 3 OSs (Ubuntu, MacOS, Windows) × 3 Python versions (3.10, 3.11, 3.12) for *every* event (push/PR).
  * **Total Jobs**: 9 per run.
  * **Missing Versions**: Does not currently test upcoming Python versions (3.13, 3.14).
  * **Cost**: High resource consumption and slower feedback for simple PRs.
* **Serial Execution**: Steps are combined in a single job. Tests wait for linting to complete.
* **Redundancy**: Runs `ruff` and `mypy` manually, then runs `pre-commit` (which likely runs them again).

### 2. Pre-commit Configuration
* **Double Jeopardy / Dead Code**: We have two conflicting systems:
  * `.pre-commit-config.yaml`: The modern standard, used by `setup-git-hooks.sh`.
  * `scripts/pre-commit-hook.sh`: A legacy manual script that duplicates validations and test runs. It appears to be unlinked but causes confusion and potential maintenance debt.
* **Missing Checks**: The legacy script includes `ascii-guard` for validating ASCII charts, which is **missing** from the modern `.pre-commit-config.yaml` setup.
* **Local Performance**: The `.pre-commit-config.yaml` includes a local hook running `uv run pytest` on *all* tests. Committing a simple change triggers the full test suite (unit + integration + e2e), which is a significant developer bottleneck.

### 3. Redundancy & Coverage Analysis
* **Duplicate Execution**:
  * **Ruff**: Runs 3 times (CI lint step, CI pre-commit step, Local pre-commit).
  * **Mypy**: Runs 3 times (CI type-check step, CI pre-commit step, Local pre-commit).
  * **Pytest**: Runs locally on commit (full suite), in CI test step (full suite), and potentially in CI pre-commit step.
* **Missing Checks**:
  * `ascii-guard`: Present in legacy script, missing in modern pre-commit.
  * `todo.ai --lint`: Present in legacy script, missing in modern pre-commit.
  * `Suspicious Filenames`: Present in legacy script, missing in modern pre-commit.
  * **Security & Hygiene**: No current checks for **secrets** (e.g., `detect-secrets`) or **spelling errors** (e.g., `codespell`), which are standard best practices.

---

## Recommendations

### 1. Implement "Smart Matrix" for CI
**Goal**: Reduce PR checks to the minimum viable verification while ensuring forward compatibility.

* **PRs**: Run `ubuntu-latest` with `Python 3.12`.
* **Main Branch**: Expand matrix to include:
  * OS: Ubuntu, MacOS, Windows
  * Python: 3.10, 3.11, 3.12, **3.13**, **3.14-dev**
* **Impact**: drastically reduces load for standard PRs while improving future-proofing on main.

### 2. Parallelize & Split Workflows
**Goal**: Get feedback on linting and unit tests as fast as possible.

* **Split Jobs**: Create separate `quality` and `test` jobs.
  * `quality`: Runs `pre-commit` (linting, formatting, static analysis).
  * `test`: Runs `pytest`.
* **Remove Redundancy**: Delete the explicit `ruff` and `mypy` steps from CI, relying solely on the `pre-commit` run in the `quality` job.

### 3. Optimize Local Pre-commit Hooks
**Goal**: Make `git commit` fast and focused on code quality.

* **Restrict Scope**: Change the local `pytest` hook in `.pre-commit-config.yaml` to run only `tests/unit`.
* **Restore Parity**: Add `ascii-guard` and `todo.ai --lint` to `.pre-commit-config.yaml`.
* **Enhance Security**: Add `codespell` (for typos) and `detect-secrets` (for security) to pre-commit config.
* **Deprecate Legacy Script**: Mark `scripts/pre-commit-hook.sh` for removal or archive it.

### 4. Enable Aggressive Caching
**Goal**: Reduce setup time.

* **Actions**:
  * Enable `actions/cache` for `~/.cache/pre-commit`.
  * Verify `astral-sh/setup-uv` has caching enabled.

## Implementation Plan

1. **Refactor `.github/workflows/ci.yml`**:
   * Split into `quality` and `test` jobs.
   * Remove redundant linting steps.
   * Add conditional logic for the matrix strategy.
   * Add Python 3.13 and 3.14 to the release matrix.
2. **Update `.pre-commit-config.yaml`**:
   * Modify `pytest` entry to target `tests/unit`.
   * Add `ascii-guard` hook.
   * Add `todo.ai --lint` hook.
   * Add `codespell` hook.
   * Add `detect-secrets` hook.
3. **Cleanup**:
   * Remove `scripts/pre-commit-hook.sh`.

## Next Steps
Approved for implementation starting with **CI Workflow Refactoring**.
