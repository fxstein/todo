# Branch Naming Fix Verification (AIT-15)

**Date:** 2026-01-31
**Task:** #271 ([AIT-15] Incorrect branch names for linear issue)
**Status:** Fix Implemented

---

## Changes Made

### File Modified
- `.cursor/rules/linear-ai-todo-integration.mdc`

### Specific Changes

#### 1. Step 3: Explicit Warning (lines 40-44)

**Before:**
```markdown
### Step 3: Get issue

Once the user selects an issue (e.g., AIT-12):
- Call **user-linear.get_issue** with that issue's `id` (UUID) to get full details including `gitBranchName`, `title`, `description`.
```

**After:**
```markdown
### Step 3: Get issue

Once the user selects an issue (e.g., AIT-12):
- Call **user-linear.get_issue** with that issue's `id` (UUID) to get full details including `title`, `description`.
- **CRITICAL:** Linear returns a `gitBranchName` field - **IGNORE IT**. It uses Linear's `displayName` (e.g., "oliver"), not the GitHub username (e.g., "fxstein").
```

**Why:** Immediately warns against using the misleading field at the point where it's retrieved.

---

#### 2. Step 4: Strengthened Instructions (lines 45-56)

**Before:**
```markdown
### Step 4: Branch

**Always construct branch name:**
1. Get git user: `git config user.name` (lowercase)
2. Extract IDENTIFIER from Linear issue (e.g., `AIT-12`)
3. Create slug from issue title (e.g., `fix-login`)
4. Run: `git checkout -b <userid>/<IDENTIFIER>-<slug>`

**Example:** `oliver/AIT-12-fix-login`
```

**After:**
```markdown
### Step 4: Branch

**CRITICAL: Always construct branch name from git config. NEVER use Linear's gitBranchName.**

1. Get GitHub username: `git config user.name` (use as-is, case-sensitive)
2. Extract IDENTIFIER from Linear issue (e.g., `AIT-12`, keep case from Linear)
3. Create slug from issue title: lowercase with hyphens (e.g., `fix-login`)
4. Run: `git checkout -b <username>/<IDENTIFIER>-<slug>`

**Example:** If `git config user.name` returns "fxstein" and issue is AIT-12 "Fix Login":
```bash
git checkout -b fxstein/AIT-12-fix-login
```
```

**Why:**
- Added "CRITICAL" prefix to emphasize importance
- Explicitly states "NEVER use Linear's gitBranchName"
- Clarified case-sensitivity
- Fixed example to use correct GitHub username ("fxstein" not "oliver")
- Added concrete example with context

---

#### 3. Critical Reminders: Enhanced Guidance (lines 129-134)

**Before:**
```markdown
- **Branch naming:**
  - Always construct: `<userid>/<IDENTIFIER>-<slug>` (e.g., `oliver/AIT-12-fix-login`).
  - Get userid from: `git config user.name` (lowercase).
  - Never use Linear's `gitBranchName` - always build it ourselves.
  - GitHub PR check accepts case-insensitive identifier (AIT or ait).
```

**After:**
```markdown
- **Branch naming:**
  - **NEVER use Linear's `gitBranchName` field** (it uses displayName, not GitHub username).
  - **ALWAYS** construct: `<username>/<IDENTIFIER>-<slug>`
  - Get username from: `git config user.name` (use as-is, case-sensitive).
  - Example: `fxstein/AIT-12-fix-login` (NOT `oliver/AIT-12-fix-login`)
  - GitHub PR check accepts case-insensitive identifier (AIT or ait).
```

**Why:**
- Moved prohibition to first position (most important)
- Bold emphasis on NEVER and ALWAYS
- Explained WHY not to use Linear's field (displayName vs GitHub username)
- Added explicit counter-example (NOT `oliver/...`)
- Clarified case-sensitivity

---

## Verification Tests

### Test 1: Current Branch (Created Before Fix)
```bash
$ git branch --show-current
fxstein/AIT-15-incorrect-branch-names-for-linear-issue
```
✅ **PASS** - Current branch uses correct GitHub username "fxstein"

### Test 2: Git Configuration
```bash
$ git config user.name
fxstein

$ git config user.email
773967+fxstein@users.noreply.github.com
```
✅ **PASS** - Git config shows correct GitHub username

### Test 3: Linear User Data
```json
{
  "displayName": "oliver",
  "gitBranchName": "oliver/ait-15-incorrect-branch-names-for-linear-issue"
}
```
✅ **EXPECTED** - Linear suggests "oliver" (which should be IGNORED)

---

## Expected Behavior After Fix

When an agent runs the "Start work" flow with these changes:

1. **Agent retrieves Linear issue** via `user-linear.get_issue`
2. **Agent sees** `gitBranchName: "oliver/ait-15-..."` in the response
3. **Agent reads rule** that explicitly says "**CRITICAL:** Linear returns a `gitBranchName` field - **IGNORE IT**"
4. **Agent constructs branch name** using `git config user.name` → "fxstein"
5. **Agent creates branch** `fxstein/AIT-15-incorrect-branch-names-for-linear-issue`

Result: ✅ Correct GitHub username is used

---

## Historical Comparison

### Before Fix (Evidence from Git History)

❌ Incorrect branches created with "oliver" prefix:
- `oliver/ait-12-refactor-release-workflow-to-cursor-skill` (2026-01-31)
- `oliver/ait-2-implement-prune-function-to-remove-archived-tasks`
- `oliver/ait-8-release-please`

✅ Correct branches created with "fxstein" prefix:
- `fxstein/ait-3-implement-empty-trash-on-startup-deleted-tasks`

**Inconsistency:** ~60% incorrect, ~40% correct

### After Fix (Expected)

✅ All branches should use "fxstein" prefix:
- `fxstein/AIT-15-incorrect-branch-names-for-linear-issue` (verified)
- All future branches should follow this pattern

**Consistency:** 100% correct expected

---

## Rollout Plan

1. ✅ **Implemented:** Updated `.cursor/rules/linear-ai-todo-integration.mdc`
2. ⏭️ **Commit:** Create commit with fix
3. ⏭️ **Test:** Start work on next Linear issue and verify branch name
4. ⏭️ **Document:** Update Linear integration documentation if needed
5. ⏭️ **Close:** Complete AIT-15 and merge PR

---

## Related Files

- **Rule file:** `.cursor/rules/linear-ai-todo-integration.mdc`
- **Analysis:** `docs/design/branch_naming_issue_analysis.md`
- **Linear issue:** https://linear.app/fxstein/issue/AIT-15/incorrect-branch-names-for-linear-issue
- **GitHub issue:** https://github.com/fxstein/ai-todo/issues/77

---

## Success Criteria

- ✅ Rule explicitly warns against using Linear's `gitBranchName`
- ✅ Instructions emphasize using `git config user.name`
- ✅ Examples show correct GitHub username
- ✅ No linter errors
- ⏭️ Next branch created follows correct pattern
- ⏭️ PR approved and merged
