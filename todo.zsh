#!/bin/zsh
# todo - AI-Agent First TODO List Tracker
# 
# Copyright 2025 Oliver Ratzesberger
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# AI-agent first TODO list management tool
# Keep AI agents on track and help humans supervise their work

set -e

# Cross-platform sed in-place editing function
sed_inplace() {
    if [[ "$(uname)" == "Darwin" ]]; then
        sed -i '' "$@"
    else
        sed -i "$@"
    fi
}

# Configuration
# Can be overridden with environment variables
TODO_FILE="${TODO_FILE:-$(pwd)/TODO.md}"
SERIAL_FILE="${TODO_SERIAL:-$(pwd)/.todo/.todo_serial}"
LOG_FILE="${TODO_LOG:-$(pwd)/.todo/.todo.log}"

# Function to get next serial number
increment_serial() {
    if [[ -f "$SERIAL_FILE" ]]; then
        local current=$(cat "$SERIAL_FILE")
        local next=$((current + 1))
        echo "$next" > "$SERIAL_FILE"
        echo "$next"
    else
        echo "1" > "$SERIAL_FILE"
        echo "1"
    fi
}

# Function to update the Last Updated date in the footer
update_footer() {
    local current_date=$(date)
    # Update the Last Updated line in the footer
    sed_inplace "s/\*\*Last Updated:\*\* .*/\*\*Last Updated:\*\* $current_date/" "$TODO_FILE"
}

# Function to log TODO operations
log_todo_action() {
    local action="$1"
    local task_id="$2"
    local description="$3"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local git_user=$(git config --get user.name 2>/dev/null || echo "unknown")
    
    # Create log entry in format: TIMESTAMP | USER | ACTION | TASK_ID | DESCRIPTION
    local log_entry="$timestamp | $git_user | $action | $task_id | $description"
    
    # Create temporary file with header preserved at top, then new entry, then existing entries
    local temp_file=$(mktemp)
    
    # Extract header lines (lines starting with #)
    grep "^#" "$LOG_FILE" > "$temp_file"
    echo "" >> "$temp_file"
    
    # Add new entry
    echo "$log_entry" >> "$temp_file"
    
    # Add existing log entries (skip header lines)
    grep -v "^#" "$LOG_FILE" | grep -v "^$" >> "$temp_file"
    
    mv "$temp_file" "$LOG_FILE"
}

# Function to initialize log file if it doesn't exist
init_log_file() {
    if [[ ! -f "$LOG_FILE" ]]; then
        echo "# TODO Tool Log File" > "$LOG_FILE"
        echo "# Format: TIMESTAMP | USER | ACTION | TASK_ID | DESCRIPTION" >> "$LOG_FILE"
        echo "# Generated: $(date)" >> "$LOG_FILE"
        echo "" >> "$LOG_FILE"
    fi
}

# Function to initialize TODO file if it doesn't exist
init_todo_file() {
    if [[ ! -f "$TODO_FILE" ]]; then
        cat > "$TODO_FILE" << 'EOF'
# Home Assistant Project Todo List

> **⚠️ IMPORTANT: This file should ONLY be edited through the `./scripts/todo/todo.zsh` script!**

## Tasks

------------------

## Recently Completed

---

**Last Updated:** $(date)
**Repository:** https://github.com/fxstein/homeassistant  
**Maintenance:** Use `./scripts/todo/todo.zsh` script only

EOF
        # Replace the $(date) placeholder with actual date
        local current_date=$(date)
        sed_inplace "s/\$(date)/$current_date/" "$TODO_FILE"
    fi
}

# Function to get current serial number
get_current_serial() {
    if [[ -f "$SERIAL_FILE" ]]; then
        cat "$SERIAL_FILE"
    else
        echo "0"
    fi
}

# Function to parse task line and extract components
parse_task() {
    local line="$1"
    local id=$(echo "$line" | grep -o '^#\([0-9.]*\)' | sed 's/#//')
    local description=$(echo "$line" | sed 's/^#[0-9.]* *//' | sed 's/ *#.*$//')
    local tags=$(echo "$line" | grep -o '#[a-zA-Z0-9]*' | grep -v '^#[0-9]' | tr '\n' ' ')
    local date=$(echo "$line" | grep -o '([^)]*)' | tr -d '()')
    
    echo "ID:$id|DESC:$description|TAGS:$tags|DATE:$date"
}

# Function to normalize malformed checkboxes
normalize_checkboxes() {
    # Fix malformed checkboxes like [  ], [   ], [] to proper [ ] or [x]
    sed_inplace 's/\[  \]/[ ]/g' "$TODO_FILE"
    sed_inplace 's/\[   \]/[ ]/g' "$TODO_FILE"
    sed_inplace 's/\[    \]/[ ]/g' "$TODO_FILE"
    sed_inplace 's/\[\]/[ ]/g' "$TODO_FILE"
    # Fix any other malformed patterns with multiple spaces
    sed_inplace 's/\[[ ]*\]/[ ]/g' "$TODO_FILE"
}

# Function to show usage
show_usage() {
    echo "Usage: ./scripts/todo/todo.zsh [command] [options]"
    echo ""
    echo "Commands:"
    echo "  add <text> [tags]             Add a new todo item with optional tags"
    echo "  add-subtask <parent-id> <text> [tags]  Add a subtask to an existing task"
    echo "  list [--tag <tag>] [--incomplete-only] [--parents-only] [--has-subtasks]  Show todo list with filters"
    echo "  complete <id> [<id>...] [--with-subtasks]  Mark item(s) as completed"
    echo "  undo <id>                     Reopen (undo) completed task (use #ID)"
    echo "  modify <id> <text> [tags]     Modify task description and/or tags"
    echo "  delete <id> [<id>...] [--with-subtasks]  Soft delete task(s) to Deleted section (30-day recovery)"
    echo "  archive <id> [<id>...] [--reason <reason>]  Move task(s) to Recently Completed (reason for incomplete tasks)"
    echo "  relate <id> --<type> <targets>  Add task relationship (completed-by, depends-on, blocks, related-to, duplicate-of)"
    echo "  note <id> <text>              Add note to task (blockquote format)"
    echo "  show <id>                     Show task with subtasks, relationships, and notes"
    echo "  restore <id>                  Restore task from Deleted or Recently Completed to active Tasks"
    echo "  --lint                        Identify formatting issues (indentation, checkboxes)"
    echo "  --reformat [--dry-run]        Apply formatting fixes (use --dry-run to preview)"
    echo "  edit                          Edit todo file in editor"
    echo "  log [--filter <text>] [--lines <n>] View TODO operation log"
    echo ""
    echo "Examples:"
    echo "  ./scripts/todo/todo.zsh add 'Fix Shelly device naming' '#api'"
    echo "  ./scripts/todo/todo.zsh add-subtask 39 'Design subtask data structure' '#feature'"
    echo "  ./scripts/todo/todo.zsh complete 1"
    echo "  ./scripts/todo/todo.zsh complete 107 108 109          # Bulk complete"
    echo "  ./scripts/todo/todo.zsh complete 104 --with-subtasks  # Complete task and all subtasks"
    echo "  ./scripts/todo/todo.zsh complete 104.3-104.10         # Complete range of subtasks"
    echo "  ./scripts/todo/todo.zsh undo 1"
    echo "  ./scripts/todo/todo.zsh modify 1 'Updated task description' '#api'"
    echo "  ./scripts/todo/todo.zsh delete 115                    # Soft delete (30-day recovery)"
    echo "  ./scripts/todo/todo.zsh delete 110 --with-subtasks    # Delete task and all subtasks"
    echo "  ./scripts/todo/todo.zsh delete 120.5-120.10           # Delete range"
    echo "  ./scripts/todo/todo.zsh archive 1"
    echo "  ./scripts/todo/todo.zsh archive 107 108 109           # Bulk archive"
    echo "  ./scripts/todo/todo.zsh archive 109 --reason obsolete # Archive incomplete task"
    echo "  ./scripts/todo/todo.zsh archive 104 --reason 'completed-by:107,108'"
    echo "  ./scripts/todo/todo.zsh relate 110 --depends-on 104  # Add dependency"
    echo "  ./scripts/todo/todo.zsh relate 104 --completed-by '107,108'"
    echo "  ./scripts/todo/todo.zsh note 110 'Testing shows issues'  # Add note"
    echo "  ./scripts/todo/todo.zsh show 110                    # Show task with relationships & notes"
    echo "  ./scripts/todo/todo.zsh restore 1"
    echo "  ./scripts/todo/todo.zsh --lint"
    echo "  ./scripts/todo/todo.zsh --reformat --dry-run"
    echo "  ./scripts/todo/todo.zsh --reformat"
    echo "  ./scripts/todo/todo.zsh list"
    echo "  ./scripts/todo/todo.zsh list --tag api"
    echo "  ./scripts/todo/todo.zsh list --incomplete-only     # Show only pending tasks"
    echo "  ./scripts/todo/todo.zsh list --parents-only        # Hide subtasks"
    echo "  ./scripts/todo/todo.zsh list --has-subtasks        # Only tasks with subtasks"
    echo "  ./scripts/todo/todo.zsh log"
    echo "  ./scripts/todo/todo.zsh log --filter ADD"
    echo "  ./scripts/todo/todo.zsh log --lines 20"
}

