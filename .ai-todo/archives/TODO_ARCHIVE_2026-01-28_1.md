# Archived Tasks - Pruned on 2026-01-28

This file contains tasks pruned from TODO.md on 2026-01-28.
These tasks were archived more than 45 days ago.

**Prune Statistics:**
- Tasks Pruned: 2 root tasks
- Subtasks Pruned: 14 subtasks
- Total: 16 items
- Retention Period: 45 days
- Original TODO.md: /Users/oratzes/cursor/ai-todo/TODO.md

## Pruned Tasks

- [x] **#167** Implement CI/CD process parity with ascii-guard (Phase 1-3) `#cicd` (2025-12-14)
  > Reference: docs/analysis/CI_CD_PROCESS_PARITY_ASSESSMENT.md. Implementation roadmap for achieving process parity with ascii-guard's modern Python development workflow (uv, pre-commit, GitHub Actions CI/CD).
  - [x] **#167.1** Phase 1.1: Add uv dependency management `#cicd` (2025-12-14)
    > Created uv.lock file via 'uv lock'. Updated pyproject.toml with dev dependencies section. Created setup.sh script with PATH handling for $HOME/.local/bin (default uv installation path). Created docs/development/SETUP.md with setup instructions.
  - [x] **#167.2** Phase 1.2: Migrate to pre-commit framework `#cicd` (2025-12-14)
    > Created .pre-commit-config.yaml with ruff, mypy, and standard pre-commit hooks. Updated scripts/setup-git-hooks.sh to use 'uv run pre-commit install' instead of custom shell script hooks.
  - [x] **#167.3** Phase 1.3: Create GitHub Actions CI/CD `#cicd` (2025-12-14)
    > Created .github/workflows/ci.yml with test matrix for Python 3.10-3.12, linting, type checking, and pre-commit checks. Created .github/workflows/release.yml for automated PyPI publishing on version tags.
  - [x] **#167.4** Phase 2.1: Add development dependencies `#cicd` (2025-12-14)
    > Added [project.optional-dependencies] dev section to pyproject.toml with: pytest, pytest-cov, ruff, mypy, pre-commit, build, twine, types-requests, types-pyyaml.
  - [x] **#167.5** Phase 2.2: Configure code quality tools `#cicd` (2025-12-14)
    > Configured [tool.ruff] section with target-version py310, select rules (E, W, F, I, B, C4, UP), and per-file ignores for tests. Configured [tool.mypy] section with python_version 3.10 and strict type checking options.
  - [x] **#167.6** Phase 2.3: Integrate automated release process with release.sh `#cicd` (2025-12-14)
    > Integration complete: release.sh creates GitHub release with shell assets and release notes. GitHub Actions workflow (triggered by tag push) builds Python package, publishes to PyPI, and attaches dist files to existing release. Clean separation of concerns achieved.
    > Release workflow (.github/workflows/release.yml) created but needs integration with existing release/release.sh process. Consider: (1) Have release.sh trigger workflow, (2) Replace release.sh with workflow, or (3) Keep both with different purposes.
  - [x] **#167.7** Phase 3.1: Add code coverage reporting (codecov) `#cicd` (2025-12-14)
  - [x] **#167.8** Phase 3.2: Expand test matrix to multiple OS (macOS, Windows) `#cicd` (2025-12-14)
  - [x] **#167.9** Phase 3.3: Add documentation automation `#cicd` (2025-12-14)

- [x] **#160** Fix issue#35: Task not found after successful modify command `#bug` (2025-12-12)
  > All functions fixed to handle both bold and non-bold task ID formats. Tested: modify and note commands work. Complete command may need additional testing with tags.
  > Issue #35: User ran './todo.ai modify 2.6' which succeeded, then immediately ran './todo.ai note 2.6' but got 'Task #2.6 not found'. The modify command reported success but task became unfindable. Version 2.4.0, macOS. Issue: https://github.com/fxstein/todo.ai/issues/35
  - [x] **#160.1** Investigate modify command: reproduce the bug and identify root cause `#bug` (2025-12-12)
    > BUG IDENTIFIED: modify_todo() finds tasks with pattern matching both bold and non-bold (line 2596), but sed replacement only matches bold format (lines 2669-2682). If task exists without bold (#2.6), modify finds it but sed replacement fails silently, leaving task unchanged. Then add_note() only searches bold format (line 4417), so it can't find the task. Fix: Make sed patterns match both bold and non-bold like grep does.
  - [x] **#160.2** Review modify_task() function for task ID resolution issues `#bug` (2025-12-12)
  - [x] **#160.3** Test modify command with various task IDs and nesting levels `#bug` (2025-12-12)
  - [x] **#160.4** Fix task ID resolution in modify command if bug confirmed `#bug` (2025-12-12)
    > FIXED ALL FUNCTIONS: Updated modify_todo(), add_note(), complete_todo(), archive_task(), show_task(), add_relationship(), update_note(), and delete_note() to handle both bold and non-bold task ID formats. All functions now search for (\*\*#task_id\*\*|#task_id) pattern. Tested: modify and note commands work correctly with non-bold tasks.
    > FIXED: Updated modify_todo() sed patterns to match both bold (\*\*#task_id\*\*) and non-bold (#task_id) formats using extended regex. Also updated add_note() grep pattern to search for both formats. Updated sed_inplace() to support -E flag for extended regex. This ensures modify command can replace tasks regardless of formatting, and note command can find them afterward.
  - [x] **#160.5** Add tests to prevent regression `#bug` (2025-12-12)

---

## Task Metadata

<!-- TASK_METADATA
# Format: task_id:created_at[:updated_at]
160:2026-01-27T23:50:41.503822:2026-01-27T23:50:41.503825
160.1:2026-01-27T23:50:41.503852:2026-01-27T23:50:41.503854
160.2:2026-01-27T23:50:41.503847:2026-01-27T23:51:37.634068
160.3:2026-01-27T23:50:41.503842:2026-01-27T23:51:37.634062
160.4:2026-01-27T23:50:41.503835:2026-01-27T23:50:41.503837
160.5:2026-01-27T23:50:41.503830:2026-01-27T23:51:37.634047
167:2026-01-27T23:50:41.503761:2026-01-27T23:50:41.503762
167.1:2026-01-27T23:50:41.503816:2026-01-27T23:50:41.503818
167.2:2026-01-27T23:50:41.503810:2026-01-27T23:50:41.503812
167.3:2026-01-27T23:50:41.503804:2026-01-27T23:50:41.503805
167.4:2026-01-27T23:50:41.503798:2026-01-27T23:50:41.503799
167.5:2026-01-27T23:50:41.503792:2026-01-27T23:50:41.503793
167.6:2026-01-27T23:50:41.503785:2026-01-27T23:50:41.503787
167.7:2026-01-27T23:50:41.503780:2026-01-27T23:51:37.633982
167.8:2026-01-27T23:50:41.503775:2026-01-27T23:51:37.633976
167.9:2026-01-27T23:50:41.503769:2026-01-27T23:51:37.633970
-->

---
**Prune Date:** 2026-01-28 23:58:13
**Retention Period:** 45 days
**Tasks Pruned:** 2 tasks, 14 subtasks
**Original TODO.md:** /Users/oratzes/cursor/ai-todo/TODO.md
