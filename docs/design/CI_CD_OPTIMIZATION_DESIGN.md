# CI/CD Optimization Design

## Overview

This design reduces redundant full CI/CD runs for metadata-only changes while
preserving strict safety for code changes and release tags. The goal is to keep
release integrity intact while using separate lightweight docs checks and
skipping all tests for log-only changes.

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

Introduce a two-workflow model using change detection:

1. **Full CI** for code changes or tag pushes:
   - Existing `quality`, `test-quick`, `test-comprehensive` jobs.
   - Unchanged release gating on tags.

2. **Docs CI** for docs changes on `main`:
   - A small job that runs:
     - forbidden-flag check
     - markdownlint (docs validation)
   - No `uv sync`, no pre-commit, no pytest matrix.

3. **Logs CI** for log-only changes on `main`:
   - No jobs run (all checks skipped).

### Change Detection

Add a `changes` job using `dorny/paths-filter@v3` to set outputs:

- `code`: any change outside docs/log files.
- `docs_only`: changes limited to `*.md` (no `*.log`).
- `logs_only`: changes limited to `*.log` (no `*.md`).

Recommended filters:

```
docs_only:
  - '**/*.md'
  - '!**/*.log'
logs_only:
  - '**/*.log'
  - '!**/*.md'
code:
  - '!**/*.md'
  - '!**/*.log'
```

Notes:
- The `code` filter is the inverse of docs/log-only changes.
- Tag events bypass filtering and always run full CI.
- Pull requests remain full CI to avoid missing regressions.

## Workflow Behavior

| Event | Change Type | Actions |
| --- | --- | --- |
| push to `main` | docs_only | Run `docs-quality` only |
| push to `main` | logs_only | Skip all checks |
| push to `main` | code | Run `quality`, `test-quick`, `test-comprehensive` |
| tag `v*` | any | Run full chain + release (unchanged) |
| pull_request | any | Run full CI (unchanged) |

## Implementation Details

### New `changes` Job

- Uses `dorny/paths-filter@v3` to detect change type.
- Runs only for `push` events on `main` (not tags).
- Outputs `docs_only`, `logs_only`, and `code` flags to downstream jobs.

### Docs Quality Job

Add a `docs-quality` job for docs-only pushes:

- Steps:
  - Checkout
  - Forbidden flag scan (existing script snippet)
  - Markdown lint (markdownlint-cli2 action)
- No Python/uv installs.

### Logs-Only Behavior

No jobs run for logs-only pushes. This keeps log commits fast and avoids
unnecessary CI usage.

### Existing Jobs (Gated)

Gate current jobs on change type:

- `quality`: run when `code` is true or on tag/PR.
- `test-quick` and `test-comprehensive`: run when `code` is true or on tag.
- `all-tests-pass`, `validate-release`, `release`: unchanged (tag only).

Example condition pattern:

```
if: |
  startsWith(github.ref, 'refs/tags/v') ||
  github.event_name == 'pull_request' ||
  (github.event_name == 'push' && needs.changes.outputs.code == 'true')
```

## Release-Specific Behavior

Release tags still trigger the full chain. The pre-tag version bump commit
continues to require CI success (release.sh gate), but if that commit only
touches `*.md` files it will run `docs-quality`, and if it only touches `*.log`
it will run nothing. This reduces redundant runs without weakening tag-based
coverage.

## Rollout Plan

1. Implement `changes` + `docs-quality` in `ci-cd.yml`.
2. Add log output that prints detected change type.
3. Validate on a docs-only commit (expect docs-quality only).
4. Validate on a small code change (expect full matrix).
5. Monitor the next beta release for reduced CI runs.

## Risks and Mitigations

- **Risk**: Misclassified code change skips full CI.
  - **Mitigation**: Conservative filters, PRs always full CI.
- **Risk**: A non-doc change might be saved in `*.md` or `*.log`.
  - **Mitigation**: Keep PRs on full CI, and reserve `*.log` for metadata only.
- **Risk**: Log-only commits skip all checks.
  - **Mitigation**: Restrict `*.log` to release logs and metadata artifacts.
- **Risk**: Workflow complexity increases.
  - **Mitigation**: Single `changes` job, minimal gating logic, no extra workflows.

## Testing and Validation

- Docs-only push (e.g., update README) should run docs checks only.
- Logs-only push (e.g., update `release/RELEASE_LOG.log`) should run nothing.
- Code change push (e.g., modify `todo_ai/`) should run full matrix.
- Tag release should still run full chain and release.

## Open Questions

None. All open questions from analysis were resolved and incorporated.