# Function to validate command arguments and detect invalid options
validate_command_args() {
    local command="$1"
    shift
    local args=("$@")
    
    case "$command" in
        "add")
            # add <text> [tags] - no additional options allowed
            for arg in "${args[@]}"; do
                if [[ "$arg" =~ ^-- ]]; then
                    echo "Error: Invalid option '$arg' for 'add' command"
                    echo "The 'add' command only accepts text and optional tags"
                    echo ""
                    show_usage
                    return 1
                fi
            done
            ;;
        "add-subtask")
            # add-subtask <parent-id> <text> [tags] - no additional options allowed
            for arg in "${args[@]}"; do
                if [[ "$arg" =~ ^-- ]]; then
                    echo "Error: Invalid option '$arg' for 'add-subtask' command"
                    echo "The 'add-subtask' command only accepts parent-id, text, and optional tags"
                    echo ""
                    show_usage
                    return 1
                fi
            done
            ;;
        "list")
            # list [--tag <tag>] [--incomplete-only] [--parents-only] [--has-subtasks]
            local expecting_tag=false
            for arg in "${args[@]}"; do
                if [[ "$arg" == "--tag" ]]; then
                    expecting_tag=true
                elif [[ "$arg" =~ ^--(incomplete-only|parents-only|has-subtasks)$ ]]; then
                    # Valid flags
                    continue
                elif [[ "$arg" =~ ^-- ]]; then
                    echo "Error: Invalid option '$arg' for 'list' command"
                    echo "The 'list' command accepts: --tag <tag>, --incomplete-only, --parents-only, --has-subtasks"
                    echo ""
                    show_usage
                    return 1
                elif [[ "$expecting_tag" == true ]]; then
                    expecting_tag=false
                fi
            done
            ;;
        "complete")
            # complete <id> [<id>...] [--with-subtasks] - allow multiple IDs and --with-subtasks flag
            for arg in "${args[@]}"; do
                if [[ "$arg" =~ ^-- ]] && [[ "$arg" != "--with-subtasks" ]]; then
                    echo "Error: Invalid option '$arg' for 'complete' command"
                    echo "The 'complete' command accepts task ID(s) and optional --with-subtasks flag"
                    echo ""
                    show_usage
                    return 1
                fi
            done
            ;;
        "undo")
            # undo <id> - no additional options allowed
            for arg in "${args[@]}"; do
                if [[ "$arg" =~ ^-- ]]; then
                    echo "Error: Invalid option '$arg' for 'undo' command"
                    echo "The 'undo' command only accepts a task ID"
                    echo ""
                    show_usage
                    return 1
                fi
            done
            ;;
        "modify")
            # modify <id> <text> [tags] - no additional options allowed
            for arg in "${args[@]}"; do
                if [[ "$arg" =~ ^-- ]]; then
                    echo "Error: Invalid option '$arg' for 'modify' command"
                    echo "The 'modify' command only accepts task-id, text, and optional tags"
                    echo ""
                    show_usage
                    return 1
                fi
            done
            ;;
        "archive")
            # archive <id> [<id>...] [--reason <reason>] - allow multiple IDs and reason
            local expecting_reason=false
            for arg in "${args[@]}"; do
                if [[ "$arg" == "--reason" ]]; then
                    expecting_reason=true
                elif [[ "$arg" =~ ^-- ]]; then
                    echo "Error: Invalid option '$arg' for 'archive' command"
                    echo "The 'archive' command accepts task ID(s) and optional --reason <reason>"
                    echo ""
                    show_usage
                    return 1
                elif [[ "$expecting_reason" == true ]]; then
                    expecting_reason=false
                fi
            done
            ;;
        "delete")
            # delete <id> [<id>...] [--with-subtasks] - allow multiple IDs and --with-subtasks
            for arg in "${args[@]}"; do
                if [[ "$arg" =~ ^-- ]] && [[ "$arg" != "--with-subtasks" ]]; then
                    echo "Error: Invalid option '$arg' for 'delete' command"
                    echo "The 'delete' command accepts task ID(s) and optional --with-subtasks flag"
                    echo ""
                    show_usage
                    return 1
                fi
            done
            ;;
        "relate")
            # relate <id> --<relation-type> <targets> - relationship management
            # Allow all --completed-by, --depends-on, --blocks, --related-to, --duplicate-of
            ;;
        "note")
            # note <id> <text> - no additional options allowed
            for arg in "${args[@]}"; do
                if [[ "$arg" =~ ^-- ]]; then
                    echo "Error: Invalid option '$arg' for 'note' command"
                    echo "The 'note' command only accepts task ID and note text"
                    echo ""
                    show_usage
                    return 1
                fi
            done
            ;;
        "show")
            # show <id> - no additional options allowed
            for arg in "${args[@]}"; do
                if [[ "$arg" =~ ^-- ]]; then
                    echo "Error: Invalid option '$arg' for 'show' command"
                    echo "The 'show' command only accepts a task ID"
                    echo ""
                    show_usage
                    return 1
                fi
            done
            ;;
        "restore")
            # restore <id> - no additional options allowed
            for arg in "${args[@]}"; do
                if [[ "$arg" =~ ^-- ]]; then
                    echo "Error: Invalid option '$arg' for 'restore' command"
                    echo "The 'restore' command only accepts a task ID"
                    echo ""
                    show_usage
                    return 1
                fi
            done
            ;;
        "log")
            # log [--filter <text>] [--lines <n>] - only --filter and --lines allowed
            local expecting_filter=false
            local expecting_lines=false
            for arg in "${args[@]}"; do
                if [[ "$arg" == "--filter" ]]; then
                    expecting_filter=true
                elif [[ "$arg" == "--lines" ]]; then
                    expecting_lines=true
                elif [[ "$arg" =~ ^-- ]]; then
                    echo "Error: Invalid option '$arg' for 'log' command"
                    echo "The 'log' command only accepts --filter <text> and --lines <n> options"
                    echo ""
                    show_usage
                    return 1
                elif [[ "$expecting_filter" == true ]]; then
                    expecting_filter=false
                elif [[ "$expecting_lines" == true ]]; then
                    expecting_lines=false
                fi
            done
            ;;
    esac
    
    return 0
}

# Function to add todo item
add_todo() {
    local text="$1"
    local tags="$2"
    
    if [[ -z "$text" ]]; then
        echo "Error: Please provide todo text"
        return 1
    fi
    
    # Get next serial number
    local serial=$(increment_serial)
    
    # Format the task line with bold task ID
    local task_line="- [ ] **#$serial** $text"
    if [[ -n "$tags" ]]; then
        # Wrap each tag in backticks for code styling
        local styled_tags=""
        # Split tags by space and process each one
        for tag in $(echo "$tags" | tr ' ' '\n'); do
            if [[ -n "$styled_tags" ]]; then
                styled_tags="$styled_tags \`$tag\`"
            else
                styled_tags="\`$tag\`"
            fi
        done
        task_line="$task_line $styled_tags"
    fi
    
    # Add to Tasks section
    local tasks_line=$(grep -n "^## Tasks" "$TODO_FILE" | cut -d: -f1)
    if [[ -n "$tasks_line" ]]; then
        # Use awk or a simpler approach for macOS compatibility
        if [[ "$(uname)" == "Darwin" ]]; then
            # Insert after the ## Tasks line with proper newline
            local temp_file=$(mktemp)
            head -n "$tasks_line" "$TODO_FILE" > "$temp_file"
            echo "$task_line" >> "$temp_file"
            tail -n +$((tasks_line + 1)) "$TODO_FILE" >> "$temp_file"
            mv "$temp_file" "$TODO_FILE"
        else
            sed_inplace "/^## Tasks$/a$task_line" "$TODO_FILE"
        fi
    fi
    update_footer
    
    # Log the action
    log_todo_action "ADD" "$serial" "$text"
    
    echo "Added: #$serial $text"
}

