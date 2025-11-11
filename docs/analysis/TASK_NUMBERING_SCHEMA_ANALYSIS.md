# Task Numbering Schema Analysis

## Overview

This document investigates the potential conflict between todo.ai task numbers (e.g., `#15`, `#50`) and GitHub issue/PR numbers when task numbers are mentioned in commit messages. GitHub automatically links any `#number` pattern in commit messages to issues and pull requests, which can cause confusion or incorrect linking.

## Problem Statement

When developers mention task numbers in commit messages (e.g., "Fix bug in task #15"), GitHub may automatically create links to GitHub issues or pull requests with those numbers, even if they don't exist or are in a different repository.

**Example conflicts:**
- Commit message: `"feat: Implement task #15 (git hooks)"`
- GitHub interprets `#15` as a reference to issue/PR #15
- If issue #15 exists, it gets incorrectly linked
- If issue #15 doesn't exist, it may create confusion

**Current usage in todo.ai:**
- Task numbers are frequently mentioned in commit messages
- Examples: `"feat: Implement git hooks (task #15)"`, `"Archive completed task #15"`
- These numbers could conflict with GitHub issue/PR numbers

## GitHub Auto-Linking Behavior

GitHub automatically links references to issues and pull requests in:
- Commit messages
- Pull request descriptions
- Issue comments
- Release notes

**Link patterns:**
- `#number` - References issues/PRs in the same repository
- `owner/repo#number` - References issues/PRs in a specific repository
- `owner/repo@commit` - References commits in a specific repository

**Scope of linking:**
- Links are created automatically without requiring the issue/PR to exist
- Links to non-existent issues show as plain text (not clickable)
- Links to existing issues/PRs become clickable

## Potential Issues

### 1. Incorrect Linking
- Task numbers like `#15` might link to issue #15 if it exists
- This creates false connections between commits and issues
- Makes it harder to track actual issue/PR relationships

### 2. Confusion
- Users might think `#15` refers to an issue when it's actually a task number
- Makes commit history harder to understand
- Reduces clarity of what issues/PRs are actually referenced

### 3. Maintenance Issues
- Harder to identify actual issue/PR references vs task numbers
- Automated tools might misinterpret task numbers as issue references
- Makes it difficult to generate accurate issue/PR statistics

### 4. Repository Context
- In this repository, task numbers are used frequently in commit messages
- If GitHub issues are created, task numbers might conflict with issue numbers
- Example: Task #15 vs Issue #15 (if created later)

## Current Commit Message Patterns

**Analysis of recent commits in todo.ai:**

Looking at commit history, task numbers are frequently mentioned:
- `"feat: Implement git hooks with pre-commit validation (task #15)"`
- `"Archive completed task #15 (git hooks), delete task #21"`
- `"feat: Add automated linter setup script (task #15.8, #15.9)"`

**Impact:**
- These commit messages contain `#15`, `#21`, `#15.8`, `#15.9`
- If corresponding GitHub issues exist, they get auto-linked
- If no issues exist, the numbers appear as plain text but could be confusing

## Alternative Numbering Schemas

### Option 1: Prefix Task Numbers

**Format:** `task#15`, `task#50`, `t#15`, `T#15`

**Pros:**
- Clearly distinguishes task numbers from issue/PR numbers
- Prevents GitHub auto-linking
- Simple and readable
- Minimal changes to existing workflow

**Cons:**
- Requires updating commit message format
- Slightly longer format

**Example:**
```
feat: Implement git hooks with pre-commit validation (task#15)
Archive completed task#15 (git hooks), delete task#21
```

### Option 2: Bracket Notation

**Format:** `[15]`, `[50]`, `task[15]`

