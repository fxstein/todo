# Multi-User/Multi-Branch Task Conflict Analysis

## Overview

This document analyzes scenarios where task numbering conflicts occur in a multi-user, multi-branch, and pull request environment when using `todo.ai`.

## Current Task Numbering System

The current `todo.ai` system uses sequential integer-based task numbering:
- Tasks are numbered sequentially: `#1`, `#2`, `#3`, etc.
- Numbers are assigned based on the highest existing task number in `TODO.md`
- Task numbers are sequential integers only (no prefix or namespace)

## Conflict Scenarios

### Scenario 1: Parallel Branch Development

**Problem:** Multiple developers create tasks on different branches simultaneously.

**Example:**
- Developer A (branch `feature-auth`) adds tasks: `#50`, `#51`, `#52`
- Developer B (branch `feature-api`) adds tasks: `#50`, `#51`, `#52`
- Both branches start from main where the highest task is `#49`

**Result:** When merging either branch, conflicts occur:
- Git merge conflict in `TODO.md`
- Duplicate task numbers
- Broken task references in commit messages (`task#50` could refer to different tasks)

**Impact:** High - This is the most common scenario in collaborative development.

---

### Scenario 2: Sequential Merges with Overlapping Number Ranges

**Problem:** Branches merged sequentially may create gaps or duplicate number assignments.

**Example Timeline:**
1. Main branch has task `#45`
2. Developer A creates branch, adds `#46`, `#47`, commits with `task#46`, `task#47`
3. Developer B creates branch from main (still at `#45`), adds `#46`, `#47`, commits with `task#46`, `task#47`
4. Developer A's branch merges first → main now has `#47`
5. Developer B's branch merges → conflicts: `#46` and `#47` already exist

**Result:**
- Git merge conflict requiring manual resolution
- Commit messages reference wrong task numbers
- Task history becomes inaccurate

**Impact:** High - Affects commit history and task tracking.

---

### Scenario 3: Subtask Numbering Conflicts

**Problem:** Subtasks inherit parent task numbers, causing conflicts when parent tasks have conflicting numbers.

**Example:**
- Branch A: Parent task `#50` with subtasks `#50.1`, `#50.2`, `#50.3`
- Branch B: Parent task `#50` with subtasks `#50.1`, `#50.2`
- When merged, subtask numbering conflicts occur

**Result:**
- Subtask relationships break
- Duplicate subtask numbers under different parents
- Task hierarchy becomes corrupted

**Impact:** Medium - Affects task organization and relationships.

---

### Scenario 4: Deleted Task Number Reuse

**Problem:** When tasks are deleted and a branch is based on an older version, deleted numbers get reused.

**Example:**
1. Main: Tasks `#1` through `#50` exist
2. Developer deletes `#25` on main
3. Developer B creates branch from old commit (where `#25` still exists)
4. Developer B adds `#25` (thinking it's available)
5. Conflict when merging: `#25` already exists in main (or was deleted, causing confusion)

**Result:**
- Number reuse creates ambiguity
- Unclear which task `#25` refers to in commit history

**Impact:** Medium - Causes confusion in historical task references.

---

### Scenario 5: Concurrent Updates to TODO.md

**Problem:** Multiple developers updating `TODO.md` simultaneously, even on the same branch.

**Example:**
1. Both Developer A and Developer B have the same branch checked out
2. Main branch is at task `#50`
3. Developer A adds task `#51`, commits
4. Developer B (not pulled yet) adds task `#51`, commits
5. Push/pull reveals conflict

**Result:**
- Git conflict in `TODO.md`
- Requires manual merge resolution
- Potential for one developer's work to be lost

**Impact:** Medium - Common in fast-moving projects.

---

### Scenario 6: Cross-Reference Conflicts in Commit Messages

**Problem:** Commit messages reference task numbers that change after merge conflicts are resolved.

**Example:**
1. Developer A commits: `feat: Implement authentication (task#50)`
2. Developer B commits: `feat: Add API endpoints (task#50)`
3. After merge resolution, one task becomes `#51`
4. Commit message still says `task#50`, but refers to wrong task

**Result:**
- Commit history becomes inaccurate
- Task references in git log point to wrong tasks
- Difficult to trace feature implementation to tasks

**Impact:** High - Breaks the connection between git history and task tracking.

---

### Scenario 7: Pull Request Reviews with Task Conflicts

**Problem:** PR reviews cannot accurately assess tasks when numbers conflict.

**Example:**
1. PR includes 10 tasks numbered `#50-59`
2. Main branch also has tasks `#50-59` (different tasks)
3. Reviewers cannot tell which tasks are new vs. conflicts

**Result:**
- Difficult to review PRs
- Unclear what work is actually in the PR
- Merge conflicts discovered late in review process

**Impact:** Medium - Slows down code review and integration.

---

### Scenario 8: Distributed Development (No Central Coordination)

**Problem:** Teams working in different time zones without coordination.

**Example:**
- Team A (US timezone) adds tasks `#50-55` during their day
- Team B (EU timezone) adds tasks `#50-52` during their day
- Both push to their feature branches
- Conflicts discovered when trying to merge to main

**Result:**
- Frequent merge conflicts
- Need for constant coordination
- Slows down parallel development

**Impact:** High - Especially problematic for distributed teams.

---

## Impact Summary

### High Impact Scenarios:
- ✅ **Scenario 1:** Parallel Branch Development
- ✅ **Scenario 2:** Sequential Merges with Overlapping Ranges
- ✅ **Scenario 6:** Cross-Reference Conflicts in Commit Messages
- ✅ **Scenario 8:** Distributed Development

### Medium Impact Scenarios:
- ✅ **Scenario 3:** Subtask Numbering Conflicts
- ✅ **Scenario 4:** Deleted Task Number Reuse
- ✅ **Scenario 5:** Concurrent Updates to TODO.md
- ✅ **Scenario 7:** Pull Request Reviews with Task Conflicts

## Root Causes

1. **Sequential Numbering:** Integer-based sequential numbering has no namespace isolation
2. **No Conflict Detection:** System doesn't detect or prevent numbering conflicts
3. **No Merge Strategy:** No automated strategy for resolving conflicts
4. **No Distributed Coordination:** No mechanism to coordinate task numbering across branches
5. **State-Dependent Assignment:** Task numbers depend on local file state, not global state

## Requirements for Solution

A solution must address:
- ✅ Prevent task number conflicts before they occur
- ✅ Detect conflicts during merge/PR operations
- ✅ Automatically resolve or guide resolution of conflicts
- ✅ Maintain commit message task reference accuracy
- ✅ Support parallel development without coordination overhead
- ✅ Preserve task history and relationships

## Next Steps

1. Research existing solutions (task #52.2)
2. Design distributed numbering scheme (task #52.5)
3. Design merge/resolution strategy (task #52.4, #52.6)
4. Create overall architecture design (task #52.3)
