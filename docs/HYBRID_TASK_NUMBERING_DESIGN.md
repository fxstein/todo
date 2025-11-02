# Hybrid Task Numbering System Design

## Overview

> **Related Documentation:** See [Usage Patterns](USAGE_PATTERNS.md) for practical examples of how to use these numbering modes in different development scenarios.

This document designs a hybrid task numbering system for `todo.ai` that supports multiple modes of operation, from simple single-user sequential numbering to sophisticated multi-user coordination with conflict resolution.

**Key Philosophy:**
- Task IDs are **temporary constructs** used during development sessions, branches, or PRs
- Task IDs are **not permanent forever numbers** - they can be reused and changed over time
- Multiple modes provide flexibility for different collaboration scenarios
- Graceful fallbacks ensure the tool always works, even when coordination fails

---

## Design Principles

1. **Progressive Enhancement:** Start simple (single-user), add complexity as needed (multi-user)
2. **Configurable Modes:** Repository owner configures the mode for their needs
3. **Backward Compatible:** Single-user mode remains the default and works as-is
4. **Graceful Degradation:** Fallback to simpler modes if coordination fails
5. **Conflict Resolution:** Automatic detection and resolution of numbering conflicts
6. **User Experience:** Users reference tasks by simple numbers; tool handles prefixes automatically

---

## Mode Overview