# Function to add subtask to existing task
add_subtask() {
    local parent_id="$1"
    local text="$2"
    local tags="$3"
    
    if [[ -z "$parent_id" || -z "$text" ]]; then
        echo "Error: Please provide parent task ID and subtask text"
        echo "Usage: ./scripts/todo/todo.zsh add-subtask <parent-id> \"<subtask text>\" [\"<tags>\"]"
        return 1
    fi
    
    # Check if parent task exists
    if ! grep -q "^- \[.*\] \*\*#$parent_id\*\* " "$TODO_FILE"; then
        echo "Error: Parent task #$parent_id not found"
        return 1
    fi
    
    # Find the next subtask number for this parent
    local next_subtask_num=1
    while grep -q "^  - \[.*\] \*\*#$parent_id\.$next_subtask_num\*\* " "$TODO_FILE"; do
        next_subtask_num=$((next_subtask_num + 1))
    done
    
    # Create subtask ID
    local subtask_id="$parent_id.$next_subtask_num"
    
    # Format the subtask line with bold task ID and proper indentation
    local task_line="  - [ ] **#$subtask_id** $text"
    if [[ -n "$tags" ]]; then
        # Wrap each tag in backticks for code styling
        local styled_tags=""
        # Split tags by space and process each one
        for tag in $(echo "$tags" | tr ' ' '\n'); do
            if [[ -n "$styled_tags" ]]; then
                styled_tags="$styled_tags \`$tag\`"
            else
                styled_tags="\`$tag\`"
            fi
        done
        task_line="$task_line $styled_tags"
    fi
    
    # Find the parent task line and add subtask after it
    local parent_line_num=$(grep -n "^- \[.*\] \*\*#$parent_id\*\* " "$TODO_FILE" | head -1 | cut -d: -f1)
    if [[ -n "$parent_line_num" ]]; then
        if [[ "$(uname)" == "Darwin" ]]; then
            local temp_file=$(mktemp)
            head -n "$parent_line_num" "$TODO_FILE" > "$temp_file"
            echo "$task_line" >> "$temp_file"
            tail -n +$((parent_line_num + 1)) "$TODO_FILE" >> "$temp_file"
            mv "$temp_file" "$TODO_FILE"
        else
            sed_inplace "${parent_line_num}a\\$task_line" "$TODO_FILE"
        fi
        update_footer
        
        # Log the action
        log_todo_action "ADD_SUBTASK" "$subtask_id" "$text (parent: #$parent_id)"
        
        echo "Added subtask: #$subtask_id $text"
    else
        echo "Error: Could not find parent task #$parent_id"
        return 1
    fi
}

