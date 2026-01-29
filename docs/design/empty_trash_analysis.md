# Empty Trash Analysis - AIT-3

**Date:** 2026-01-29
**Linear Issue:** [AIT-3](https://linear.app/fxstein/issue/AIT-3/implement-empty-trash-on-startup-deleted-tasks)
**GitHub Issue:** [#52](https://github.com/fxstein/ai-todo/issues/52)
**Task:** #268

## Executive Summary

Implement startup policy to permanently remove items from "Deleted Tasks" section older than 7 days, providing an "Empty Trash" operation similar to desktop operating systems.

## Current State

### Existing Deleted Tasks Infrastructure

**1. Task Model (`ai_todo/core/task.py`)**
- `deleted_at`: Timestamp when task was deleted
- `expires_at`: Timestamp when task should be purged (30 days after deletion)
- `mark_deleted()`: Sets both timestamps, expiration = deletion + 30 days
- `restore()`: Clears deletion timestamps

**2. Deletion Metadata Format**
```markdown
- [D] **#123** Task description (deleted 2026-01-27, expires 2026-02-26)
```

**3. File Structure**
```
## Tasks
(active tasks)

## Archived Tasks
(completed, archived tasks)

## Deleted Tasks
(soft-deleted tasks with expiration dates)

---
(footer with metadata)
```

**4. Legacy Bash Implementation**

The legacy `todo.bash` script already has `purge_expired_deleted_tasks()` function:
- Runs on startup (line 3224-3225)
- Finds tasks with `[D]` checkbox
- Parses expiration dates from metadata
- Removes tasks where `expire_date < current_date`
- Reports: "Auto-purged N expired task(s)"

**Key Code:**
```bash
purge_expired_deleted_tasks() {
    local current_date=$(date +"%Y-%m-%d")
    local purged_count=0

    while IFS= read -r line; do
        if [[ "$line" =~ "expires ([0-9]{4}-[0-9]{2}-[0-9]{2})" ]]; then
            local expire_date="${BASH_REMATCH[1]}"
            if [[ "$expire_date" < "$current_date" ]]; then
                # Remove expired task
                sed_inplace "/$(echo "$line" | sed 's/[]\/$*.^[]/\\&/g')/d" "$TODO_FILE"
                purged_count=$((purged_count + 1))
            fi
        fi
    done < <(grep "^\- \[D\]" "$TODO_FILE")
}
```

### Related: Prune Implementation (AIT-2/task#267)

The recently completed prune functionality provides a strong foundation:

**`ai_todo/core/prune.py` - Key Components:**
- `PruneManager` class for managing pruning operations
- `PruneResult` dataclass for operation results
- Git history analysis for accurate date detection
- Backup creation with complete TASK_METADATA
- Filtering logic by age, date, and task ID range
- Dry-run mode for safe preview
- CLI and MCP tool interfaces

**Reusable Patterns:**
1. Manager class pattern (`PruneManager` → `EmptyTrashManager`)
2. Result dataclass for operation feedback
3. Filtering by date/age
4. Backup creation before removal
5. Dry-run mode
6. CLI + MCP parity

## Requirements Analysis

### AIT-3 Specifications

**Target:**
- Only items explicitly in "Deleted Tasks" section
- Never touch "Archived Tasks" or active "Tasks"

**Retention Rule:**
- Remove items older than 7 days (from deletion date)
- Note: This is DIFFERENT from the existing 30-day expiration!

**Trigger:**
- Automatic on startup (similar to legacy bash behavior)

**Safety:**
- Strict section isolation
- No impact on other sections
- Clear logging of what was removed

### Key Differences from Prune

| Feature | Prune (task#267) | Empty Trash (task#268) |
|---------|------------------|------------------------|
| **Target Section** | Archived Tasks | Deleted Tasks |
| **Retention** | 30 days (default, configurable) | 7 days (fixed) |
| **Trigger** | Manual command | Automatic on startup |
| **Backup** | Yes, in `.ai-todo/archives/` | Maybe (optional) |
| **Git History** | Yes, for accurate dates | Not needed (has `deleted_at`) |
| **Options** | --days, --older-than, --from-task | None (fixed policy) |

## Technical Considerations

### 1. Expiration Logic Conflict

**Current Behavior:**
- Tasks are deleted with 30-day expiration: `expires_at = deleted_at + timedelta(days=30)`
- Metadata shows: `(deleted 2026-01-27, expires 2026-02-26)`

**AIT-3 Requirement:**
- Remove tasks older than 7 days from deletion

**Issue:**
The AIT-3 7-day policy is MORE AGGRESSIVE than the existing 30-day expiration metadata. This creates a conflict:

**Options:**
1. **Ignore `expires_at`, use 7-day rule** - Most direct, but creates inconsistency
2. **Update `expires_at` to 7 days** - Breaking change, affects existing deleted tasks
3. **Make it configurable** - More flexible, aligns with prune's design
4. **Separate policies** - Empty trash (7 days) vs expiration (30 days display)

**Recommendation:** Option 3 or 4 - see Design section below.

### 2. Startup Trigger

**Python Context:**
- Legacy bash called `purge_expired_deleted_tasks()` on startup
- Python has two entry points:
  - CLI: `ai_todo/cli/main.py`
  - MCP Server: `ai_todo/mcp/server.py`

**Implementation Options:**
1. **Call on every CLI command** (like bash startup)
2. **Call on MCP server startup** (when Cursor launches)
3. **Explicit command only** (`ai-todo empty-trash`)
4. **Hybrid**: Automatic in MCP, manual in CLI

**Recommendation:** Option 4 - automatic in MCP (most common use case), manual command available for CLI.

### 3. Backup Strategy

**Prune** creates extensive backups because archived tasks have historical value.

**Empty Trash** is different:
- Users explicitly deleted these tasks
- Tasks already have 7-30 day retention
- "Empty Trash" implies permanence

**Options:**
1. **No backup** - Matches desktop OS "Empty Trash" semantics
2. **Optional backup** - Safety net, like prune's `--no-backup`
3. **Temporary backup** - Keep for 24-48 hours then auto-remove

**Recommendation:** Option 2 - default no backup, but allow `--backup` flag for paranoid users.

### 4. Safety Verification

**Critical:** Must NOT remove tasks from other sections.

**Strategy:**
- Parse TODO.md to identify section boundaries
- Only process tasks where `current_section == "Deleted Tasks"`
- Verify task status is `TaskStatus.DELETED`
- Double-check before removal

## Proposed Architecture

### Core Module: `ai_todo/core/empty_trash.py`

```python
@dataclass
class EmptyTrashResult:
    """Result of empty trash operation."""
    tasks_removed: int
    subtasks_removed: int
    dry_run: bool
    removed_task_ids: list[str]

class EmptyTrashManager:
    """Manage empty trash operations on deleted tasks."""

    def identify_expired_deleted_tasks(
        self, tasks: list[Task], days: int = 7
    ) -> list[Task]:
        """Identify deleted tasks older than N days."""

    def empty_trash(
        self, days: int = 7, dry_run: bool = False, backup: bool = False
    ) -> EmptyTrashResult:
        """Permanently remove old deleted tasks."""
```

### CLI Command: `ai-todo empty-trash`

```bash
ai-todo empty-trash              # Remove deleted tasks older than 7 days
ai-todo empty-trash --days 14    # Custom retention period
ai-todo empty-trash --dry-run    # Preview what would be removed
ai-todo empty-trash --backup     # Create backup before removal
```

### MCP Tool: `empty_trash`

```python
@mcp.tool()
def empty_trash(
    days: int = 7,
    dry_run: bool = False,
    backup: bool = False,
) -> dict:
    """Permanently remove old deleted tasks."""
```

### Startup Hook

**MCP Server (`ai_todo/mcp/server.py`):**
```python
# On server startup
@mcp.init()
async def init():
    """Initialize MCP server and run startup tasks."""
    # Auto empty trash (silent, no backup)
    try:
        mgr = EmptyTrashManager(CURRENT_TODO_PATH)
        mgr.empty_trash(days=7, dry_run=False, backup=False)
    except Exception:
        pass  # Fail silently on startup
```

## Implementation Strategy

### Phase 1: Core Functionality
1. Create `ai_todo/core/empty_trash.py`
2. Implement `EmptyTrashManager` class
3. Implement `identify_expired_deleted_tasks()` filtering
4. Implement `empty_trash()` removal logic
5. Reuse `FileOps` for safe file operations

### Phase 2: CLI & MCP Interfaces
1. Add `empty_trash_command()` to `ai_todo/cli/commands/__init__.py`
2. Add CLI command to `ai_todo/cli/main.py`
3. Add MCP tool to `ai_todo/mcp/server.py`
4. Add startup hook to MCP server

### Phase 3: Testing
1. Unit tests for `EmptyTrashManager`
2. Integration tests for CLI command
3. Integration tests for MCP tool
4. Test startup behavior
5. Test safety (section isolation)

### Phase 4: Documentation
1. Update CLI docs with `empty-trash` command
2. Update MCP docs with empty_trash tool
3. Add examples to docs/examples/
4. Update CHANGELOG.md

## Open Questions

### 1. Retention Period: 7 vs 30 days

**AIT-3 says:** 7 days
**Current expiration:** 30 days (in `expires_at` metadata)

**Resolution needed:**
- Keep 7 days for AIT-3 (as specified)?
- Make it configurable (default 7, allow override)?
- Align with existing 30-day expiration?

### 2. Startup Behavior

**Should empty trash run:**
- On every command?
- Only on MCP server startup?
- Only when explicitly called?
- Hybrid approach?

### 3. User Notification

**When auto-running on startup:**
- Silent (no output)?
- Log to `.ai-todo/.ai-todo.log`?
- Show notification (could be annoying)?

### 4. Backup Default

**Empty trash implies permanence, but:**
- Should we default to creating backups?
- Or default to no backup (like desktop OS)?
- User preference in config.yaml?

## Risk Assessment

### High Risk
- **Section confusion**: Accidentally removing tasks from wrong section
  - *Mitigation*: Strict section boundary checking, status verification

### Medium Risk
- **Premature removal**: Removing tasks user wanted to keep
  - *Mitigation*: Conservative default (7 days), dry-run mode, optional backup

### Low Risk
- **Performance**: Empty trash on every startup
  - *Mitigation*: Fast operation (only scans Deleted section), fail silently

## Dependencies

### External:
- None (uses existing infrastructure)

### Internal:
- `ai_todo.core.file_ops.FileOps` (reading/writing TODO.md)
- `ai_todo.core.task.Task` (task model with deleted_at/expires_at)
- `ai_todo.utils.logging` (logging operations)

### Blocked By:
- ~~AIT-2 (prune mechanics)~~ ✅ Complete

## Success Criteria

1. ✅ Deleted tasks older than 7 days are permanently removed
2. ✅ Only tasks in "Deleted Tasks" section are affected
3. ✅ Archived and active tasks are never touched
4. ✅ Operation runs automatically on MCP server startup
5. ✅ CLI command available for manual operation
6. ✅ Dry-run mode works correctly
7. ✅ Optional backup creation works
8. ✅ All operations logged
9. ✅ Complete test coverage (unit + integration)
10. ✅ Documentation updated

## Next Steps

1. Review this analysis with stakeholders
2. Create design document addressing open questions
3. Implement core `EmptyTrashManager` class
4. Add CLI and MCP interfaces
5. Write comprehensive tests
6. Update documentation

---

**Status:** Analysis complete, ready for design phase.
**Author:** AI Assistant
**Date:** 2026-01-29
