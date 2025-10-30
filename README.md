# todo - AI-Agent First TODO List Tracker

**Keep AI agents on track and help humans supervise their work**

A powerful, zero-interaction TODO list management system designed specifically for AI-agent workflows. Built for speed, simplicity, and AI compatibility.

## Features

### Phase 1: Essential Features

- **Bulk Operations**: Complete or archive multiple tasks in one command
  ```zsh
  ./todo.zsh complete 107 108 109
  ./todo.zsh complete 104 --with-subtasks
  ./todo.zsh complete 104.3-10  # Range notation
  ```

- **Archive States**: Accurate task lifecycle with visual indicators
  ```zsh
  ./todo.zsh archive 109 --reason obsolete    # [~] checkbox
  ./todo.zsh archive 110 --reason wontfix     # [-] checkbox
  ./todo.zsh archive 104 --reason 'completed-by:107,108'  # [>] checkbox
  ```

- **Enhanced Filtering**: Powerful queries for task discovery
  ```zsh
  ./todo.zsh list --incomplete-only   # Focus on pending work
  ./todo.zsh list --parents-only      # High-level overview
  ./todo.zsh list --has-subtasks      # Find active projects
  ```

- **Soft Delete**: Safe deletion with 30-day recovery
  ```zsh
  ./todo.zsh delete 115               # Soft delete
  ./todo.zsh restore 115              # Restore if needed
  ```

### Phase 2: High Value Features

- **Task Relationships**: Track dependencies and connections
  ```zsh
  ./todo.zsh relate 110 --depends-on 104
  ./todo.zsh relate 104 --completed-by '107,108'
  ./todo.zsh show 110  # Display with relationships
  ```

- **Task Notes**: Add context using markdown blockquotes
  ```zsh
  ./todo.zsh note 110 'Testing shows timeout issues'
  ```

- **Enhanced Lint**: Comprehensive validation
  - Orphaned subtasks detection
  - Duplicate task ID detection
  - Empty line detection
  - Indentation checking
  - Checkbox validation

## Design Principles

- **Zero-Interaction**: No prompts - AI agents can use without blocking
- **Simple Sequential IDs**: Just 1, 2, 3... (human-friendly)
- **Fast Local Operations**: Instant responses, no API latency
- **Pure Markdown**: Everything in TODO.md (git-friendly)
- **Backward Compatible**: All existing workflows preserved

## Installation

```zsh
# Clone the repository
git clone https://github.com/fxstein/todo.git
cd todo

# Make executable
chmod +x todo.zsh

# Optional: Add to PATH
sudo ln -s $(pwd)/todo.zsh /usr/local/bin/todo

# Or use directly
./todo.zsh --help
```

## Quick Start

```zsh
# Initialize TODO.md in your project
./todo.zsh add "First task" "#feature"
# Added: #1 First task

# Add subtasks
./todo.zsh add-subtask 1 "Design phase" "#design"
./todo.zsh add-subtask 1 "Implementation" "#dev"

# Complete tasks
./todo.zsh complete 1 --with-subtasks

# View all tasks
./todo.zsh list

# View only pending work
./todo.zsh list --incomplete-only
```

## File Structure

```
your-project/
  TODO.md              # Your tasks (stays in your repo)
  .todo/               # Support files (gitignored)
    .todo.log          # Operation log
    .todo_serial       # Next ID counter
    archives/          # Old archived tasks
    templates/         # Task templates
```

## Configuration

Edit the paths at the top of `todo.zsh`:

```zsh
# Configuration
TODO_FILE="/path/to/your/TODO.md"
SERIAL_FILE="/path/to/your/.todo/.todo_serial"
LOG_FILE="/path/to/your/.todo/.todo.log"
```

Or set environment variables:

```zsh
export TODO_FILE="$HOME/project/TODO.md"
export TODO_SERIAL="$HOME/project/.todo/.todo_serial"
export TODO_LOG="$HOME/project/.todo/.todo.log"
```

## Usage Examples

### Bulk Operations
```zsh
# Complete multiple tasks
./todo.zsh complete 10 11 12

# Complete parent and all children
./todo.zsh complete 5 --with-subtasks

# Complete range of subtasks
./todo.zsh complete 10.3-10.15
```

### Task States
```zsh
# Normal completion
./todo.zsh complete 20
./todo.zsh archive 20
# Result: [x] Task (completed)

# Task no longer needed
./todo.zsh archive 21 --reason obsolete
# Result: [~] Task (obsolete)

# Won't implement
./todo.zsh archive 22 --reason wontfix
# Result: [-] Task (wontfix)

# Completed by other work
./todo.zsh archive 23 --reason 'completed-by:24,25'
# Result: [>] Task (completed-by:24,25)
```

### Filtering
```zsh
# Show only incomplete tasks (no archive)
./todo.zsh list --incomplete-only

# Show only parent tasks (no subtasks)
./todo.zsh list --parents-only

# Show only tasks with subtasks
./todo.zsh list --has-subtasks

# Combine filters
./todo.zsh list --has-subtasks --parents-only --incomplete-only
```