# Function to list todos
list_todos() {
    local filter_tag=""
    local incomplete_only=false
    local parents_only=false
    local has_subtasks_only=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --tag)
                filter_tag="$2"
                shift 2
                ;;
            --incomplete-only)
                incomplete_only=true
                shift
                ;;
            --parents-only)
                parents_only=true
                shift
                ;;
            --has-subtasks)
                has_subtasks_only=true
                shift
                ;;
            *)
                shift
                ;;
        esac
    done
    
    if [[ ! -f "$TODO_FILE" ]]; then
        echo "Todo file not found: $TODO_FILE"
        return 1
    fi
    
    # If using tag filter, use original implementation
    if [[ -n "$filter_tag" ]] && [[ "$incomplete_only" == false ]] && [[ "$parents_only" == false ]] && [[ "$has_subtasks_only" == false ]]; then
        # Add # prefix if missing
        if [[ ! "$filter_tag" =~ ^# ]]; then
            filter_tag="#$filter_tag"
        fi
        
        # Filter by tag - show tasks with the specified tag
        echo "# Home Assistant Project Todo List"
        echo ""
        echo "## Tasks with tag: $filter_tag"
        echo ""
        grep -E "\`$filter_tag\`|$filter_tag" "$TODO_FILE" | grep "^-.*\[.*\]"
        echo ""
        echo "## Recently Completed with tag: $filter_tag"
        echo ""
        grep -E "\`$filter_tag\`|$filter_tag" "$TODO_FILE" | grep "^-.*\[x\]"
        return
    fi
    
    # Enhanced filtering logic
    local in_tasks_section=false
    local in_recently_completed=false
    local current_parent=""
    local parent_has_subtasks=false
    local last_parent_shown=false
    
    # First pass: identify parents with subtasks if needed
    local parents_with_subtasks=()
    if [[ "$has_subtasks_only" == true ]]; then
        while IFS= read -r line; do
            # Check if this is a subtask (starts with "  - ")
            if [[ "$line" =~ ^"  - ".+#([0-9]+)\.([0-9]+) ]]; then
                local parent_id="${match[1]}"
                if [[ ! " ${parents_with_subtasks[@]} " =~ " ${parent_id} " ]]; then
                    parents_with_subtasks+=("$parent_id")
                fi
            fi
        done < "$TODO_FILE"
    fi
    
    # Second pass: filter and display
    while IFS= read -r line; do
        # Track sections
        if [[ "$line" == "## Tasks" ]]; then
            in_tasks_section=true
            in_recently_completed=false
            if [[ "$incomplete_only" == false ]]; then
                echo "$line"
            fi
            continue
        elif [[ "$line" == "## Recently Completed" ]]; then
            in_tasks_section=false
            in_recently_completed=true
            if [[ "$incomplete_only" == false ]]; then
                echo "$line"
            fi
            continue
        elif [[ "$line" =~ ^## ]]; then
            # Other section, stop filtering
            if [[ "$incomplete_only" == false ]]; then
                echo "$line"
            fi
            in_tasks_section=false
            in_recently_completed=false
            continue
        fi
        
        # Skip completed section if --incomplete-only
        if [[ "$incomplete_only" == true ]] && [[ "$in_recently_completed" == true ]]; then
            continue
        fi
        
        # Check if this is a parent task (starts with "- [" and has **#num** but not **#num.num**)
        if [[ "$line" == "- ["*"**#"*"**"* ]] && [[ "$line" != *"**#"*"."*"**"* ]]; then
            # Extract task ID and checkbox
            local checkbox=$(echo "$line" | sed 's/^- \[\(.\)\].*/\1/')
            current_parent=$(echo "$line" | grep -o '#[0-9]\+' | sed 's/#//' | head -1)
            
            # Apply filters
            local should_show=true
            
            # Filter: incomplete only (skip completed tasks)
            if [[ "$incomplete_only" == true ]] && [[ "$checkbox" == "x" ]]; then
                should_show=false
            fi
            
            # Filter: has-subtasks only
            if [[ "$has_subtasks_only" == true ]]; then
                if [[ ! " ${parents_with_subtasks[@]} " =~ " ${current_parent} " ]]; then
                    should_show=false
                fi
            fi
            
            # Filter: tag
            if [[ -n "$filter_tag" ]]; then
                if [[ ! "$filter_tag" =~ ^# ]]; then
                    filter_tag="#$filter_tag"
                fi
                if [[ ! "$line" =~ $filter_tag ]]; then
                    should_show=false
                fi
            fi
            
            last_parent_shown=$should_show
            if [[ "$should_show" == true ]]; then
                echo "$line"
            fi
        # Check if this is a subtask (starts with "  - ")
        elif [[ "$line" =~ ^"  - " ]]; then
            # Show subtasks unless --parents-only, and only if parent was shown
            if [[ "$parents_only" == false ]] && [[ "$last_parent_shown" == true ]]; then
                # Apply same filters as parent
                local should_show=true
                
                # Tag filter
                if [[ -n "$filter_tag" ]]; then
                    if [[ ! "$line" =~ $filter_tag ]]; then
                        should_show=false
                    fi
                fi
                
                if [[ "$should_show" == true ]]; then
                    echo "$line"
                fi
            fi
        else
            # Non-task line (headers, footers, blank lines, etc.)
            # Only show if not heavily filtering
            if [[ "$incomplete_only" == false ]] && [[ "$parents_only" == false ]] && [[ "$has_subtasks_only" == false ]]; then
                echo "$line"
            elif [[ "$in_tasks_section" == true ]] || [[ "$line" == "" ]] || [[ "$line" =~ ^## ]]; then
                # Always show headers and blank lines in tasks section
                echo "$line"
            fi
        fi
    done < "$TODO_FILE"
}

# Function to get line number of task by serial number
get_task_line() {
    local task_id="$1"
    local line_number=0
    
    while IFS= read -r line; do
        line_number=$((line_number + 1))
        if [[ "$line" =~ "^-.*\[.*\].*" || "$line" =~ "^  -.*\[.*\].*" ]]; then
            # Extract the ID from the line (handle both bold and non-bold formatting, and subtasks)
            local line_id=$(echo "$line" | grep -o '\*\*#\([0-9][0-9.]*\)\*\*\|#[0-9][0-9.]*' | sed 's/\*\*#//g' | sed 's/\*\*//g' | sed 's/#//')
            if [[ "$line_id" == "$task_id" ]]; then
                echo "$line_number"
                return 0
            fi
        fi
    done < "$TODO_FILE"
    
    echo "Task #$task_id not found"
    return 1
}

# Function to mark as complete
complete_todo() {
    local with_subtasks=false
    local task_ids=()
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --with-subtasks)
                with_subtasks=true
                shift
                ;;
            *)
                task_ids+=("$1")
                shift
                ;;
        esac
    done
    
    if [[ ${#task_ids[@]} -eq 0 ]]; then
        echo "Error: Please provide at least one task number"
        return 1
    fi
    
    # Normalize any malformed checkboxes first
    normalize_checkboxes
    
    # Expand ranges and collect all task IDs to complete
    local all_ids=()
    for id in "${task_ids[@]}"; do
        # Match range format: 104.3-104.10 or 122.3-10 (both formats supported)
        if [[ "$id" =~ ^([0-9]+)\.([0-9]+)-([0-9]+)\.([0-9]+)$ ]]; then
            # Full format: 122.3-122.10
            local parent=${match[1]}
            local start=${match[2]}
            local end_parent=${match[3]}
            local end=${match[4]}
            # Verify parent IDs match
            if [[ "$parent" == "$end_parent" ]]; then
                for ((i=start; i<=end; i++)); do
                    all_ids+=("${parent}.${i}")
                done
            else
                echo "Warning: Range parent IDs don't match ($parent vs $end_parent), treating as literal"
                all_ids+=("$id")
            fi
        elif [[ "$id" =~ ^([0-9]+)\.([0-9]+)-([0-9]+)$ ]]; then
            # Short format: 122.3-10 (assumes same parent)
            local parent=${match[1]}
            local start=${match[2]}
            local end=${match[3]}
            for ((i=start; i<=end; i++)); do
                all_ids+=("${parent}.${i}")
            done
        else
            all_ids+=("$id")
        fi
    done
    
    # If --with-subtasks, add all subtasks for parent tasks
    if [[ "$with_subtasks" == "true" ]]; then
        local expanded_ids=()
        for id in "${all_ids[@]}"; do
            expanded_ids+=("$id")
            # Find all subtasks for this parent (e.g., if id is 104, find 104.1, 104.2, etc.)
            # Check if this is a parent task (doesn't contain a dot)
            if [[ "$id" != *.* ]]; then
                # This is a parent task, find its subtasks
                # Find all subtasks (both [ ] and [x] checkboxes)
                while IFS= read -r line; do
                    # Extract subtask ID from line
                    if [[ "$line" =~ '#([0-9]+\.[0-9]+)' ]]; then
                        local subtask_id="${match[1]}"
                        expanded_ids+=("$subtask_id")
                    fi
                done < <(grep "^  - \[.\] \*\*#${id}\." "$TODO_FILE")
            fi
        done
        all_ids=("${expanded_ids[@]}")
    fi
    
    # Complete all tasks
    local completed_count=0
    for number in "${all_ids[@]}"; do
        # Skip if task doesn't exist (escape asterisks for grep)
        if ! grep -q "\*\*#$number\*\*" "$TODO_FILE"; then
            echo "Warning: Task #$number not found, skipping"
            continue
        fi
        
        # Complete the task
        sed_inplace "s/- \[ \] \*\*#$number\*\* /- [x] **#$number** /" "$TODO_FILE"
        sed_inplace "s/  - \[ \] \*\*#$number\*\* /  - [x] **#$number** /" "$TODO_FILE"
        
        # Get task description for logging
        local task_description=$(grep "\*\*#$number\*\*" "$TODO_FILE" | head -1 | sed 's/.*\*\*#[0-9.]*\*\* *//' | sed 's/ *`.*$//')
        
        # Log the action
        log_todo_action "COMPLETE" "$number" "$task_description"
        
        completed_count=$((completed_count + 1))
    done
    
    update_footer
    
    echo "Marked $completed_count task(s) as completed"
}

# Function to undo completion (reopen task)
undo_todo() {
    local number="$1"
    if [[ -z "$number" ]]; then
        echo "Error: Please provide todo number"
        return 1
    fi
    
    # Normalize any malformed checkboxes first
    normalize_checkboxes
    
    # Use sed to directly find and replace the specific task (handle bold formatting and subtasks)
    sed_inplace "s/- \[x\] \*\*#$number\*\* /- [ ] **#$number** /" "$TODO_FILE"
    sed_inplace "s/  - \[x\] \*\*#$number\*\* /  - [ ] **#$number** /" "$TODO_FILE"
    update_footer
    
    # Get task description for logging
    local task_description=$(grep "\*\*#$number\*\*" "$TODO_FILE" | head -1 | sed 's/.*\*\*#[0-9.]*\*\* *//' | sed 's/ *`.*$//')
    
    # Log the action
    log_todo_action "UNDO" "$number" "$task_description"
    
    echo "Reopened task $number"
}

# Function to modify a specific task
modify_todo() {
    local task_id="$1"
    local new_text="$2"
    local new_tags="$3"
    
    if [[ -z "$task_id" || -z "$new_text" ]]; then
        echo "Error: Please provide task ID and new text"
        echo "Usage: ./scripts/todo/todo.zsh modify <id> \"<new text>\" [\"<new tags>\"]"
        return 1
    fi
    
    # Normalize any malformed checkboxes first
    normalize_checkboxes
    
    # Get the current completion status (handle both bold and non-bold formatting, and subtasks)
    local current_status=$(grep -E "^- \[.*\] (\*\*#$task_id\*\*|#$task_id) |^  - \[.*\] (\*\*#$task_id\*\*|#$task_id) " "$TODO_FILE" | sed 's/- \[\([^]]*\)\].*/\1/' | sed 's/  - \[\([^]]*\)\].*/\1/' | head -1)
    
    # Format the new task line preserving completion status with bold task ID
    # Check if this is a subtask (has decimal point) and add proper indentation
    if [[ "$task_id" =~ \. ]]; then
        local new_task_line="  - [$current_status] **#$task_id** $new_text"
    else
        local new_task_line="- [$current_status] **#$task_id** $new_text"
    fi
    if [[ -n "$new_tags" ]]; then
        # Wrap each tag in backticks for code styling
        local styled_tags=""
        # Split tags by space and process each one
        for tag in $(echo "$new_tags" | tr ' ' '\n'); do
            if [[ -n "$styled_tags" ]]; then
                styled_tags="$styled_tags \`$tag\`"
            else
                styled_tags="\`$tag\`"
            fi
        done
        new_task_line="$new_task_line $styled_tags"
    fi
    
    # Replace the task line using sed (handle bold formatting and subtasks)
    # Escape special characters for sed replacement (using pipe as delimiter)
    # Need to escape: & \ and any pipes in the replacement text
    local escaped_line=$(printf '%s\n' "$new_task_line" | sed 's/\\/\\\\/g' | sed 's/&/\\&/g' | sed 's/|/\\|/g')
    
    # Use pipe delimiter to avoid conflicts with / and other characters in replacement
    if [[ "$task_id" =~ \. ]]; then
        # For subtasks, replace with proper 2-space indentation
        sed_inplace "s|^  - \[.*\] \*\*#$task_id\*\* .*|$escaped_line|" "$TODO_FILE"
    else
        # For main tasks, replace without indentation
        sed_inplace "s|^- \[.*\] \*\*#$task_id\*\* .*|$escaped_line|" "$TODO_FILE"
    fi
    update_footer
    
    # Log the action
    log_todo_action "MODIFY" "$task_id" "$new_text"
    
    echo "Modified task #$task_id"
}

# Function to archive a completed task and its subtasks
archive_task() {
    local task_id=""
    local reason=""
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --reason)
                reason="$2"
                shift 2
                ;;
            *)
                task_id="$1"
                shift
                ;;
        esac
    done
    
    if [[ -z "$task_id" ]]; then
        echo "Error: Please provide task ID"
        echo "Usage: ./scripts/todo/todo.zsh archive <id> [--reason <reason>]"
        return 1
    fi
    
    # Normalize any malformed checkboxes first
    normalize_checkboxes
    
    # Determine task status and checkbox style
    local checkbox=""
    local status_note=""
    local is_completed=false
    
    # Check if task exists and its current state
    if grep -q "^- \[x\] \*\*#$task_id\*\* " "$TODO_FILE"; then
        # Task is completed
        is_completed=true
        checkbox="x"
    elif grep -q "^- \[ \] \*\*#$task_id\*\* " "$TODO_FILE"; then
        # Task is incomplete - need reason to archive
        if [[ -z "$reason" ]]; then
            echo "Error: Task #$task_id is not completed"
            echo "To archive incomplete tasks, provide --reason: obsolete, duplicate, wontfix, or completed-by:<tasks>"
            return 1
        fi
        # Set checkbox based on reason
        case "$reason" in
            obsolete)
                checkbox="~"
                status_note=" (obsolete)"
                ;;
            duplicate|duplicate:*)
                checkbox="~"
                status_note=" (duplicate)"
                ;;
            wontfix)
                checkbox="-"
                status_note=" (wontfix)"
                ;;
            completed-by:*)
                checkbox=">"
                status_note=" (${reason})"
                ;;
            *)
                checkbox="~"
                status_note=" (${reason})"
                ;;
        esac
    else
        echo "Error: Task #$task_id not found"
        return 1
    fi
    
    # Simple implementation: move the task to Recently Completed section
    # Get the task line (either completed or incomplete)
    local task_line=$(grep "^- \[[x ]\] \*\*#$task_id\*\* " "$TODO_FILE")
    if [[ -z "$task_line" ]]; then
        echo "Error: Could not find task #$task_id"
        return 1
    fi
    
    # Update checkbox in task line if needed (for incomplete tasks with reason)
    if [[ "$checkbox" != "x" ]]; then
        # Replace checkbox: [ ] or [x] → [$checkbox]
        task_line=$(echo "$task_line" | sed "s/\[.\]/[$checkbox]/")
    fi
    
    # Add completion date if not already present
    local archive_date=$(date +"%Y-%m-%d")
    if [[ ! "$task_line" =~ "\([0-9]{4}-[0-9]{2}-[0-9]{2}\)" ]]; then
        task_line="$task_line${status_note} ($archive_date)"
    fi
    
    # Collect all subtasks (completed or not)
    local subtasks=()
    while IFS= read -r line; do
        if [[ "$line" =~ "^  - \[.*\] \*\*#$task_id\." ]]; then
            # Add completion date if not already present
            if [[ ! "$line" =~ "\([0-9]{4}-[0-9]{2}-[0-9]{2}\)" ]]; then
                line="$line ($archive_date)"
            fi
            subtasks+=("$line")
        fi
    done < "$TODO_FILE"
    
    # Remove from Tasks section (main task and all subtasks)
    # Handle both completed [x] and incomplete [ ] tasks
    sed_inplace "/^- \[[x ]\] \*\*#$task_id\*\* /d" "$TODO_FILE"
    sed_inplace "/^  - \[.*\] \*\*#$task_id\\./d" "$TODO_FILE"
    
    # Create a complete block with main task and subtasks
    local complete_block="$task_line"
    if [[ ${#subtasks[@]} -gt 0 ]]; then
        # Join subtasks with newlines
        local subtasks_text=$(printf '%s\n' "${subtasks[@]}")
        complete_block="$complete_block
$subtasks_text"
    fi
    
    # Add to Recently Completed section
    local recently_completed_section=$(grep -n "^## Recently Completed" "$TODO_FILE" | cut -d: -f1)
    if [[ -n "$recently_completed_section" ]]; then
        # Insert the complete block after the "## Recently Completed" line
        local temp_file=$(mktemp)
        echo -e "$complete_block" > "$temp_file"
        sed_inplace "${recently_completed_section}r $temp_file" "$TODO_FILE"
        rm -f "$temp_file"
    else
        # Add Recently Completed section if it doesn't exist
        echo "" >> "$TODO_FILE"
        echo "------------------" >> "$TODO_FILE"
        echo "" >> "$TODO_FILE"
        echo "## Recently Completed" >> "$TODO_FILE"
        echo -e "$complete_block" >> "$TODO_FILE"
    fi
    
    # Count subtasks for reporting
    local subtask_count=${#subtasks[@]}
    update_footer
    
    # Get task description for logging
    local task_description=$(echo "$task_line" | sed 's/.*\*\*#[0-9.]*\*\* *//' | sed 's/ *`.*$//' | sed 's/ *([^)]*)$//')
    
    # Log the action
    log_todo_action "ARCHIVE" "$task_id" "$task_description (with $subtask_count subtasks)"
    
    echo "Archived task #$task_id and $subtask_count subtasks to Recently Completed section"
}

# Function to soft delete a task (move to Deleted section)
delete_task() {
    local with_subtasks=false
    local task_ids=()
    
    # Parse arguments (same pattern as complete)
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --with-subtasks)
                with_subtasks=true
                shift
                ;;
            *)
                task_ids+=("$1")
                shift
                ;;
        esac
    done
    
    if [[ ${#task_ids[@]} -eq 0 ]]; then
        echo "Error: Please provide at least one task number"
        return 1
    fi
    
    # Normalize any malformed checkboxes first
    normalize_checkboxes
    
    # Auto-purge expired deleted tasks first
    purge_expired_deleted_tasks
    
    # Expand ranges and collect all task IDs (same logic as complete)
    local all_ids=()
    for id in "${task_ids[@]}"; do
        if [[ "$id" =~ ^([0-9]+)\.([0-9]+)-([0-9]+)\.([0-9]+)$ ]]; then
            local parent=${match[1]}
            local start=${match[2]}
            local end_parent=${match[3]}
            local end=${match[4]}
            if [[ "$parent" == "$end_parent" ]]; then
                for ((i=start; i<=end; i++)); do
                    all_ids+=("${parent}.${i}")
                done
            else
                all_ids+=("$id")
            fi
        elif [[ "$id" =~ ^([0-9]+)\.([0-9]+)-([0-9]+)$ ]]; then
            local parent=${match[1]}
            local start=${match[2]}
            local end=${match[3]}
            for ((i=start; i<=end; i++)); do
                all_ids+=("${parent}.${i}")
            done
        else
            all_ids+=("$id")
        fi
    done
    
    # If --with-subtasks, add all subtasks
    if [[ "$with_subtasks" == "true" ]]; then
        local expanded_ids=()
        for id in "${all_ids[@]}"; do
            expanded_ids+=("$id")
            if [[ "$id" != *.* ]]; then
                while IFS= read -r line; do
                    if [[ "$line" =~ '#([0-9]+\.[0-9]+)' ]]; then
                        local subtask_id="${match[1]}"
                        expanded_ids+=("$subtask_id")
                    fi
                done < <(grep "^  - \[.\] \*\*#${id}\." "$TODO_FILE")
            fi
        done
        all_ids=("${expanded_ids[@]}")
    fi
    
    # Delete all tasks
    local deleted_count=0
    local delete_date=$(date +"%Y-%m-%d")
    local expire_date=$(date -d "+30 days" +"%Y-%m-%d" 2>/dev/null || date -v+30d +"%Y-%m-%d" 2>/dev/null || echo "2025-11-29")
    
    for number in "${all_ids[@]}"; do
        # Find task (anywhere - Tasks or Recently Completed)
        local task_line=$(grep "^- \[.\] \*\*#$number\*\* \|^  - \[.\] \*\*#$number\*\* " "$TODO_FILE" | head -1)
        
        if [[ -z "$task_line" ]]; then
            echo "Warning: Task #$number not found, skipping"
            continue
        fi
        
        # Change checkbox to [D] and add deletion metadata
        task_line=$(echo "$task_line" | sed 's/\[.\]/[D]/')
        
        # Remove any existing date, then add deletion metadata
        task_line=$(echo "$task_line" | sed 's/ *([^)]*)$//')
        task_line="$task_line (deleted $delete_date, expires $expire_date)"
        
        # Find task line number to also remove following notes
        local task_line_num=$(grep -n "^- \[.\] \*\*#$number\*\* \|^  - \[.\] \*\*#$number\*\* " "$TODO_FILE" | head -1 | cut -d: -f1)
        
        if [[ -n "$task_line_num" ]]; then
            # Remove the task line
            sed_inplace "${task_line_num}d" "$TODO_FILE"
            
            # Remove any following blockquote notes (lines starting with "  > " or "    > ")
            # Keep removing lines as long as they're blockquotes
            while true; do
                local next_line=$(sed -n "${task_line_num}p" "$TODO_FILE")
                if [[ "$next_line" =~ ^"  > " ]] || [[ "$next_line" =~ ^"    > " ]]; then
                    sed_inplace "${task_line_num}d" "$TODO_FILE"
                else
                    break
                fi
            done
        fi
        
        # Add to Deleted section
        ensure_deleted_section
        local deleted_section=$(grep -n "^## Deleted Tasks" "$TODO_FILE" | cut -d: -f1)
        if [[ -n "$deleted_section" ]]; then
            if [[ "$(uname)" == "Darwin" ]]; then
                local temp_file=$(mktemp)
                head -n "$deleted_section" "$TODO_FILE" > "$temp_file"
                echo "$task_line" >> "$temp_file"
                tail -n +$((deleted_section + 1)) "$TODO_FILE" >> "$temp_file"
                mv "$temp_file" "$TODO_FILE"
            else
                sed_inplace "${deleted_section}a$task_line" "$TODO_FILE"
            fi
        fi
        
        # Log the action
        local task_description=$(echo "$task_line" | sed 's/.*\*\*#[0-9.]*\*\* *//' | sed 's/ *`.*$//' | sed 's/ *(deleted.*//')
        log_todo_action "DELETE" "$number" "$task_description"
        
        deleted_count=$((deleted_count + 1))
    done
    
    update_footer
    
    echo "Moved $deleted_count task(s) to Deleted section"
}

# Function to ensure Deleted Tasks section exists
ensure_deleted_section() {
    if ! grep -q "^## Deleted Tasks" "$TODO_FILE"; then
        # Add Deleted section before Recently Completed
        local recently_completed_line=$(grep -n "^## Recently Completed" "$TODO_FILE" | cut -d: -f1)
        if [[ -n "$recently_completed_line" ]]; then
            sed_inplace "${recently_completed_line}i## Deleted Tasks\n" "$TODO_FILE"
        fi
    fi
}

# Function to purge expired deleted tasks
purge_expired_deleted_tasks() {
    local current_date=$(date +"%Y-%m-%d")
    local purged_count=0
    
    # Find and remove expired tasks
    while IFS= read -r line; do
        if [[ "$line" =~ "expires ([0-9]{4}-[0-9]{2}-[0-9]{2})" ]]; then
            local expire_date="${match[1]}"
            # Compare dates (simple string comparison works for YYYY-MM-DD format)
            if [[ "$expire_date" < "$current_date" ]]; then
                # Task expired, remove it
                sed_inplace "/$(echo "$line" | sed 's/[]\/$*.^[]/\\&/g')/d" "$TODO_FILE"
                purged_count=$((purged_count + 1))
            fi
        fi
    done < <(grep "^\- \[D\]" "$TODO_FILE")
    
    if [[ $purged_count -gt 0 ]]; then
        echo "Auto-purged $purged_count expired task(s)" >&2
    fi
}

# Function to restore a task and its subtasks from Recently Completed to Tasks
restore_task() {
    local task_id="$1"
    
    if [[ -z "$task_id" ]]; then
        echo "Error: Please provide task ID"
        echo "Usage: ./scripts/todo/todo.zsh restore <id>"
        return 1
    fi
    
    # Simple implementation: move the task back to Tasks section
    # Get the task line (from Recently Completed or Deleted section)
    local task_line=$(grep "^- \[[xD~>\-]\] \*\*#$task_id\*\* " "$TODO_FILE" | head -1)
    if [[ -z "$task_line" ]]; then
        echo "Error: Could not find task #$task_id in Recently Completed or Deleted section"
        return 1
    fi
    
    # Restore to [ ] checkbox and remove metadata
    task_line=$(echo "$task_line" | sed 's/\[.\]/[ ]/')
    task_line=$(echo "$task_line" | sed 's/ *(deleted.*//' | sed 's/ *(completed.*//' | sed 's/ *(.*)$//')
    
    # Remove from current section (Recently Completed or Deleted)
    sed_inplace "/^- \[[xD~>\-]\] \*\*#$task_id\*\* /d" "$TODO_FILE"
    
    # Add to Tasks section
    local tasks_section=$(grep -n "^## Tasks" "$TODO_FILE" | cut -d: -f1)
    if [[ -n "$tasks_section" ]]; then
        # Insert after the "## Tasks" line
        if [[ "$(uname)" == "Darwin" ]]; then
            local temp_file=$(mktemp)
            head -n "$tasks_section" "$TODO_FILE" > "$temp_file"
            echo "$task_line" >> "$temp_file"
            tail -n +$((tasks_section + 1)) "$TODO_FILE" >> "$temp_file"
            mv "$temp_file" "$TODO_FILE"
        else
            sed_inplace "${tasks_section}a$task_line" "$TODO_FILE"
        fi
    else
        echo "Error: Tasks section not found"
        return 1
    fi
    
    update_footer
    
    # Get task description for logging
    local task_description=$(echo "$task_line" | sed 's/.*\*\*#[0-9.]*\*\* *//' | sed 's/ *`.*$//' | sed 's/ *([^)]*)$//')
    
    # Log the action
    log_todo_action "RESTORE" "$task_id" "$task_description"
    
    echo "Restored task #$task_id to Tasks section"
}

# Function to ensure Task Metadata section exists
ensure_metadata_section() {
    if ! grep -q "^## Task Metadata" "$TODO_FILE"; then
        # Add metadata section at the end
        echo "" >> "$TODO_FILE"
        echo "## Task Metadata" >> "$TODO_FILE"
        echo "" >> "$TODO_FILE"
        echo "Task relationships and dependencies (managed by todo.zsh tool)." >> "$TODO_FILE"
        echo "View with: \`./scripts/todo/todo.zsh show <task-id>\`" >> "$TODO_FILE"
        echo "" >> "$TODO_FILE"
        echo "<!-- TASK RELATIONSHIPS" >> "$TODO_FILE"
        echo "-->" >> "$TODO_FILE"
    fi
}

# Function to add a task relationship
add_relationship() {
    local task_id="$1"
    local rel_type="$2"
    local target_tasks="$3"
    
    # Ensure metadata section exists
    ensure_metadata_section
    
    # Remove any existing relationship of this type for this task
    sed_inplace "/^$task_id:$rel_type:/d" "$TODO_FILE"
    
    # Add new relationship before the closing -->
    sed_inplace "/^-->/i$task_id:$rel_type:$target_tasks" "$TODO_FILE"
    
    update_footer
}

# Function to remove a task relationship
remove_relationship() {
    local task_id="$1"
    local rel_type="$2"
    local target_task="$3"
    
    if [[ -n "$target_task" ]]; then
        # Remove specific target from relationship list
        # This is complex, for now just remove the whole relationship
        sed_inplace "/^$task_id:$rel_type:/d" "$TODO_FILE"
    else
        # Remove all relationships of this type for this task
        sed_inplace "/^$task_id:$rel_type:/d" "$TODO_FILE"
    fi
    
    update_footer
}

# Function to get relationships for a task
get_relationships() {
    local task_id="$1"
    
    # Extract relationships from metadata section
    sed -n '/<!-- TASK RELATIONSHIPS/,/-->/p' "$TODO_FILE" | \
        grep "^$task_id:" | \
        while IFS=: read -r id rel_type targets; do
            echo "$rel_type:$targets"
        done
}

# Function to show a task with its relationships
show_task() {
    local task_id="$1"
    
    if [[ -z "$task_id" ]]; then
        echo "Error: Please provide task ID"
        echo "Usage: ./scripts/todo/todo.zsh show <id>"
        return 1
    fi
    
    # Find and display the task
    local task_line=$(grep "^- \[.\] \*\*#$task_id\*\* \|^  - \[.\] \*\*#$task_id\*\* " "$TODO_FILE" | head -1)
    
    if [[ -z "$task_line" ]]; then
        echo "Error: Task #$task_id not found"
        return 1
    fi
    
    echo "$task_line"
    
    # Get line number for note detection
    local task_line_num=$(grep -n "^- \[.\] \*\*#$task_id\*\* \|^  - \[.\] \*\*#$task_id\*\* " "$TODO_FILE" | head -1 | cut -d: -f1)
    
    # Display notes if they exist (blockquotes immediately after task)
    if [[ -n "$task_line_num" ]]; then
        local next_line_num=$((task_line_num + 1))
        local next_line=$(sed -n "${next_line_num}p" "$TODO_FILE")
        while [[ "$next_line" =~ ^"  > " ]] || [[ "$next_line" =~ ^"    > " ]]; do
            echo "$next_line"
            next_line_num=$((next_line_num + 1))
            next_line=$(sed -n "${next_line_num}p" "$TODO_FILE")
        done
    fi
    
    # Find and display subtasks if this is a parent
    if [[ "$task_id" != *.* ]]; then
        grep "^  - \[.\] \*\*#$task_id\." "$TODO_FILE" | while read -r subtask; do
            echo "$subtask"
        done
    fi
    
    # Display relationships if any exist
    local has_relationships=false
    while IFS=: read -r rel_type targets; do
        if [[ -n "$rel_type" ]]; then
            has_relationships=true
            # Format relationship type (replace - with space, capitalize)
            local formatted_type=""
            case "$rel_type" in
                completed-by) formatted_type="Completed by" ;;
                depends-on) formatted_type="Depends on" ;;
                blocks) formatted_type="Blocks" ;;
                related-to) formatted_type="Related to" ;;
                duplicate-of) formatted_type="Duplicate of" ;;
                *) formatted_type="$rel_type" ;;
            esac
            echo "  ↳ $formatted_type: $targets"
        fi
    done < <(get_relationships "$task_id")
    
    if [[ "$has_relationships" == false ]]; then
        echo "  (No relationships)"
    fi
}

# Function to manage task relationships
relate_task() {
    local task_id=""
    local rel_type=""
    local targets=""
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --completed-by)
                rel_type="completed-by"
                targets="$2"
                shift 2
                ;;
            --depends-on)
                rel_type="depends-on"
                targets="$2"
                shift 2
                ;;
            --blocks)
                rel_type="blocks"
                targets="$2"
                shift 2
                ;;
            --related-to)
                rel_type="related-to"
                targets="$2"
                shift 2
                ;;
            --duplicate-of)
                rel_type="duplicate-of"
                targets="$2"
                shift 2
                ;;
            *)
                task_id="$1"
                shift
                ;;
        esac
    done
    
    if [[ -z "$task_id" ]] || [[ -z "$rel_type" ]] || [[ -z "$targets" ]]; then
        echo "Error: Missing required parameters"
        echo "Usage: ./scripts/todo/todo.zsh relate <id> --<relation-type> <target-ids>"
        echo ""
        echo "Relation types:"
        echo "  --completed-by <ids>   Task completed by other task(s)"
        echo "  --depends-on <ids>     Task depends on other task(s)"
        echo "  --blocks <ids>         Task blocks other task(s)"
        echo "  --related-to <ids>     General relationship"
        echo "  --duplicate-of <id>    Task is duplicate of another"
        return 1
    fi
    
    # Verify task exists
    if ! grep -q "\*\*#$task_id\*\*" "$TODO_FILE"; then
        echo "Error: Task #$task_id not found"
        return 1
    fi
    
    # Add the relationship
    add_relationship "$task_id" "$rel_type" "$targets"
    
    # Log the action
    log_todo_action "RELATE" "$task_id" "$rel_type: $targets"
    
    echo "Added relationship: #$task_id $rel_type $targets"
}

