# CI/CD Optimization Design

## Overview

This design reduces redundant full CI/CD runs for metadata-only changes while
preserving strict safety for code changes and release tags. The goal is to keep
release integrity intact while running a lightweight docs workflow and skipping
all checks for log-only changes.

## Problem Statement

The current `CI/CD` workflow runs the full test matrix on every push to `main`,
including changes limited to release notes, release logs, and other
documentation. During beta releases, several small commits (notes, logs, tag
release) trigger multiple full CI runs, multiplying compute time and delaying
feedback.

## Goals

1. Skip full tests for metadata-only changes.
2. Preserve full test coverage for any code change or tag release.
3. Keep release safety guarantees intact (tag-driven release flow unchanged).
4. Minimize workflow complexity and avoid fragile conditional logic.
5. Provide a lightweight validation path for docs-only changes.
6. Skip all checks for log-only changes.

## Non-Goals

- Remove or weaken release gates for tag pushes.
- Change release.sh behavior or release commit sequencing.
- Modify test contents or coverage thresholds.

## Constraints

- `ci-cd.yml` currently owns both CI and release flows.
- Tag pushes must continue to run full quality + tests before release.
- Pull requests should remain conservative (full coverage by default).

## Proposed Approach

Introduce a single workflow with change detection:

1. **Full CI** for code changes or tag pushes:
   - Existing `quality`, `test-quick`, `test-comprehensive` jobs.
   - Unchanged release gating on tags.

2. **Docs CI** for docs changes on `main`:
   - A small job that runs:
     - forbidden-flag check
     - markdownlint (docs validation)
   - No `uv sync`, no pre-commit, no pytest matrix.

3. **Logs-only pushes**:
   - No jobs run (all checks skipped).

### Workflow Routing

- A `changes` job uses `dorny/paths-filter@v3` to detect:
  - `docs`: any `*.md`
  - `logs_only`: only `*.log`
  - `code`: any non-`*.md` and non-`*.log`
- `docs-quality` runs for docs changes (push/PR).
- `quality`, `test-quick`, `test-comprehensive` run only when code changes are present (push/PR), and always for tags.
- Tag events still run full CI + release.

## Workflow Behavior

| Event | Change Type | Actions |
| --- | --- | --- |
| push to `main` | `*.md` only | Run `docs-quality` only |
| push to `main` | `*.log` only | Skip all checks |
| push to `main` | other files | Run `quality`, `test-quick`, `test-comprehensive` |
| push to `main` | docs + code | Run both `docs-quality` and code checks |
| tag `v*` | any | Run full chain + release (unchanged) |
| pull_request | docs | Run `docs-quality` only |
| pull_request | code | Run `quality` + tests |
| pull_request | docs + code | Run both `docs-quality` and code checks |

## Implementation Details

### `ci-cd.yml` (All Behavior)

- Add a `changes` job using `dorny/paths-filter@v3`.
- Add a `docs-quality` job gated by `docs` output on push/PR.
- Gate `quality` and test jobs by `code` output on push.
- Keep `pull_request` and tag triggers unchanged.

## Release-Specific Behavior

Release tags still trigger the full chain. The pre-tag version bump commit
continues to require CI success (release.sh gate), but if that commit only
touches `*.md` files it will run `docs-quality`, and if it only touches `*.log`
it will run nothing. This reduces redundant runs without weakening tag-based
coverage.

## Rollout Plan

1. Add change detection (`changes` job) to `ci-cd.yml`.
2. Add `docs-quality` job gated by docs changes.
3. Ensure `all-tests-pass` depends on docs + code checks (skips allowed).
4. Validate on a docs-only commit (expect docs-quality only).
5. Validate on a logs-only commit (expect no jobs beyond change detection).
6. Validate on a code change (expect full matrix).
7. Monitor the next beta release for reduced CI runs.

## Risks and Mitigations

- **Risk**: Misclassified code change skips full CI.
  - **Mitigation**: Conservative filters, PRs always full CI.
- **Risk**: A non-doc change might be saved in `*.md` or `*.log`.
  - **Mitigation**: Keep PRs on full CI, and reserve `*.log` for metadata only.
- **Risk**: Log-only commits skip all checks.
  - **Mitigation**: Restrict `*.log` to release logs and metadata artifacts.
- **Risk**: Workflow complexity increases.
  - **Mitigation**: Single `changes` job, minimal gating logic in `ci-cd.yml`.

## Testing and Validation

- Docs-only push (e.g., update README) should run docs checks only.
- Logs-only push (e.g., update `release/RELEASE_LOG.log`) should run no jobs beyond change detection.
- Mixed push (docs + code) should run both docs and code checks.
- Code change push (e.g., modify `todo_ai/`) should run full matrix.
- Tag release should still run full chain and release.

## Open Questions

None. All open questions from analysis were resolved and incorporated.
