# Branch Naming Issue Analysis (AIT-15)

**Date:** 2026-01-31
**Task:** #271 ([AIT-15] Incorrect branch names for linear issue)
**Status:** Investigation Complete

---

## Executive Summary

Branches are being created inconsistently with incorrect user prefixes. Some branches use "oliver" (Linear's displayName) instead of "fxstein" (the correct GitHub username from git config). This occurs despite the current rule explicitly stating to NOT use Linear's suggested branch name.

---

## Evidence

### Git Configuration (Correct)
```bash
$ git config user.name
fxstein

$ git config user.email
773967+fxstein@users.noreply.github.com

$ git remote -v
origin  https://github.com/fxstein/ai-todo.git
```

### Linear User Data (Source of Confusion)
```json
{
  "name": "Oliver Ratzesberger",
  "displayName": "oliver",
  "gitBranchName": "oliver/ait-15-incorrect-branch-names-for-linear-issue"
}
```

### Branch History (Inconsistent)

**Incorrect branches (using "oliver" from Linear):**
- ❌ `oliver/ait-12-refactor-release-workflow-to-cursor-skill` (2026-01-31)
- ❌ `oliver/ait-2-implement-prune-function-to-remove-archived-tasks`
- ❌ `oliver/ait-8-release-please`

**Correct branches (using "fxstein" from git config):**
- ✅ `fxstein/AIT-15-incorrect-branch-names-for-linear-issue` (2026-01-31)
- ✅ `fxstein/ait-3-implement-empty-trash-on-startup-deleted-tasks`

---

## Root Cause Analysis

### Timeline of Rule Changes

1. **2026-01-29**: Rule fixed with commit `2cf15f6`
   - "refactor: Always construct branch names, never use Linear's gitBranchName"
   - Explicitly added: "Never use Linear's `gitBranchName` - always build it ourselves"

2. **2026-01-31**: Despite the fix, `oliver/ait-12` branch still created with wrong prefix

### Why the Issue Persists

The current rule (`.cursor/rules/linear-ai-todo-integration.mdc` lines 47-51, 125-128) states:

```markdown
**Always construct branch name:**
1. Get git user: `git config user.name` (lowercase)
2. Extract IDENTIFIER from Linear issue (e.g., `AIT-12`)
3. Create slug from issue title (e.g., `fix-login`)
4. Run: `git checkout -b <userid>/<IDENTIFIER>-<slug>`

- Never use Linear's `gitBranchName` - always build it ourselves.
- Get userid from: `git config user.name` (lowercase).
```

**Possible reasons for non-compliance:**

1. **Ambiguity in step order:** The rule mentions getting the issue with `get_issue` (which includes `gitBranchName`), then says to construct the branch name. An agent might be tempted to use the provided `gitBranchName` value.

2. **Insufficient emphasis:** The "Never use..." instruction appears later in "CRITICAL REMINDERS" section, not immediately in the branch creation steps.

3. **Lack of explicit prohibition:** The rule doesn't explicitly say "IGNORE the gitBranchName field from Linear" at the point where the field is mentioned.

---

## Proposed Solution

### Option 1: Strengthen the Rule (Recommended)

**Change lines 40-44 from:**
```markdown
### Step 3: Get issue

Once the user selects an issue (e.g., AIT-12):
- Call **user-linear.get_issue** with that issue's `id` (UUID) to get full details including `gitBranchName`, `title`, `description`.
```

**To:**
```markdown
### Step 3: Get issue

Once the user selects an issue (e.g., AIT-12):
- Call **user-linear.get_issue** with that issue's `id` (UUID) to get full details including `title`, `description`.
- **IGNORE** the `gitBranchName` field from Linear (it uses displayName, not GitHub username).
```

**And strengthen lines 47-51:**
```markdown
### Step 4: Branch

**CRITICAL: Always construct branch name from git config, NEVER use Linear's gitBranchName:**

1. Get GitHub username: `git config user.name` (use as-is, case-sensitive)
2. Extract IDENTIFIER from Linear issue (e.g., `AIT-12`, keep case from Linear)
3. Create slug from issue title: lowercase with hyphens (e.g., `fix-login`)
4. Run: `git checkout -b <username>/<IDENTIFIER>-<slug>`

**Example:** `fxstein/AIT-15-incorrect-branch-names-for-linear-issue`
```

### Option 2: Add Explicit Validation

Add a validation step after branch creation:
```markdown
5. **Verify:** Confirm the branch prefix matches `git config user.name`, NOT Linear's displayName
```

### Option 3: Remove gitBranchName from Documentation

Remove all mentions of `gitBranchName` from the rule to avoid temptation.

---

## Recommended Action

**Implement Option 1** (strengthen the rule) because:

1. ✅ Makes the prohibition explicit and immediate
2. ✅ Explains WHY not to use Linear's suggestion (displayName vs GitHub username)
3. ✅ Provides clear, step-by-step instructions with examples
4. ✅ Puts the critical instruction at the exact point of use

---

## Test Cases

After implementing the fix, test:

1. **Happy path:** Start work on a new Linear issue, verify branch uses correct GitHub username
2. **Edge case:** User with different Linear displayName and GitHub username
3. **Verification:** Branch name matches `git config user.name`, not Linear user displayName

---

## Files to Modify

- `.cursor/rules/linear-ai-todo-integration.mdc` (lines 40-54, 125-128)

---

## Related Issues

- **Linear:** https://linear.app/fxstein/issue/AIT-15/incorrect-branch-names-for-linear-issue
- **GitHub:** https://github.com/fxstein/ai-todo/issues/77
- **Previous fixes:**
  - Commit `2cf15f6` (2026-01-29): "Always construct branch names, never use Linear's gitBranchName"
  - Commit `bb10c31`: "Correct username logic for Linear integration (task#266)"