# Function to add a note to a task (using blockquote format)
add_note() {
    local task_id="$1"
    local note_text="$2"
    
    if [[ -z "$task_id" ]] || [[ -z "$note_text" ]]; then
        echo "Error: Please provide task ID and note text"
        echo "Usage: ./scripts/todo/todo.zsh note <id> <note-text>"
        return 1
    fi
    
    # Verify task exists
    local task_line_num=$(grep -n "^- \[.\] \*\*#$task_id\*\* \|^  - \[.\] \*\*#$task_id\*\* " "$TODO_FILE" | head -1 | cut -d: -f1)
    
    if [[ -z "$task_line_num" ]]; then
        echo "Error: Task #$task_id not found"
        return 1
    fi
    
    # Format note as blockquote with proper indentation
    local indent=""
    local task_line=$(sed -n "${task_line_num}p" "$TODO_FILE")
    if [[ "$task_line" =~ ^"  - " ]]; then
        # This is a subtask, needs extra indentation
        indent="  "
    fi
    
    # Create blockquote note
    local note_line="${indent}  > ${note_text}"
    
    # Insert note after the task line
    if [[ "$(uname)" == "Darwin" ]]; then
        local temp_file=$(mktemp)
        head -n "$task_line_num" "$TODO_FILE" > "$temp_file"
        echo "$note_line" >> "$temp_file"
        tail -n +$((task_line_num + 1)) "$TODO_FILE" >> "$temp_file"
        mv "$temp_file" "$TODO_FILE"
    else
        sed_inplace "${task_line_num}a\\$note_line" "$TODO_FILE"
    fi
    
    update_footer
    
    # Log the action
    log_todo_action "NOTE" "$task_id" "$note_text"
    
    echo "Added note to task #$task_id"
}

