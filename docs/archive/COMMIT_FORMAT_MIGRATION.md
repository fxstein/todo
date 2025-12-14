# Commit Format Migration Plan

## Overview

This document tracks commits that use the old task number format (`#nn`) instead of the new format (`task#nn`) to avoid GitHub auto-linking.

## Strategy

**No destructive Git operations** - We will not rewrite history, rebase, or reset.

**Approach:**
- Document all commits with old format
- For the most recent commit with old format, touch the affected files and recommit with correct format
- Historical commits remain unchanged (preserves Git history)

## Commits with Old Format (#nn instead of task#nn)

### Recent Commits (Can be fixed)

1. **70f70f1** - `Archive completed task #15 (git hooks), delete task #21`
   - Should be: `Archive completed task#15 (git hooks), delete task#21`
   - Files: TODO.md, .todo.ai/.todo.ai.log, .todo.ai/.todo.ai.serial

2. **1dc223c** - `feat: Add automated linter setup script (task #15.8, #15.9)`
   - Should be: `feat: Add automated linter setup script (task#15.8, task#15.9)`
   - Files: TODO.md, developer/setup-linters.sh, .todo.ai/.todo.ai.log, .todo.ai/.todo.ai.serial

3. **b2f4c34** - `Add subtask #15.8: investigate linter installation options`
   - Should be: `Add subtask#15.8: investigate linter installation options`
   - Files: TODO.md, .todo.ai/.todo.ai.log, .todo.ai/.todo.ai.serial

4. **bd4abb3** - `Archive completed task #15 (git hooks implementation)`
   - Should be: `Archive completed task#15 (git hooks implementation)`
   - Files: TODO.md, .todo.ai/.todo.ai.log, .todo.ai/.todo.ai.serial

5. **9c9ece0** - `feat: Implement git hooks with pre-commit validation (task #15)`
   - Should be: `feat: Implement git hooks with pre-commit validation (task#15)`
   - Files: Multiple files for git hooks implementation

6. **c4ef8ad** - `Update task #15 with detailed implementation requirements from design document`
   - Should be: `Update task#15 with detailed implementation requirements from design document`
   - Files: TODO.md, .todo.ai/.todo.ai.log, .todo.ai/.todo.ai.serial

7. **34f9acd** - `docs: Create git hooks design document for task #15`
   - Should be: `docs: Create git hooks design document for task#15`
   - Files: docs/GIT_HOOKS_DESIGN.md, TODO.md, .todo.ai/.todo.ai.log, .todo.ai/.todo.ai.serial

8. **78a14a3** - `Archive completed tasks: #19, #37, #43, #44; Delete tasks #33, #34`
   - Should be: `Archive completed tasks: task#19, task#37, task#43, task#44; Delete tasks task#33, task#34`
   - Files: TODO.md, .todo.ai/.todo.ai.log, .todo.ai/.todo.ai.serial

9. **6fe2c08** - `feat: Fix update logic error - execute new version's code before replacement (#48)`
   - Should be: `feat: Fix update logic error - execute new version's code before replacement (task#48)`
   - Files: todo.ai, release/RELEASE_SUMMARY.md

10. **3287327** - `feat: Add task #48 to fix update logic error`
    - Should be: `feat: Add task#48 to fix update logic error`
    - Files: TODO.md, .todo.ai/.todo.ai.log, .todo.ai/.todo.ai.serial

11. **db3022e** - `feat: Implement cleanup of .cursorrules during migration (#44.10)`
    - Should be: `feat: Implement cleanup of .cursorrules during migration (task#44.10)`
    - Files: todo.ai, TODO.md

12. **b81315e** - `feat: Add subtask #44.10 to cleanup .cursorrules during migration`
    - Should be: `feat: Add subtask#44.10 to cleanup .cursorrules during migration`
    - Files: TODO.md, .todo.ai/.todo.ai.log, .todo.ai/.todo.ai.serial

13. **789de6a** - `feat: Add task #47 for feature request capability`
    - Should be: `feat: Add task#47 for feature request capability`
    - Files: TODO.md, .todo.ai/.todo.ai.log, .todo.ai/.todo.ai.serial

14. **f923eec** - `bug: Add task #46 to fix release numbering bug`
    - Should be: `bug: Add task#46 to fix release numbering bug`
    - Files: TODO.md, .todo.ai/.todo.ai.log, .todo.ai/.todo.ai.serial

15. **c13f4c4** - `feat: Complete task #44 - Cursor rules migration to .cursor/rules/`
    - Should be: `feat: Complete task#44 - Cursor rules migration to .cursor/rules/`
    - Files: TODO.md, .todo.ai/.todo.ai.log, .todo.ai/.todo.ai.serial

16. **b1f2cb0** - `feat: Add task #45 for pre-release support in release process`
    - Should be: `feat: Add task#45 for pre-release support in release process`
    - Files: TODO.md, .todo.ai/.todo.ai.log, .todo.ai/.todo.ai.serial

### Historical Commits (Documented only)

1. **1942e44** - `Merge pull request #1 from fxstein/cursor/check-current-status-61ac` (This is a PR number, not a task number - OK)

2. **f91afe4** - `Complete task #32: Implement nested subtasks support (2-level limit)`
   - Should be: `Complete task#32: Implement nested subtasks support (2-level limit)`

3. **b0b6e39** - `Add task #32: Plan for nested subtasks support (2-level limit)`
   - Should be: `Add task#32: Plan for nested subtasks support (2-level limit)`

4. **246264d** - `Complete task #30: Implement versioned backups and rollback capability`
   - Should be: `Complete task#30: Implement versioned backups and rollback capability`

## Implementation Plan

### Step 1: Fix Most Recent Commit (70f70f1)

The most recent commit with wrong format is **70f70f1**:
- Old message: `Archive completed task #15 (git hooks), delete task #21`
- New message: `Archive completed task#15 (git hooks), delete task#21`
- Files touched: TODO.md, .todo.ai/.todo.ai.log, .todo.ai/.todo.ai.serial

**Action:**
1. Touch the affected files (TODO.md has likely changed since then)
2. Commit with corrected message format
3. This creates a new commit with correct format

### Step 2: Document Historical Commits

All other commits remain as-is (preserves Git history). They are documented here for reference.

## Rationale

- **No history rewrite**: Keeps Git history intact and safe
- **Forward-looking fix**: New commits use correct format
- **Documentation**: Historical commits documented for reference
- **Minimal impact**: Only fix the most recent problematic commit

## Status

- ✅ Commits with old format identified
- ✅ Migration plan documented
- 🔄 Ready to implement Step 1 (fix most recent commit)
