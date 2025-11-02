# todo.ai Numbering Modes Test Plan

## Overview

This document outlines comprehensive testing for all task numbering modes in `todo.ai`. Tests verify correct task assignment, reference resolution, and conflict handling across all modes.

---

## Test Environment Setup

### Prerequisites
- `todo.ai` script installed
- Git repository initialized
- GitHub CLI installed (for enhanced mode tests)

### Test Data
- Clean `TODO.md` file
- Clean `.todo.ai/` directory
- Backup existing data before testing

---

## Test Suite: All Numbering Modes

### Test 1: Single-User Mode

**Objective:** Verify sequential numbering works correctly

**Steps:**
1. Switch to single-user mode (or ensure default)
2. Add multiple tasks
3. Add subtasks
4. Verify task IDs are sequential
5. Test task reference resolution
6. Test commands (complete, modify, show, etc.)

**Expected Results:**
- Tasks assigned: `#57`, `#58`, `#59` (continuing from existing serial)
- Subtasks: `#57.1`, `#57.2`, etc.
- Number-only references work: `complete 57` → finds `#57`
- Full references work: `show 57` → finds `#57`

---

### Test 2: Multi-User Mode

**Objective:** Verify prefix-based numbering and auto-resolution

**Steps:**
1. Switch to multi-user mode
2. Add multiple tasks
3. Verify tasks get user prefix (e.g., `fxstein-60`)
4. Test number-only reference resolution (`complete 60` → `fxstein-60`)
5. Test full reference resolution (`show fxstein-60`)
6. Test cross-user references (`show alice-61`)

**Expected Results:**
- Tasks assigned: `#fxstein-60`, `#fxstein-61`, `#fxstein-62`
- User prefix = first 7 chars of GitHub username
- Number-only references auto-resolve to user's prefix
- Full references work for any user's prefix

---

### Test 3: Branch Mode

**Objective:** Verify branch-prefixed numbering

**Steps:**
1. Switch to branch mode
2. Check current branch name
3. Add multiple tasks
4. Verify tasks get branch prefix (e.g., `main-60` or `featur-60`)
5. Test number-only reference resolution
6. Switch branches and verify prefix changes

**Expected Results:**
- Tasks assigned: `#main-60`, `#main-61` (on main branch)
- Branch prefix = first 7 chars of branch name
- Number-only references auto-resolve to branch prefix
- Prefix changes when switching branches

---

### Test 4: Enhanced Multi-User Mode (GitHub Issues)

**Objective:** Verify atomic coordination via GitHub Issues

**Prerequisites:**
- GitHub CLI authenticated
- Test issue created for coordination

**Steps:**
1. Create test GitHub issue for coordination
2. Switch to enhanced mode with GitHub Issues coordination
3. Add multiple tasks
4. Verify tasks assigned atomically
5. Test fallback to multi-user if GitHub Issues unavailable
6. Test reference resolution

**Expected Results:**
- Tasks assigned atomically: `#fxstein-60`, `#fxstein-61`
- No numbering conflicts even with concurrent usage
- Falls back to multi-user mode if GitHub Issues unavailable
- Reference resolution works same as multi-user mode

---

### Test 5: Enhanced Multi-User Mode (CounterAPI)

**Objective:** Verify atomic coordination via CounterAPI

**Steps:**
1. Switch to enhanced mode with CounterAPI coordination
2. Add multiple tasks
3. Verify tasks assigned atomically
4. Test fallback to multi-user if CounterAPI unavailable

**Expected Results:**
- Tasks assigned atomically via CounterAPI
- Falls back to multi-user mode if CounterAPI unavailable
- Reference resolution works same as multi-user mode

---

## Test Suite: Reference Resolution

### Test 6: Number-Only Reference Resolution

**Objective:** Verify automatic prefix addition for number-only references

**Test Cases:**
1. **Single-User Mode:**
   - `complete 57` → resolves to `#57` ✓
   - `show 57` → resolves to `#57` ✓

2. **Multi-User Mode:**
   - `complete 60` → resolves to `#fxstein-60` ✓
   - `show 60` → resolves to `#fxstein-60` ✓

3. **Branch Mode:**
   - `complete 60` → resolves to `#main-60` (or current branch prefix) ✓
   - `show 60` → resolves to `#main-60` ✓

4. **Enhanced Mode:**
   - `complete 60` → resolves to `#fxstein-60` ✓
   - `show 60` → resolves to `#fxstein-60` ✓

**Expected Results:**
- All commands accept number-only references
- Tool automatically adds appropriate prefix based on mode
- Full references (with prefix) also work

---

### Test 7: Cross-User/Branch Reference Resolution

**Objective:** Verify full references work for other users' tasks

**Test Cases:**
1. **Multi-User Mode:**
   - `show alice-61` → finds `#alice-61` ✓
   - `complete alice-61` → finds `#alice-61` ✓
   - Number-only reference for other user's task fails (expected)

