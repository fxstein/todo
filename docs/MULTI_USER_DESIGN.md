# Design: Multi-User Conflict-Free Task Numbering Architecture

## Overview

This document proposes the solution architecture for conflict-free task numbering in a multi-user, multi-branch, and pull request environment for `todo.ai`.

**Scope:** This design is intended for **single Git repository** scenarios where multiple users work on different branches within the same repository. It does **not** support coordination across forks or completely independent repositories.

## Decision Summary

**Selected Approach:** Git-Based Atomic Assignment (Option 1)

After analyzing conflict scenarios and researching existing solutions, **Git-Based Atomic Assignment** has been selected as the implementation approach. This approach simulates server-side atomic assignment using Git as a coordination mechanism, preserving sequential numbering while minimizing conflicts.

---

## Architecture Overview

### Core Principle

**Simulate server-side atomic assignment using Git as a coordination layer.**

Instead of requiring a central server (like GitHub Issues or JIRA), we use Git itself as the coordination mechanism. This allows multiple users to work in parallel while maintaining sequential numbering and minimizing conflicts.

### High-Level Flow

```
User Action: Add Task
    ↓
1. Git Pull from main (get latest authoritative state)
    ↓
2. Calculate MAX(local, remote) + 1
    ↓
3. Assign task number
    ↓
4. Commit immediately (local commit)
    ↓
5. Push to current branch (make visible to others)
    ↓
6. Done (minimal conflict window)
```

**Key Points:**
- **Pull from main**: Always pull from main branch to get authoritative task numbers
- **Commit locally**: Commit changes to current branch (feature branch or main)
- **Push to current branch**: Push immediately after commit to make changes visible
- **Serial file coordination**: Serial file is synchronized across all branches via main

---

## Detailed Architecture

### 1. Git Pull Before Assignment (Coordination Step)

**Purpose:** Synchronize with remote state before assigning task numbers.

**Critical Decision: Coordinate with main AND current branch's remote state**

Each branch has its own copy of the serial file. We need to coordinate with:
1. **Main branch** (authoritative for merged tasks)
2. **Current branch's remote** (for unmerged tasks already pushed to this branch)

