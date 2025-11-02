# Design: Multi-User Conflict-Free Task Numbering Architecture

## Overview

This document proposes the solution architecture for conflict-free task numbering in a multi-user, multi-branch, and pull request environment for `todo.ai`.

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
1. Git Pull (get latest state)
    ↓
2. Calculate MAX(local, remote) + 1
    ↓
3. Assign task number
    ↓
4. Commit immediately
    ↓
5. Done (minimal conflict window)
```

---

## Detailed Architecture

### 1. Git Pull Before Assignment (Coordination Step)

**Purpose:** Synchronize with remote state before assigning task numbers.

**Implementation:**
- Perform `git pull` (or equivalent) before assigning new task numbers
- Target only `TODO.md` and `.todo.ai/.todo.ai.serial` files
- Handle pull failures gracefully (network issues, authentication, etc.)

**When to Pull:**
- Before `add` command (new tasks)
- Before `add-subtask` command (new subtasks)
- Before any operation that creates a new task number

**Pull Strategy:**
```bash
# Silent pull (no output if no changes)
git pull --quiet origin <branch> -- TODO.md .todo.ai/.todo.ai.serial 2>/dev/null || true

# If pull fails, continue with local state (better than blocking)
# User can retry or resolve manually
```

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
    local remote_file="${TODO_FILE}.remote"  # From git pull
    
    local local_max=$(get_highest_task_number "$local_file")
    local remote_max=0
    
    if [[ -f "$remote_file" ]]; then
        remote_max=$(get_highest_task_number "$remote_file")
    fi
    
    # Take maximum and add 1
    local next_id
    if [[ $local_max -gt $remote_max ]]; then
        next_id=$((local_max + 1))
    else
        next_id=$((remote_max + 1))
    fi
    
    echo $next_id
}
```

**Edge Cases:**
- If remote pull fails: Use local maximum + 1
- If both files are empty: Start at `#1`
- If one file is missing: Use available file's maximum

---

### 3. Immediate Commit After Assignment

**Purpose:** Minimize the conflict window by committing the task assignment immediately.

**Implementation:**
- After assigning task number and adding to `TODO.md`
- Update `.todo.ai/.todo.ai.serial` immediately
- Commit both files in a single atomic commit
- Do not wait for other operations

**Commit Message Format:**
```bash
git commit -m "task: Add task #$task_id $task_description" -- TODO.md .todo.ai/.todo.ai.serial
```

**Why Immediate:**
- Reduces time between pull and commit (smaller conflict window)
- Makes the assignment "visible" to other users quickly
- Follows atomic assignment pattern

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
- Branch A pulls, calculates MAX(49, 49) + 1 = `#50`
- Branch B pulls, calculates MAX(49, 49) + 1 = `#50`
- If Branch A commits first, Branch B's pull will see `#50` and calculate `#51`
- Result: No duplicate numbers

---

### Scenario 2: Sequential Merges with Overlapping Ranges

**Solution:** Continuous synchronization via git pull

- Each merge updates main's task numbers
- Subsequent branches pull latest main before creating tasks
- MAX algorithm ensures new numbers are always higher

**Example:**
- Main: `#45`
- Branch A: Pulls (sees `#45`), adds `#46`, `#47`, commits, merges → Main now has `#47`
- Branch B: Pulls (sees `#47`), adds `#48`, `#49`, commits, merges → No conflicts

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
    # Step 1: Pull latest changes
    git_pull_todo_files
    
    # Step 2: Calculate next safe task number
    local next_id=$(calculate_next_task_number)
    
    # Step 3: Create task with safe number
    local task_line="- [ ] **#$next_id** $text $tags"
    add_task_to_file "$task_line"
    
    # Step 4: Update serial file
    echo $((next_id + 1)) > "$SERIAL_FILE"
    
    # Step 5: Commit immediately
    git commit -m "task: Add task #$next_id $text" -- TODO.md "$SERIAL_FILE"
    
    # Step 6: Log action
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

**Purpose:** Centralize git pull logic for TODO files.

**Implementation:**
```bash
git_pull_todo_files() {
    # Get current branch
    local current_branch=$(git branch --show-current 2>/dev/null || echo "main")
    
    # Pull only TODO-related files (silent, no output if no changes)
    git pull --quiet origin "$current_branch" -- TODO.md .todo.ai/.todo.ai.serial 2>/dev/null || {
        # If pull fails, log but don't block (better than blocking user)
        log_todo_action "WARNING" "GIT_PULL_FAILED" "Could not pull latest changes, using local state"
        return 1
    }
    
    return 0
}
```

**Error Handling:**
- If pull fails (network, auth, etc.), continue with local state
- Log warning but don't block user
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
2. Script performs: git pull (sync with remote)
3. Script calculates: MAX(local, remote) + 1
4. Assigns safe task number
5. Adds to TODO.md
6. Updates serial file
7. Commits immediately (atomic assignment)
8. Logs action
9. Done
```

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

1. **Requires Git:**
   - Not applicable to non-Git repositories
   - Requires network access for coordination
   - Fails gracefully if Git unavailable

2. **Small Conflict Window:**
   - Rare conflicts still possible
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

