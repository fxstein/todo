# Release Numbering Mapping Document

## Overview

This document provides a clear mapping of commit message prefixes/tags to release types and a priority matrix showing how numbering decisions are made.

## Commit Prefix to Release Type Mapping

### Explicit Prefixes → Release Type

| Prefix | Release Type | Example |
|--------|--------------|---------|
| `backend:` | PATCH | `backend: Fix release script error handling` |
| `infra:` | PATCH | `infra: Add release logging` |
| `release:` | PATCH | `release: Add commit link support` |
| `internal:` | PATCH | `internal: Refactor version update function` |
| `feat:` | MINOR* | `feat: Add task filtering command` |
| `feature:` | MINOR* | `feature: Implement uninstall feature` |
| `fix:` | PATCH | `fix: Correct task modification logic` |
| `bugfix:` | PATCH | `bugfix: Fix orphaned subtasks bug` |
| `patch:` | PATCH | `patch: Update version number` |
| `docs:` | PATCH** | `docs: Update README with examples` |
| `refactor:` | PATCH | `refactor: Simplify migration logic` |
| `breaking:`, `!:` | MAJOR | `feat!: Change API behavior` |
| `major:` | MAJOR | `major: Remove deprecated command` |

\* MINOR only if not explicitly marked as backend/infrastructure
\** PATCH for developer docs, may be MINOR for user-facing docs

### Keyword-Based Classification (Fallback)

If no explicit prefix exists, commits are analyzed by keywords:

| Keywords | Release Type | Example |
|----------|--------------|---------|
| `breaking`, `break`, `major`, `!:`, `!` suffix | MAJOR | `Remove deprecated API (breaking change)` |
| `feat:`, `feature:`, `add`, `new`, `implement`, `create`, `support` | MINOR | `Implement nested subtasks support` |
| `fix:`, `bugfix:`, `patch:`, `fix`, `bug`, `patch`, `hotfix`, `correct` | PATCH | `Fix bug in delete task function` |
| All other | PATCH | `Update documentation` |

## Priority Matrix