**The Problem:**
- If we only check main, feature branches can create conflicts
- Example: Branch A fetches main (#49), calculates #50, pushes to Branch A
- Main still has #49 (Branch A can't push to main)
- Branch B fetches main (#49), calculates #50 → conflict when merging!

**The Solution:**
- Check main's max (merged tasks)
- Check current branch's remote max (unmerged but pushed tasks on this branch)
- Calculate MAX(local, main, current_branch_remote) + 1
- Accept that cross-branch conflicts can occur until merge (resolve at merge time)

**Implementation:**
- Fetch from **main branch** (authoritative source)
- Fetch from **current branch's remote** (if on a feature branch)
- Check both for highest task numbers
- Use MAX of all sources for safe numbering

**When to Pull:**
- Before `add` command (new tasks)
- Before `add-subtask` command (new subtasks)
- Before any operation that creates a new task number

**Pull Strategy:**
```bash
# Fetch from main branch (authoritative source)
git fetch origin main --quiet 2>/dev/null || true

# Get main's TODO.md and serial file for coordination
git show origin/main:TODO.md > "$TODO_FILE.tmp.main" 2>/dev/null || true
git show origin/main:.todo.ai/.todo.ai.serial > "$SERIAL_FILE.tmp.main" 2>/dev/null || true

# If on a feature branch, also fetch from current branch's remote
current_branch=$(git branch --show-current 2>/dev/null || echo "")
if [[ -n "$current_branch" ]] && [[ "$current_branch" != "main" ]]; then
    git fetch origin "$current_branch" --quiet 2>/dev/null || true
    git show "origin/$current_branch:TODO.md" > "$TODO_FILE.tmp.branch" 2>/dev/null || true
    git show "origin/$current_branch:.todo.ai/.todo.ai.serial" > "$SERIAL_FILE.tmp.branch" 2>/dev/null || true
fi

# Use these for MAX calculation (see step 2)
```

**Why coordinate with main AND current branch?**
- **Main is authoritative**: Contains all merged tasks (definitive sequence)
- **Current branch remote**: Contains unmerged tasks already pushed to this branch
- **Prevents local conflicts**: If we already pushed #50 to Branch A, next add on Branch A should see it
- **Cross-branch conflicts**: Two different feature branches may still conflict (resolved at merge time)

**Limitations:**
- We can't see unmerged tasks from OTHER feature branches until merge
- Example: Branch A has #50 (not in main), Branch B won't see it until merge
- This is acceptable: conflicts resolved at merge time via conflict resolution

---

### 2. MAX(local, remote) + 1 Algorithm

**Purpose:** Determine the next safe task number by taking the maximum of local and remote highest task numbers.

**Algorithm:**
1. Scan local `TODO.md` for highest task number
2. Scan remote `TODO.md` (from git pull) for highest task number
3. Calculate: `next_id = MAX(local_max, remote_max) + 1`
4. Use this number for the new task

**Implementation Details:**

```bash
# Find highest task number in TODO.md
get_highest_task_number() {
    local todo_file="$1"
    local highest=0
    
    # Extract all task IDs (handles main tasks and subtasks)
    # Pattern: #123 or #123.4 (subtasks)
    local task_ids=$(grep -oE '#[0-9]+(\.[0-9]+)?' "$todo_file" | sed 's/#//' | sort -t. -k1,1n -k2,2n)
    
    # Find highest main task ID (non-subtask)
    for id in $task_ids; do
        # Skip subtasks (contain dot)
        if [[ ! "$id" =~ \. ]]; then
            if [[ $id -gt $highest ]]; then
                highest=$id
            fi
        fi
    done
    
    echo $highest
}

# Calculate next safe task number
calculate_next_task_number() {
    local local_file="$TODO_FILE"
    
    # Find highest task number in local TODO.md
    local local_max=$(get_highest_task_number "$local_file")
    
    # Check main's TODO.md (from git_pull_todo_files)
    local main_max=0
    if [[ -f "$TODO_FILE.tmp.main" ]]; then
        main_max=$(get_highest_task_number "$TODO_FILE.tmp.main")
        # Also check main's serial file
        if [[ -f "$SERIAL_FILE.tmp.main" ]]; then
            local main_serial=$(cat "$SERIAL_FILE.tmp.main" 2>/dev/null || echo "0")
            if [[ "$main_serial" =~ ^[0-9]+$ ]]; then
                local main_serial_max=$((main_serial - 1))
                if [[ $main_serial_max -gt $main_max ]]; then
                    main_max=$main_serial_max
                fi
            fi
        fi
    fi
    
    # Check current branch's remote TODO.md (if on feature branch)
    local branch_max=0
    local current_branch=$(git branch --show-current 2>/dev/null || echo "")
    if [[ -n "$current_branch" ]] && [[ "$current_branch" != "main" ]]; then
        if [[ -f "$TODO_FILE.tmp.branch" ]]; then
            branch_max=$(get_highest_task_number "$TODO_FILE.tmp.branch")
            # Also check branch's remote serial file
            if [[ -f "$SERIAL_FILE.tmp.branch" ]]; then
                local branch_serial=$(cat "$SERIAL_FILE.tmp.branch" 2>/dev/null || echo "0")
                if [[ "$branch_serial" =~ ^[0-9]+$ ]]; then
                    local branch_serial_max=$((branch_serial - 1))
                    if [[ $branch_serial_max -gt $branch_max ]]; then
                        branch_max=$branch_serial_max
                    fi
                fi
            fi
        fi
    fi
    
    # Take maximum of all sources and add 1
    local overall_max=$local_max
    if [[ $main_max -gt $overall_max ]]; then
        overall_max=$main_max
    fi
    if [[ $branch_max -gt $overall_max ]]; then
        overall_max=$branch_max
    fi
    
    local next_id=$((overall_max + 1))
    
    # Cleanup temp files
    rm -f "$TODO_FILE.tmp.main" "$TODO_FILE.tmp.branch" "$SERIAL_FILE.tmp.main" "$SERIAL_FILE.tmp.branch" 2>/dev/null || true
    
    echo $next_id
}
```

**Edge Cases:**
- If remote pull fails: Use local maximum + 1
- If both files are empty: Start at `#1`
- If one file is missing: Use available file's maximum

---

### 3. Immediate Commit and Push After Assignment

**Purpose:** Minimize the conflict window by committing the task assignment immediately and making it visible to others.

**Implementation:**
- After assigning task number and adding to `TODO.md`
- Update `.todo.ai/.todo.ai.serial` immediately
- Commit both files in a single atomic commit to **current branch**
- Push to current branch immediately to make changes visible

**Commit and Push:**
```bash
# Commit to current branch (feature branch or main)
git commit -m "task: Add task #$task_id $task_description" -- TODO.md .todo.ai/.todo.ai.serial

# Push to current branch immediately
git push origin $(git branch --show-current) --quiet 2>/dev/null || {
    # If push fails, log warning but don't block
    # User can push manually later
    log_todo_action "WARNING" "GIT_PUSH_FAILED" "Could not push changes, commit is local only"
}
```

**Why Immediate Commit and Push:**
- Reduces time between pull and commit (smaller conflict window)
- Makes the assignment "visible" to other users quickly (via push)
- Other users' next pull from main will see these changes
- Follows atomic assignment pattern
- Serial file on current branch is updated and pushed

**Branch Strategy:**
- **If on main branch**: Commit and push directly to main
- **If on feature branch**: Commit and push to feature branch
- **When merging to main**: Feature branch's serial file is merged with main's serial file
- **After merge to main**: All branches pull from main's authoritative serial file state

---

### 4. Conflict Window Minimization

**Problem:** Even with pull + immediate commit, there's a small window where conflicts can occur.

**Solution Strategy:**
1. **Minimize window size**: Make pull-to-commit time as short as possible
2. **Accept rare conflicts**: Handle conflicts when they occur (see Conflict Resolution)
3. **Auto-retry on conflict**: If conflict detected, retry the assignment

**Conflict Window:**
- Time between git pull and git commit
- Typically: milliseconds to seconds
- Rare but possible when two users pull simultaneously

---

## Handling Conflict Scenarios

### Scenario 1: Parallel Branch Development

**Solution:** Git pull before assignment + MAX algorithm

- Each branch pulls latest main before creating tasks
- MAX algorithm ensures numbers don't overlap
- Immediate commit minimizes conflict window

**Example:**
- Main: Highest task `#49`
- Branch A: Fetches from origin/main (sees `#49`), fetches from origin/Branch A (sees `#49`), calculates MAX(49, 49, 49) + 1 = `#50`, commits to Branch A, pushes to origin/Branch A
- Branch B: Fetches from origin/main (sees `#49`), fetches from origin/Branch B (sees `#49`), calculates MAX(49, 49, 49) + 1 = `#50`, commits to Branch B, pushes to origin/Branch B
- **Note**: Branch B can't see Branch A's `#50` because it's on a different branch (this is a limitation we accept)
- When Branch A merges to main first → main now has `#50` (and serial file = 51)
- When Branch B tries to merge to main: Git merge conflict in TODO.md and serial file (both have `#50`)
- **Conflict resolution**: Git detects duplicate `#50`, automatic or manual resolution renumbers one to `#51`
- Result: No duplicate numbers in main after merge resolution, sequential numbering maintained

---

### Scenario 2: Sequential Merges with Overlapping Ranges

**Solution:** Continuous synchronization via git pull

- Each merge updates main's task numbers
- Subsequent branches pull latest main before creating tasks
- MAX algorithm ensures new numbers are always higher

**Example:**
- Main: `#45`
- Branch A: Fetches main (sees `#45`), adds `#46`, `#47`, commits to Branch A, pushes to Branch A, merges to main → Main now has `#47` (and serial file = 48)
- Branch B: Fetches main (now sees `#47`), calculates MAX(local, 47) + 1 = `#48`, adds `#48`, `#49`, commits to Branch B, pushes to Branch B
- When Branch B merges to main: No conflicts (Branch B has `#48-49`, main has `#47`)
- Result: Sequential numbering: `#47`, `#48`, `#49`

---

### Scenario 3: Subtask Numbering Conflicts

**Solution:** Parent task number determines subtask numbering

- Subtasks inherit parent task number: `#50.1`, `#50.2`, etc.
- When parent task number is determined (via MAX), subtask numbers are derived
- If parent conflicts, subtasks are renumbered with parent (see Conflict Resolution)

**Example:**
- Branch A: Parent `#50` with subtasks `#50.1`, `#50.2`
- Branch B: Parent `#50` with subtasks `#50.1`
- When merged, parent conflict is resolved first, then subtasks are renumbered accordingly

---

### Scenario 4: Deleted Task Number Reuse

**Solution:** Always use MAX (including deleted tasks)

- Deleted tasks remain in "Deleted Tasks" section
- MAX algorithm considers all task numbers (including deleted)
- Prevents reuse of deleted task numbers

**Example:**
- Main: Tasks `#1-50` exist, `#25` is deleted (moved to Deleted section)
- New branch: Pulls, sees highest is `#50` (includes deleted `#25` in count)
- Next task: `#51` (not `#25`)
- Result: No ambiguity about which task `#25` refers to

---

### Scenario 5: Concurrent Updates to TODO.md

**Solution:** Git pull before assignment + Git handles merge conflicts

- Each user pulls before making changes
- Git handles merge conflicts naturally
- If conflict occurs, resolve and retry assignment

**Example:**
- Both users on same branch, both pull before adding tasks
- User A commits first → User B's next pull will see User A's task
- User B's assignment will use MAX and avoid conflicts

---

### Scenario 6: Cross-Reference Conflicts in Commit Messages

**Solution:** Accept that commit messages may reference old numbers

- Commit messages are immutable (cannot be changed after commit)
- Task numbers in commit messages are historical references
- Accept that `task#50` in commit message may not match current task `#50`
- Provide tool to update task references if needed (future enhancement)

**Mitigation:**
- Keep commit messages accurate at time of commit
- Use git blame/log to trace task history
- Accept minor inaccuracies as trade-off for simplicity

---

### Scenario 7: Pull Request Reviews with Task Conflicts

**Solution:** Git pull before PR creation

- PRs should be created after pulling latest main
- MAX algorithm ensures PR tasks don't conflict with main
- PR reviewers see sequential numbers without conflicts

**Example:**
- Before creating PR: Pull latest main
- MAX ensures PR tasks start after main's highest task
- Reviewers see clean, conflict-free task numbering

---

### Scenario 8: Distributed Development

**Solution:** Git pull + MAX algorithm handles time zone differences

- Each team pulls before creating tasks
- MAX algorithm coordinates across time zones
- No manual coordination needed

**Example:**
- US team: Pulls (sees `#50`), adds `#51-55`, commits
- EU team: Pulls (sees `#55`), adds `#56-60`, commits
- No conflicts, no coordination overhead

---

## Implementation Components

### 1. Enhanced `add_todo()` Function

**Changes:**
- Add git pull before task assignment
- Use MAX algorithm to calculate next task number
- Update `.todo.ai/.todo.ai.serial` immediately
- Commit immediately after assignment

**Pseudo-code:**
```bash
add_todo() {
    # Step 1: Pull latest changes from main (for coordination)
    git_pull_todo_files
    
    # Step 2: Calculate next safe task number (using MAX of local and main)
    local next_id=$(calculate_next_task_number)
    
    # Step 3: Create task with safe number
    local task_line="- [ ] **#$next_id** $text $tags"
    add_task_to_file "$task_line"
    
    # Step 4: Update serial file (on current branch)
    echo $((next_id + 1)) > "$SERIAL_FILE"
    
    # Step 5: Commit immediately to current branch
    git commit -m "task: Add task #$next_id $text" -- TODO.md "$SERIAL_FILE"
    
    # Step 6: Push to current branch (make visible to others)
    git push origin $(git branch --show-current) --quiet 2>/dev/null || {
        log_todo_action "WARNING" "PUSH_FAILED" "Could not push, commit is local only"
    }
    
    # Step 7: Log action
    log_todo_action "ADD" "$next_id" "$text"
    
    echo "Added: #$next_id $text"
}
```

---

### 2. Enhanced `add_subtask()` Function

**Changes:**
- Pull before subtask assignment
- Derive parent task number first (via MAX if needed)
- Calculate subtask number based on parent's existing subtasks
- Commit immediately

**Pseudo-code:**
```bash
add_subtask() {
    local parent_id="$1"
    local text="$2"
    local tags="$3"
    
    # Step 1: Pull latest changes
    git_pull_todo_files
    
    # Step 2: Verify parent exists (may have been renumbered)
    parent_id=$(verify_parent_task "$parent_id")
    
    # Step 3: Calculate next subtask number
    local next_subtask=$(calculate_next_subtask_number "$parent_id")
    
    # Step 4: Create subtask
    local subtask_line="  - [ ] **#$parent_id.$next_subtask** $text $tags"
    add_subtask_to_parent "$parent_id" "$subtask_line"
    
    # Step 5: Commit immediately
    git commit -m "task: Add subtask #$parent_id.$next_subtask $text" -- TODO.md
    
    log_todo_action "ADD_SUBTASK" "$parent_id.$next_subtask" "$text"
    
    echo "Added subtask: #$parent_id.$next_subtask $text"
}
```

---

### 3. Git Pull Helper Function

**Purpose:** Centralize git pull logic for TODO files. **Coordinates with main AND current branch's remote** for safe numbering.

**Implementation:**
```bash
git_pull_todo_files() {
    # Fetch from main branch (authoritative source for merged tasks)
    git fetch origin main --quiet 2>/dev/null || {
        log_todo_action "WARNING" "GIT_FETCH_FAILED" "Could not fetch from main, using local state"
        # Continue anyway - will use local state only
    }
    
    # Get main's TODO.md and serial file for comparison
    git show origin/main:TODO.md > "$TODO_FILE.tmp.main" 2>/dev/null || true
    git show origin/main:.todo.ai/.todo.ai.serial > "$SERIAL_FILE.tmp.main" 2>/dev/null || true
    
    # If on a feature branch, also fetch from current branch's remote
    # This ensures we see unmerged tasks already pushed to this branch
    local current_branch=$(git branch --show-current 2>/dev/null || echo "")
    if [[ -n "$current_branch" ]] && [[ "$current_branch" != "main" ]]; then
        # Fetch from current branch's remote
        git fetch origin "$current_branch" --quiet 2>/dev/null || {
            log_todo_action "WARNING" "GIT_FETCH_BRANCH_FAILED" "Could not fetch from origin/$current_branch, using main and local state"
            # Continue anyway - will use main and local state
        }
        
        # Get current branch's remote TODO.md and serial file
        git show "origin/$current_branch:TODO.md" > "$TODO_FILE.tmp.branch" 2>/dev/null || true
        git show "origin/$current_branch:.todo.ai/.todo.ai.serial" > "$SERIAL_FILE.tmp.branch" 2>/dev/null || true
    fi
    
    # Temp files are now available for MAX algorithm in calculate_next_task_number()
    # They will be cleaned up after use
    
    return 0
}
```

**Why Coordinate with Main AND Current Branch:**
- **Main is authoritative**: Contains all merged tasks (definitive sequence)
- **Current branch remote**: Contains unmerged tasks already pushed to this branch
- **Prevents local conflicts**: If we already pushed #50 to Branch A remote, next add on Branch A should see it and use #51
- **Cross-branch coordination**: We can't see other feature branches' unmerged tasks (acceptable - resolved at merge time)

**Limitations and Trade-offs:**
- **Cross-branch conflicts possible**: Branch A and Branch B may both calculate #50 if they fetch at the same time
- **Acceptable**: Conflicts are resolved at merge time via Git's merge conflict resolution
- **Alternative**: Could fetch ALL remote branches (expensive, complex)
- **Chosen approach**: Coordinate with main + current branch (good balance of simplicity and effectiveness)

**Error Handling:**
- If main fetch fails: Continue with local and current branch state only
- If current branch fetch fails: Continue with main and local state only
- If both fail: Continue with local state only (worst case - conflicts possible)
- Log warnings but don't block user
- Better to have slightly outdated state than to block entirely

---

### 4. Conflict Detection and Resolution

**Purpose:** Detect and resolve conflicts when they occur.

**Conflict Detection:**
- Git merge conflicts in `TODO.md` or `.todo.ai/.todo.ai.serial`
- Duplicate task numbers detected during assignment
- Subtask numbering conflicts

**Resolution Strategy:**
1. **Automatic Resolution:**
   - Renumber conflicting tasks to next available numbers
   - Update all references (subtasks, relationships)
   - Commit resolution

2. **Manual Resolution:**
   - If automatic resolution fails, prompt user
   - Provide tools to view and resolve conflicts
   - User can choose resolution strategy

**Implementation:**
```bash
resolve_conflicts() {
    local conflict_file="$1"
    
    # Check for merge conflict markers
    if grep -q "^<<<<<<< " "$conflict_file"; then
        # Merge conflict detected
        echo "⚠️  Merge conflict detected in $conflict_file"
        
        # Try automatic resolution
        if auto_resolve_conflicts "$conflict_file"; then
            echo "✅ Conflicts resolved automatically"
            return 0
        else
            echo "❌ Automatic resolution failed"
            echo "Please resolve conflicts manually: $conflict_file"
            return 1
        fi
    fi
    
    return 0
}

auto_resolve_conflicts() {
    local file="$1"
    
    # Strategy: Take both sets of tasks, renumber conflicting ones
    # Keep highest numbers, renumber duplicates to next available
    
    # Extract all task numbers from both sides of conflict
    local local_tasks=$(extract_task_numbers "$file" "local")
    local remote_tasks=$(extract_task_numbers "$file" "remote")
    
    # Find duplicates
    local duplicates=$(find_duplicate_numbers "$local_tasks" "$remote_tasks")
    
    # Renumber duplicates (use remote's numbering as base, renumber local)
    renumber_conflicting_tasks "$file" "$duplicates"
    
    # Remove conflict markers
    remove_conflict_markers "$file"
    
    return 0
}
```

---

## Workflow Integration

### Current Workflow (Single User)

```
1. User runs: ./todo.ai add "Task description"
2. Script finds highest task number
3. Assigns next number
4. Adds to TODO.md
5. Updates serial file
6. Logs action
7. Done
```

### New Workflow (Multi-User)

```
1. User runs: ./todo.ai add "Task description"
2. Script fetches from origin/main (sync with authoritative source)
3. Script calculates: MAX(local, main) + 1
4. Assigns safe task number
5. Adds to TODO.md
6. Updates serial file (on current branch)
7. Commits to current branch (atomic assignment)
8. Pushes to current branch (make visible to others)
9. Logs action
10. Done
```

**Branch-Specific Behavior:**

**If on main branch:**
```
1. Fetch from origin/main
2. Calculate MAX(local main, remote main) + 1
3. Assign task number
4. Commit to main
5. Push to origin/main
```

**If on feature branch:**
```
1. Fetch from origin/main (for merged tasks)
2. Fetch from origin/feature-branch (for unmerged tasks on this branch)
3. Calculate MAX(local, main, feature-branch remote) + 1
4. Assign task number
5. Commit to feature branch
6. Push to origin/feature-branch (make visible for next operation on this branch)
7. When merging to main: Merge serial file state with main (conflicts resolved if any)
```

**Example:**
- Main: `#49`
- Branch A local: `#49`
- Branch A remote (already pushed): `#50`
- Fetch from main (sees `#49`), fetch from origin/Branch A (sees `#50`)
- Calculate MAX(49, 49, 50) + 1 = `#51`
- Assign `#51`, commit, push → Branch A remote now has `#50-51`
- Next add on Branch A will fetch and see `#51`, calculate `#52`

---

## Configuration Options

### Enable/Disable Git Coordination

**Option:** Allow users to disable git pull if needed.

**Use Cases:**
- Working offline
- No Git repository
- Testing/development mode

**Implementation:**
```bash
# Configuration variable
GIT_COORDINATION_ENABLED="${GIT_COORDINATION_ENABLED:-true}"

# In add_todo():
if [[ "$GIT_COORDINATION_ENABLED" == "true" ]] && git rev-parse --git-dir >/dev/null 2>&1; then
    git_pull_todo_files
fi
```

---

### Silent vs. Verbose Mode

**Option:** Control output from git pull operations.

**Silent Mode (default):**
- No output if pull succeeds
- Only show errors or warnings
- Better for AI agents

**Verbose Mode:**
- Show pull status
- Show what changed
- Better for human debugging

---

## Error Handling

### Network Failures

**Scenario:** Git pull fails due to network issues.

**Handling:**
- Continue with local state
- Log warning
- Don't block user
- User can retry later

### Authentication Failures

**Scenario:** Git pull fails due to authentication.

**Handling:**
- Continue with local state
- Log error message
- Suggest user configure Git credentials
- Don't block user

### Merge Conflicts

**Scenario:** Git pull results in merge conflict.

**Handling:**
- Detect conflict markers
- Try automatic resolution
- If automatic fails, prompt user
- Provide tools for manual resolution

### Git Not Available

**Scenario:** Git is not installed or not in PATH.

**Handling:**
- Disable git coordination automatically
- Continue with local-only numbering
- Log warning that conflicts may occur
- Suggest installing Git for multi-user support

---

## Benefits of This Architecture

1. **Preserves Sequential Numbering:**
   - Maintains todo.ai's core strength
   - Simple, human-readable task numbers
   - No complex prefixes or UUIDs

2. **Minimal Changes to Existing Workflow:**
   - Git pull is transparent to user
   - Commits happen automatically
   - No new commands needed

3. **Uses Existing Infrastructure:**
   - Leverages Git already in place
   - No new servers or services needed
   - Works with existing Git workflow

4. **Prevents Most Conflicts:**
   - MAX algorithm ensures no overlaps
   - Immediate commit minimizes window
   - Handles edge cases gracefully

5. **AI-Agent Friendly:**
   - All operations are automatic
   - No interactive prompts required
   - Works seamlessly in automated workflows

---

## Limitations and Trade-offs

### Critical Limitation: Single Repository Scope

**This design only works within a single Git repository, not across forks or unreachable branches.**

**What works:**
- ✅ Multiple branches in the same repository
- ✅ Multiple developers working on the same repository
- ✅ Coordination via main branch and current branch remote

**What does NOT work:**
- ❌ **Multiple forks of the same repository** (cannot coordinate task numbers across forks)
- ❌ **Multiple remote repositories** (cannot see task numbers in other remotes)
- ❌ **Completely independent branches** (cannot coordinate if branches never merge)
- ❌ **Cross-fork collaboration** (each fork would have its own task numbering sequence)

**Why this limitation exists:**
- Git-based coordination requires access to all branches/remotes being coordinated
- Forks are separate repositories with separate Git histories
- We cannot fetch or query branches from forks we don't have access to
- Even if we could, fetching ALL remote branches from ALL forks would be:
  - Expensive (network overhead)
  - Complex (managing multiple remotes)
  - Incomplete (still can't see private forks)

**Impact:**
- Each fork maintains its own independent task numbering sequence
- Task numbers may overlap between forks (e.g., Fork A has `#50`, Fork B also has `#50`)
- When merging forks via pull requests, conflicts are resolved at merge time
- This is **acceptable** for the use case: single-repo, multi-user collaboration

**Alternative Approaches (Not Implemented):**
1. **External coordination service**: Use a shared API/service for task number assignment
2. **UUID-based numbering**: Use UUIDs instead of sequential numbers (breaks simplicity)
3. **Namespace-based numbering**: Prefix task numbers with branch/fork identifier (e.g., `feature-auth#50`)
4. **Server-side assignment**: Require a central server for all task management (not distributed)

**Chosen Approach Rationale:**
- Git-based coordination works for the primary use case: single repository, multiple branches
- Accepts limitation that it doesn't work across forks
- Simplicity and effectiveness for the intended scope
- Conflicts resolved at merge time (Git's native capability)

### Other Limitations

1. **Requires Git:**
   - Not applicable to non-Git repositories
   - Requires network access for coordination
   - Fails gracefully if Git unavailable

2. **Small Conflict Window:**
   - Rare conflicts still possible (even within single repo)
   - Requires conflict resolution mechanism
   - May need manual intervention in edge cases

3. **Commit Message Accuracy:**
   - Commit messages may reference old numbers
   - Historical references may become inaccurate
   - Trade-off for simplicity

4. **Offline Limitations:**
   - Works best with network access
   - Offline mode uses local-only numbering
   - Conflicts may occur when coming back online

---

## Migration Path

### Phase 1: Add Git Pull to add_todo()
- Add git pull before task assignment
- Use MAX algorithm for numbering
- Immediate commit after assignment
- Test with parallel branches

### Phase 2: Add Conflict Detection
- Detect merge conflicts
- Implement auto-resolution
- Test conflict scenarios

### Phase 3: Add Conflict Resolution Tools
- Manual resolution helpers
- Task renumbering tools
- Reference update tools

### Phase 4: Enhance Subtask Support
- Apply same logic to subtasks
- Handle parent task conflicts
- Renumber subtasks with parents

### Phase 5: Testing and Refinement
- Test all conflict scenarios
- Refine edge case handling
- Optimize performance

---

## Testing Strategy

### Unit Tests
- Test MAX algorithm with various scenarios
- Test conflict detection logic
- Test conflict resolution algorithms

### Integration Tests
- Test git pull integration
- Test commit flow
- Test error handling

### Multi-User Tests
- Simulate parallel branch development
- Test sequential merges
- Test distributed development scenarios
- Test all 8 conflict scenarios

---

## Success Metrics

1. **Conflict Reduction:**
   - Target: 95%+ reduction in numbering conflicts
   - Measure: Before vs. after implementation

2. **User Experience:**
   - No additional user steps required
   - Transparent git coordination
   - Seamless workflow integration

3. **Performance:**
   - Git pull adds < 1 second overhead
   - Immediate commit adds < 500ms overhead
   - Total overhead: < 2 seconds per task

---

## Conclusion

The **Git-Based Atomic Assignment** architecture provides a robust solution for multi-user conflict-free task numbering while preserving todo.ai's core strengths:

- ✅ Simple sequential numbering maintained
- ✅ Minimal changes to existing workflow
- ✅ Uses existing Git infrastructure
- ✅ Prevents most conflicts automatically
- ✅ Handles edge cases gracefully
- ✅ AI-agent friendly

This architecture balances simplicity with effectiveness, making it the ideal solution for todo.ai's multi-user support system.

---

## Next Steps

1. **Task #52.5:** Design distributed task numbering scheme details
   - Refine MAX algorithm implementation
   - Design subtask numbering strategy
   - Design serial file synchronization

2. **Task #52.4:** Design branch/PR task merging strategy
   - Design merge-time conflict resolution
   - Design PR review integration
   - Design branch coordination

3. **Task #52.6:** Design task resolution mechanism
   - Design automatic conflict resolution
   - Design manual resolution tools
   - Design reference update mechanisms

