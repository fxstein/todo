# Empty Trash Design - AIT-3

**Date:** 2026-01-29
**Linear Issue:** [AIT-3](https://linear.app/fxstein/issue/AIT-3/implement-empty-trash-on-startup-deleted-tasks)
**GitHub Issue:** [#52](https://github.com/fxstein/ai-todo/issues/52)
**Task:** #268
**Depends On:** Analysis document (task#268.1)

## Overview

This design implements an automatic "Empty Trash" operation that permanently removes expired deleted tasks from the "Deleted Tasks" section. The implementation leverages existing infrastructure and follows patterns established by the prune functionality (AIT-2).

## Design Decisions (from Analysis)

All open questions have been resolved:

1. ✅ **Retention Period:** 30 days (use existing `expires_at` field)
2. ✅ **Startup Behavior:** MCP server startup + manual CLI command
3. ✅ **User Notification:** Silent with logging to `.ai-todo/.ai-todo.log`
4. ✅ **Backup Default:** No backup (true "Empty Trash" semantics)

## Architecture

### Module Structure

```
ai_todo/
├── core/
│   └── empty_trash.py (NEW)
├── cli/
│   ├── commands/__init__.py (UPDATE)
│   └── main.py (UPDATE)
└── mcp/
    └── server.py (UPDATE)
```

### Core Module: `ai_todo/core/empty_trash.py`

**Purpose:** Encapsulate all empty trash logic.

**Components:**

```python
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from ai_todo.core.file_ops import FileOps
from ai_todo.core.task import Task, TaskStatus
from ai_todo.utils.logging import log_operation


@dataclass
class EmptyTrashResult:
    """Result of an empty trash operation."""

    tasks_removed: int
    subtasks_removed: int
    dry_run: bool
    removed_task_ids: list[str]
    backup_path: str | None = None

    @property
    def total_removed(self) -> int:
        """Total items removed (tasks + subtasks)."""
        return self.tasks_removed + self.subtasks_removed


class EmptyTrashManager:
    """Manage empty trash operations on deleted tasks."""

    def __init__(self, todo_path: str = "TODO.md"):
        """Initialize with TODO.md path."""
        self.todo_path = todo_path
        self.file_ops = FileOps(todo_path)

    def empty_trash(
        self,
        dry_run: bool = False,
        backup: bool = False,
    ) -> EmptyTrashResult:
        """
        Permanently remove expired deleted tasks.

        Args:
            dry_run: If True, only report what would be removed
            backup: If True, create backup before removal

        Returns:
            EmptyTrashResult with operation details
        """

    def identify_expired_deleted_tasks(
        self, tasks: list[Task]
    ) -> list[Task]:
        """
        Identify deleted tasks where expires_at < current_date.

        Args:
            tasks: All tasks from TODO.md

        Returns:
            List of expired deleted tasks (includes root + subtasks)
        """

    def _create_backup(self, tasks: list[Task]) -> str:
        """
        Create backup file with removed tasks (optional).

        Args:
            tasks: Tasks to backup

        Returns:
            Path to backup file
        """
```

## Detailed Implementation

### 1. Core Logic: `EmptyTrashManager`

#### `empty_trash()` Method

**Workflow:**
1. Read all tasks from TODO.md via FileOps
2. Identify expired deleted tasks
3. If dry_run: return preview, exit
4. If backup: create backup file
5. Remove expired tasks from task manager
6. Save changes via FileOps
7. Log operation
8. Return EmptyTrashResult

**Pseudocode:**
```python
def empty_trash(self, dry_run: bool = False, backup: bool = False) -> EmptyTrashResult:
    # Read current state
    self.file_ops.read_tasks()
    all_tasks = self.file_ops.task_manager.list_tasks()

    # Identify expired deleted tasks
    expired_tasks = self.identify_expired_deleted_tasks(all_tasks)

    if not expired_tasks:
        return EmptyTrashResult(0, 0, dry_run, [], None)

    # Count root vs subtasks
    root_count = sum(1 for t in expired_tasks if "." not in t.id)
    subtask_count = len(expired_tasks) - root_count
    task_ids = [t.id for t in expired_tasks]

    # Dry run: return preview
    if dry_run:
        return EmptyTrashResult(root_count, subtask_count, True, task_ids, None)

    # Optional backup
    backup_path = None
    if backup:
        backup_path = self._create_backup(expired_tasks)

    # Remove tasks
    for task in expired_tasks:
        self.file_ops.task_manager.remove_task(task.id)

    # Save changes
    self.file_ops.write_tasks()

    # Log operation
    log_operation(
        "EMPTY_TRASH",
        f"Removed {len(expired_tasks)} expired deleted task(s)",
        details={"task_ids": task_ids, "backup": backup_path}
    )

    return EmptyTrashResult(root_count, subtask_count, False, task_ids, backup_path)
```

#### `identify_expired_deleted_tasks()` Method

**Logic:**
1. Filter for status == DELETED
2. Verify expires_at is not None
3. Compare expires_at < current_date (timezone-aware UTC)
4. Return matching tasks

**Pseudocode:**
```python
def identify_expired_deleted_tasks(self, tasks: list[Task]) -> list[Task]:
    current_date = datetime.now(UTC)
    expired = []

    for task in tasks:
        # Must be deleted with expiration date
        if task.status != TaskStatus.DELETED:
            continue
        if task.expires_at is None:
            continue

        # Normalize to UTC if needed
        expires = task.expires_at
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=UTC)

        # Check if expired
        if expires < current_date:
            expired.append(task)

    return expired
```

#### `_create_backup()` Method

**Backup Location:**
- Directory: `.ai-todo/trash/`
- Filename: `TRASH_BACKUP_YYYY-MM-DD[_N].md`
- Format: Similar to prune archives

**Backup Structure:**
```markdown
# Empty Trash Backup - YYYY-MM-DD HH:MM:SS

**Retention Policy:** 30 days (expires_at)
**Operation Date:** YYYY-MM-DD HH:MM:SS UTC
**Tasks Removed:** N

---

## Removed Tasks

- [D] **#123** Task description (deleted 2026-01-27, expires 2026-02-26)
- [D] **#125** Another task (deleted 2026-01-20, expires 2026-02-19)

<!-- TASK_METADATA
123:2026-01-15T10:00:00:2026-01-27T15:30:00
125:2026-01-10T08:00:00:2026-01-20T12:00:00
-->

---
**Backup Created:** YYYY-MM-DD HH:MM:SS UTC
```

### 2. CLI Interface

#### Command Definition (`ai_todo/cli/main.py`)

```python
@cli.command("empty-trash")
@click.option("--dry-run", is_flag=True, help="Preview without removing")
@click.option("--backup", is_flag=True, help="Create backup before removal")
@click.pass_context
def empty_trash_cmd(ctx, dry_run: bool, backup: bool):
    """Permanently remove expired deleted tasks (30-day retention)."""
    empty_trash_command(
        dry_run=dry_run,
        backup=backup,
        todo_path=ctx.obj["todo_file"],
    )
```

#### Command Implementation (`ai_todo/cli/commands/__init__.py`)

```python
def empty_trash_command(
    dry_run: bool = False,
    backup: bool = False,
    todo_path: str = "TODO.md",
):
    """Permanently remove expired deleted tasks."""
    from ai_todo.core.empty_trash import EmptyTrashManager

    manager = EmptyTrashManager(todo_path)
    result = manager.empty_trash(dry_run=dry_run, backup=backup)

    if result.total_removed == 0:
        print("ℹ️ No expired deleted tasks found.")
        return

    if dry_run:
        print(f"🔍 Would remove {result.total_removed} expired task(s):")
        print(f"   - Root tasks: {result.tasks_removed}")
        print(f"   - Subtasks: {result.subtasks_removed}")
        print(f"   - IDs: {', '.join(result.removed_task_ids)}")
    else:
        print(f"🗑️ Removed {result.total_removed} expired task(s)")
        if result.backup_path:
            print(f"📦 Backup: {result.backup_path}")
```

### 3. MCP Interface

#### Tool Definition (`ai_todo/mcp/server.py`)

```python
@mcp.tool()
def empty_trash(
    dry_run: bool = False,
    backup: bool = False,
) -> dict:
    """
    Permanently remove expired deleted tasks (30-day retention).

    This operation removes tasks from the "Deleted Tasks" section where
    the expiration date (expires_at) has passed. By default, no backup
    is created (true "Empty Trash" semantics).

    Args:
        dry_run: Preview without removing (default: False)
        backup: Create backup before removal (default: False)

    Returns:
        dict with operation results
    """
    from ai_todo.core.empty_trash import EmptyTrashManager

    manager = EmptyTrashManager(CURRENT_TODO_PATH)
    result = manager.empty_trash(dry_run=dry_run, backup=backup)

    return {
        "tasks_removed": result.tasks_removed,
        "subtasks_removed": result.subtasks_removed,
        "total_removed": result.total_removed,
        "dry_run": result.dry_run,
        "removed_task_ids": result.removed_task_ids,
        "backup_path": result.backup_path,
        "message": _format_result_message(result),
    }


def _format_result_message(result: EmptyTrashResult) -> str:
    """Format user-friendly result message."""
    if result.total_removed == 0:
        return "ℹ️ No expired deleted tasks found."

    if result.dry_run:
        return (
            f"🔍 Would remove {result.total_removed} expired task(s): "
            f"{result.tasks_removed} root, {result.subtasks_removed} subtasks"
        )

    msg = f"🗑️ Removed {result.total_removed} expired task(s)"
    if result.backup_path:
        msg += f" (backup: {result.backup_path})"
    return msg
```

### 4. Startup Hook

#### MCP Server Init (`ai_todo/mcp/server.py`)

**Location:** After server initialization, before accepting requests.

```python
# At module level or in server setup
def _auto_empty_trash():
    """Auto-run empty trash on server startup (silent)."""
    try:
        from ai_todo.core.empty_trash import EmptyTrashManager

        manager = EmptyTrashManager(CURRENT_TODO_PATH)
        result = manager.empty_trash(dry_run=False, backup=False)

        # Only log if tasks were removed
        if result.total_removed > 0:
            log_operation(
                "AUTO_EMPTY_TRASH",
                f"Startup: Removed {result.total_removed} expired task(s)",
                details={"task_ids": result.removed_task_ids}
            )
    except Exception as e:
        # Fail silently - don't block server startup
        log_operation("AUTO_EMPTY_TRASH_ERROR", f"Failed: {e}")


# In server initialization
if __name__ == "__main__":
    # Run auto empty trash before starting server
    _auto_empty_trash()

    # Start MCP server
    mcp.run()
```

**Note:** For CLI, empty trash is NOT auto-run on every command. Users must explicitly call `ai-todo empty-trash`.

## Safety Mechanisms

### 1. Section Boundary Checking

**Critical:** Only process tasks in "Deleted Tasks" section.

**Implementation:**
- FileOps already tracks `current_section` during parsing
- Task objects have `.status == TaskStatus.DELETED`
- Double verification:
  1. Task status must be DELETED
  2. Task must have `expires_at` field
  3. Only remove if both conditions met

### 2. Expiration Date Validation

**Requirements:**
- Must have `expires_at` field (not None)
- Must be in the past (< current_date)
- Use timezone-aware UTC datetimes for comparison

### 3. Subtask Handling

**Behavior:**
- If root task is expired, include all its subtasks
- If subtask is expired but parent is not, only remove subtask
- Maintain task hierarchy in removal

**Logic:**
```python
# Natural behavior: just filter by expires_at
# FileOps will handle subtask cleanup when root is removed
```

### 4. Idempotency

**Guarantee:** Running empty trash multiple times has same effect as once.

**Implementation:**
- Read current state each time
- Only remove tasks meeting criteria
- No side effects if already empty

## Error Handling

### Startup Errors

**Requirement:** Never block MCP server startup.

**Strategy:**
```python
try:
    manager.empty_trash()
except Exception as e:
    log_operation("AUTO_EMPTY_TRASH_ERROR", str(e))
    # Continue server startup
```

### CLI Errors

**Requirement:** Report errors clearly to user.

**Strategy:**
- Catch `ValueError` for invalid task operations
- Catch `FileNotFoundError` for missing TODO.md
- Report via print() with clear error messages
- Exit with code 1 on failure

### MCP Errors

**Requirement:** Return error in response, don't crash.

**Strategy:**
- Catch all exceptions
- Return error in result dict
- Log error for debugging

## Logging Strategy

### Log Entries

**Format:** Existing ai-todo log format in `.ai-todo/.ai-todo.log`

**Operations to Log:**

1. **AUTO_EMPTY_TRASH** (startup)
   - Only log if tasks were removed
   - Include task IDs

2. **EMPTY_TRASH** (manual command)
   - Always log (even if 0 tasks)
   - Include dry_run flag
   - Include backup path if created

3. **AUTO_EMPTY_TRASH_ERROR** (startup failure)
   - Log error details for debugging

**Example Log Lines:**
```
2026-01-29 03:00:15 | system | AUTO_EMPTY_TRASH | Removed 3 expired task(s) | task_ids: 123,125,127
2026-01-29 10:30:00 | oratzes | CLI | EMPTY_TRASH | Dry run: 2 expired task(s) | task_ids: 130,132
2026-01-29 10:30:30 | oratzes | CLI | EMPTY_TRASH | Removed 2 expired task(s) | task_ids: 130,132
```

## Performance Considerations

### Startup Performance

**Goal:** Minimal impact on MCP server startup time.

**Optimizations:**
1. Only scan "Deleted Tasks" section (FileOps already separates sections)
2. Simple date comparison (no git operations)
3. Fail silently on error (don't block)
4. Skip if section is empty

**Expected Time:** <100ms for typical case (0-50 deleted tasks)

### Memory Usage

**Consideration:** Load only deleted tasks, not entire TODO.md.

**Implementation:**
- FileOps loads all tasks (needed for integrity)
- Filter to deleted tasks immediately
- Release references after operation

## CLI + MCP Parity

### Feature Parity Matrix

| Feature | CLI | MCP | Notes |
|---------|-----|-----|-------|
| **Remove expired tasks** | ✅ | ✅ | Core functionality |
| **Dry run mode** | ✅ | ✅ | `--dry-run` flag |
| **Optional backup** | ✅ | ✅ | `--backup` flag |
| **Auto-run on startup** | ❌ | ✅ | MCP only |
| **Result details** | ✅ | ✅ | Same info, different format |

### Output Format Differences

**CLI Output (human-readable):**
```
🗑️ Removed 3 expired task(s)
   - Root tasks: 2
   - Subtasks: 1
   - IDs: 123, 125, 127
```

**MCP Output (structured):**
```json
{
  "tasks_removed": 2,
  "subtasks_removed": 1,
  "total_removed": 3,
  "dry_run": false,
  "removed_task_ids": ["123", "125", "127"],
  "backup_path": null,
  "message": "🗑️ Removed 3 expired task(s)"
}
```

## File Operations

### Removal Process

**Use:** `TaskManager.remove_task(task_id)` (existing method)

**Behavior:**
- Removes task from internal task list
- Removes from TASK_METADATA
- Does NOT write to file (caller's responsibility)

**Safety:**
- Atomic: all removals in memory, single write at end
- FileOps handles checksums and shadow copies
- Tamper detection works normally

### Backup Creation (Optional)

**Directory:** `.ai-todo/trash/`
**Naming:** `TRASH_BACKUP_YYYY-MM-DD[_N].md`
**Content:** Full task details + TASK_METADATA

**Implementation:**
```python
def _create_backup(self, tasks: list[Task]) -> str:
    backup_dir = Path(self.todo_path).parent / ".ai-todo" / "trash"
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    base_name = f"TRASH_BACKUP_{datetime.now(UTC).strftime('%Y-%m-%d')}"
    backup_path = backup_dir / f"{base_name}.md"

    counter = 1
    while backup_path.exists():
        backup_path = backup_dir / f"{base_name}_{counter}.md"
        counter += 1

    # Write backup file
    with open(backup_path, "w") as f:
        f.write(self._format_backup(tasks))

    return str(backup_path)
```

## Edge Cases

### 1. Empty Deleted Tasks Section

**Scenario:** No deleted tasks in TODO.md

**Behavior:**
- Return EmptyTrashResult with 0 tasks removed
- CLI: Print "ℹ️ No expired deleted tasks found."
- MCP: Return success with 0 count
- Don't log (nothing happened)

### 2. No Expired Tasks

**Scenario:** Deleted tasks exist, but none expired

**Behavior:**
- Same as above (0 tasks removed)

### 3. Deleted Task Without expires_at

**Scenario:** Malformed deleted task (missing expiration date)

**Behavior:**
- Skip the task (don't remove)
- Log warning for investigation
- Continue processing other tasks

### 4. Concurrent Modifications

**Scenario:** TODO.md modified while empty trash is running

**Behavior:**
- FileOps handles via checksums
- If tamper detected: operation fails safely
- User must resolve with `ai-todo tamper`

### 5. Backup Directory Doesn't Exist

**Scenario:** `.ai-todo/trash/` doesn't exist

**Behavior:**
- Create directory automatically
- No error, just create and proceed

## Testing Strategy

### Unit Tests (`tests/unit/test_empty_trash.py`)

**Coverage:**
1. `identify_expired_deleted_tasks()` - basic filtering
2. `identify_expired_deleted_tasks()` - timezone handling
3. `identify_expired_deleted_tasks()` - missing expires_at
4. `identify_expired_deleted_tasks()` - not expired
5. `empty_trash()` - dry run mode
6. `empty_trash()` - actual removal
7. `empty_trash()` - with backup
8. `empty_trash()` - empty section
9. `_create_backup()` - file creation
10. `_create_backup()` - filename collision

### Integration Tests (`tests/integration/test_empty_trash_integration.py`)

**Coverage:**
1. CLI: Basic empty trash
2. CLI: Dry run mode
3. CLI: With backup flag
4. CLI: Empty section handling
5. MCP: Basic empty trash
6. MCP: Dry run mode
7. MCP: With backup flag
8. MCP/CLI parity: Same result for same input
9. Safety: Only removes from Deleted Tasks section
10. Safety: Never touches Archived or active tasks
11. Subtasks: Removed with parent
12. Subtasks: Removed independently if parent not expired
13. Logging: Operations logged correctly
14. Backup: File created with correct content
15. Backup: TASK_METADATA included

### Startup Tests

**Challenge:** Testing MCP server startup is complex.

**Approach:**
- Test `_auto_empty_trash()` function directly
- Mock file operations if needed
- Verify silent failure on error

## Migration Considerations

### Backward Compatibility

**No Breaking Changes:**
- Existing delete/restore commands unchanged
- Expiration metadata format unchanged
- Task model unchanged

### Data Migration

**None Required:**
- All existing deleted tasks already have `expires_at`
- Format is consistent

### User Impact

**Minimal:**
- Transparent operation (silent on startup)
- Old deleted tasks automatically cleaned up
- Manual command available if needed

## Documentation Updates

### 1. User-Facing Docs

**Files to Update:**
- `docs/guides/GETTING_STARTED.md` - Add empty-trash command
- `docs/user/MCP_SETUP.md` - Add empty_trash tool
- `docs/examples/` - Create EMPTY_TRASH_EXAMPLES.md (optional)
- `CHANGELOG.md` - Add feature entry
- `README.md` - Mention empty trash (optional)

### 2. Developer Docs

**Files to Update:**
- `CONTRIBUTING.md` - Mention startup hook testing
- Architecture docs (if any)

## Comparison with Prune

### Similarities

- Manager class pattern
- Result dataclass
- Dry-run mode
- Optional backup
- CLI + MCP interfaces
- FileOps integration
- Logging

### Differences

| Aspect | Prune | Empty Trash |
|--------|-------|-------------|
| **Target** | Archived Tasks | Deleted Tasks |
| **Date Source** | Git history + metadata | expires_at field |
| **Complexity** | High (git analysis) | Low (simple comparison) |
| **Default Backup** | Yes | No |
| **Auto-run** | No | Yes (MCP startup) |
| **Configurability** | High (days/date/range) | Low (fixed policy) |

## Security & Safety

### Permissions

**No Special Permissions Needed:**
- Reads/writes TODO.md (same as other commands)
- Creates backup in `.ai-todo/trash/` (user's directory)

### Data Loss Prevention

**Mechanisms:**
1. **30-day retention** - conservative default
2. **Optional backup** - user can enable if paranoid
3. **Dry-run mode** - preview before removal
4. **Clear metadata** - users see expiration dates
5. **Logging** - audit trail of all removals

### Attack Vectors

**None Identified:**
- No external input (uses expires_at from file)
- No code execution
- No network operations
- Bounded operation (single file)

## Implementation Checklist

### Phase 1: Core (task#268.3)
- [ ] Create `ai_todo/core/empty_trash.py`
- [ ] Implement `EmptyTrashResult` dataclass
- [ ] Implement `EmptyTrashManager` class
- [ ] Implement `identify_expired_deleted_tasks()` method
- [ ] Implement `empty_trash()` method
- [ ] Implement `_create_backup()` method (optional)
- [ ] Add proper error handling
- [ ] Add logging integration

### Phase 2: Interfaces (task#268.3)
- [ ] Add `empty_trash_command()` to `ai_todo/cli/commands/__init__.py`
- [ ] Add CLI command to `ai_todo/cli/main.py`
- [ ] Add `empty_trash` MCP tool to `ai_todo/mcp/server.py`
- [ ] Add `_auto_empty_trash()` startup hook to `ai_todo/mcp/server.py`
- [ ] Add `_format_result_message()` helper

### Phase 3: Testing (task#268.4)
- [ ] Create `tests/unit/test_empty_trash.py` (10 tests)
- [ ] Create `tests/integration/test_empty_trash_integration.py` (15 tests)
- [ ] Test startup hook behavior
- [ ] Test all edge cases
- [ ] Verify CLI/MCP parity

### Phase 4: Documentation (task#268.6)
- [ ] Update `docs/guides/GETTING_STARTED.md`
- [ ] Update `docs/user/MCP_SETUP.md`
- [ ] Create `docs/examples/EMPTY_TRASH_EXAMPLES.md` (optional)
- [ ] Update `CHANGELOG.md`

## Success Metrics

**Definition of Done:**
1. ✅ All unit tests pass (10+ tests)
2. ✅ All integration tests pass (15+ tests)
3. ✅ Full test suite passes (300+ tests)
4. ✅ Linting passes (ruff, markdownlint)
5. ✅ Manual testing via MCP confirms behavior
6. ✅ Startup hook runs silently
7. ✅ CLI command works as expected
8. ✅ Documentation complete and accurate

---

**Status:** Design complete, ready for implementation.
**Author:** AI Assistant
**Date:** 2026-01-29