The release numbering logic uses a **highest-level-first approach** to determine version bumps:

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Scan ALL commits and classify each by release level       │
│ ─────────────────────────────────────────────────────────────  │
│ Process each commit individually:                              │
│ → Classify each commit: MAJOR > MINOR > PATCH                   │
│ → Step down from highest to lowest level per commit             │
│ → Track the HIGHEST level found across all commits              │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Find Highest Level Across All Commits                    │
│ ─────────────────────────────────────────────────────────────  │
│ Logic:                                                           │
│ → A single MAJOR commit makes the entire release MAJOR          │
│ → A single MINOR commit (with no MAJOR) makes release MINOR     │
│ → Otherwise, it's PATCH                                         │
│                                                                  │
│ Priority order (highest to lowest):                             │
│ 1. MAJOR: breaking, break, major, !:, feat!:, fix!:             │
│ 2. MINOR: feat:, feature: (if user-facing)                     │
│ 3. PATCH: backend:, infra:, release:, internal:, fix:, bugfix:  │
│ 4. MINOR: add, new, implement, create, support (if not backend) │
│ 5. PATCH: (default for all other commits)                       │
└─────────────────────────────────────────────────────────────────┘
```

### Classification Logic per Commit

Each commit is classified by checking for MAJOR and MINOR only. Everything else defaults to PATCH:

1. **MAJOR** - Breaking changes (checked first)
   - Keywords: `breaking`, `break`, `major`, `!:`
   - Prefixes with `!` suffix: `feat!:`, `fix!:`, `refactor!:`, `perf!:`

2. **MINOR** - User-facing features (checked second)
   - **Explicit frontend prefixes** (if user-facing):
     - Prefixes: `feat:`, `feature:`
     - Check files changed in this commit:
       - If `todo.ai` changed → MINOR (unless explicitly backend)
       - If `.cursor/rules/` changed → MINOR (unless explicitly backend)
       - Otherwise → MINOR (unless contains backend keywords)
   - **Feature keywords** (if not backend-only):
     - Keywords: `add`, `new`, `implement`, `create`, `support`
     - Check files: If only backend files → PATCH, otherwise → MINOR

3. **PATCH** - Default for all other commits
   - **All commits default to PATCH** unless they match MAJOR or MINOR criteria above
   - This includes (examples for clarity, but code doesn't explicitly check for these):
     - Explicit backend prefixes: `backend:`, `infra:`, `release:`, `internal:`
     - Fix prefixes: `fix:`, `bugfix:`, `patch:`
     - Commits with words like "fix", "bug", "correct" in the message body
     - Commits without any recognizable pattern

## Decision Flow Examples

### Example 1: Cursor Rules Migration (Feature)

**Commit:** `feat: Migrate cursor rules to .cursor/rules/ structure`

**Files Changed:** `.cursor/rules/`, `todo.ai`

**Classification:**
- Step down from highest: Not MAJOR (no breaking change)
- Step down: Not explicit backend prefix (`backend:`, `infra:`, etc.)
- Step down: Has `feat:` prefix → Check files changed in this commit
  - `.cursor/rules/` changed: YES
  - Backend keywords in commit: NO
  - **Commit Level: MINOR** ✅

**Release Level:** **MINOR** (highest level found)

### Example 2: Backend Infrastructure Fix

**Commit:** `backend: Fix release script version update logic`

**Files Changed:** `release/release.sh`

**Classification:**
- Step down from highest: Not MAJOR (no breaking change)
- Step down: Has explicit `backend:` prefix
  - **Commit Level: PATCH** ✅

**Release Level:** **PATCH** (highest level found)

### Example 3: User-Facing Feature

**Commit:** `feat: Add uninstall feature`

**Files Changed:** `todo.ai`, `README.md`

**Classification:**
- Step down from highest: Not MAJOR (no breaking change)
- Step down: Not explicit backend prefix
- Step down: Has `feat:` prefix → Check files changed in this commit
  - `todo.ai` changed: YES
  - Backend keywords in commit: NO
  - **Commit Level: MINOR** ✅

**Release Level:** **MINOR** (highest level found)

### Example 4: Bug Fix Without Prefix

**Commit:** `Fix orphaned subtasks when deleting parent task`

**Files Changed:** `todo.ai`

**Classification:**
- Step down from highest: Not MAJOR (no breaking change)
- Step down: Not explicit backend prefix (`backend:`, `infra:`, etc.)
- Step down: Not explicit `feat:` prefix
- Step down: Not explicit `fix:` prefix (no colon after "fix")
- Step down: Not feature keywords (`add`, `new`, `implement`, `create`, `support`)
- Default: **Commit Level: PATCH** ✅ (default classification)

**Note:** The script doesn't explicitly check for "fix" as a keyword in the commit message body. Commits without matching prefixes or keywords default to PATCH, which correctly classifies bug fixes without explicit `fix:` prefixes.

**Release Level:** **PATCH** (highest level found)

### Example 5: Backend-Only Without Prefix

**Commit:** `Add release logging functionality`

**Files Changed:** `release/release.sh`, `release/RELEASE_LOG.log`

**Classification:**
- Step down from highest: Not MAJOR (no breaking change)
- Step down: Not explicit backend prefix
- Step down: Not explicit `feat:` prefix
- Step down: Not explicit `fix:` prefix
- Step down: Contains keyword "add" → Check files
  - Only backend files changed: `release/release.sh`, `release/RELEASE_LOG.log`
  - Frontend files: NONE
  - **Commit Level: PATCH** ✅

**Release Level:** **PATCH** (highest level found)

### Example 6: Breaking Change

**Commit:** `feat!: Remove deprecated command`

**Files Changed:** `todo.ai`, `README.md`

**Classification:**
- Step down from highest: Has `!` suffix (breaking change indicator)
  - **Commit Level: MAJOR** ✅

**Release Level:** **MAJOR** (highest level found - stops scanning other commits)

## File Classification

### Backend Files (Infrastructure)

These files are considered backend-only and don't affect end users:

- `release/release.sh` - Release automation script
- `.cursor/rules/` - Agent configuration (context-dependent)
- `.todo.ai/` - Internal state/logs
- `tests/` - Test infrastructure
- `release/RELEASE_SUMMARY.md` - Release process files
- `release/RELEASE_LOG.log` - Release process files
- `release/RELEASE_PROCESS.md` - Developer documentation
- `docs/TEST_PLAN.md` - Developer documentation
- `release/RELEASE_NUMBERING_ANALYSIS.md` - Developer documentation

### Frontend Files (User-Facing)

These files directly affect end users or AI agents:

- `todo.ai` - Main CLI tool (if functional changes)
- `README.md` - User documentation
- `docs/*.md` - User-facing documentation (excluding developer docs)
- `.cursor/rules/` - **Special case**: User-facing if `feat:` prefix exists (shipped with tool)

### Ambiguous Files

Some files require context to classify:

- `.cursor/rules/`:
  - **User-facing** if `feat:` prefix and ships with tool (end-user rules)
  - **Backend** if `backend:` prefix or developer-specific rules
  - **Backend** if no prefix but only infrastructure changes

- `todo.ai`:
  - **Frontend** if functional changes (new commands, behavior changes)
  - **Backend** if only internal refactoring (no behavior change)
  - **Backend** if only version bumps or bug fixes

- `docs/*.md`:
  - **Frontend** if user-facing documentation
  - **Backend** if developer documentation (`RELEASE_PROCESS.md`, `TEST_PLAN.md`)

### Example 7: Mixed Release (Multiple Commits)

**Commits:**
- `feat: Add new command`
- `backend: Fix release script bug`
- `fix: Correct task deletion logic`

**Classification per commit:**
1. `feat: Add new command` → **MINOR** (feat: prefix, user-facing)
2. `backend: Fix release script bug` → **PATCH** (backend: prefix)
3. `fix: Correct task deletion logic` → **PATCH** (fix: prefix)

**Release Level:** **MINOR** (highest level found across all commits)

**Note:** A single MINOR commit makes the entire release MINOR, even if there are multiple PATCH commits.

### Example 8: Mixed Release with Breaking Change

**Commits:**
- `feat: Add new feature`
- `feat!: Remove deprecated API`
- `fix: Correct bug`

**Classification per commit:**
1. `feat: Add new feature` → **MINOR** (feat: prefix, user-facing)
2. `feat!: Remove deprecated API` → **MAJOR** (breaking change - `!` suffix)
3. `fix: Correct bug` → **PATCH** (fix: prefix)

**Release Level:** **MAJOR** (highest level found - stops at first MAJOR commit)

**Note:** A single MAJOR commit makes the entire release MAJOR, overriding all other commits.

## Special Cases

### `.cursor/rules/` Migration

**Problem:** `.cursor/rules/` changes were incorrectly classified as PATCH even with `feat:` prefix.

**Solution:** When scanning commits, each commit with `feat:` prefix is checked individually. If `feat:` exists and `.cursor/rules/` changed in that commit, it's classified as MINOR (user-facing feature).

**Before Fix:**
- `feat: Migrate cursor rules` + `.cursor/rules/` only
- → File analysis detected backend-only files
- → **Result: PATCH** ❌

**After Fix:**
- `feat: Migrate cursor rules` + `.cursor/rules/` only
- → Scan commit: Has `feat:` prefix
- → Check files changed in this commit: `.cursor/rules/` changed
- → No backend keywords → **Commit Level: MINOR** ✅
- → **Release Level: MINOR** ✅ (highest level found)

### Mixed Commits

When a release contains both backend and frontend changes, the script scans all commits individually and selects the highest level found:

1. **Scan all commits** and classify each individually by stepping down the levels
2. **Select highest level** found across all commits:
   - A single MAJOR commit → entire release is MAJOR
   - A single MINOR commit (with no MAJOR) → entire release is MINOR
   - All PATCH commits → entire release is PATCH

**Example:** If a release has commits `feat: Add feature`, `backend: Fix bug`, `fix: Correct logic`:
- Commit 1: `feat: Add feature` → **MINOR** (feat: prefix, user-facing)
- Commit 2: `backend: Fix bug` → **PATCH** (backend: prefix)
- Commit 3: `fix: Correct logic` → **PATCH** (fix: prefix)
- **Release Level: MINOR** (highest level found)

**Result:** Frontend changes take precedence (MINOR), unless explicitly marked as backend, or unless a MAJOR commit is found.

## Quick Reference

**Use PATCH for:**
- Bug fixes
- Infrastructure improvements
- Backend-only changes
- Internal refactoring
- Documentation updates (developer docs)

**Use MINOR for:**
- New user-facing features (`feat:` prefix)
- User-facing `.cursor/rules/` changes (`feat:` prefix)
- Functional changes to `todo.ai` (`feat:` prefix)
- User-facing documentation updates

**Use MAJOR for:**
- Breaking changes (`!:` suffix or `breaking:` prefix)
- API changes that break backward compatibility

**Explicit Prefixes Override:**
- `backend:` → Always PATCH (even if `feat:`)
- `feat:` → MINOR (unless explicitly `backend:`)
- `breaking:`, `!:` → Always MAJOR

## Implementation Details

The priority system ensures:
1. **Explicit prefixes take precedence** over file analysis
2. **User-facing features are recognized** even when touching backend files
3. **Backend work is correctly classified** as PATCH
4. **Keyword analysis provides fallback** for commits without prefixes

This hybrid approach balances:
- Developer control (explicit prefixes)
- Automatic detection (file analysis)
- Semantic versioning compliance
