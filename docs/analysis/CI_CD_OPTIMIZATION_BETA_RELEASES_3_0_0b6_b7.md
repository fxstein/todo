This document analyzes CI/CD redundancy for beta releases v3.0.0b6 and v3.0.0b7.
It compares commit activity and GitHub Actions runs to identify repeated full
test executions and suggests optimization directions.

Scope
- Focus releases: v3.0.0b6 and v3.0.0b7
- Signals reviewed: release/RELEASE_LOG.log and GitHub Actions runs (CI/CD)

Sources
- release/RELEASE_LOG.log entries for b6 and b7
- GitHub Actions runs (CI/CD workflow) around the release timestamps

Release timeline snapshots

Release 3.0.0b6 (2026-01-23)
- Prepare: 20:47:01
- Version commit: 20:49:26 (after hooks)
- Tag created: 20:49:28
- CI pass for version commit: 20:51:42
- Tag push: 20:51:43
- Release workflow success: 20:55:44
- Release complete: 20:55:45

Related CI/CD workflow runs (all CI/CD):
- release notes preview commit (release: Update release notes preview) -> run
- version bump commit (chore: Bump version to 3.0.0b6) -> run
- release workflow run (📦 Release v3.0.0b6) -> run
- release log commit (Add release log for 3.0.0b6) -> run

Release 3.0.0b7 (2026-01-23)
- Prepare: 21:41:35
- Version commit: 21:54:24 (after hooks)
- Tag created: 21:54:27
- CI pass for version commit: 21:56:40
- Tag push: 21:56:41
- Release workflow success: 22:01:05
- Release complete: 22:01:06

Related CI/CD workflow runs (all CI/CD):
- release notes preview commit (release: Update release notes preview) -> run
- version bump commit (chore: Bump version to 3.0.0b7) -> run
- release workflow run (📦 Release v3.0.0b7) -> run
- release log commit (Add release log for 3.0.0b7) -> run

Observations
1) Full CI/CD runs are triggered for each release step commit.
   - prepare notes preview
   - version bump commit (pre-tag)
   - release workflow (tag)
   - release log commit

2) The release workflow already runs the full suite after tag.
   - The version commit CI pass is required before tag push (release.sh gate).
   - The tag push triggers a full CI/CD run again.

3) Release log commits are pure metadata changes.
   - They still trigger the full CI/CD workflow.

4) Release notes preview commits are text-only changes.
   - They still trigger the full CI/CD workflow.

5) Net effect: a single release executes the full suite 4 times.
   - One for release notes preview commit
   - One for version bump commit (pre-tag)
   - One for tag-triggered release workflow
   - One for release log commit

Root causes (based on current workflow behavior)
- Single CI/CD workflow runs on all pushes without path filters.
- Release flow uses multiple commits to persist artifacts.
- Release workflow is triggered by tag and also by pushes.

Optimization directions (design candidates)

1) Add path filters to skip heavy suites for release metadata commits.
   - Ignore changes limited to release/RELEASE_LOG.log
   - Ignore changes limited to release/RELEASE_NOTES.md
   - Ignore changes limited to release/AI_RELEASE_SUMMARY.md
   - For these changes, run a lightweight job (lint only) or skip CI entirely.

2) Split workflows: lightweight vs full.
   - A small workflow for docs/log-only changes.
   - Full matrix only when code changes occur.

3) Limit release note preview checks.
   - If the only changes are release notes and summary, skip full tests.
   - Keep a formatting/markdown validation job only.

4) Reduce redundant runs in release execution.
   - The release workflow (tag) already builds/tests.
   - Consider relaxing the pre-tag CI gate to a smaller subset
     for version bump commits that only touch version files.

5) Consolidate release commits when possible.
   - Fewer commits -> fewer push-triggered CI runs.
   - Example: combine release notes preview and summary in one commit.

Open questions (answered)
- Is CI/CD workflow already configured with path filters or job-level filters?
  - No. The CI/CD workflow has no path filters on push or pull_request, and
    jobs only check event type (push vs pull_request) or tag refs.
- Is it acceptable to skip full tests for release-log-only commits?
  - Yes.
- Are there compliance requirements that force CI on every push?
  - None.

Next steps (task #183.2+)
- Map workflow triggers and job definitions in .github/workflows.
- Propose path filters and job-level "if" conditions.
- Decide which steps must always run for release commits.
