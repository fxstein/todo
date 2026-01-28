# Prune Function Analysis

**Task:** #267 [AIT-2] Implement --prune function to remove archived tasks
**Linear Issue:** https://linear.app/fxstein/issue/AIT-2
**Original Task:** #129 (existing in TODO.md)
**Date:** 2026-01-28
**Status:** Analysis Complete - Ready for Design

## Executive Summary

This analysis reviews the existing planning for the prune function (task #129) and assesses requirements for implementation. The prune function will remove old archived tasks from TODO.md based on git history analysis, with configurable retention periods and targeting options.

**Key Findings:**
- Detailed specification already exists in `docs/development/TODO_TOOL_IMPROVEMENTS.md` (section 3.4)
- Task #129 outlines three implementation steps (design, git analysis, CLI command)
- No existing prune implementation in codebase
- Strong foundation exists: FileOps for TODO.md operations, git utilities, archive functionality
- Clear requirements from Linear issue align with existing task #129

## Background

### Original Task #129

Located at line 105-108 in TODO.md:

```markdown
- [ ] **#129** Implement --prune function to remove old archived tasks based on git history
  - [ ] **#129.3** Add prune command with --days and --from-task options
  - [ ] **#129.2** Implement git history analysis to identify archive dates for tasks
  - [ ] **#129.1** Design prune function with 30-day default and task ID targeting options
```

**Tags:** `#feature`
**Status:** Pending (never started)

### Linear Issue AIT-2 Requirements

From https://linear.app/fxstein/issue/AIT-2:

1. Design prune function with 30-day default and task ID targeting options
2. Implement git history analysis to identify archive dates for tasks
3. Add prune command with --days and --from-task options
4. Add equivalent to MCP server

**Priority:** High
**Labels:** Feature
**Original GitHub Issue:** #51

### Existing Specification

The `docs/development/TODO_TOOL_IMPROVEMENTS.md` document contains a comprehensive specification (section 3.4, lines 808-891):

**Core Requirements:**
- 30-day default retention period
- Custom age specification (--days, --older-than)
- Task ID range targeting (--from-task)
- Dry-run mode
- Backup archive creation
- Git history analysis for accurate archive dates

**Proposed Commands:**
```bash
./todo.ai prune                              # 30 days default
./todo.ai prune --days 60                    # Custom age
./todo.ai prune --older-than "2025-10-01"    # Specific date
./todo.ai prune --from-task 50               # Remove #1-#50
./todo.ai prune --dry-run                    # Preview only
./todo.ai prune --backup                     # Keep archive backup
```

**Archive Backup Location:**
- `.ai-todo/archives/TODO_ARCHIVE_YYYY-MM-DD.md`

## Current Codebase Assessment

### Existing Components

#### 1. Archive Functionality
**Location:** `ai_todo/cli/commands/__init__.py` (lines 401-433)

The `archive_command()` already exists and handles:
- Moving tasks to "Archived Tasks" section
- Bulk operations with subtasks
- Reason tracking via notes
- Task expansion (ranges, with-subtasks)

**Relevance:** Prune will operate on archived tasks, so understanding archive mechanics is critical.

#### 2. FileOps Class
**Location:** `ai_todo/core/file_ops.py`

Provides safe TODO.md operations:
- Atomic reads/writes with checksums
- Shadow copy management
- Tamper detection integration
- Section management (Tasks, Archived Tasks, Deleted Tasks)

**Relevance:** MUST use FileOps for all TODO.md operations. Never use `open()` directly.

#### 3. Git Utilities
**Location:** `ai_todo/utils/git.py` (lines 1-45)

Existing git functions:
```python
get_git_root() -> str | None
get_current_branch() -> str
get_user_name() -> str
get_user_email() -> str
is_git_repo() -> bool
```

**Gap:** No git history analysis functions. Need to add:
- `get_task_archive_date(task_id: str) -> datetime | None`
- `get_git_log_for_task(task_id: str) -> list[GitCommit]`

#### 4. Task Management
**Location:** `ai_todo/core/task.py`

The `TaskManager` and `Task` classes handle:
- Task CRUD operations
- Status management (pending, completed, archived, deleted)
- Subtask relationships
- Notes and descriptions

**Relevance:** Will need to identify and filter archived tasks for pruning.

#### 5. CLI Structure
**Location:** `ai_todo/cli/main.py` and `ai_todo/cli/commands/__init__.py`

Standard command pattern:
```python
def command_name(args..., todo_path: str = "TODO.md"):
    """Command description."""
    manager = get_manager(todo_path)
    # ... operation ...
    save_changes(manager, todo_path)
    print("Success message")
```

**Relevance:** Prune command will follow this pattern.

#### 6. MCP Server
**Location:** `ai_todo/mcp/server.py`

MCP tools follow FastMCP pattern with:
- Tool decorators (`@mcp.tool()`)
- Parameter validation
- Result formatting
- Parity with CLI commands

**Relevance:** Need to add `prune_tasks` MCP tool matching CLI functionality.

### Existing Gaps

1. **No Git History Analysis**
   - Need functions to parse git log for task archive dates
   - Need to extract task IDs from commit messages
   - Need to handle tasks without git history (fallback to metadata)

2. **No Archive Date Tracking**
   - Archived tasks show completion date: `(2026-01-28)`
   - Need to determine if this is archive date or completion date
   - May need to parse git log to get actual archive date

3. **No Backup/Archive Export**
   - Need to create `.ai-todo/archives/` directory structure
   - Need to export pruned tasks to timestamped archive files
   - Need to maintain archive file format compatibility

4. **No Date-Based Filtering**
   - Task model has `completed_at` datetime but not `archived_at`
   - Need to add archive date detection logic
   - Need to calculate task age from archive date

## Requirements Analysis

### Functional Requirements

#### FR1: Prune Command (CLI)
- **Priority:** P0 (Critical)
- **Input:** Optional flags (--days, --from-task, --dry-run, --backup)
- **Output:** Count of pruned tasks, archive location
- **Behavior:** Remove archived tasks matching criteria

#### FR2: Git History Analysis
- **Priority:** P0 (Critical)
- **Input:** Task ID or TODO.md file
- **Output:** Archive date for task
- **Behavior:** Parse git log to find when task was archived
- **Fallback:** Use completion date if git history unavailable

#### FR3: Archive Backup
- **Priority:** P1 (High)
- **Input:** List of tasks to prune
- **Output:** Archive file path
- **Behavior:** Export pruned tasks to `.ai-todo/archives/` before removal
- **Format:** Standard TODO.md format with metadata

#### FR4: MCP Server Integration
- **Priority:** P1 (High)
- **Input:** Same parameters as CLI
- **Output:** JSON result with pruned count and archive path
- **Behavior:** Identical to CLI, callable via MCP protocol

#### FR5: Dry-Run Mode
- **Priority:** P1 (High)
- **Input:** --dry-run flag
- **Output:** Preview of what would be pruned
- **Behavior:** Analyze without modifying TODO.md

#### FR6: Flexible Targeting
- **Priority:** P2 (Medium)
- **Options:** --days N, --older-than DATE, --from-task ID
- **Behavior:** Support multiple filtering strategies

### Non-Functional Requirements

#### NFR1: Safety
- **MUST** use FileOps for all TODO.md operations
- **MUST** create backup before pruning
- **MUST** preserve git history
- **MUST** be reversible (archived tasks can be restored from backup)

#### NFR2: Performance
- Git log parsing should be efficient (avoid full history scan)
- Should handle TODO.md files with 1000+ archived tasks
- Should complete in < 5 seconds for typical workload

#### NFR3: Compatibility
- Must work with existing TODO.md format
- Must preserve tamper detection integrity
- Must maintain MCP-CLI parity
- Must follow existing command patterns

#### NFR4: User Experience
- Clear progress messages
- Confirmation prompts for destructive operations (optional --force)
- Helpful error messages with recovery suggestions
- Dry-run preview shows exactly what will happen

## Technical Design Considerations

### 1. Git History Analysis Strategy

**Challenge:** Archived tasks show `(2026-01-28)` but this may be completion date, not archive date.

**Options:**

**Option A: Parse Git Log (Recommended)**
```python
def get_archive_date(task_id: str) -> datetime | None:
    """Parse git log to find when task was archived."""
    # git log --all --grep="archive.*{task_id}" --format="%ai" -- TODO.md
    # Extract date from commit timestamp
    # Return datetime or None if not found
```

**Pros:**
- Accurate archive dates
- Works for all previously archived tasks
- Respects actual history

**Cons:**
- Requires git repository
- Performance overhead for large histories
- Complex parsing logic

**Option B: Use Completion Date (Fallback)**
```python
def get_archive_date_fallback(task: Task) -> datetime | None:
    """Extract date from archived task line."""
    # Parse (YYYY-MM-DD) from task metadata
    # Return datetime or None
```

**Pros:**
- No git dependency
- Fast and simple
- Always available

**Cons:**
- May not be actual archive date
- Less accurate for age calculations

**Recommendation:** Use Option A with Option B as fallback.

### 2. Archive Backup Strategy

**Location:** `.ai-todo/archives/TODO_ARCHIVE_YYYY-MM-DD.md`

**Format:**
```markdown
# Archived Tasks - Pruned on YYYY-MM-DD

This file contains tasks pruned from TODO.md on YYYY-MM-DD.
These tasks were archived more than N days ago.

## Pruned Tasks

[All pruned tasks in standard TODO.md format]

---
**Prune Date:** YYYY-MM-DD HH:MM:SS
**Retention Period:** N days
**Tasks Pruned:** X tasks, Y subtasks
**Original TODO.md:** [path]
```

**Restoration:**
- Manual: Copy tasks from archive back to TODO.md
- Automated: Future enhancement - `./todo.ai restore-from-archive`

### 3. Command Interface Design

**CLI Command:**
```bash
./todo.ai prune [OPTIONS]

Options:
  --days N              Prune tasks older than N days (default: 30)
  --older-than DATE     Prune tasks archived before DATE (YYYY-MM-DD)
  --from-task ID        Prune tasks from #1 to #ID (numeric range)
  --dry-run             Preview without making changes
  --backup              Create archive backup (default: true)
  --no-backup           Skip backup creation
  --force               Skip confirmation prompts
```

**MCP Tool:**
```python
@mcp.tool()
def prune_tasks(
    days: int = 30,
    older_than: str | None = None,
    from_task: str | None = None,
    dry_run: bool = False,
    backup: bool = True,
) -> PruneResult:
    """Prune old archived tasks from TODO.md."""
    # Implementation...
```

### 4. FileOps Integration

**Critical Rules:**
1. **ALWAYS** use `FileOps(todo_path)` for reading TODO.md
2. **NEVER** use `open()` or `write()` directly on TODO.md
3. **ALWAYS** call `file_ops.write_tasks(tasks)` to save changes
4. FileOps handles checksums, shadow copies, and tamper detection automatically

**Example Pattern:**
```python
def prune_command(days: int = 30, todo_path: str = "TODO.md"):
    file_ops = FileOps(todo_path)
    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)

    # Identify tasks to prune
    to_prune = identify_tasks_to_prune(tasks, days)

    # Create backup
    if backup:
        create_archive_backup(to_prune, days)

    # Remove from task list
    remaining_tasks = [t for t in tasks if t not in to_prune]

    # Save changes via FileOps
    file_ops.write_tasks(remaining_tasks)

    print(f"Pruned {len(to_prune)} task(s)")
```

### 5. Edge Cases to Handle

1. **No Archived Tasks**
   - Message: "No archived tasks found. Nothing to prune."
   - Exit gracefully

2. **No Git Repository**
   - Fall back to completion date parsing
   - Warn user: "Git history unavailable, using completion dates"

3. **Tasks Without Dates**
   - Skip these tasks
   - Warn user: "Skipped N tasks without archive dates"

4. **Empty Archive Result**
   - Message: "No archived tasks older than N days found."
   - No backup created, no changes made

5. **Tamper Detection Conflicts**
   - FileOps handles this automatically
   - If tamper detected, abort with error message

6. **Prune Entire Archive**
   - Allow if explicit (--from-task covers all)
   - Warn if > 90% of tasks would be pruned

## Implementation Checklist

### Phase 1: Core Git Analysis (task#267.3)
- [ ] Add git history analysis functions to `ai_todo/utils/git.py`
  - [ ] `get_task_archive_date(task_id: str) -> datetime | None`
  - [ ] `parse_archive_date_from_task(task: Task) -> datetime | None` (fallback)
  - [ ] Unit tests for date extraction

### Phase 2: Archive Backup System (task#267.3)
- [ ] Create archive directory structure
  - [ ] `.ai-todo/archives/` directory creation
  - [ ] Archive file naming: `TODO_ARCHIVE_YYYY-MM-DD.md`
  - [ ] Archive file format (header + tasks + footer)
- [ ] Implement backup functions
  - [ ] `create_archive_backup(tasks: list[Task], retention_days: int) -> str`
  - [ ] Archive file writer with metadata
- [ ] Unit tests for backup creation

### Phase 3: Prune Core Logic (task#267.3)
- [ ] Implement task filtering
  - [ ] `identify_tasks_to_prune(tasks: list[Task], days: int) -> list[Task]`
  - [ ] `filter_by_age(tasks: list[Task], days: int) -> list[Task]`
  - [ ] `filter_by_date(tasks: list[Task], older_than: str) -> list[Task]`
  - [ ] `filter_by_task_range(tasks: list[Task], from_task: str) -> list[Task]`
- [ ] Implement prune operation
  - [ ] Use FileOps for TODO.md operations
  - [ ] Handle subtask removal (prune parent = prune subtasks)
  - [ ] Transaction safety (backup first, then prune)
- [ ] Unit tests for filtering and pruning

### Phase 4: CLI Command (task#267.4)
- [ ] Add prune command to `ai_todo/cli/main.py`
  - [ ] Argument parsing (--days, --older-than, --from-task, --dry-run, --backup)
  - [ ] User confirmation prompts (skippable with --force)
  - [ ] Progress messages
  - [ ] Error handling
- [ ] Add to command registration
- [ ] Integration tests for CLI

### Phase 5: MCP Integration (task#267.5)
- [ ] Add `prune_tasks` tool to `ai_todo/mcp/server.py`
  - [ ] MCP tool decorator
  - [ ] Parameter validation
  - [ ] Call core prune logic
  - [ ] Return structured result (PruneResult)
- [ ] MCP-CLI parity tests

### Phase 6: Testing (task#267.6 & 267.7)
- [ ] Unit tests
  - [ ] Git history parsing
  - [ ] Date calculations
  - [ ] Task filtering
  - [ ] Archive backup creation
- [ ] Integration tests
  - [ ] End-to-end CLI prune command
  - [ ] End-to-end MCP prune_tasks tool
  - [ ] Dry-run mode
  - [ ] Error scenarios
- [ ] Edge case tests
  - [ ] No git repository
  - [ ] Empty archive
  - [ ] Tasks without dates

### Phase 7: Documentation (task#267.9)
- [ ] Update `docs/cli.md` with prune command
- [ ] Update `docs/mcp.md` with prune_tasks tool
- [ ] Add examples to `docs/examples/`
- [ ] Update README.md
- [ ] Update CHANGELOG.md
- [ ] Add inline help text

## Open Questions for Design Phase

1. **Archive Date Ambiguity**
   - Should we prefer git log or completion date metadata?
   - How to handle discrepancies between the two?
   - **Recommendation:** Git log first, fall back to metadata

2. **Subtask Handling**
   - Should pruning parent auto-prune subtasks? (Probably yes)
   - Should we allow pruning individual subtasks? (Probably no - would orphan)
   - **Recommendation:** Always prune parent + all subtasks together

3. **Confirmation Prompts**
   - Should prune require confirmation by default?
   - Should --force skip all prompts (for AI agents)?
   - **Recommendation:** Yes to both. Default = prompt, --force = no prompts

4. **Backup Default**
   - Should backup be default ON or OFF?
   - Should --no-backup be available?
   - **Recommendation:** Default ON (safer), allow --no-backup for advanced users

5. **Archive Restoration**
   - Should we implement `restore-from-archive` command now or later?
   - Is manual restoration sufficient?
   - **Recommendation:** Manual for now, add command in future if needed

6. **Performance Thresholds**
   - What's the maximum number of archived tasks to handle efficiently?
   - Should we paginate or stream for very large archives?
   - **Recommendation:** Design for 1000+ tasks, optimize if needed

## Risk Assessment

### High Risk
- **Git history parsing complexity:** Mitigate with robust testing and fallback
- **Data loss if backup fails:** Mitigate with transaction safety (backup first, fail if backup fails)
- **FileOps integration errors:** Mitigate by following existing patterns exactly

### Medium Risk
- **Performance with large archives:** Mitigate with profiling and optimization if needed
- **MCP-CLI parity drift:** Mitigate with parity tests

### Low Risk
- **Command interface usability:** Mitigate with clear help text and examples
- **Archive file format compatibility:** Mitigate by using standard TODO.md format

## References

- **Original Task:** #129 (lines 105-108 in TODO.md)
- **Linear Issue:** https://linear.app/fxstein/issue/AIT-2
- **Specification:** `docs/development/TODO_TOOL_IMPROVEMENTS.md` (section 3.4)
- **GitHub Issue:** #51 (referenced in Linear attachments)
- **FileOps Class:** `ai_todo/core/file_ops.py`
- **Git Utilities:** `ai_todo/utils/git.py`
- **Archive Command:** `ai_todo/cli/commands/__init__.py` (lines 401-433)

## Next Steps

1. ✅ **Analysis Complete** (this document)
2. ⏭️ **Create Design Document** (task#267.2)
   - Finalize technical approach
   - Create detailed implementation plan
   - Define API contracts
   - Design test strategy
   - **STOP FOR REVIEW AFTER DESIGN**
3. ⏸️ **Implementation** (blocked until design approval)

---

**Analysis Completed:** 2026-01-28
**Analyst:** AI Agent (Cursor)
**Status:** Ready for design phase
**Blocking:** None
