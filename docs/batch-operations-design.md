# Batch Operations Design Document

**Task:** #261 - Implement batch operations for task state commands
**Status:** APPROVED
**Date:** 2026-01-27
**Decision:** Option A - Single `task_ids: list[str]` parameter (1 to n items)

## Executive Summary

Add consistent batch support (single ID or list of IDs) to `complete`, `archive`, `delete`, and `restore` commands across CLI and MCP interfaces.

## Current State Analysis

| Command | CLI | Commands Module | MCP Server |
|---------|-----|-----------------|------------|
| complete | `task_ids` (list) | `list[str]` | single `task_id` |
| delete | `task_ids` (list) | `list[str]` | single `task_id` |
| archive | `task_ids` (list) | `list[str]` | single `task_id` |
| restore | `task_id` (single) | single `str` | single `task_id` |

### Key Findings

1. **CLI already supports batch** for `complete`, `delete`, `archive` via `nargs=-1`
2. **CLI restore is inconsistent** - only accepts single task ID
3. **MCP tools all single-ID only** - no batch support
4. **Commands module has batch support** via `expand_task_ids()` helper

## Proposed Design

### Option A: Single `task_ids` List Parameter (Recommended)

Replace `task_id: str` with `task_ids: list[str]` that accepts 1 to n items.

**MCP Tool Signatures:**

```python
# Before
def complete_task(task_id: str, with_subtasks: bool = False) -> str:

# After
def complete_task(task_ids: list[str], with_subtasks: bool = False) -> str:
```

**Advantages:**
- Single, consistent parameter across all tools
- No ambiguity about which parameter takes precedence
- Cleaner API surface
- List of 1 item is equivalent to single task ID

**Validation:**
```python
# Simple validation - list must have at least 1 item
if not task_ids:
    raise ValueError("task_ids must contain at least one task ID")
```

### Option B: Keep Both Parameters (Backward Compatible)

Keep `task_id: str | None` and add `task_ids: list[str] | None`, with `task_ids` taking precedence.

**Pros:** Backward compatible with existing MCP clients
**Cons:** Two parameters doing similar things, complexity

### Option C: Comma-Separated String

Accept comma-separated IDs in `task_id` parameter: `"123,124,125"`

**Pros:** No signature change
**Cons:** Less explicit, parsing overhead, inconsistent with CLI

## Approved Approach: Option A

### Implementation Plan

#### 1. CLI Changes

**`restore` command** - Add batch support:
```python
# Before
@click.argument("task_id")
def restore(ctx, task_id):

# After
@click.argument("task_ids", nargs=-1, required=True)
def restore(ctx, task_ids):
```

**`restore_command`** - Accept list:
```python
def restore_command(task_ids: list[str], todo_path: str = "TODO.md"):
    for task_id in task_ids:
        # existing restore logic
```

#### 2. MCP Server Changes

Update all four tools with consistent `task_ids: list[str]` pattern:

```python
@mcp.tool()
def complete_task(task_ids: list[str], with_subtasks: bool = False) -> str:
    """Mark task(s) as complete.

    Args:
        task_ids: List of task IDs (1 to n items)
        with_subtasks: Include subtasks in operation
    """
    return _capture_output(complete_command, task_ids, with_subtasks, todo_path=CURRENT_TODO_PATH)

@mcp.tool()
def delete_task(task_ids: list[str], with_subtasks: bool = True) -> str:
    """Delete task(s) and move to Deleted section.

    Args:
        task_ids: List of task IDs (1 to n items)
        with_subtasks: Include subtasks (default: True)
    """
    return _capture_output(delete_command, task_ids, with_subtasks, todo_path=CURRENT_TODO_PATH)

@mcp.tool()
def archive_task(task_ids: list[str], reason: str | None = None, with_subtasks: bool = False) -> str:
    """Archive task(s) to Recently Completed section.

    Args:
        task_ids: List of task IDs (1 to n items)
        reason: Optional reason for archiving
        with_subtasks: Include subtasks (default: False)
    """
    # Cooldown check for each root task
    for tid in task_ids:
        if "." not in tid and tid in SESSION_COMPLETIONS:
            elapsed = (datetime.now() - SESSION_COMPLETIONS[tid]).total_seconds()
            if elapsed < ARCHIVE_COOLDOWN_SECONDS:
                return f"Task #{tid} requires human review before archiving."
    return _capture_output(archive_command, task_ids, reason, todo_path=CURRENT_TODO_PATH)

@mcp.tool()
def restore_task(task_ids: list[str]) -> str:
    """Restore task(s) from Deleted or Archived.

    Args:
        task_ids: List of task IDs (1 to n items)
    """
    return _capture_output(restore_command, task_ids, todo_path=CURRENT_TODO_PATH)
```

### Breaking Change Notice

This is a **breaking change** for MCP clients:
- `task_id: str` → `task_ids: list[str]`
- Existing calls like `complete_task(task_id="123")` must change to `complete_task(task_ids=["123"])`

**Mitigation:** This is an internal tool primarily used by AI agents within Cursor. The change improves consistency and the migration is straightforward.

### Output Format

Batch operations return aggregated results:

```
Completed: #123 Task one
Completed: #124 Task two
Completed: #125 Task three
```

Or for delete/archive:
```
Deleted 3 task(s)
Archived 3 task(s)
```

## Testing Strategy

### Unit Tests

1. `test_batch_complete()` - single and multiple IDs
2. `test_batch_delete()` - with/without subtasks
3. `test_batch_archive()` - cooldown behavior per task
4. `test_batch_restore()` - from both deleted and archived
5. `test_empty_task_ids()` - validation error for empty list

### Integration Tests

1. CLI batch commands with multiple IDs
2. MCP tools with `task_ids` parameter
3. Mixed scenarios (some succeed, some fail)

### MCP/CLI Parity Tests

Extend `test_mcp_cli_parity.py` for batch operations.

## Open Questions

1. **Error handling:** Should batch fail-fast or process all and report errors?
   - **Recommendation:** Process all, collect errors, report at end

2. **Transaction semantics:** Should batch be atomic (all-or-nothing)?
   - **Recommendation:** No, individual operations (matches current behavior)

3. **Archive cooldown:** Apply to entire batch or per-task?
   - **Recommendation:** Per-task (any blocked task blocks that task only)

## Summary of Changes

| File | Change |
|------|--------|
| `ai_todo/mcp/server.py` | Change `task_id: str` → `task_ids: list[str]` on 4 tools |
| `ai_todo/cli/main.py` | Update `restore` to accept multiple IDs |
| `ai_todo/cli/commands/__init__.py` | Update `restore_command` to accept list |
| `tests/unit/test_batch_ops.py` | New unit tests |
| `tests/integration/test_mcp_cli_parity.py` | Add batch parity tests |

---

**APPROVED** - Ready for implementation.