# Function to lint (identify) formatting issues
lint_todo() {
    local issues_found=0
    
    echo "🔍 Checking TODO.md for formatting issues..."
    echo ""
    
    # Check for indentation issues
    echo "📋 Checking indentation:"
    local indent_issues=0
    
    # Find subtasks that are not properly indented (should start with "  -")
    while IFS= read -r line; do
        if [[ "$line" =~ "^- \[.*\] \*\*#[0-9]+\.[0-9]+\*\* " ]]; then
            echo "  ❌ Subtask not indented: $line"
            indent_issues=$((indent_issues + 1))
            issues_found=$((issues_found + 1))
        fi
    done < "$TODO_FILE"
    
    if [[ $indent_issues -eq 0 ]]; then
        echo "  ✅ All subtasks properly indented"
    else
        echo "  📊 Found $indent_issues indentation issues"
    fi
    echo ""
    
    # Check for malformed checkboxes
    echo "☑️  Checking checkboxes:"
    local checkbox_issues=0
    
    # Find malformed checkboxes
    while IFS= read -r line; do
        if [[ "$line" =~ "^- \[.*\] " || "$line" =~ "^  - \[.*\] " ]]; then
            # Check for various malformed checkbox patterns
            if [[ "$line" =~ "\[  \]" || "$line" =~ "\[   \]" || "$line" =~ "\[    \]" || "$line" =~ "\[\]" ]]; then
                echo "  ❌ Malformed checkbox: $line"
                checkbox_issues=$((checkbox_issues + 1))
                issues_found=$((issues_found + 1))
            fi
        fi
    done < "$TODO_FILE"
    
    if [[ $checkbox_issues -eq 0 ]]; then
        echo "  ✅ All checkboxes properly formatted"
    else
        echo "  📊 Found $checkbox_issues checkbox issues"
    fi
    echo ""
    
    # Check for orphaned subtasks (subtasks without parent tasks)
    echo "🔗 Checking for orphaned subtasks:"
    local orphan_issues=0
    local seen_parents=()
    
    # First pass: collect all parent task IDs
    while IFS= read -r line; do
        if [[ "$line" == "- ["*"**#"*"**"* ]] && [[ "$line" != *"**#"*"."*"**"* ]]; then
            local parent_id=$(echo "$line" | grep -o '#[0-9]\+' | sed 's/#//' | head -1)
            seen_parents+=("$parent_id")
        fi
    done < "$TODO_FILE"
    
    # Second pass: check all subtasks have parents
    while IFS= read -r line; do
        if [[ "$line" =~ '#([0-9]+)\.([0-9]+)' ]]; then
            local parent_id="${match[1]}"
            local subtask_id="${match[1]}.${match[2]}"
            if [[ ! " ${seen_parents[@]} " =~ " ${parent_id} " ]]; then
                echo "  ❌ Orphaned subtask #$subtask_id (parent #$parent_id not found)"
                orphan_issues=$((orphan_issues + 1))
                issues_found=$((issues_found + 1))
            fi
        fi
    done < <(grep "\*\*#[0-9]\+\.[0-9]\+\*\*" "$TODO_FILE")
    
    if [[ $orphan_issues -eq 0 ]]; then
        echo "  ✅ No orphaned subtasks"
    else
        echo "  📊 Found $orphan_issues orphaned subtasks"
    fi
    echo ""
    
    # Check for duplicate task IDs
    echo "🔢 Checking for duplicate task IDs:"
    local duplicate_issues=0
    local task_ids=()
    local duplicates=()
    
    while IFS= read -r line; do
        if [[ "$line" =~ '#([0-9]+\.[0-9]+|[0-9]+)' ]]; then
            local task_id="${match[1]}"
            if [[ " ${task_ids[@]} " =~ " ${task_id} " ]]; then
                if [[ ! " ${duplicates[@]} " =~ " ${task_id} " ]]; then
                    echo "  ❌ Duplicate task ID: #$task_id"
                    duplicates+=("$task_id")
                    duplicate_issues=$((duplicate_issues + 1))
                    issues_found=$((issues_found + 1))
                fi
            else
                task_ids+=("$task_id")
            fi
        fi
    done < <(grep "\*\*#[0-9]\|\*\*#[0-9]\+\.[0-9]\+" "$TODO_FILE")
    
    if [[ $duplicate_issues -eq 0 ]]; then
        echo "  ✅ No duplicate task IDs"
    else
        echo "  📊 Found $duplicate_issues duplicate task IDs"
    fi
    echo ""
    
    # Check for empty lines in task sections
    echo "📄 Checking for problematic empty lines:"
    local empty_line_issues=0
    local in_tasks=false
    local line_num=0
    
    while IFS= read -r line; do
        line_num=$((line_num + 1))
        if [[ "$line" == "## Tasks" ]] || [[ "$line" == "## Deleted Tasks" ]] || [[ "$line" == "## Recently Completed" ]]; then
            in_tasks=true
        elif [[ "$line" =~ ^"## " ]]; then
            in_tasks=false
        elif [[ $in_tasks == true ]] && [[ -z "$line" ]]; then
            # Check if previous and next lines are both tasks (not blockquotes or other content)
            local prev_line=$(sed -n "$((line_num-1))p" "$TODO_FILE")
            local next_line=$(sed -n "$((line_num+1))p" "$TODO_FILE")
            # Empty line between tasks is problematic
            if [[ "$prev_line" == "- ["*"**#"* ]] && [[ "$next_line" == "- ["*"**#"* ]]; then
                echo "  ⚠️  Empty line between tasks at line $line_num"
                empty_line_issues=$((empty_line_issues + 1))
                issues_found=$((issues_found + 1))
            fi
        fi
    done < "$TODO_FILE"
    
    if [[ $empty_line_issues -eq 0 ]]; then
        echo "  ✅ No problematic empty lines"
    else
        echo "  📊 Found $empty_line_issues empty line issues"
    fi
    echo ""
    
    # Summary
    if [[ $issues_found -eq 0 ]]; then
        echo "🎉 No formatting issues found! TODO.md is properly formatted."
    else
        echo "⚠️  Found $issues_found total formatting issues"
        echo "💡 Run './scripts/todo/todo.zsh --reformat --dry-run' to see what would be fixed"
        echo "💡 Run './scripts/todo/todo.zsh --reformat' to apply fixes"
    fi
}

