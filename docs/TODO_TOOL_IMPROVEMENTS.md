# TODO Tool Improvement Proposals

**Created:** 2025-10-30  
**Status:** Proposal Phase  
**Current Version:** 1.0  

## Executive Summary

Based on production usage patterns from October 2025, this document proposes 15 enhancements to the `./scripts/todo/todo.zsh` task management system. The improvements focus on bulk operations, task deletion, better lifecycle management, enhanced relationships, repository context awareness, validation, and git-based multi-developer support.

**Incorporates Existing Tasks:** This proposal consolidates 5 previously planned TODO tool improvements (tasks #43, #45, #47, #54, #78) with 10 new proposals, creating a comprehensive enhancement plan.

**Implementation Status:** 15 features approved for implementation. Interactive Review Mode (16th proposal) documented but excluded due to AI-agent incompatibility.

## Background

### Current System Capabilities

The TODO system (`./scripts/todo/todo.zsh`) currently provides:
- ✅ Serial-numbered tasks with unique IDs
- ✅ Hierarchical subtasks (parent.child format)
- ✅ Tag-based categorization
- ✅ Archive/restore functionality
- ✅ Search and filtering by tags
- ✅ Comprehensive logging (.todo.log)
- ✅ Task modification and state management
- ✅ Statistics and analytics

### Current File Structure

```
/homeassistant/
  TODO.md              # Main task list (visible in root)
  .todo.log            # Operation log (hidden)
  .todo_serial         # Next ID counter (hidden)
  scripts/todo/
    todo.zsh           # Main tool script
    TODO_TAGGING_SYSTEM_DESIGN.md
```

### Proposed File Structure

**Hybrid Approach:** Keep TODO.md discoverable in root, organize support files in `.todo/` directory.

```
/homeassistant/
  TODO.md              # Main task list (stays in root for visibility)
  .todo/
    .todo.log          # Operation log
    .todo_serial       # Next ID counter
    archives/          # Old archived tasks (from prune command)
      TODO_ARCHIVE_2025-10-30.md
      TODO_ARCHIVE_2025-09-30.md
    templates/         # Task templates (one file per template)
      solax-fix.md
      validator-impl.md
      feature-dev.md
    config.yaml        # Tool configuration (future)
  scripts/todo/
    todo.zsh           # Main tool script
    TODO_TAGGING_SYSTEM_DESIGN.md
```

**Rationale:**
- **TODO.md in root:** High visibility, easy to find, follows convention (like README.md)
- **Support files in `.todo/`:** Keeps root clean, groups related files, room for growth
- **Subdirectories:** Organized by function (archives/, templates/)
- **Version controlled:** All files tracked in git
- **Best of both worlds:** Discoverability + organization

**Migration:**
- Move `.todo.log` → `.todo/.todo.log`
- Move `.todo_serial` → `.todo/.todo_serial`
- Create `.todo/archives/` for prune command
- Create `.todo/templates/` for template system
- Update tool to use new paths

### Usage Analysis (October 2025)

**Key Patterns Observed:**
- Frequent bulk operations (archiving 4 tasks with 15+ subtasks in one session)
- Tasks completed indirectly (task A completed by work on task B)
- Tasks becoming obsolete without completion
- Need for cross-repository task tracking
- Complex task relationships and dependencies
- Manual identification of completed tasks ready for archiving

**Pain Points Identified:**
1. No native bulk operations (requires shell loops)
2. Must mark tasks complete before archiving (even if obsolete)
3. No way to delete tasks or subtasks (requires manual file editing)
4. No way to express task relationships
5. No repository/branch context
6. Limited context capture (why was task completed? by what?)
7. Manual review process for identifying archivable tasks

## Proposed Improvements

### Priority 1: Essential Enhancements

#### 1.1 Bulk Operations

**Problem:** Requires shell loops to complete multiple tasks:
```zsh
for subtask in 104.3 104.4 104.5 104.6 104.7 104.8 104.9 104.10; do 
    ./scripts/todo/todo.zsh complete $subtask
done
```

**Proposed Solution:**

```zsh
# Complete multiple tasks at once
./scripts/todo/todo.zsh complete 107 108 109

# Complete parent and all subtasks
./scripts/todo/todo.zsh complete 104 --with-subtasks

# Complete range of subtasks
./scripts/todo/todo.zsh complete 104.3-104.10

# Archive multiple tasks
./scripts/todo/todo.zsh archive 107 108 109
```

**Implementation Notes:**
- Parse multiple task IDs from command line
- Support ranges with dash notation (e.g., 104.3-104.10)
- Add `--with-subtasks` flag to operate on entire task tree
- Validate all tasks exist before performing operations
- Log each operation individually for audit trail

**Estimated Complexity:** Easy (< 1 hour)

#### 1.2 Archive Without Completion

**Problem:** Tasks that are obsolete or "won't fix" must be marked complete before archiving, which misrepresents their status.

**Current Workaround:**
```zsh
./scripts/todo/todo.zsh complete 109  # Task wasn't completed
./scripts/todo/todo.zsh archive 109    # Just needed to archive it
```

**Proposed Solution:**

```zsh
# Archive with status reason
./scripts/todo/todo.zsh archive 109 --reason "obsolete"
./scripts/todo/todo.zsh archive 109 --reason "duplicate"
./scripts/todo/todo.zsh archive 109 --reason "wontfix"
./scripts/todo/todo.zsh archive 109 --reason "completed-by:107,108"

# Force archive without completion
./scripts/todo/todo.zsh archive 109 --force

# Archive and mark as cancelled (new state)
./scripts/todo/todo.zsh cancel 109 --reason "No longer needed"
```

**Display Format:**

```markdown
## Recently Completed
- [x] **#108** Fix remote control (completed) (2025-10-30)
- [~] **#109** Apply delta correction (obsolete) (2025-10-30)
- [-] **#110** Old feature (wontfix) (2025-10-30)
- [>] **#104** Meter direction fix (completed-by: #107, #108) (2025-10-30)
```

**Status Indicators:**
- `[x]` - Completed
- `[~]` - Obsolete
- `[-]` - Won't fix / Cancelled
- `[>]` - Completed by other task(s)

**Implementation Notes:**
- Add `--reason` parameter to archive command
- Create new task states: obsolete, wontfix, cancelled, completed-by
- Update archive logic to allow incomplete tasks with reason
- Modify display format to show different checkbox styles
- Add filtering: `list --status obsolete`

**Estimated Complexity:** Easy (< 1 hour)

#### 1.3 Enhanced List Filtering

**Problem:** Limited filtering capabilities make it hard to find specific tasks.

**Current Capabilities:**
- `list` - Show all tasks
- `list --tag` - Filter by single tag
- `search` - Text search

**Proposed Solution:**

```zsh
# Filter by multiple criteria
./scripts/todo/todo.zsh list --tag solax --status pending
./scripts/todo/todo.zsh list --has-subtasks --incomplete
./scripts/todo/todo.zsh list --updated-after "2025-10-25"
./scripts/todo/todo.zsh list --priority high
./scripts/todo/todo.zsh list --repo solax-repo

# Combine filters
./scripts/todo/todo.zsh list --tag solax --repo solax-repo --status pending

# Exclude completed tasks from list
./scripts/todo/todo.zsh list --incomplete-only

# Show only parent tasks (no subtasks)
./scripts/todo/todo.zsh list --parents-only
```

**Implementation Notes:**
- Add multiple filter parameters
- Implement filter composition (AND logic)
- Maintain backward compatibility with existing list command
- Optimize filtering for large task lists

**Estimated Complexity:** Easy (< 1 hour)

#### 1.4 Task and Subtask Deletion

**Problem:** No way to delete tasks or subtasks that were created by mistake or are no longer needed. Currently requires manual editing of TODO.md file.

**Real Example:** After creating task #110 with subtasks #110.1 through #110.6, realized subtasks 110.2-110.6 were premature. Had to manually edit TODO.md to remove them since there's no delete command.

**Current Workaround:**
```zsh
# Must manually edit TODO.md file
# This violates the "ONLY edit through todo.zsh script" rule
```

**Proposed Solution (Always Soft Delete):**

```zsh
# Delete a single task (always soft delete)
./scripts/todo/todo.zsh delete 110
# Moved task #110 to Deleted section (auto-purges in 30 days)

# Delete a subtask
./scripts/todo/todo.zsh delete 110.5
# Moved subtask #110.5 to Deleted section

# Delete multiple tasks
./scripts/todo/todo.zsh delete 110 111 112
# Moved 3 tasks to Deleted section

# Delete task and all subtasks
./scripts/todo/todo.zsh delete 110 --with-subtasks
# Moved task #110 and 6 subtasks to Deleted section

# Delete range of subtasks
./scripts/todo/todo.zsh delete 110.2-110.6
# Moved 5 subtasks to Deleted section
```

**Restore Command:**

```zsh
# Restore soft-deleted task
./scripts/todo/todo.zsh restore 110
# Restored task #110 to active tasks

# List deleted tasks
./scripts/todo/todo.zsh list --deleted
# Shows all tasks in Deleted section with expiry dates
```

**Auto-Purge:**

```zsh
# Automatically purge tasks deleted more than 30 days ago
# Runs during any delete operation (silent)
# Old deleted tasks are permanently removed

# Manual purge if needed
./scripts/todo/todo.zsh purge-deleted
# Removed 5 expired tasks from Deleted section
```

**Display Format:**

```markdown
## Deleted Tasks
- [D] **#110** Enhance TODO tool (deleted 2025-10-30, expires 2025-11-29)
- [D] **#111** Old feature (deleted 2025-10-25, expires 2025-11-25)
```

**Design Philosophy:**

**Why Always Soft Delete:**
- ✅ **Safe:** Can undo mistakes (30-day window)
- ✅ **Simple:** No options to remember
- ✅ **AI-friendly:** No prompts or confirmations needed
- ✅ **Automatic:** Auto-purge keeps file clean
- ✅ **Auditable:** Full trail in .todo.log

**What's NOT Included:**
- ❌ No confirmation prompts (always succeeds)
- ❌ No --force or --permanent flags (always soft)
- ❌ No relationship warnings (keep it simple)
- ❌ No interactive decisions

**Implementation Notes:**
- Add `delete` command (no prompts)
- Move tasks to "## Deleted Tasks" section
- Add deletion date and 30-day expiry
- Log all deletions to .todo.log with full content
- Support bulk deletion (multiple IDs)
- Auto-purge expired tasks on any delete operation
- Restore command moves back to active tasks

**Use Cases:**

1. **Mistake Correction:**
   ```zsh
   ./scripts/todo/todo.zsh add "Fix bug in wrong component" "#bug"
   # Added: #115
   ./scripts/todo/todo.zsh delete 115
   # Moved task #115 to Deleted section
   ```

2. **Premature Planning:**
   ```zsh
   ./scripts/todo/todo.zsh delete 110.2-110.6
   # Moved 5 subtasks to Deleted section
   ```

3. **Accidental Deletion Recovery:**
   ```zsh
   ./scripts/todo/todo.zsh delete 115
   # Oops, didn't mean to delete that
   ./scripts/todo/todo.zsh restore 115
   # Back to active tasks
   ```

**Error Handling:**

```zsh
# Try to delete non-existent task
./scripts/todo/todo.zsh delete 999
# Error: Task #999 not found

# Try to restore non-existent task
./scripts/todo/todo.zsh restore 999
# Error: Task #999 not found in Deleted section
```

**Estimated Complexity:** Easy (< 1 hour)

### Priority 2: High Value Enhancements

#### 2.1 Task Relationships and Dependencies

**Problem:** No way to express that tasks are related, depend on each other, or complete each other.

**Real Example:** Task #104 was completed by work done in #107 and #108, but this relationship is only captured in commit messages and memory.

**Proposed Solution:**

```zsh
# Add task relationships
./scripts/todo/todo.zsh relate 104 --completed-by "107,108"
./scripts/todo/todo.zsh relate 110 --depends-on 104
./scripts/todo/todo.zsh relate 111 --blocks 112
./scripts/todo/todo.zsh relate 113 --related-to "114,115"
./scripts/todo/todo.zsh relate 116 --duplicate-of 117

# Remove relationships
./scripts/todo/todo.zsh unrelate 104 --completed-by 107

# View task with relationships
./scripts/todo/todo.zsh show 104 --with-relations

# List tasks with specific relationship
./scripts/todo/todo.zsh list --blocked
./scripts/todo/todo.zsh list --depends-on 104
./scripts/todo/todo.zsh list --ready  # no incomplete dependencies
```

**Display Format:**

```markdown
- [x] **#104** Design meter direction fix `#solax` (2025-10-30)
  ↳ Completed by: #107, #108
  ↳ Depends on: #94 (completed)
  - [x] **#104.1** Create testing infrastructure

- [ ] **#110** Implement new feature `#development`
  ↳ Depends on: #104 (completed)
  ↳ Blocks: #112
```

**Relationship Types:**
- `completed-by` - This task was completed by other task(s)
- `depends-on` - This task requires another task to be complete
- `blocks` - This task blocks another task
- `related-to` - General relationship
- `duplicate-of` - This task is a duplicate

**Storage Format (at end of TODO.md):**

```markdown
---
**Last Updated:** Thu Oct 30 14:23:45 CET 2025
**Repository:** https://github.com/fxstein/homeassistant  
**Maintenance:** Use `./scripts/todo/todo.zsh` script only

## Task Metadata

Task relationships and dependencies (managed by todo.zsh tool).
View with: `./scripts/todo/todo.zsh show <task-id>`

<!-- TASK RELATIONSHIPS
104:completed-by:107,108
104:depends-on:94
110:depends-on:104
110:blocks:112
-->
```

**Display Format:**

In IDE (raw markdown):
```markdown
## Task Metadata

Task relationships and dependencies (managed by todo.zsh tool).
View with: `./scripts/todo/todo.zsh show <task-id>`

<!-- TASK RELATIONSHIPS
104:completed-by:107,108
...
-->
```

In rendered markdown (GitHub, handbook):
```markdown
## Task Metadata

Task relationships and dependencies (managed by todo.zsh tool).
View with: `./scripts/todo/todo.zsh show <task-id>`

[relationships are hidden in HTML comments]
```

**Why At The End:**
- Keeps active tasks section clean and readable in IDE
- All relationships in one place (easy to find)
- Visible header makes section discoverable
- Instructions for users viewing rendered markdown
- Can use IDE folding to collapse section
- Easy to manage and update

**Implementation Notes:**
- Store relationships at end of TODO.md (after footer)
- Parse and display relationships when showing tasks
- Validate relationship targets exist
- Auto-update when tasks are archived
- Warning when archiving tasks that block others

**Estimated Complexity:** Medium (2-4 hours)

#### 2.2 Repository and Branch Context

**Problem:** No indication of which repository or branch a task relates to, making it unclear where work should be done. Repository short names (`ha-repo`, `solax-repo`) exist but aren't documented in TODO.md.

**Use Case:** Working across ha-repo and solax-repo, need to know which tasks belong where. New users need to understand what `@ha-repo` means.

**Proposed Solution:**

**1. Document Repository Mappings in Header:**

```markdown
# Home Assistant Project Todo List

> **⚠️ IMPORTANT: This file should ONLY be edited through the `./scripts/todo/todo.zsh` script!**

## Repository Mappings

This workspace contains multiple repositories. Tasks can be tagged with repository shortnames:

- **ha-repo** → `/homeassistant` (Main Home Assistant configuration)
  - Remote: https://github.com/fxstein/homeassistant
- **solax-repo** → `/homeassistant/custom_components/solax_modbus_repo` (SolaX Modbus integration)
  - Remote: https://github.com/fxstein/solax-modbus

View all repos: `./scripts/git-status-all.zsh`

## Tasks
[... tasks here ...]
```

**2. Tag Tasks With Repository:**

```zsh
# Add repo/branch metadata when creating tasks
./scripts/todo/todo.zsh add "Fix parallel mode" "#solax" \
  --repo solax-repo \
  --branch fix/parallel-mode-and-remote-control

# Update task with repo/branch
./scripts/todo/todo.zsh modify 110 \
  --repo solax-repo \
  --branch feature/new-sensor

# Filter by repo
./scripts/todo/todo.zsh list --repo solax-repo
./scripts/todo/todo.zsh list --repo ha-repo

# Show tasks for current branch
./scripts/todo/todo.zsh list --current-branch

# List tasks by branch
./scripts/todo/todo.zsh list --branch fix/parallel-mode-and-remote-control

# Auto-detect repo/branch
./scripts/todo/todo.zsh add "Fix issue" --auto-context
# Automatically detects current repo and branch
```

**Display Format:**

```markdown
- [ ] **#110** Fix parallel mode `#solax` [solax-repo:fix/parallel-mode]
- [ ] **#111** Update handbook `#docs` [ha-repo:main]
```

**Storage Format:**

Add metadata to task line:
```markdown
- [ ] **#110** Fix parallel mode `#solax` `@solax-repo` `@fix/parallel-mode`
```

**Integration with git-status-all.zsh:**

```zsh
./scripts/git-status-all.zsh
# Output includes:
# 📋 TODO tasks for this branch (solax-repo:fix/parallel-mode):
#   - [ ] #110 Fix parallel mode
#   - [ ] #115 Add validation
```

**Implementation Notes:**
- Add "## Repository Mappings" section to TODO.md header (one-time setup)
- Maintain repository mapping list (shortname → path → remote)
- Add `--repo` and `--branch` parameters to add/modify commands
- Store as special tags (e.g., `@solax-repo`, `@branch-name`)
- Integrate with current repository detection (pwd comparison)
- Update git-status-all.zsh to show related tasks for current branch
- Support auto-detection from current directory
- Validate repo shortnames against documented mappings

**Header Management:**
- Auto-create "## Repository Mappings" section if missing
- Detect repositories by scanning for .git directories
- Update header when new repositories are added
- Keep mappings version-controlled in TODO.md
- Human-readable format for clarity

**Estimated Complexity:** Medium (2-4 hours)

#### 2.3 Task Notes and Context

**Problem:** No way to add detailed notes or context to tasks beyond the description.

**Use Case:** When archiving #104, need to record that it was completed by other tasks, why, and what the resolution was.

**Proposed Solution:**

```zsh
# Add note to task
./scripts/todo/todo.zsh note 104 "Completed as part of #107 and #108 work"

# Append additional notes
./scripts/todo/todo.zsh note 104 --append "Oscillation issues fully resolved in production"

# Add note when completing
./scripts/todo/todo.zsh complete 104 --note "All subtasks completed by related work"

# Add note when archiving
./scripts/todo/todo.zsh archive 104 --note "Superseded by #107 and #108"

# View task with notes
./scripts/todo/todo.zsh show 104
./scripts/todo/todo.zsh show 104 --with-notes

# Edit notes in editor
./scripts/todo/todo.zsh note 104 --edit
```

**Display Format (Simple Markdown Blockquotes):**

```markdown
- [x] **#104** Design meter direction fix `#solax` (2025-10-30)
  > Completed as part of #107 and #108 work  
  > Oscillation issues fully resolved in production
```

**Why Blockquotes:**
- ✅ Pure markdown (no HTML)
- ✅ Visually distinct in IDE (indented with | marker)
- ✅ Renders beautifully (styled box in GitHub/handbook)
- ✅ Semantically correct (quotes are for notes/context)
- ✅ Easy to parse (starts with >)
- ✅ Multi-line support built-in
- ✅ Readable in both raw and rendered views
- ✅ Simple and consistent (no label prefix needed)

**How It Looks:**

In IDE (raw markdown):
```
- [x] **#104** Design meter direction fix `#solax` (2025-10-30)
  > Completed as part of #107 and #108 work
  > Oscillation issues fully resolved in production
```

In rendered markdown (GitHub):
```
- [x] **#104** Design meter direction fix `#solax` (2025-10-30)
  
  > Completed as part of #107 and #108 work
  > Oscillation issues fully resolved in production
```

**Implementation Notes:**
- Store notes as indented blockquotes under task
- Support multi-line notes (each line starts with >)
- Add `--note` flag to complete, archive, modify commands
- Create dedicated `note` command
- Parse blockquotes when reading tasks
- Preserve blockquotes when modifying tasks

**Estimated Complexity:** Medium (2-4 hours)

### Priority 3: Nice to Have Enhancements

#### 3.1 Smart Archive Suggestions

**Problem:** Manual process to identify completed tasks that should be archived.

**Proposed Solution:**

```zsh
# Show completed tasks not yet archived
./scripts/todo/todo.zsh list --completed --not-archived

# Suggest tasks ready for archiving
./scripts/todo/todo.zsh suggest-archive
# Output:
# Tasks ready for archiving:
#   #107 - Completed 5 days ago
#   #108 - Completed 5 days ago
#   #109 - Completed 5 days ago

# Auto-archive old completed tasks
./scripts/todo/todo.zsh auto-archive --older-than 7d
./scripts/todo/todo.zsh auto-archive --older-than 30d --dry-run

# Interactive archive mode
./scripts/todo/todo.zsh archive-review
# Shows each completed task, prompts: [a]rchive, [k]eep, [s]kip
```

**Implementation Notes:**
- Parse completion dates from task metadata
- Calculate age of completed tasks
- Implement dry-run mode for safety
- Interactive mode with y/n prompts

**Estimated Complexity:** Medium (2-4 hours)

#### 3.2 Enhanced Lint Command (Task #47)

**Problem:** Current lint command has limited validation capabilities. Cannot detect orphaned subtasks or formatting issues.

**Existing Task:** #47 - Enhance --lint command to detect orphaned subtasks  
**Subtasks:**
- #47.1 - Detect empty lines in task lists
- #47.2 - Detect orphaned subtasks (subtasks without parent tasks)

**Proposed Solution:**

```zsh
# Enhanced lint with multiple checks
./scripts/todo/todo.zsh lint

# Checks performed:
# 1. Orphaned subtasks (subtasks without parents)
# 2. Empty lines in task sections
# 3. Malformed task IDs
# 4. Duplicate task IDs
# 5. Invalid tag format
# 6. Missing task descriptions
# 7. Broken relationships (if implemented)
# 8. Repository/branch references that don't exist

# Lint with auto-fix
./scripts/todo/todo.zsh lint --fix

# Lint specific checks only
./scripts/todo/todo.zsh lint --check orphaned
./scripts/todo/todo.zsh lint --check formatting
./scripts/todo/todo.zsh lint --check duplicates
```

**Output Format:**

```
Running TODO list validation...

❌ Found 3 issues:

  Issue 1: Orphaned subtask
    Task: #115.3 Fix validation
    Problem: Parent task #115 not found
    Suggestion: Delete subtask or create parent task

  Issue 2: Empty line in tasks section
    Line: 45
    Problem: Empty line breaks task grouping
    Suggestion: Remove empty line

  Issue 3: Duplicate task ID
    Tasks: #120 appears twice (lines 50 and 120)
    Problem: Duplicate task IDs
    Suggestion: Renumber one of the tasks

Run with --fix to automatically fix formatting issues
```

**Implementation Notes:**
- Validate task ID format and uniqueness
- Detect subtasks without parents
- Check for formatting issues (empty lines, indentation)
- Validate tag format
- Check relationship integrity (when implemented)
- Support auto-fix for simple issues
- Detailed error reporting with line numbers

**Estimated Complexity:** Medium (2-4 hours)

#### 3.3 Git Commit Hook Integration (Task #45)

**Problem:** No automated validation before commits. Can accidentally commit broken TODO.md files.

**Existing Task:** #45 - Create git commit hook for todo list linting and validation

**Proposed Solution:**

```zsh
# Add TODO validation to pre-commit hooks
./scripts/setup-git-hooks.zsh

# Hook validates:
# 1. TODO.md syntax is correct
# 2. No orphaned subtasks
# 3. No duplicate task IDs
# 4. Valid task format
# 5. No broken relationships

# Skip hook if needed (emergency only)
git commit --no-verify
```

**Hook Behavior:**

```zsh
# During git commit
git commit -m "Update tasks"

# Hook output:
🔍 Validating TODO.md...
❌ TODO validation failed:
  - Orphaned subtask: #115.3
  - Duplicate task ID: #120

Fix issues and try again, or use --no-verify to skip (not recommended)

# After fixing:
git commit -m "Update tasks"
🔍 Validating TODO.md...
✅ TODO validation passed
[main abc1234] Update tasks
```

**Integration:**
- Add to `scripts/setup-git-hooks.zsh`
- Use existing `lint` command
- Fast validation (< 1 second)
- Clear error messages
- Allow bypass with `--no-verify` (logged)

**Implementation Notes:**
- Add validation script to `.git/hooks/pre-commit`
- Call `todo.zsh lint` from hook
- Exit with error code if validation fails
- Log bypass attempts
- Fast execution (no network calls)

**Estimated Complexity:** Easy (< 1 hour)

#### 3.4 Prune Old Archived Tasks (Task #43)

**Problem:** Archived tasks accumulate indefinitely, making TODO.md large and slow to parse. No way to clean up old completed work.

**Existing Task:** #43 - Implement --prune function to remove old archived tasks based on git history  
**Subtasks:**
- #43.1 - Design prune function with 30-day default and task ID targeting options
- #43.2 - Implement git history analysis to identify archive dates for tasks
- #43.3 - Add prune command with --days and --from-task options

**Proposed Solution:**

```zsh
# Prune archived tasks older than 30 days (default)
./scripts/todo/todo.zsh prune

# Prune with custom age
./scripts/todo/todo.zsh prune --days 60
./scripts/todo/todo.zsh prune --older-than "2025-10-01"

# Prune from specific task onwards
./scripts/todo/todo.zsh prune --from-task 50
# Removes tasks #1-#50 from archive

# Dry run to see what would be removed
./scripts/todo/todo.zsh prune --dry-run

# Keep archive backup before pruning
./scripts/todo/todo.zsh prune --backup

# Prune permanently (no backup)
./scripts/todo/todo.zsh prune --permanent
```

**Behavior:**

```zsh
./scripts/todo/todo.zsh prune --dry-run

# Output:
Analyzing archived tasks...

Would remove 25 tasks (30+ days old):
  #50 - Task from 2025-09-15 (45 days ago)
  #48 - Task from 2025-09-20 (40 days ago)
  ...

Total: 25 tasks, 60 subtasks
Archive size reduction: ~150 lines

Run without --dry-run to prune
Backup will be created at .todo/archives/TODO_ARCHIVE_2025-10-30.md
```

**Archive Backup:**

Pruned tasks are saved to `.todo/archives/` directory:
```
.todo/archives/
  TODO_ARCHIVE_2025-10-30.md
  TODO_ARCHIVE_2025-09-30.md
  TODO_ARCHIVE_2025-08-30.md
```

**Git History Analysis:**

Uses git log to determine actual archive dates:
```zsh
# Analyze git history to find when task was archived
git log --all --grep="archive 104" -- TODO.md

# Extract archive date from git history
# Use for accurate age calculation
```

**Implementation Notes:**
- Parse archive dates from task metadata or git log
- Create backup before pruning
- Support dry-run mode
- Flexible age criteria (days, date, task ID range)
- Preserve backup archives
- Log all prune operations

**Estimated Complexity:** Medium (2-4 hours)

#### 3.5 Handbook TODO Dashboard (Task #54)

**Problem:** TODO tasks are only visible in terminal. No web-based view integrated with the handbook.

**Existing Task:** #54 - Create handbook TODO page showing currently active tasks and display in index

**Proposed Solution:**

```zsh
# Generate TODO dashboard for handbook
./scripts/todo/todo-handbook-export.zsh

# Output: docs/handbook/src/development/active-todos.md
# Automatically included in handbook build

# Update during handbook build
./scripts/handbook/build_handbook.zsh
# Regenerates TODO page automatically
```

**Handbook Page Features:**

- **Active Tasks View**: List of all pending tasks
- **Recently Completed**: Last 10 completed tasks  
- **Statistics**: Task counts by tag, status
- **Progress Indicators**: Visual progress bars
- **Repository Context**: Tasks grouped by repo
- **Links**: Links to related handbook pages
- **Auto-Generated**: Updates on every handbook build

**Display Format:**

```markdown
# Active TODO Tasks

Last Updated: 2025-10-30 12:34:56

## Summary
- 📋 Total Active: 15 tasks
- ✅ Recently Completed: 4 tasks
- 🏗️ In Progress: 2 tasks

## Active Tasks

### High Priority
- [ ] **#110** Enhance TODO tool `#feature` `#todo-system`
  - [x] #110.1 Create proposal document ✅

### By Repository
**ha-repo (10 tasks)**
- [ ] #83 Device exclusion list
- [ ] #82 Fixed IP validation
...

**solax-repo (5 tasks)**
- [ ] #104 Meter direction fix
...

## Recently Completed (Last 7 Days)
- [x] #109 Delta correction (2025-10-30)
- [x] #108 Power calculation fix (2025-10-30)
...
```

**Integration:**
- Add export script to handbook build process
- Auto-regenerate on git commit (post-commit hook)
- Include in handbook navigation
- Style with handbook theme
- Link to GitHub Issues (when #78 implemented)

**Implementation Notes:**
- Parse TODO.md and generate markdown
- Format for MDBook compatibility
- Add to handbook SUMMARY.md
- Trigger regeneration in build_handbook.zsh
- Cache to avoid rebuilding if unchanged

**Estimated Complexity:** Medium (2-4 hours)

#### 3.6 Multi-Developer Git Synchronization

**Problem:** Multiple developers creating tasks simultaneously can create duplicate task IDs. Without synchronization, two developers might both create task #115, causing conflicts.

**Solution:** Simple, automatic git synchronization with zero user interaction required. AI-agent friendly with no prompts.

**Core Principles:**
- Simple sequential IDs (current system preserved)
- Optimistic auto-sync (silent git pull before operations)
- Auto-resolution of conflicts (take MAX, renumber duplicates)
- No interactive prompts (AI agents can use without blocking)
- Fail gracefully with clear error messages for humans

**Auto-Sync Behavior:**

```zsh
# AI agent creates task (no prompts required)
./scripts/todo/todo.zsh add "Fix bug" "#bugfix"

# Behind the scenes (silent):
# 1. git pull origin main -- TODO.md .todo_serial
# 2. If .todo_serial conflict: take MAX(local, remote) + 1
# 3. If duplicate ID detected: renumber local task
# 4. Create new task with safe ID
# 5. Done

# Output (only if successful):
Added: #115 Fix bug

# Output (only if needs human):
Error: TODO.md has conflicts. Please resolve manually.
```

**Conflict Resolution (Automatic):**

1. **.todo_serial conflicts:** Take highest number
2. **Duplicate task IDs:** Renumber local task to next available
3. **TODO.md content conflicts:** Fail with clear error for human

**Recovery Commands (No Interaction):**

```zsh
# Detect and fix duplicate IDs
./scripts/todo/todo.zsh lint
# Reports: Duplicate task ID #115 found

./scripts/todo/todo.zsh fix-duplicates
# Renumbered task at line 45: #115 → #117
# Updated .todo_serial to 118

# Fix .todo_serial if out of sync
./scripts/todo/todo.zsh fix-serial
# Scanned TODO.md, updated .todo_serial: 100 → 151
```

**Implementation Details:**

```zsh
add_todo() {
    # Step 1: Silent git pull (optimistic)
    git pull --quiet origin main -- TODO.md .todo_serial
    
    # Step 2: Auto-resolve .todo_serial conflicts (take MAX)
    resolve_serial_conflict
    
    # Step 3: Get next safe ID (skip any duplicates)
    next_id=$(get_next_safe_id)
    
    # Step 4: Create task
    echo "- [ ] **#${next_id}** ${text} ${tags}" >> TODO.md
    echo $((next_id + 1)) > .todo_serial
    
    # Done (no prompts, no interaction)
}
```

**AI-Agent Compatible:**
- ✅ All commands run without prompts
- ✅ Auto-fixes common issues
- ✅ Clear error messages for humans
- ✅ Simple recovery commands
- ✅ Works with existing git workflow

**What's NOT Included (Keeping Simple):**
- ❌ No interactive prompts or confirmations
- ❌ No auto-commit or auto-push (manual git workflow)
- ❌ No complex ID reservation systems
- ❌ No configuration options
- ❌ No GitHub Issues integration (see Future Considerations)

**Implementation Notes:**
- Enhance add/add-subtask commands with silent sync
- Simple MAX() logic for .todo_serial conflicts
- Scan and renumber for duplicate IDs
- Fail gracefully if TODO.md has content conflicts
- Log all auto-resolutions to .todo.log

**Estimated Complexity:** Easy (2 hours)

#### 3.7 Progress Statistics and Analytics

**Problem:** No visibility into completion velocity or progress trends.

**Proposed Solution:**

```zsh
# Show completion stats for time period
./scripts/todo/todo.zsh stats --period week
# This week: 4 tasks, 15 subtasks completed
# Completion rate: 95% increase from last week
# Average completion time: 2.3 days

./scripts/todo/todo.zsh stats --period month
./scripts/todo/todo.zsh stats --period all

# Show progress by tag
./scripts/todo/todo.zsh stats --by-tag
# #solax: 3 completed, 2 pending (60% complete)
# #docs: 5 completed, 8 pending (38% complete)
# #feature: 10 completed, 5 pending (67% complete)

# Show repository distribution
./scripts/todo/todo.zsh stats --by-repo
# ha-repo: 25 tasks (10 pending, 15 completed)
# solax-repo: 15 tasks (5 pending, 10 completed)

# Velocity chart
./scripts/todo/todo.zsh velocity --days 30
# Week 1: 5 tasks completed
# Week 2: 8 tasks completed
# Week 3: 3 tasks completed
# Week 4: 10 tasks completed

# Task age distribution
./scripts/todo/todo.zsh stats --age-distribution
# 0-7 days: 5 tasks
# 8-14 days: 3 tasks
# 15-30 days: 8 tasks
# 31+ days: 2 tasks
```

**Implementation Notes:**
- Parse .todo.log for historical data
- Calculate time between task creation and completion
- Group by tags, repos, time periods
- Display in table or simple chart format
- Use existing logging data

**Estimated Complexity:** Medium (2-4 hours)

#### 3.8 Task Templates

**Problem:** Complex tasks have predictable structures that require manual recreation.

**Use Case:** Task #104 had standard subtasks (investigation, design, implementation, testing, validation, documentation).

**Proposed Solution:**

```zsh
# Create task from template
./scripts/todo/todo.zsh add-from-template solax-fix "Fix battery mode" "#solax"
# Automatically creates parent task with standard subtasks

# Define a template
./scripts/todo/todo.zsh template create solax-fix \
  --description "Standard SolaX fix workflow" \
  --subtasks "investigation,design,implementation,testing,validation,documentation" \
  --tags "#solax"

# List available templates
./scripts/todo/todo.zsh template list

# Show template details
./scripts/todo/todo.zsh template show solax-fix

# Edit template
./scripts/todo/todo.zsh template edit solax-fix

# Delete template
./scripts/todo/todo.zsh template delete solax-fix
```

**Template Storage Format:**

Templates stored in `.todo/templates/` directory:

```
.todo/
  templates/
    solax-fix.md           # SolaX fix workflow template
    validator-impl.md      # Validator implementation template
    feature-dev.md         # Feature development template
```

**Template File Format (`.todo/templates/solax-fix.md`):**

```markdown
# SolaX Fix Workflow Template

**Description:** Standard SolaX fix workflow
**Tags:** #solax, #development
**Repository:** solax-repo

## Subtasks

1. Investigation - Root cause analysis `#investigation`
2. Design - Solution design `#design`
3. Implementation - Code changes `#development`
4. Testing - Validation `#testing`
5. Documentation - Update docs `#docs`
```

**Another Example (`.todo/templates/validator-impl.md`):**

```markdown
# Validator Implementation Template

**Description:** New validator implementation
**Tags:** #feature, #validation
**Repository:** ha-repo

## Subtasks

1. Design validator interface `#design`
2. Implement validation logic `#development`
3. Add to main validator script `#integration`
4. Create handbook documentation `#docs`
5. Test with real devices `#testing`
```

**File Organization:**
- `.todo/templates/` - Template directory
- One file per template (kebab-case naming)
- Simple markdown format
- Human-readable and editable
- Version controlled with TODO system

**Implementation Notes:**
- Create `.todo/templates/` directory
- Store each template as separate markdown file
- Parse template definitions from files
- Generate tasks and subtasks from template
- Allow template customization during creation
- Scan templates directory for `template list`
- Edit templates directly or via `template edit` command

**Estimated Complexity:** Complex (1+ day)

#### 3.9 Interactive Review Mode

**⚠️ NOT FOR IMPLEMENTATION** - This feature is documented for completeness but will not be implemented.

**Why Not:**
- Interactive prompts are incompatible with AI-agent usage (core design principle)
- Adds complexity without sufficient value
- Other features (bulk operations, smart suggestions) address the same needs non-interactively
- Conflicts with "zero-interaction" design philosophy

**Problem:** Manual, repetitive process when reviewing and cleaning up tasks.

**Proposed Solution (For Reference Only):**

```zsh
# Interactive review of completed tasks
./scripts/todo/todo.zsh review --completed
# Shows each completed task:
# [x] #107 Investigate PM overflow (completed 5 days ago)
# Actions: [a]rchive, [k]eep, [n]ote, [s]how, [q]uit: 

# Review all tasks
./scripts/todo/todo.zsh review
# Shows each task with options based on status

# Review by tag
./scripts/todo/todo.zsh review --tag solax

# Review stale tasks
./scripts/todo/todo.zsh review --stale --older-than 30d
# Shows tasks without updates in 30+ days
# Actions: [c]omplete, [a]rchive, [d]elete, [k]eep, [s]how, [q]uit:

# Weekly planning mode
./scripts/todo/todo.zsh plan --week
# Shows:
# - High priority tasks
# - Blocked tasks
# - Ready tasks (no dependencies)
# - Stale tasks
# Prompts for prioritization
```

**Interactive Actions:**
- `a` - Archive task
- `c` - Complete task
- `k` - Keep as-is
- `n` - Add note
- `s` - Show task details
- `e` - Edit task
- `d` - Delete task
- `q` - Quit review

**Implementation Notes:**
- Use `read` for interactive prompts
- Implement action handlers
- Support batch operations (review all in category)
- Save state on quit (resume later)
- Colorize output for readability

**Estimated Complexity:** Complex (1+ day)

## Implementation Roadmap

### Phase 1: Essential Features (Week 1)
**Goal:** Immediate productivity improvements

1. **Bulk Operations** [1 hour]
   - Complete multiple tasks
   - Complete with subtasks
   - Range notation for subtasks

2. **Archive Without Completion** [1 hour]
   - Add `--reason` parameter
   - Implement task states (obsolete, wontfix, etc.)
   - Update display format

3. **Enhanced List Filtering** [1 hour]
   - Multiple filter parameters
   - Filter composition
   - Status and date filtering

4. **Task and Subtask Deletion** [1 hour]
   - Implement delete command
   - Add confirmation prompts
   - Soft delete with restore
   - Bulk deletion support

**Deliverables:**
- Updated todo.zsh script
- Updated documentation
- Test cases
- Migration notes

### Phase 2: High Value Features (Week 2)
**Goal:** Better context and relationships

5. **Task Relationships** [3 hours]
   - Implement relationship storage
   - Add relate/unrelate commands
   - Update display logic
   - Add relationship filtering

6. **Repository/Branch Context** [3 hours]
   - Add repo/branch metadata
   - Implement auto-detection
   - Integrate with git-status-all
   - Add context filtering

7. **Task Notes** [2 hours]
   - Implement note storage
   - Add note command
   - Integrate with complete/archive
   - Update display

**Deliverables:**
- Enhanced todo.zsh script
- Updated handbook documentation
- Integration with git tools
- Migration guide

### Phase 3: Advanced Features (Week 3-4)
**Goal:** Automation, intelligence, and integration

8. **Smart Archive Suggestions** [2 hours]
9. **Multi-Developer Git Synchronization** [2 hours]
10. **Enhanced Lint Command** (Task #47) [2 hours]
11. **Git Commit Hook Integration** (Task #45) [1 hour]
12. **Prune Old Archived Tasks** (Task #43) [2 hours]
13. **Handbook TODO Dashboard** (Task #54) [2 hours]
14. **Progress Statistics** [3 hours]
15. **Task Templates** [8 hours]

**Not Included:**
- ~~16. Interactive Review Mode~~ (incompatible with AI-agent design)

**Deliverables:**
- Full-featured todo.zsh
- Multi-developer git synchronization
- Git hook integration
- Handbook integration
- Template system
- Comprehensive documentation
- Training materials

## Testing Strategy

### Unit Tests
- Test each new command in isolation
- Verify backward compatibility
- Test error handling
- Validate data integrity

### Integration Tests
- Test workflow scenarios
- Multi-task operations
- Cross-repository contexts
- Template creation and usage

### Migration Testing
- Test upgrade from current version
- Verify existing tasks unaffected
- Test new features with existing data
- Rollback capability

## Documentation Updates

### Files to Update
1. `scripts/todo/TODO_TAGGING_SYSTEM_DESIGN.md` - Add new features
2. `docs/handbook/src/development/todo-management.md` - User guide
3. `scripts/todo/todo.zsh` - Inline help text
4. `.cursor/rules/` - AI assistant rules

### New Documentation
1. Task relationships guide
2. Template creation guide
3. Migration guide
4. Best practices guide

## Backward Compatibility

### Requirements
- Existing tasks must continue to work
- Existing commands must maintain behavior
- New features must be opt-in
- File format must remain parseable

### Migration Path
- Current TODO.md format remains valid
- New metadata sections are optional
- Gradual adoption of new features
- No breaking changes

## Success Criteria

### Phase 1 Success
- ✅ Can complete 10 tasks in a single command
- ✅ Can archive obsolete tasks without marking complete
- ✅ Can filter tasks by multiple criteria
- ✅ All existing functionality preserved
- ✅ Zero data loss during migration

### Phase 2 Success
- ✅ Task relationships are discoverable
- ✅ Repository context is always visible
- ✅ Can add detailed notes to any task
- ✅ Cross-repository workflows are smooth
- ✅ Dependencies are tracked automatically

### Phase 3 Success
- ✅ Archive suggestions save 5+ minutes per session
- ✅ Statistics provide actionable insights
- ✅ Templates reduce task creation time by 50%
- ✅ Interactive mode streamlines reviews
- ✅ System scales to 500+ tasks

## Risk Assessment

### Low Risk
- Bulk operations (well-defined scope)
- Enhanced filtering (additive feature)
- Task notes (isolated feature)

### Medium Risk
- Archive without completion (changes core logic)
- Task relationships (data model changes)
- Repository context (integration complexity)

### High Risk
- Task templates (complex feature)
- Interactive review mode (user interaction complexity)
- Statistics (performance with large datasets)

### Mitigation Strategies
- Comprehensive testing before deployment
- Incremental rollout by phase
- Backup mechanisms for TODO.md
- Rollback capability
- User acceptance testing

## Future Considerations

### GitHub Issues Integration (Task #78) - Deferred

**Status:** Analyzed but not prioritized for initial implementation.

**Why Deferred:**
1. **Solo developer workflow**: Current system optimized for single developer with AI assistant
2. **Speed critical**: Local TODO.md operations are instant, GitHub API adds latency
3. **AI integration**: Current workflow relies on direct TODO.md access
4. **Complexity**: Adds sync conflicts, authentication, rate limits
5. **Current system works**: TODO.md + git is simple, fast, and effective

**If Needed in Future:**

**Option A: Hybrid (Recommended for Future)**
- Keep TODO.md as primary source (fast, AI-friendly, offline)
- One-way export to GitHub Issues (visibility only)
- No sync back from GitHub (avoids conflicts)
- GitHub used for external visibility and discussion

**Implementation:**
```zsh
# Export tasks to GitHub for visibility
./scripts/todo/todo.zsh export-github
# Creates/updates GitHub Issues
# Local TODO.md remains authoritative

# No bidirectional sync (avoids complexity)
```

**Option B: Full Integration**
- If team collaboration becomes necessary
- If community contributions are desired
- If offline work is rare
- Requires significant implementation effort

**Recommendation:** 
- Re-evaluate in 6-12 months
- Only if collaboration needs emerge
- Current git-based multi-developer support (3.6) handles team scenarios
- GitHub export can be added later if visibility is needed

**Related:** See Open Questions #5 below.

## Open Questions

1. **Multi-user support:** Should we add task assignment?
   - Current: Single user assumed
   - Future: Could add `--assigned-to` field

2. **Task priority:** Should we add explicit priority levels?
   - Current: Priority via ordering and tags
   - Future: Could add `--priority high/medium/low`

3. **Recurring tasks:** Do we need recurring task support?
   - Current: Manual recreation
   - Future: Could add `--recurring weekly` option

4. **Time tracking:** Should we add time estimates/actual?
   - Current: No time tracking
   - Future: Could add `--estimate 2h` and time logging

5. **GitHub Issues integration:** When/if to implement?
   - Current: Deferred (see Future Considerations above)
   - Decision point: When collaboration needs become clear
   - Options: One-way export vs. full bidirectional sync

6. **Mobile access:** How to access TODOs on mobile?
   - Current: Terminal only
   - Future: Could generate web dashboard or handbook integration

## References

### Related Tasks
- #43 - Implement --prune function (incorporated)
- #45 - Create git commit hook (incorporated)
- #47 - Enhance --lint command (incorporated)
- #54 - Create handbook TODO page (incorporated)
- #78 - GitHub Issues backend (deferred to future considerations)
- #104 - GEN4 meter direction fix (usage example)
- #107, #108, #109 - Recently archived tasks (usage patterns)
- #110 - TODO tool enhancements (parent task)

### Existing Documentation
- `scripts/todo/TODO_TAGGING_SYSTEM_DESIGN.md` - Current design
- `docs/handbook/src/development/todo-management.md` - User guide
- `.todo.log` - Historical usage data

### External References
- [TaskWarrior](https://taskwarrior.org/) - Task management CLI
- [GitHub CLI](https://cli.github.com/) - Issue management patterns
- [Org Mode](https://orgmode.org/) - Task organization concepts

## Appendix A: Example Usage Scenarios

### Scenario 1: Bulk Task Cleanup
```zsh
# Weekly review - archive all completed tasks from last week
./scripts/todo/todo.zsh list --completed --updated-after "2025-10-23"
# Shows: #107, #108, #109, #104

./scripts/todo/todo.zsh archive 107 108 109 104
# Archived 4 tasks and 20 subtasks to Recently Completed section
```

### Scenario 2: Feature Development Workflow
```zsh
# Create feature task with template
./scripts/todo/todo.zsh add-from-template solax-fix "Fix inverter communication" \
  --repo solax-repo \
  --branch feature/fix-communication

# Adds relationships
./scripts/todo/todo.zsh relate 120 --depends-on 119

# Work on task, add notes
./scripts/todo/todo.zsh note 120 "Testing shows timeout issues"

# Complete task with context
./scripts/todo/todo.zsh complete 120 --note "Fixed by improving retry logic"
```

### Scenario 3: Cross-Repository Work
```zsh
# Switch to solax-repo branch
./scripts/git-switch.zsh solax-repo feature/new-sensor

# See tasks for this context
./scripts/todo/todo.zsh list --current-branch
# Shows: #115 Add new sensor (solax-repo:feature/new-sensor)

# Complete work in solax-repo
./scripts/todo/todo.zsh complete 115

# Related task in ha-repo is now unblocked
./scripts/todo/todo.zsh list --ready
# Shows: #116 Update HA config (was blocked by #115)
```

## Appendix B: Data Format Examples

### Complete TODO.md File Structure

```markdown
# Home Assistant Project Todo List

> **⚠️ IMPORTANT: This file should ONLY be edited through the `./scripts/todo/todo.zsh` script!**

## Repository Mappings

This workspace contains multiple repositories. Tasks can be tagged with repository shortnames:

- **ha-repo** → `/homeassistant` (Main Home Assistant configuration)
  - Remote: https://github.com/fxstein/homeassistant
- **solax-repo** → `/homeassistant/custom_components/solax_modbus_repo` (SolaX Modbus integration)
  - Remote: https://github.com/fxstein/solax-modbus

View all repos: `./scripts/git-status-all.zsh`

## Tasks
- [ ] **#120** Fix inverter communication `#solax` `#bugfix` `@solax-repo` `@feature/fix-communication`
  ↳ Depends on: #119
  ↳ Blocks: #121
  > Testing shows timeout issues with Gen4 inverters
  > Need to review retry logic in plugin_solax.py
  - [ ] **#120.1** Investigate timeout patterns `#investigation`
  - [ ] **#120.2** Implement retry improvements `#development`
  - [ ] **#120.3** Test with all inverter types `#testing`
- [ ] **#119** Upgrade Modbus library `#solax` `@solax-repo` `@main`

## Deleted Tasks
- [D] **#118** Old approach discarded (deleted 2025-10-15, expires 2025-11-14)

## Recently Completed
- [x] **#117** Add logging `#development` (2025-10-30)

---
**Last Updated:** Thu Oct 30 14:23:45 CET 2025
**Repository:** https://github.com/fxstein/homeassistant  
**Maintenance:** Use `./scripts/todo/todo.zsh` script only

## Task Metadata

Task relationships and dependencies (managed by todo.zsh tool).
View with: `./scripts/todo/todo.zsh show <task-id>`

<!-- TASK RELATIONSHIPS
120:depends-on:119
120:blocks:121
122:completed-by:120,121
123:duplicate-of:120
-->
```

### Individual Task with Full Metadata
```markdown
- [ ] **#120** Fix inverter communication `#solax` `#bugfix` `@solax-repo` `@feature/fix-communication`
  ↳ Depends on: #119
  ↳ Blocks: #121
  > Testing shows timeout issues with Gen4 inverters
  > Need to review retry logic in plugin_solax.py
  - [ ] **#120.1** Investigate timeout patterns `#investigation`
  - [ ] **#120.2** Implement retry improvements `#development`
  - [ ] **#120.3** Test with all inverter types `#testing`
```

### Template Definition (`.todo/templates/solax-bugfix.md`)
```markdown
# SolaX Bug Fix Workflow Template

**Description:** Standard SolaX bug fix workflow
**Tags:** #solax, #bugfix
**Repository:** solax-repo

## Subtasks

1. Investigation - Reproduce and analyze `#investigation`
2. Fix - Implement solution `#development`
3. Testing - Validate across all inverters `#testing`
4. Documentation - Update changelog `#docs`
```

## Conclusion

These 15 enhancements will significantly improve the TODO tool's usability and power while maintaining its simplicity, speed, and AI-agent compatibility. The phased approach ensures we can validate each enhancement before adding complexity.

**Key Design Principles Maintained:**
- Zero-interaction (AI-agent friendly)
- Simple sequential IDs
- Fast local operations
- Git-based collaboration
- TODO.md stays in root (discoverable)
- Support files organized in `.todo/` (clean)

**Total Estimated Effort:**
- Phase 1 (Essential): 4 hours
- Phase 2 (High Value): 8 hours
- Phase 3 (Advanced): 25 hours
- **Total: ~37 hours** (~5 days)

The proposed changes address real pain points observed in production use while maintaining the system's core strengths: simplicity, speed, and effectiveness.

---

**Next Steps:**
1. ✅ Review this proposal (complete)
2. Prioritize features for Phase 1 implementation
3. Create implementation tasks
4. Begin Phase 1 development
5. Migrate files to `.todo/` directory structure