2. **Branch Mode:**
   - Switch to branch A, create task `#brancha-60`
   - Switch to branch B, verify can't find `#brancha-60` by number-only
   - Can find with full reference: `show brancha-60`

**Expected Results:**
- Full references (with prefix) work for any user/branch
- Number-only references only resolve to current user/branch prefix
- Clear error messages for invalid references

---

## Test Suite: Conflict Handling

### Test 8: Duplicate Detection

**Objective:** Verify duplicate task ID detection

**Steps:**
1. Manually create duplicate task IDs in TODO.md
2. Run `./todo.ai --lint`
3. Verify duplicates are detected
4. Run `./todo.ai resolve-conflicts --dry-run`
5. Verify conflicts are identified and mapping created
6. Run `./todo.ai resolve-conflicts`
7. Verify duplicates renumbered correctly

**Expected Results:**
- Duplicates detected by `--lint` command
- Conflict resolution identifies all duplicates
- First occurrence kept, subsequent ones renumbered
- All references updated correctly

---

### Test 9: Automatic Conflict Resolution

**Objective:** Verify automatic renumbering fixes conflicts

**Steps:**
1. Create scenario with duplicate IDs (e.g., two `#60` tasks)
2. Run `./todo.ai resolve-conflicts`
3. Verify first `#60` kept, second renumbered to `#61` (or next available)
4. Verify all references updated
5. Verify backup created

**Expected Results:**
- Conflicts resolved automatically
- Backup created before changes
- All task references updated
- TODO.md structure maintained

---

## Test Suite: Mode Switching

### Test 10: Switch Mode Without Renumbering

**Objective:** Verify mode switch preserves existing task IDs

**Steps:**
1. Create tasks in single-user mode (`#57`, `#58`)
2. Switch to multi-user mode (without `--renumber`)
3. Verify existing tasks keep old format (`#57`, `#58`)
4. Add new task
5. Verify new task uses new format (`#fxstein-59`)

**Expected Results:**
- Existing tasks keep old IDs: `#57`, `#58`
- New tasks use new format: `#fxstein-59`
- Both formats work for references
- Backup created before switch

---

### Test 11: Switch Mode With Renumbering

**Objective:** Verify mode switch with renumbering updates all tasks

**Steps:**
1. Create tasks in single-user mode (`#57`, `#58`)
2. Switch to multi-user mode with `--renumber`
3. Verify tasks renumbered: `#fxstein-57`, `#fxstein-58`
4. Verify all references updated
5. Verify backup created

**Expected Results:**
- All tasks renumbered to new format
- All references updated (relationships, notes, subtasks)
- Backup created before changes
- Rollback works if needed

---

## Test Suite: Fallback Scenarios

### Test 12: Enhanced Mode GitHub Issues Fallback

**Objective:** Verify fallback to multi-user when GitHub Issues unavailable

**Steps:**
1. Switch to enhanced mode with GitHub Issues
2. Disconnect network or invalidate GitHub CLI
3. Add task
4. Verify fallback to multi-user mode
5. Verify task assigned with prefix (not atomically)

**Expected Results:**
- Falls back to multi-user mode gracefully
- Task assigned with user prefix
- Error logged but operation continues
- No exception or crash

---

### Test 13: Enhanced Mode CounterAPI Fallback

**Objective:** Verify fallback to multi-user when CounterAPI unavailable

**Steps:**
1. Switch to enhanced mode with CounterAPI
2. Use invalid namespace or disconnect network
3. Add task
4. Verify fallback to multi-user mode

**Expected Results:**
- Falls back to multi-user mode gracefully
- Task assigned with user prefix
- Error logged but operation continues

---

## Test Execution

### Running Tests

```bash
# Navigate to test directory
cd /path/to/test-repo

# Run individual tests
./test_single_user_mode.sh
./test_multi_user_mode.sh
./test_branch_mode.sh
./test_enhanced_mode.sh
./test_reference_resolution.sh
./test_conflict_resolution.sh
./test_mode_switching.sh
./test_fallback_scenarios.sh
```

### Test Results Format

Each test should output:
- ✅ Pass / ❌ Fail
- Test name
- Expected vs actual results
- Error messages (if any)

---

## Known Issues and Limitations

### Current Limitations
1. Enhanced mode requires GitHub CLI or CounterAPI
2. Branch mode prefix changes when switching branches (by design)
3. Cross-user references require full ID (by design)
4. Mode switching requires backup (automatic)

### Known Issues
- None currently identified

---

## Test Coverage Summary

| Test Category | Tests | Status |
|--------------|-------|--------|
| All Numbering Modes | 5 | Pending |
| Reference Resolution | 2 | Pending |
| Conflict Handling | 2 | Pending |
| Mode Switching | 2 | Pending |
| Fallback Scenarios | 2 | Pending |
| **Total** | **13** | **Pending** |

---

## Next Steps

1. Execute test suite systematically
2. Document test results
3. Fix any issues found
4. Re-run tests to verify fixes
5. Update this document with test results