# Function to reformat (fix) formatting issues
reformat_todo() {
    local dry_run=false
    
    # Check for --dry-run flag
    if [[ "$1" == "--dry-run" ]]; then
        dry_run=true
        echo "🔍 DRY RUN: Showing what would be fixed..."
    else
        echo "🔧 Applying formatting fixes..."
    fi
    echo ""
    
    local fixes_applied=0
    
    # Fix indentation issues
    echo "📋 Fixing indentation:"
    local indent_fixes=0
    
    # Find subtasks that are not properly indented
    while IFS= read -r line; do
        if [[ "$line" =~ "^- \[.*\] \*\*#[0-9]+\.[0-9]+\*\* " ]]; then
            local fixed_line="  $line"
            if [[ "$dry_run" == true ]]; then
                echo "  🔄 Would fix: $line"
                echo "  ➡️  To:        $fixed_line"
            else
                sed_inplace "s|^$line|$fixed_line|" "$TODO_FILE"
                echo "  ✅ Fixed: $line"
            fi
            indent_fixes=$((indent_fixes + 1))
            fixes_applied=$((fixes_applied + 1))
        fi
    done < "$TODO_FILE"
    
    if [[ $indent_fixes -eq 0 ]]; then
        echo "  ✅ No indentation issues found"
    else
        if [[ "$dry_run" == true ]]; then
            echo "  📊 Would fix $indent_fixes indentation issues"
        else
            echo "  📊 Fixed $indent_fixes indentation issues"
        fi
    fi
    echo ""
    
    # Fix checkbox issues
    echo "☑️  Fixing checkboxes:"
    local checkbox_fixes=0
    
    # Check if there are malformed checkboxes
    if grep -q "\[  \]\|\[   \]\|\[    \]\|\[\]" "$TODO_FILE"; then
        if [[ "$dry_run" == true ]]; then
            echo "  🔄 Would fix malformed checkboxes:"
            grep -n "\[  \]\|\[   \]\|\[    \]\|\[\]" "$TODO_FILE" | while read -r line; do
                echo "    Line: $line"
            done
        else
            # Use the existing normalize_checkboxes function directly
            normalize_checkboxes
            echo "  ✅ Fixed malformed checkboxes"
        fi
        checkbox_fixes=$((checkbox_fixes + 1))
        fixes_applied=$((fixes_applied + 1))
    fi
    
    if [[ $checkbox_fixes -eq 0 ]]; then
        echo "  ✅ No checkbox issues found"
    else
        if [[ "$dry_run" == true ]]; then
            echo "  📊 Would fix $checkbox_fixes checkbox patterns"
        else
            echo "  📊 Fixed $checkbox_fixes checkbox patterns"
        fi
    fi
    echo ""
    
    # Summary
    if [[ "$dry_run" == true ]]; then
        echo "💡 Run './scripts/todo/todo.zsh --reformat' to apply these fixes"
    elif [[ $fixes_applied -gt 0 ]]; then
        echo "🎉 Applied $fixes_applied formatting fixes to TODO.md"
    else
        echo "🎉 No formatting issues found - TODO.md is already properly formatted!"
    fi
}

