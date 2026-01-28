# Linear Integration Review — Task #266

**Date:** 2026-01-28
**Scope:** Review of assessment, design, and implementation for consistency, issues, and gaps.

---

## Summary of Artifacts Created

| Artifact | Purpose | Status |
|----------|---------|--------|
| `docs/linear_integration_assessment.md` | Current Linear MCP capabilities and payload verification | ✅ Complete (#266.1) |
| `docs/linear_integration_design.md` | Data model, branching strategy, Life of a Ticket, automation spec | ✅ Complete (#266.2, #266.3) |
| `.cursor/rules/linear-workflow.mdc` | **NEW** Cursor rule: kickoff and branching automation | ✅ Complete (#266.4) |
| `.github/workflows/linear-pr-check.yml` | GitHub workflow: enforce branch naming | ✅ Complete (#266.4) |
| `CONTRIBUTING.md` | Developer guide: Linear workflow, branch naming | ✅ Complete (#266.4) |

---

## Issues Found

### 🔴 **CRITICAL: Conflicting Cursor rules**

**Issue:** Two rules with overlapping functionality and **incorrect API calls** in the old rule.

- **Old rule:** `.cursor/rules/linear-ai-todo-integration.mdc`
  - ❌ Line 21: Uses `user-linear.get_viewer()` — **does not exist** (should be `get_user("me")`).
  - ❌ Line 21: Uses `user-linear.get_issues({ assignee_id: <user_id> })` — **wrong tool/param** (should be `list_issues({ assignee: "me" })`).
  - ❌ Line 31: Uses `linear.update_issue(id="AIT-204", status="In Review")` — **wrong param** (should be `user-linear.update_issue` with `state`, not `status`).

- **New rule:** `.cursor/rules/linear-workflow.mdc`
  - ✅ Correct API calls: `user-linear.list_issues`, `user-linear.get_issue`, `user-linear.update_issue` with `state`.

**Problem:** Both rules trigger on "Start work" / "Kickoff". The old rule has **outdated/incorrect** API references from before the assessment was done.

**Impact:** Agents will get conflicting instructions; old rule will cause MCP errors.

**Recommendation:**
- **Option 1 (Preferred):** Delete `.cursor/rules/linear-ai-todo-integration.mdc` entirely. Use only the new `linear-workflow.mdc`.
- **Option 2:** Update the old rule with correct API calls and merge it with the new rule into one comprehensive rule (kickoff + closing + ai-todo planning).

---

### 🟡 **Branch naming case inconsistency**

**Issue:** Linear's `gitBranchName` might be lowercase; GitHub PR check expects uppercase.

- **Assessment (actual payload):** `"gitBranchName": "fxstein/ait-1-test-issue"` — lowercase `ait`.
- **Design doc:** Specifies `fxstein/AIT-12-fix-login` — uppercase `AIT`.
- **Cursor rule:** Says "use `gitBranchName` when present" (which is lowercase) OR "construct as `fxstein/AIT-12-fix-login`" (uppercase).
- **GitHub workflow:** Checks for `^.+/AIT-[0-9]+-.+$` — **uppercase only**.

**Problem:** If we use Linear's `gitBranchName` as-is (lowercase `ait-1-test-issue`), it will **fail** the PR check.

**Recommendation:**
- **Option 1 (Preferred):** Make GitHub PR check **case-insensitive**: `^.+/[Aa][Ii][Tt]-[0-9]+-.+$` or `(?i)^.+/ait-[0-9]+-.+$`.
- **Option 2:** When constructing branch name (if `gitBranchName` missing), force identifier to uppercase. When using `gitBranchName`, transform it to uppercase before running `git checkout -b`.
- **Option 3:** Accept lowercase in docs and PR check (e.g., `ait-123-desc` is valid). Update design doc and workflow to use `[Aa][Ii][Tt]` or just lowercase.

---

### 🟡 **Hardcoded username "fxstein"**

**Issue:** Cursor rule and CONTRIBUTING.md hardcode username as `fxstein`.

- **Cursor rule (line 23):** "Construct the branch name as `fxstein/<IDENTIFIER>-<slug>`"
- **CONTRIBUTING.md (line 24, 30, 54):** Examples and instructions use `fxstein` as the username.

**Problem:** Not portable to other users/contributors. Should be dynamic.

**Recommendation:**
- **Cursor rule:** Change to: "Construct as `<user>/<IDENTIFIER>-<slug>` where `<user>` is the user's Linear displayName (from `get_user("me")`) or git config `user.name` (lowercase, no spaces)."
- **CONTRIBUTING.md:** Change examples to use a placeholder like `<your-username>` or `yourname`, and clarify: "Replace `<user>` with your GitHub/Linear username."

---

### 🟡 **Missing: ai-todo planning step**

**Issue:** The new Cursor rule (`linear-workflow.mdc`) does NOT create ai-todo tasks from the Linear issue.

- **Design doc (section 3.1, step 4):** "Agent creates ai-todo task + subtasks from issue description; confirms plan with user."
- **Old rule (line 25):** "Initialize ai-todo: Call `ai-todo.add_task` to create the main task and `ai-todo.add_subtask`…"
- **New rule:** Only does: list issues → get issue → create branch → offer to set "In Progress". **No ai-todo task creation.**

**Problem:** Breaks the "macro-micro bridge" philosophy (Linear → ai-todo execution tracking).

**Recommendation:**
- **Add to linear-workflow.mdc** after branching step:
  ```markdown
  ## ai-todo Planning (optional but recommended)

  After creating the branch:
  - **Offer:** Ask: "Should I create an ai-todo task for this Linear issue?"
  - **If yes:**
    1. Call **ai-todo.add_task** with title from Linear issue (e.g., "[AIT-12] Fix login validation").
    2. If the Linear issue description has subtasks or steps, create subtasks with **ai-todo.add_subtask**.
    3. Confirm plan with user.
  ```

---

### 🟡 **Missing: closing workflow (In Review / Done)**

**Issue:** No automation for updating Linear when PR is opened or merged.

- **Design doc (section 3.1, steps 7, 9):** Optional: update_issue(state: "In Review") when PR opened; update_issue(state: "Done") when merged.
- **Old rule (section 4):** "When all tasks in ai-todo are marked done: ask to move to 'In Review'."
- **New rule:** Only has "In Progress" after branching. **No closing workflow.**

**Problem:** Manual step to update Linear when work is done or PR is ready.

**Recommendation:**
- **Add closing workflow section to linear-workflow.mdc** or create a separate rule:
  ```markdown
  ## Closing Workflow

  When the user says **"PR opened"** or **"Ready for review"**:
  - **Offer:** "Should I set this Linear issue to **In Review**?"
  - **If yes:** Call **user-linear.update_issue** with `id` and `state: "In Review"`.

  When the user says **"PR merged"** or **"Close issue"**:
  - **Offer:** "Should I set this Linear issue to **Done**?"
  - **If yes:** Call **user-linear.update_issue** with `id` and `state: "Done"`.
  ```
- **Optional:** Implement the GitHub Action "on merge → update Linear" from design doc (requires LINEAR_API_KEY secret). Mark this as "Future enhancement" if not doing now.

---

### 🟢 **Minor: update_issue id parameter clarification**

**Issue:** Unclear if `update_issue` accepts identifier (e.g., "AIT-12") or only UUID.

- **Assessment:** update_issue schema says `"id": { "type": "string", "description": "Issue ID" }` — doesn't specify UUID vs identifier.
- **Cursor rule (line 34):** "`id` (issue UUID or identifier)" — **assumes both work, but untested**.

**Problem:** If identifier doesn't work, the rule will fail when trying to update by identifier.

**Recommendation:**
- **Test:** Call `user-linear.update_issue` with identifier `"AIT-1"` vs UUID `"9d8c7da7-..."` to verify which works.
- **Document:** In the Cursor rule, clarify: "Use the issue's `id` (UUID) from `get_issue` response."
- If identifier works, note: "You can use identifier (e.g., 'AIT-12') or UUID."

---

### 🟢 **Not implemented: on-merge Linear update (optional)**

**Issue:** Design doc specifies optional GitHub Action: "On merge: Update Linear (optional, needs secret)."

- **Design doc (section 4.2):** "On push to `main` (merge): Parse commit or PR for identifier. Call Linear API to set issue state to 'Done'. Requires `LINEAR_API_KEY` in repo secrets."
- **Implementation:** We did NOT create this job.

**Problem:** Not a gap per se (marked "optional" in design), but should be tracked.

**Recommendation:**
- **Document as future enhancement:** Add to design doc or create a follow-up task: "Implement on-merge Linear state update (requires LINEAR_API_KEY secret and additional workflow job)."
- Or mark as out-of-scope for this phase and revisit after testing the manual workflow.

---

## Consistency Checks

| Area | Assessment | Design | Implementation | Status |
|------|------------|--------|----------------|--------|
| **API tool names** | `list_issues`, `get_issue`, `update_issue` | Same | ✅ New rule correct; ❌ old rule wrong | 🔴 Fix old rule |
| **API parameters** | `assignee: "me"`, `state` (not status) | Same | ✅ New rule correct; ❌ old rule wrong | 🔴 Fix old rule |
| **Branch format** | `fxstein/ait-1-test-issue` (lowercase) | `fxstein/AIT-12-fix-login` (uppercase) | PR check expects uppercase only | 🟡 Case mismatch |
| **gitBranchName usage** | Assessment shows it exists in payload | Design: prefer gitBranchName | Cursor rule: use if present | ✅ Consistent |
| **1 Team = 1 Repo** | ai-todo → fxstein/ai-todo | Same | CONTRIBUTING.md matches | ✅ Consistent |
| **ai-todo planning** | N/A (not in assessment) | Design: step 4 in Life of a Ticket | ❌ Not in new rule | 🟡 Gap |
| **Closing workflow** | N/A | Design: optional steps 7, 9 | ❌ Not in new rule | 🟡 Gap |

---

## Gaps Summary

| Gap | Severity | Recommendation |
|-----|----------|----------------|
| Old Cursor rule with wrong API calls | 🔴 Critical | Delete or fix `.cursor/rules/linear-ai-todo-integration.mdc` |
| Branch naming case mismatch | 🟡 Medium | Make PR check case-insensitive or force uppercase |
| Hardcoded username "fxstein" | 🟡 Medium | Make username dynamic (from Linear or git config) |
| Missing ai-todo planning step | 🟡 Medium | Add ai-todo task creation to Cursor rule |
| Missing closing workflow | 🟡 Medium | Add "In Review" / "Done" triggers to Cursor rule |
| update_issue id clarification | 🟢 Low | Test and document: identifier vs UUID |
| On-merge Linear update not implemented | 🟢 Low | Mark as future enhancement or out-of-scope |

---

## Recommended Actions

### Immediate (before using the workflow)

1. **Fix or delete old Cursor rule:**
   - Delete `.cursor/rules/linear-ai-todo-integration.mdc`, OR
   - Update it with correct API calls and merge with `linear-workflow.mdc`.

2. **Fix branch naming case:**
   - Update `.github/workflows/linear-pr-check.yml` to accept case-insensitive `AIT` / `ait`.
   - Document in CONTRIBUTING.md that Linear's `gitBranchName` might be lowercase.

3. **Make username dynamic:**
   - Update `linear-workflow.mdc` to derive username from Linear `get_user("me")` or git config.
   - Update CONTRIBUTING.md examples to use placeholder `<your-username>`.

### High Priority (for complete workflow)

1. **Add ai-todo planning step:**
   - Extend `linear-workflow.mdc` with: after branching, offer to create ai-todo task + subtasks.

2. **Add closing workflow:**
   - Extend `linear-workflow.mdc` or create new rule: "PR opened" → "In Review"; "PR merged" → "Done".

### Low Priority (can defer)

1. **Test and document update_issue id parameter.**
2. **Consider implementing on-merge Linear update (with LINEAR_API_KEY secret).**

---

*Review completed for task #266. Next: Task #266.5 (Test & document) can address these gaps.*