### Mode 1: Single-User (Default)
- **Current behavior:** Simple sequential numbering (#1, #2, #3, ...)
- **Use case:** Single developer, single repository
- **No coordination needed**

### Mode 2: Simple Multi-User (Prefix with GitHub User ID)
- **Format:** `{userid-prefix}-{number}` (e.g., `fxstein-50`)
- **Use case:** Multiple developers, same repository
- **Coordination:** Minimal - each user has their own number sequence
- **Example:** User `fxstein` gets `fxstein-50`, user `alice` gets `alice-50`

### Mode 3: Branch Mode (Prefix with Branch Name)
- **Format:** `{branch-prefix}-{number}` (e.g., `feature-50`)
- **Use case:** Feature branch development, branch-specific task numbering
- **Coordination:** Minimal - each branch has its own number sequence
- **Example:** Branch `feature-auth` gets `feature-50`, branch `fix-api` gets `fix-api-50`

### Mode 4: Enhanced Multi-User (GitHub Issues or CounterAPI)
- **Format:** `{userid-prefix}-{number}` or simple `{number}` (depending on coordination)
- **Use case:** Teams needing true atomic coordination
- **Coordination:** GitHub Issues API or CounterAPI for atomic assignment
- **Fallback:** Automatically falls back to Mode 2 if coordination unavailable

---

## Configuration System

### Configuration File: `.todo.ai/config.yaml`

**Location:** `.todo.ai/config.yaml` (committed to repository)

**Format:** YAML specification

**Structure:**
```yaml
# todo.ai Configuration File
# This file configures the task numbering system for this repository

# Mode: single-user | multi-user | branch | enhanced
mode: multi-user

# Coordination settings (for enhanced mode)
coordination:
  # Type: github-issues | counterapi | firebase | none
  type: github-issues
  
  # GitHub Issues coordination
  issue_number: 123  # Issue number for task number coordination
  
  # CounterAPI coordination
  namespace: todo-ai-repo-name  # Namespace for counter
  
  # Fallback mode if coordination fails
  fallback: multi-user

# Conflict resolution settings
conflict_resolution:
  enabled: true
  auto_resolve: true
  renumber_on_conflict: true
  notify_on_conflict: false

# Display settings
display:
  show_prefix: false  # Show prefix in output (users can still use numbers)
  user_reference_style: number-only  # number-only | full-id
```

**Configuration Setup:**
- Repository owner/initial user creates `.todo.ai/config.yaml`
- Tool reads config on startup using YAML parser
- Config is committed to repository (shared across team)
- Tool validates config and falls back to defaults if invalid
- YAML format is human-readable and easy to edit

---

## Mode 1: Single-User (Default)

### Current Implementation
- Sequential numbering: `#1`, `#2`, `#3`, ...
- No coordination needed
- Works offline
- Fast and simple

### Behavior
- Read highest task number from `TODO.md`
- Increment by 1
- Assign to new task
- Update `.todo.ai/.todo.ai.serial`

### Configuration
```yaml
# .todo.ai/config.yaml
mode: single-user
```

**This is the default mode - no coordination needed.**

---

## Mode 2: Simple Multi-User (User ID Prefix)

### Format
- **Task ID:** `{first-7-chars-of-github-userid}-{number}`
- **Examples:**
  - User `fxstein` → `fxstein-50`
  - User `alice123` → `alice12-50`
  - User `bob` → `bob-50` (padded or full)

### Implementation

**1. Get GitHub User ID:**
```bash
get_github_user_id() {
    local user_id=$(gh api user --jq '.login' 2>/dev/null || echo "")
    if [[ -z "$user_id" ]]; then
        # Fallback to Git user.name or Git user.email
        user_id=$(git config user.name | tr '[:upper:]' '[:lower:]' | tr -cd '[:alnum:]')
    fi
    # Take first 7 characters
    echo "${user_id:0:7}"
}
```

**2. Assign Task Number:**
```bash
assign_task_number_multi_user() {
    local user_prefix=$(get_github_user_id)
    local todo_file="$TODO_FILE"
    
    # Find highest task number for this user prefix
    local highest=0
    local pattern="${user_prefix}-([0-9]+)"
    
    while IFS= read -r line; do
        if [[ "$line" =~ $pattern ]]; then
            local num="${match[1]}"
            if [[ $num -gt $highest ]]; then
                highest=$num
            fi
        fi
    done < "$todo_file"
    
    local next_num=$((highest + 1))
    echo "${user_prefix}-${next_num}"
}
```

**3. User Interface:**
- **Display:** Users see `fxstein-50` in TODO.md
- **Reference:** Users can type `50` and tool auto-adds prefix `fxstein-`
- **Commands:** `./todo.ai show 50` → looks up `fxstein-50` for current user

**4. Task Reference Handling:**
```bash
# User types: ./todo.ai show 50
# Tool automatically: ./todo.ai show fxstein-50

resolve_task_id() {
    local input_id="$1"
    
    # If already has prefix, use as-is
    if [[ "$input_id" =~ ^[a-z0-9]{1,7}-[0-9]+$ ]]; then
        echo "$input_id"
        return 0
    fi
    
    # If just a number, add current user's prefix
    if [[ "$input_id" =~ ^[0-9]+$ ]]; then
        local user_prefix=$(get_github_user_id)
        echo "${user_prefix}-${input_id}"
        return 0
    fi
    
    # Invalid format
    return 1
}
```

### Configuration
```yaml
# .todo.ai/config.yaml
mode: multi-user
coordination:
  type: none
```

### Benefits
- ✅ **No conflicts:** Each user has their own number sequence
- ✅ **No coordination needed:** Works offline, no API calls
- ✅ **Simple:** Minimal implementation complexity
- ✅ **Works for forks:** No write access needed
- ✅ **Scalable:** Unlimited users, each with their own sequence

### Limitations
- ⚠️ **No global sequential numbering:** Users have independent sequences
- ⚠️ **Prefix visible:** Task IDs include user prefix (e.g., `fxstein-50`)
- ⚠️ **Cross-user references:** Must use full ID (e.g., `alice-50`) when referencing other users' tasks

---

## Mode 3: Branch Mode

### Format
- **Task ID:** `{first-7-chars-of-branch-name}-{number}`
- **Examples:**
  - Branch `feature-auth` → `feature-50`
  - Branch `fix-api-bug` → `fix-api-50`
  - Branch `main` → `main-50`

### Implementation

**1. Get Branch Name:**
```bash
get_branch_name() {
    local branch=$(git branch --show-current 2>/dev/null || echo "")
    if [[ -z "$branch" ]]; then
        branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
    fi
    # Take first 7 characters, sanitize
    echo "${branch:0:7}" | tr '[:upper:]' '[:lower:]' | tr -cd '[:alnum:]-'
}
```

**2. Assign Task Number:**
- Similar to Mode 2, but uses branch prefix instead of user prefix
- Each branch maintains its own number sequence

### Configuration
```yaml
# .todo.ai/config.yaml
mode: branch
coordination:
  type: none
```

### Benefits
- ✅ **Branch-specific numbering:** Each branch has independent task sequence
- ✅ **No conflicts between branches:** Branch prefixes prevent collisions
- ✅ **Works for forks:** No write access needed
- ✅ **Clear branch association:** Task IDs show which branch they belong to

### Limitations
- ⚠️ **Branch-specific:** Tasks renumbered if moved to different branch
- ⚠️ **Merge complexity:** May have duplicate numbers across branches after merge

---

## Mode 4: Enhanced Multi-User (GitHub Issues or CounterAPI)

### Format
- **Task ID:** `{userid-prefix}-{coordinated-number}` (if user prefix enabled)
- **Or:** `{coordinated-number}` (if global coordination)
- Coordination ensures globally unique sequential numbers

### Implementation

**Approach A: GitHub Issues API**

**1. Setup:**
- Repository owner creates coordination issue (e.g., "Task Number Coordination")
- Config stores issue number: `COORDINATION_ISSUE=123`

**2. Atomic Assignment:**
```bash
assign_task_number_enhanced_issues() {
    local config_file=".todo.ai/config"
    local issue_num=$(grep "COORDINATION_ISSUE=" "$config_file" | cut -d'=' -f2)
    local user_prefix=$(get_github_user_id)
    
    # Get latest comment from coordination issue
    local latest_comment=$(gh api repos/:owner/:repo/issues/$issue_num/comments \
        --jq '.[0].body' 2>/dev/null || echo "")
    
    # Extract current number
    local current_num=$(echo "$latest_comment" | grep -oP '\d+' | head -n1 || echo "0")
    
    # Increment
    local new_num=$((current_num + 1))
    
    # Post new comment atomically
    gh api -X POST repos/:owner/:repo/issues/$issue_num/comments \
        --field "body=Next task number: $new_num" 2>/dev/null || {
        # Fallback to multi-user mode
        return 1
    }
    
    # Return formatted ID
    if [[ -n "$user_prefix" ]]; then
        echo "${user_prefix}-${new_num}"
    else
        echo "$new_num"
    fi
}
```

**3. Retry Logic:**
- If comment creation fails, check if latest comment changed
- Retry with new number if concurrent update detected
- Fallback to Mode 2 after max retries

**Approach B: CounterAPI**

**1. Setup:**
- Repository owner creates namespace: `todo-ai-repo-name`
- Config stores namespace: `COORDINATION_NAMESPACE=todo-ai-repo-name`

**2. Atomic Assignment:**
```bash
assign_task_number_enhanced_counterapi() {
    local config_file=".todo.ai/config"
    local namespace=$(grep "COORDINATION_NAMESPACE=" "$config_file" | cut -d'=' -f2)
    local counter_name="task-counter"
    local user_prefix=$(get_github_user_id)
    
    # Increment atomically via CounterAPI
    local response=$(curl -s -X POST \
        "https://api.counterapi.dev/v1/${namespace}/${counter_name}/up" || echo "")
    
    if [[ -z "$response" ]] || ! echo "$response" | jq -e '.value' >/dev/null 2>&1; then
        # Fallback to multi-user mode
        return 1
    fi
    
    local new_num=$(echo "$response" | jq -r '.value')
    
    # Return formatted ID
    if [[ -n "$user_prefix" ]]; then
        echo "${user_prefix}-${new_num}"
    else
        echo "$new_num"
    fi
}
```

**3. Fallback Handling:**
- If CounterAPI unavailable (network, service down), fallback to Mode 2
- Log warning but continue working
- Periodic retry to restore coordination

### Configuration

**GitHub Issues:**
```json
{
  "mode": "enhanced",
  "coordination": {
    "type": "github-issues",
    "issue_number": 123,
    "fallback": "multi-user"
  }
}
```

**CounterAPI:**
```json
{
  "mode": "enhanced",
  "coordination": {
    "type": "counterapi",
    "namespace": "todo-ai-repo-name",
    "fallback": "multi-user"
  }
}
```

### Benefits
- ✅ **True atomic coordination:** Prevents conflicts even with concurrent access
- ✅ **Global sequential numbering:** Single sequence across all users
- ✅ **Graceful fallback:** Automatically falls back if coordination fails
- ✅ **Works for forks:** GitHub Issues works with forks, CounterAPI works anywhere

### Limitations
- ⚠️ **Requires coordination service:** GitHub Issues or CounterAPI must be available
- ⚠️ **Network dependency:** Cannot work fully offline
- ⚠️ **Setup required:** Repository owner must configure coordination

---

## Conflict Resolution System

### Purpose
Automatically detect and resolve numbering conflicts that may occur despite coordination.

### Detection

**1. Conflict Detection:**
```bash
detect_conflicts() {
    local todo_file="$TODO_FILE"
    local conflicts=()
    
    # Extract all task IDs
    local task_ids=$(grep -oE '#[a-z0-9]{1,7}-[0-9]+' "$todo_file" | sed 's/#//')
    
    # Find duplicates
    local sorted_ids=$(echo "$task_ids" | sort)
    local prev_id=""
    for id in $sorted_ids; do
        if [[ "$id" == "$prev_id" ]]; then
            conflicts+=("$id")
        fi
        prev_id="$id"
    done
    
    echo "${conflicts[@]}"
}
```

**2. Conflict Types:**
- **Duplicate IDs:** Same task ID appears multiple times
- **Overlapping numbers:** Different users have same number (only in global mode)
- **Orphaned references:** Subtask references non-existent parent

### Resolution

**1. Automatic Renumbering:**
```bash
resolve_conflicts() {
    local todo_file="$TODO_FILE"
    local mode=$(get_config_mode)
    
    case "$mode" in
        "multi-user"|"enhanced")
            resolve_multi_user_conflicts "$todo_file"
            ;;
        "branch")
            resolve_branch_conflicts "$todo_file"
            ;;
        "single-user")
            resolve_single_user_conflicts "$todo_file"
            ;;
    esac
}
```

**2. Renumbering Strategy:**
- **Keep first occurrence:** First task with ID keeps it
- **Renumber duplicates:** Subsequent duplicates get next available number
- **Update references:** Update all subtask references to new IDs
- **Log changes:** Record renumbering in log file

**3. Implementation Example:**
```bash
resolve_multi_user_conflicts() {
    local todo_file="$1"
    local temp_file=$(mktemp)
    local seen_ids=()
    local next_numbers=()  # Per user prefix
    
    while IFS= read -r line; do
        if [[ "$line" =~ ^-.*\*\#([a-z0-9]{1,7}-[0-9]+)\*\ ]]; then
            local task_id="${match[1]}"
            local prefix="${task_id%-*}"
            local num="${task_id##*-}"
            
            # Check if already seen
            if [[ " ${seen_ids[*]} " =~ " ${task_id} " ]]; then
                # Duplicate - get next number for this prefix
                local next_num=$(get_next_number_for_prefix "$prefix" "$next_numbers")
                local new_id="${prefix}-${next_num}"
                
                # Update task ID in line
                line=$(echo "$line" | sed "s/#${task_id}/#${new_id}/")
                task_id="$new_id"
                
                # Update references
                update_subtask_references "$task_id" "$new_id" "$todo_file"
            fi
            
            seen_ids+=("$task_id")
            update_next_number_for_prefix "$prefix" "$num" "$next_numbers"
        fi
        
        echo "$line" >> "$temp_file"
    done < "$todo_file"
    
    mv "$temp_file" "$todo_file"
}
```

**4. Manual Resolution:**
- If automatic resolution fails or conflicts are complex:
- Prompt user for resolution strategy
- Provide interactive resolution tool
- Preview changes before applying

### Configuration
```yaml
# .todo.ai/config.yaml
conflict_resolution:
  enabled: true
  auto_resolve: true
  renumber_on_conflict: true
  notify_on_conflict: false
```

---

## Configuration File Design

### Location
`.todo.ai/config` (committed to repository)

### Format Options

**Option 1: JSON (Recommended)**
```json
{
  "mode": "multi-user",
  "coordination": {
    "type": "github-issues",
    "issue_number": 123,
    "fallback": "multi-user"
  },
  "conflict_resolution": {
    "enabled": true,
    "auto_resolve": true
  },
  "display": {
    "show_prefix": false,
    "user_reference_style": "number-only"
  }
}
```

**Option 2: Simple Key-Value**
```bash
# .todo.ai/config
# Task Numbering Configuration

MODE=multi-user
COORDINATION_TYPE=github-issues
COORDINATION_ISSUE=123
FALLBACK_MODE=multi-user

CONFLICT_RESOLUTION_ENABLED=true
CONFLICT_RESOLUTION_AUTO=true

DISPLAY_SHOW_PREFIX=false
DISPLAY_USER_REFERENCE_STYLE=number-only
```

### Configuration Functions

**1. Read Configuration:**
```bash
get_config_mode() {
    local config_file=".todo.ai/config"
    if [[ ! -f "$config_file" ]]; then
        echo "single-user"  # Default
        return 0
    fi
    
    # Try JSON first
    if command -v jq >/dev/null 2>&1; then
        local mode=$(jq -r '.mode' "$config_file" 2>/dev/null || echo "")
        if [[ -n "$mode" ]] && [[ "$mode" != "null" ]]; then
            echo "$mode"
            return 0
        fi
    fi
    
    # Fallback to key-value
    grep "^MODE=" "$config_file" 2>/dev/null | cut -d'=' -f2 || echo "single-user"
}
```

**2. Validate Configuration:**
```bash
validate_config() {
    local config_file=".todo.ai/config"
    local mode=$(get_config_mode)
    
    # Check mode is valid
    case "$mode" in
        "single-user"|"multi-user"|"branch"|"enhanced")
            ;;
        *)
            echo "ERROR: Invalid mode: $mode" >&2
            return 1
            ;;
    esac
    
    # Validate coordination settings if enhanced mode
    if [[ "$mode" == "enhanced" ]]; then
        local coord_type=$(get_config "coordination.type")
        case "$coord_type" in
            "github-issues")
                local issue_num=$(get_config "coordination.issue_number")
                if [[ -z "$issue_num" ]] || ! [[ "$issue_num" =~ ^[0-9]+$ ]]; then
                    echo "ERROR: Invalid or missing coordination.issue_number" >&2
                    return 1
                fi
                ;;
            "counterapi")
                local namespace=$(get_config "coordination.namespace")
                if [[ -z "$namespace" ]]; then
                    echo "ERROR: Missing coordination.namespace" >&2
                    return 1
                fi
                ;;
        esac
    fi
    
    return 0
}
```

**3. Setup Configuration:**
```bash
setup_config() {
    local mode="$1"
    local config_file=".todo.ai/config"
    
    # Create config directory if needed
    mkdir -p "$(dirname "$config_file")"
    
    case "$mode" in
        "single-user")
            echo '{"mode":"single-user"}' > "$config_file"
            ;;
        "multi-user")
            echo '{"mode":"multi-user","coordination":{"type":"none"}}' > "$config_file"
            ;;
        "branch")
            echo '{"mode":"branch","coordination":{"type":"none"}}' > "$config_file"
            ;;
        "enhanced")
            # Interactive setup
            setup_enhanced_config "$config_file"
            ;;
    esac
    
    echo "Configuration saved to $config_file"
    echo "Please commit this file to share with your team."
}
```

---

## User Interface & Experience

### Task Reference Handling

**1. Display Format:**
- **In TODO.md:** Show full ID with prefix (e.g., `fxstein-50`)
- **In commands:** User can type just number (e.g., `50`), tool auto-adds prefix
- **In output:** Show full ID, but emphasize number (e.g., "Task fxstein-50 (50)")

**2. Command Examples:**
```bash
# User types:
./todo.ai add "Implement feature"

# Tool assigns: fxstein-51
# TODO.md shows: - [ ] **#fxstein-51** Implement feature

# User references:
./todo.ai show 51          # Auto-resolves to fxstein-51
./todo.ai complete 51      # Auto-resolves to fxstein-51
./todo.ai show fxstein-51 # Explicit reference works too

# Cross-user references:
./todo.ai show alice-50    # Must use full ID for other users' tasks
```

**3. Reference Resolution:**
```bash
resolve_task_reference() {
    local input="$1"
    local current_user=$(get_github_user_id)
    
    # Already has prefix
    if [[ "$input" =~ ^[a-z0-9]{1,7}-[0-9]+$ ]]; then
        echo "$input"
        return 0
    fi
    
    # Just a number - add current user's prefix
    if [[ "$input" =~ ^[0-9]+$ ]]; then
        echo "${current_user}-${input}"
        return 0
    fi
    
    # Invalid
    echo "ERROR: Invalid task ID format: $input" >&2
    return 1
}
```

### Mode Selection UI

**1. Setup Command:**
```bash
./todo.ai setup-mode [single-user|multi-user|branch|enhanced]
```

**2. Interactive Setup:**
```bash
./todo.ai setup-mode enhanced
# Interactive prompts:
# - Coordination type? (github-issues|counterapi)
# - GitHub issue number? (for github-issues)
# - CounterAPI namespace? (for counterapi)
# - Fallback mode? (multi-user|branch)
```

**3. Mode Status:**
```bash
./todo.ai status
# Output:
# Current mode: multi-user
# Coordination: none
# User prefix: fxstein
# Conflict resolution: enabled
```

---

## Implementation Phases

### Phase 1: Configuration System
- [ ] Create `.todo.ai/config` file format
- [ ] Implement config reading/validation
- [ ] Add `setup-mode` command
- [ ] Add `status` command

### Phase 2: Simple Multi-User Mode
- [ ] Implement GitHub user ID detection
- [ ] Implement prefix-based numbering
- [ ] Implement task reference resolution
- [ ] Update `add_todo()` function
- [ ] Update task display/commands

### Phase 3: Branch Mode
- [ ] Implement branch name detection
- [ ] Implement branch prefix numbering
- [ ] Add branch mode to config

### Phase 4: Conflict Resolution
- [ ] Implement conflict detection
- [ ] Implement automatic renumbering
- [ ] Implement reference updating
- [ ] Add conflict resolution commands

### Phase 5: Enhanced Multi-User Mode
- [ ] Implement GitHub Issues API coordination
- [ ] Implement CounterAPI coordination
- [ ] Implement fallback logic
- [ ] Add retry mechanisms

### Phase 6: Testing & Refinement
- [ ] Test all modes
- [ ] Test conflict resolution
- [ ] Test fallback scenarios
- [ ] Refine user experience

---

## Migration Path

### From Current (Single-User) to Multi-User

**1. No Breaking Changes:**
- Single-user mode remains default
- Existing repositories continue working as-is
- Users opt-in to multi-user mode

**2. Migration Steps:**
```bash
# 1. Repository owner runs:
./todo.ai setup-mode multi-user

# 2. Config file created
# 3. Next task assignment uses new mode
# 4. Existing tasks keep old format (#1, #2, etc.)
# 5. New tasks use new format (fxstein-50, etc.)
```

**3. Mixed Mode Support:**
- Support both old format (`#50`) and new format (`fxstein-50`) during transition
- Gradually migrate old tasks if needed
- Or leave old tasks as-is (they still work)

---

## Benefits of This Design

1. **Flexibility:** Multiple modes for different scenarios
2. **Backward Compatible:** Single-user mode unchanged
3. **Graceful Degradation:** Falls back to simpler modes if coordination fails
4. **User-Friendly:** Users reference tasks by number; tool handles prefixes
5. **Conflict Resolution:** Automatic detection and fixing of numbering conflicts
6. **No Breaking Changes:** Existing repositories continue working

---

## Limitations & Trade-offs

1. **Prefix Visibility:** Multi-user modes show prefixes in TODO.md (can be hidden in display)
2. **Cross-User References:** Must use full ID for other users' tasks
3. **Coordination Dependency:** Enhanced mode requires external service
4. **Configuration Required:** Repository owner must configure mode
5. **Migration Complexity:** Moving between modes may require task renumbering

---

## Conclusion

This hybrid approach provides a flexible, scalable solution for task numbering that:
- ✅ Works for single developers (current mode)
- ✅ Works for teams without coordination (simple multi-user)
- ✅ Works for branch-based development (branch mode)
- ✅ Works for teams needing atomic coordination (enhanced mode)
- ✅ Handles conflicts gracefully (conflict resolution)
- ✅ Maintains backward compatibility (existing repos work)

The key innovation is treating task IDs as **temporary session IDs** rather than permanent identifiers, allowing flexibility and reuse while maintaining usability during development sessions.

---

## Next Steps

1. **Review design** with stakeholders
2. **Phase 1 implementation** - Configuration system
3. **Phase 2 implementation** - Simple multi-user mode
4. **Phase 3 implementation** - Branch mode
5. **Phase 4 implementation** - Conflict resolution
6. **Phase 5 implementation** - Enhanced multi-user mode
7. **Testing** - All modes and fallback scenarios
8. **Documentation** - User guide for each mode