# Function to edit todo file
edit_todo() {
    ${EDITOR:-nano} "$TODO_FILE"
}

# Function to view TODO log
view_log() {
    local filter="$1"
    local lines="$2"
    
    if [[ ! -f "$LOG_FILE" ]]; then
        echo "No log file found at $LOG_FILE"
        return 1
    fi
    
    echo "📋 TODO Tool Log"
    echo "================="
    echo ""
    
    if [[ -n "$filter" ]]; then
        echo "Filtering by: $filter"
        echo ""
        grep -i "$filter" "$LOG_FILE" | head -n "${lines:-50}"
    else
        head -n "${lines:-50}" "$LOG_FILE"
    fi
}




# Initialize log file
init_log_file

# Initialize TODO file
init_todo_file

# Main script logic
case "${1:-}" in
    "add")
        # Validate arguments before proceeding
        shift
        if ! validate_command_args "add" "$@"; then
            exit 1
        fi
        add_todo "$1" "$2"
        ;;
    "add-subtask")
        # Validate arguments before proceeding
        shift
        if ! validate_command_args "add-subtask" "$@"; then
            exit 1
        fi
        add_subtask "$1" "$2" "$3"
        ;;
    "list")
        # Validate arguments before proceeding
        shift
        if ! validate_command_args "list" "$@"; then
            exit 1
        fi
        list_todos "$@"
        ;;
    "complete")
        # Validate arguments before proceeding
        shift
        if ! validate_command_args "complete" "$@"; then
            exit 1
        fi
        complete_todo "$@"
        ;;
    "undo")
        # Validate arguments before proceeding
        shift
        if ! validate_command_args "undo" "$@"; then
            exit 1
        fi
        undo_todo "$1"
        ;;
    "modify")
        # Validate arguments before proceeding
        shift
        if ! validate_command_args "modify" "$@"; then
            exit 1
        fi
        modify_todo "$1" "$2" "$3"
        ;;
    "archive")
        # Validate arguments before proceeding
        shift
        if ! validate_command_args "archive" "$@"; then
            exit 1
        fi
        # Parse task IDs and reason flag
        local task_ids=()
        local reason_arg=""
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --reason)
                    reason_arg="--reason"
                    reason_value="$2"
                    shift 2
                    ;;
                *)
                    task_ids+=("$1")
                    shift
                    ;;
            esac
        done
        # Archive each task with reason if provided
        for task_id in "${task_ids[@]}"; do
            if [[ -n "$reason_arg" ]]; then
                archive_task "$task_id" --reason "$reason_value"
            else
                archive_task "$task_id"
            fi
        done
        ;;
    "delete")
        # Validate arguments before proceeding
        shift
        if ! validate_command_args "delete" "$@"; then
            exit 1
        fi
        delete_task "$@"
        ;;
    "relate")
        # Validate arguments before proceeding
        shift
        if ! validate_command_args "relate" "$@"; then
            exit 1
        fi
        relate_task "$@"
        ;;
    "note")
        # Validate arguments before proceeding
        shift
        if ! validate_command_args "note" "$@"; then
            exit 1
        fi
        add_note "$1" "$2"
        ;;
    "show")
        # Validate arguments before proceeding
        shift
        if ! validate_command_args "show" "$@"; then
            exit 1
        fi
        show_task "$1"
        ;;
    "restore")
        # Validate arguments before proceeding
        shift
        if ! validate_command_args "restore" "$@"; then
            exit 1
        fi
        restore_task "$1"
        ;;
    "--lint")
        lint_todo
        ;;
    "--reformat")
        if [[ "$2" == "--dry-run" ]]; then
            reformat_todo "--dry-run"
        else
            reformat_todo
        fi
        ;;
    "edit")
        edit_todo
        ;;
    "log")
        # Validate arguments before proceeding
        shift
        if ! validate_command_args "log" "$@"; then
            exit 1
        fi
        if [[ "$1" == "--filter" && -n "$2" ]]; then
            view_log "$2" "$3"
        elif [[ "$1" == "--lines" && -n "$2" ]]; then
            view_log "" "$2"
        else
            view_log
        fi
        ;;
    *)
        show_usage
        ;;
esac