**Pros:**
- No conflict with GitHub auto-linking (doesn't match `#number` pattern)
- Clean and readable
- No ambiguity

**Cons:**
- Different from standard GitHub issue format
- Requires updating commit message format

**Example:**
```
feat: Implement git hooks with pre-commit validation (task [15])
Archive completed task [15] (git hooks), delete task [21]
```

### Option 3: Alternate Format

**Format:** `task-15`, `task-50`, `t15`, `T15`

**Pros:**
- No `#` symbol, so no auto-linking
- Clear that it's a task number
- Easy to parse programmatically

**Cons:**
- Different from current format
- Requires updating commit message format

**Example:**
```
feat: Implement git hooks with pre-commit validation (task-15)
Archive completed task-15 (git hooks), delete task-21
```

### Option 4: Escaped Format

**Format:** `##15` (double hash to escape), `\#15` (backslash escape)

**Pros:**
- Keeps single hash visible
- GitHub doesn't auto-link escaped formats
- Minimal visual change

**Cons:**
- Not intuitive
- Escape characters might be removed by some tools
- Requires escaping in commit messages

**Example:**
```
feat: Implement git hooks with pre-commit validation (task ##15)
Archive completed task ##15 (git hooks), delete task ##21
```

### Option 5: Custom Prefix Repository

**Format:** `todo.ai#15`, `TODO#15`, `todo#15`

**Pros:**
- Explicitly identifies the repository/context
- Prevents linking to GitHub issues (unless owner/repo is specified)
- Clear and unambiguous

**Cons:**
- Longer format
- Requires updating commit message format

**Example:**
```
feat: Implement git hooks with pre-commit validation (todo.ai#15)
Archive completed todo.ai#15 (git hooks), delete todo.ai#21
```

### Option 6: Separate Namespace

**Format:** Use different number ranges for tasks vs issues

**Approach:**
- Reserve certain number ranges for tasks (e.g., 1-1000 for tasks)
- Use different ranges for GitHub issues (e.g., 1001+ for issues)
- Or use different prefixes entirely

**Pros:**
- No conflicts if ranges don't overlap
- Allows keeping `#number` format for tasks

**Cons:**
- Requires coordination and documentation
- Doesn't prevent confusion, only avoids conflicts
- Limits flexibility

## Recommended Solution

**✅ SELECTED: Option 1 - Prefix Task Numbers** with `task#` format

**Rationale:**
1. **Clear and explicit**: `task#15` clearly indicates it's a task number, not an issue
2. **Prevents auto-linking**: GitHub won't auto-link `task#15` as it doesn't match the `#number` pattern
3. **Minimal change**: Only requires adding `task` prefix to commit messages
4. **Backward compatible**: Existing commit history can be left as-is
5. **Readable**: Still easy to read and understand

**Implementation Status:**
- ✅ Option 1 selected and documented
- 🔄 Update Cursor rules to enforce `task#` format in commit messages
- 🔄 Check existing commits for wrong format and create migration plan
- ⏳ Document format in commit message prefix guidelines
- ⏳ Optionally: Create a git hook to warn about `#number` patterns that might be task numbers

**Format Examples:**
- ✅ Correct: `feat: Implement git hooks with pre-commit validation (task#15)`
- ✅ Correct: `Archive completed task#15 (git hooks), delete task#21`
- ✅ Correct: `feat: Add automated linter setup script (task#15.8, task#15.9)`
- ❌ Incorrect: `feat: Implement git hooks (task #15)` - space breaks pattern
- ❌ Incorrect: `feat: Implement git hooks (#15)` - will auto-link to issue #15

## Alternative: Commit Message Format Guidelines

If we keep `#15` format but add context:

**Format:** `Fix bug (todo.ai task #15)` or `Task #15: Fix bug`

**Pros:**
- Adds context to prevent confusion
- Still uses `#number` format

**Cons:**
- GitHub will still try to auto-link `#15`
- Less clear distinction

## Testing and Validation

### Test Cases

1. **Commit with task number:**
   - Create commit with `task#15` in message
   - Verify GitHub doesn't auto-link it
   - Verify commit message is readable

2. **Commit with issue number:**
   - Create commit with `#123` (actual issue number)
   - Verify GitHub auto-links it correctly
   - Verify it doesn't conflict with task numbers

3. **Commit with both:**
   - Create commit mentioning both `task#15` and `#123`
   - Verify only `#123` gets auto-linked
   - Verify task number doesn't create confusion

### Validation Criteria

- Task numbers in commit messages don't trigger GitHub auto-linking
- Issue/PR numbers still work correctly
- Commit messages remain readable and clear
- No confusion between task numbers and issue/PR numbers

## Migration Strategy

**Phase 1: Documentation** ✅
- ✅ Update analysis document with selected option
- ✅ Update Cursor rules to enforce `task#nn` format
- ✅ Document format in commit message prefix guidelines

**Phase 2: Check Existing Commits** 🔄
- Scan commit history for commits using `#nn` format for task numbers
- Create migration plan:
  - Option A: Leave existing commits as-is (recommended - no history rewrite)
  - Option B: Create new commits with corrected format (if needed for documentation)
  - Document which commits use old format

**Phase 3: Gradual Adoption** ⏳
- Use new `task#nn` format for all new commits
- Update templates and examples
- Monitor for any conflicts or confusion

**Phase 4: Validation** ⏳
- Add git hook warning for `#number` patterns (optional)
- Monitor for any conflicts or confusion
- Gather feedback from developers

## Implementation Status

✅ **Option 1 selected** - `task#nn` format  
✅ **Cursor rules updated** - `todo.ai-commit-format.mdc` rule created  
✅ **Developer rules updated** - `commit-prefixes.mdc` includes task number format  
🔄 **Checking existing commits** - Subtask #50.4 to identify and document old format commits

## Decisions Made

1. **✅ Format selected**: `task#nn` (e.g., `task#15`, `task#50`)
2. **✅ No history rewrite**: Existing commits left as-is to preserve Git history
3. **✅ Cursor rules enforced**: New commits must use `task#nn` format
4. **🔄 Migration plan**: Check existing commits and document which ones use old format

## Open Questions

1. **Should we use git hooks to warn about `#number` patterns?**
   - Could warn developers when using `#number` in commits
   - Suggest using `task#number` instead
   - Status: Optional enhancement for future

2. **What about issue references in commit messages?**
   - Real GitHub issues should still use `#nn` format (will auto-link correctly)
   - Task numbers use `task#nn` format (will not auto-link)
   - Status: Clear distinction established

## References

- [GitHub Documentation: Referencing issues and pull requests](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls)
- [GitHub Auto-linking Documentation](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls#issues-and-pull-requests)
- Current commit message format in `release/RELEASE_PROCESS.md`
- Current Cursor rules in `.cursor/rules/commit-prefixes.mdc`