### Relationships
```zsh
# Add dependencies
./todo.zsh relate 30 --depends-on 25

# Show what blocks what
./todo.zsh relate 30 --blocks 35

# Document completion chain
./todo.zsh relate 40 --completed-by '38,39'

# View relationships
./todo.zsh show 30
# Output:
#   - [ ] **#30** Task name
#     ↳ Depends on: 25
#     ↳ Blocks: 35
```

### Task Notes
```zsh
# Add context to tasks
./todo.zsh note 50 'Need to test with production data'
./todo.zsh note 50 'Also check edge cases'

# Notes display as blockquotes
./todo.zsh show 50
# Output:
#   - [ ] **#50** Task name
#     > Need to test with production data
#     > Also check edge cases
```

## AI-Agent Integration

This tool is specifically designed for AI agents (like Claude, GPT, Gemini) to manage tasks during long-running sessions:

### Why AI-Agent First?

- **No Prompts**: All commands run without confirmation
- **Predictable**: Simple, consistent command patterns
- **Fast**: Local files, instant operations
- **Recoverable**: Soft delete, archive states
- **Trackable**: Complete audit trail in `.todo.log`

### AI Agent Usage Pattern

```zsh
# Agent creates tasks as it works
./todo.zsh add "Fix authentication bug" "#bugfix"
./todo.zsh add-subtask 1 "Investigate root cause" "#investigation"
./todo.zsh add-subtask 1 "Implement fix" "#development"
./todo.zsh add-subtask 1 "Add tests" "#testing"

# Agent marks progress
./todo.zsh complete 1.1  # Investigation done
./todo.zsh complete 1.2  # Fix implemented
./todo.zsh complete 1.3  # Tests added

# Agent completes parent
./todo.zsh complete 1

# Human reviews
./todo.zsh list --incomplete-only
./todo.zsh show 1
```

### Human Supervision

Humans can easily review AI agent work:

```zsh
# What's the agent working on?
./todo.zsh list --has-subtasks --parents-only

# What progress has been made?
./todo.zsh list --incomplete-only

# Detailed task view
./todo.zsh show <task-id>

# Check the log
./todo.zsh log --lines 50
```

## Documentation

- **Design Document**: `docs/TODO_TAGGING_SYSTEM_DESIGN.md`
- **Implementation Proposal**: `docs/TODO_TOOL_IMPROVEMENTS.md` (comprehensive)
- **Help**: Run `./todo.zsh --help` for complete command reference

## Advanced Features

### Repository Context

Tag tasks with repository information:

```zsh
./todo.zsh add "Fix bug" "#bugfix" "@frontend" "@feature-branch"
# Result: Task tagged with repo/branch context
```

### Validation

```zsh
# Comprehensive lint checking
./todo.zsh --lint

# Checks:
# ✓ Indentation
# ✓ Checkboxes
# ✓ Orphaned subtasks
# ✓ Duplicate IDs
# ✓ Empty lines
```

### Auto-Fix

```zsh
# Preview fixes
./todo.zsh --reformat --dry-run

# Apply fixes
./todo.zsh --reformat
```

## Why This Tool?

### For AI Agents

Traditional TODO tools require human interaction (confirmations, selections, prompts). This tool is **designed for automated workflows**:

- Every command succeeds or fails cleanly
- No interactive prompts
- Predictable outputs
- Fast operations
- Complete audit trail

### For Humans

Supervising AI agents requires visibility:

- **Quick Overview**: See what the agent is working on
- **Progress Tracking**: Monitor completion status
- **Context Preservation**: Relationships and notes explain why
- **Safe Operations**: Soft delete, archive states preserve history
- **Powerful Filtering**: Find exactly what you need

### For Teams

Git-based workflow enables collaboration:

- **Version Controlled**: TODO.md tracked in git
- **Merge Friendly**: Simple text format
- **No Conflicts**: Sequential IDs prevent collisions
- **Audit Trail**: Complete history in `.todo.log`

## Status Indicators

| Checkbox | Meaning | Usage |
|----------|---------|-------|
| `[ ]` | Pending | Active tasks |
| `[x]` | Completed | Normal completion |
| `[~]` | Obsolete/Duplicate | Task no longer needed |
| `[-]` | Won't Fix | Decided not to implement |
| `[>]` | Completed By | Finished by other tasks |
| `[D]` | Deleted | Soft-deleted (30-day recovery) |

## Contributing

Contributions welcome! This tool was built iteratively with real usage feedback.

See `docs/TODO_TOOL_IMPROVEMENTS.md` for the complete implementation proposal and design decisions.

## License

Apache License 2.0 - See LICENSE file

## Credits

Built by [fxstein](https://github.com/fxstein) for the AI-agent development community.

Developed through extensive real-world use in the [homeassistant](https://github.com/fxstein/homeassistant) project.

---

**"The TODO tool that AI agents actually want to use."**

