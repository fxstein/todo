# Todo Tagging System Design Document

## Overview
This document outlines the design decisions for implementing a tagging system in the `todo.zsh` script to replace the current section-based TODO structure with a more flexible, tag-based approach.

## Design Decisions

### 1. Task Format Structure
**Decision**: ID-first format with consistent structure
```
#ID Task Description #tag1 #tag2 #tag3 (date)
```

**Rationale**: 
- ID is immediately visible for quick identification
- Natural sorting by ID
- Clean parsing structure
- Consistent format across all tasks

### 2. Serial Number System
**Decision**: Auto-incrementing serial numbers with sub-task support
- Main tasks: `#1`, `#2`, `#3`, etc.
- Sub-tasks: `#3.1`, `#3.2`, `#3.3`, etc.

**Rationale**:
- Unique identification for every task
- Clear parent-child relationships
- Easy to reference specific tasks
- Maintains task history and relationships

### 3. Date Format
**Decision**: Simple date format in parentheses
```
(2025-01-19)
```

**Rationale**:
- Clean and readable
- Consistent with current format
- Easy to parse and display
- Minimal visual clutter

### 4. Tag Categories
**Decision**: Minimal set of core categories
- `#api` - API development and integration
- `#docs` - Documentation tasks
- `#bug` - Bug fixes and issues
- `#feature` - New feature development
- `#maintenance` - System maintenance and updates

**Rationale**:
- Keeps system simple and manageable
- Covers main project areas
- Easy to remember and use
- Can be extended later if needed

### 5. Status Tags
**Decision**: Core status indicators
- `#inprogress` - Task is actively being worked on
- `#blocked` - Task is blocked by external factors
- `#waiting` - Task is waiting for something/someone
- `#review` - Task is ready for review

**Rationale**:
- Covers common workflow states
- Provides visibility into task status
- Helps with project management
- Can be extended as needed

### 6. Priority Tags
**Decision**: Three-level priority system
- `#high` - High priority tasks
- `#medium` - Medium priority tasks  
- `#low` - Low priority tasks

**Rationale**:
- Simple three-tier system
- Easy to understand and use
- Covers most priority needs
- Can be extended if required

## File Structure

### New TODO.md Format
```markdown
# Home Assistant Project Todo List

> **⚠️ IMPORTANT: This file should ONLY be edited through the `./scripts/todo/todo.zsh` script!**

## Tasks
- [ ] #1 Fix Shelly device naming #api #high
- [ ] #2 Update handbook with new API features #docs #medium
- [ ] #3 Resolve Hue bridge mapping issue #bug #high
  - [ ] #3.1 Investigate device registry structure #api
  - [ ] #3.2 Document findings #docs
- [ ] #4 Add undo functionality to todo.zsh #feature #low #inprogress

## Recently Completed
- [x] #5 Review PIONIZER documentation #docs #medium (2025-01-19)
- [x] #6 Fix todo.zsh script bugs #maintenance #high (2025-01-19)

## Tags Used
- **Categories**: #api, #docs, #bug, #feature, #maintenance
- **Priority**: #high, #medium, #low
- **Status**: #inprogress, #blocked, #waiting, #review
```

## Implementation Phases

### Phase 1: Core Serial Number System
- Add auto-incrementing serial number generation
- Modify `add_todo()` to assign serial numbers
- Update `get_task_line()` to work with serial numbers
- Add serial number tracking in separate file

### Phase 2: Basic Tag Support
- Add tag parsing and storage
- Implement `tag` and `untag` commands
- Add tag filtering to `list` command
- Update help and examples

### Phase 3: Advanced Features
- Add `search` functionality
- Add `stats` command for tag analytics
- Add `next` command to show next serial number
- Add sub-task serial number support

### Phase 4: Migration
- Create migration script to convert existing TODO.md
- Add backward compatibility
- Update documentation

## Technical Implementation

### Serial Number Storage
```bash
# Store in /homeassistant/.todo_serial
echo "4" > /homeassistant/.todo_serial
```

### Task Parsing
```bash
# Extract ID, description, and tags
parse_task() {
    local line="$1"
    local id=$(echo "$line" | grep -o '^#\([0-9.]*\)' | sed 's/#//')
    local description=$(echo "$line" | sed 's/^#[0-9.]* *//' | sed 's/ *#.*$//')
    local tags=$(echo "$line" | grep -o '#[a-zA-Z0-9]*' | grep -v '^#[0-9]' | tr '\n' ' ')
    local date=$(echo "$line" | grep -o '([^)]*)' | tr -d '()')
}
```

### Enhanced Commands
```bash
# Basic operations
./scripts/todo/todo.zsh add "Fix Shelly device naming" --tags "#api #high"
./scripts/todo/todo.zsh add-subtask 1 "Investigate device registry" --tags "#api"
./scripts/todo/todo.zsh complete 1
./scripts/todo/todo.zsh undo 1

# Tag operations
./scripts/todo/todo.zsh tag 1 "#inprogress"          # Add tag to task
./scripts/todo/todo.zsh untag 1 "#inprogress"        # Remove tag from task
./scripts/todo/todo.zsh list --tag "#api"            # Filter by tag
./scripts/todo/todo.zsh list --status "#inprogress"  # Show active tasks

# ID operations
./scripts/todo/todo.zsh next                         # Show next available ID
./scripts/todo/todo.zsh get 1                        # Show task #1 details
./scripts/todo/todo.zsh search "device"              # Search task descriptions
```

## Migration Strategy

### Current Format
```markdown
- [x] **Fix todo.zsh script bugs** (2025-01-19)
```

### New Format
```markdown
- [x] #6 Fix todo.zsh script bugs #maintenance #high (2025-01-19)
```

### Migration Steps
1. Backup current TODO.md
2. Create new structure with single "Tasks" section
3. Convert existing tasks to new format with serial numbers
4. Add tags based on current section placement
5. Test new functionality
6. Update documentation

## Benefits

1. **Unique Identification**: Every task has a permanent, unique ID
2. **Flexible Categorization**: No predefined sections, use tags instead
3. **Status Tracking**: Clear visibility of what's being worked on
4. **Searchable**: Easy to find tasks by tag or description
5. **Sub-task Support**: Clear parent-child relationships
6. **Simplified Structure**: Single task list instead of multiple sections
7. **Extensible**: Easy to add new tags and categories as needed

## Future Considerations

- **Tag Analytics**: Statistics on tag usage and task completion
- **Tag Validation**: Ensure only valid tags are used
- **Tag Suggestions**: Auto-suggest tags based on task description
- **Export/Import**: Support for exporting tasks with tags
- **Integration**: Potential integration with other project management tools

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-19  
**Author**: AI Assistant  
**Status**: Design Complete - Ready for Implementation

