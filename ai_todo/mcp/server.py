"""MCP server for ai-todo."""

import asyncio
import io
import json
import sys
from datetime import datetime
from pathlib import Path

from fastmcp import FastMCP

from ai_todo.cli.commands import (
    add_command,
    add_subtask_command,
    archive_command,
    complete_command,
    config_command,
    delete_command,
    delete_note_command,
    detect_coordination_tool_command,
    lint_command,
    list_command,
    modify_command,
    note_command,
    reformat_command,
    relate_command,
    reorder_command,
    resolve_conflicts_command,
    restore_command,
    setup_coordination_tool_command,
    show_command,
    switch_mode_tool_command,
    undo_command,
    update_note_command,
)
from ai_todo.core.exceptions import TamperError

# Initialize FastMCP
mcp = FastMCP("ai-todo")

# Global state for todo path (set by run_server)
CURRENT_TODO_PATH: str = "TODO.md"

# Session-based tracking for archive cooldown
# Maps task_id -> completion timestamp (only tracks completions in current session)
SESSION_COMPLETIONS: dict[str, datetime] = {}
ARCHIVE_COOLDOWN_SECONDS = 60


def _capture_output(func, *args, **kwargs) -> str:
    """Capture stdout from a function call."""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    try:
        func(*args, **kwargs)
        return captured_output.getvalue() or "Success"
    except TamperError as e:
        return (
            f"⛔ TAMPER DETECTED: TODO.md has been modified externally.\n"
            f"Expected hash: {e.expected_hash[:8]}...\n"
            f"Actual hash:   {e.actual_hash[:8]}...\n\n"
            f"Use 'accept_tamper' tool to resolve."
        )
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        sys.stdout = old_stdout


# Basic Task Operations


@mcp.tool()
def add_task(title: str, description: str | None = None, tags: list[str] | None = None) -> str:
    """Add a new task to TODO.md.

    Args:
        title: The task headline (required)
        description: Optional detailed notes for the task
        tags: Optional list of tags
    """
    if tags is None:
        tags = []
    result = _capture_output(add_command, title, tags, todo_path=CURRENT_TODO_PATH)

    # If description provided and task was added successfully, add notes
    if description and "Added:" in result:
        # Extract task ID from result (format: "Added: #123 ...")
        import re

        match = re.search(r"Added: #(\S+)", result)
        if match:
            task_id = match.group(1)
            _capture_output(note_command, task_id, description, todo_path=CURRENT_TODO_PATH)

    return result


@mcp.tool()
def add_subtask(
    parent_id: str, title: str, description: str | None = None, tags: list[str] | None = None
) -> str:
    """Add a subtask to an existing task.

    Args:
        parent_id: ID of the parent task
        title: The subtask headline (required)
        description: Optional detailed notes for the subtask
        tags: Optional list of tags
    """
    if tags is None:
        tags = []
    result = _capture_output(
        add_subtask_command, parent_id, title, tags, todo_path=CURRENT_TODO_PATH
    )

    # If description provided and subtask was added successfully, add notes
    if description and "Added subtask:" in result:
        import re

        match = re.search(r"Added subtask: #(\S+)", result)
        if match:
            task_id = match.group(1)
            _capture_output(note_command, task_id, description, todo_path=CURRENT_TODO_PATH)

    return result


@mcp.tool()
def complete_task(task_ids: list[str], with_subtasks: bool = False) -> str:
    """Mark task(s) as complete.

    Args:
        task_ids: List of task IDs (1 to n items)
        with_subtasks: Include subtasks in operation
    """
    result = _capture_output(complete_command, task_ids, with_subtasks, todo_path=CURRENT_TODO_PATH)
    # Track completion time for archive cooldown (session-based)
    for task_id in task_ids:
        if "Completed:" in result or "Error" not in result:
            SESSION_COMPLETIONS[task_id] = datetime.now()
    return result


@mcp.tool()
def list_tasks(status: str | None = None, tag: str | None = None) -> str:
    """List tasks from TODO.md.

    Args:
        status: Filter by status (pending, completed, archived). currently only 'pending' supported via incomplete_only=True
        tag: Filter by tag
    """
    incomplete_only = status == "pending"
    return _capture_output(
        list_command, tag=tag, incomplete_only=incomplete_only, todo_path=CURRENT_TODO_PATH
    )


# Phase 1: Task Management


@mcp.tool()
def modify_task(
    task_id: str, title: str, description: str | None = None, tags: list[str] | None = None
) -> str:
    """Modify a task's title, description, and/or tags.

    Args:
        task_id: ID of the task to modify
        title: The new task headline (required)
        description: Optional new detailed notes (replaces existing notes if provided)
        tags: Optional list of tags (preserves existing tags if not provided)
    """
    if tags is None:
        tags = []
    result = _capture_output(modify_command, task_id, title, tags, todo_path=CURRENT_TODO_PATH)

    # If description provided and modify was successful, update notes
    if description is not None and "Modified:" in result:
        if description == "":
            # Clear notes
            _capture_output(delete_note_command, task_id, todo_path=CURRENT_TODO_PATH)
        else:
            # Set/replace notes
            _capture_output(update_note_command, task_id, description, todo_path=CURRENT_TODO_PATH)

    return result


@mcp.tool()
def delete_task(task_ids: list[str], with_subtasks: bool = True) -> str:
    """Delete task(s) and move to Deleted section.

    Args:
        task_ids: List of task IDs (1 to n items)
        with_subtasks: Include subtasks (default: True)
    """
    return _capture_output(delete_command, task_ids, with_subtasks, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def archive_task(
    task_ids: list[str], reason: str | None = None, with_subtasks: bool = False
) -> str:
    """Archive task(s) to Recently Completed section.

    Args:
        task_ids: List of task IDs (1 to n items)
        reason: Optional reason for archiving
        with_subtasks: Include subtasks (default: False)
    """
    # Session-based cooldown check for root tasks completed in this session
    for task_id in task_ids:
        if "." not in task_id and task_id in SESSION_COMPLETIONS:
            elapsed = (datetime.now() - SESSION_COMPLETIONS[task_id]).total_seconds()
            if elapsed < ARCHIVE_COOLDOWN_SECONDS:
                return f"Task #{task_id} requires human review before archiving."
    return _capture_output(archive_command, task_ids, reason, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def restore_task(task_ids: list[str]) -> str:
    """Restore task(s) from Deleted or Archived back to Tasks section.

    Args:
        task_ids: List of task IDs (1 to n items)
    """
    return _capture_output(restore_command, task_ids, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def prune_tasks(
    days: int | None = None,
    older_than: str | None = None,
    from_task: str | None = None,
    dry_run: bool = False,
    backup: bool = True,
) -> dict:
    """
    Prune old archived tasks from TODO.md.

    Args:
        days: Prune tasks older than N days (default: 30 if no other filter)
        older_than: Prune tasks before YYYY-MM-DD (format: YYYY-MM-DD)
        from_task: Prune tasks from #1 to #ID (numeric task ID)
        dry_run: Preview without making changes (default: False)
        backup: Create archive backup (default: True)

    Returns:
        dict with keys:
            - tasks_pruned: Number of root tasks pruned
            - subtasks_pruned: Number of subtasks pruned
            - total_pruned: Total items pruned
            - archive_path: Path to backup archive (if created)
            - dry_run: Whether this was a dry run
            - pruned_task_ids: List of task IDs pruned (preview in dry run)

    Examples:
        # Prune tasks older than 30 days (default)
        prune_tasks()

        # Prune tasks older than 60 days
        prune_tasks(days=60)

        # Prune tasks before specific date
        prune_tasks(older_than="2025-10-01")

        # Prune tasks from #1 to #50
        prune_tasks(from_task="50")

        # Preview what would be pruned
        prune_tasks(dry_run=True)

        # Prune without backup (not recommended)
        prune_tasks(backup=False)
    """
    from ai_todo.core.prune import PruneManager

    try:
        prune_mgr = PruneManager(CURRENT_TODO_PATH)
        result = prune_mgr.prune_tasks(
            days=days,
            older_than=older_than,
            from_task=from_task,
            dry_run=dry_run,
            backup=backup,
        )

        return {
            "tasks_pruned": result.tasks_pruned,
            "subtasks_pruned": result.subtasks_pruned,
            "total_pruned": result.total_pruned,
            "archive_path": result.archive_path,
            "dry_run": result.dry_run,
            "pruned_task_ids": result.pruned_task_ids,
        }
    except Exception as e:
        raise ValueError(f"Prune operation failed: {e}") from e


@mcp.tool()
def empty_trash(dry_run: bool = False) -> dict:
    """
    Permanently remove expired deleted tasks (30-day retention).

    This operation removes tasks from the "Deleted Tasks" section where
    the expiration date (expires_at) has passed. This is a permanent
    deletion with no backup (true "Empty Trash" semantics).

    Args:
        dry_run: Preview without removing (default: False)

    Returns:
        dict with keys:
            - tasks_removed: Number of root tasks removed
            - subtasks_removed: Number of subtasks removed
            - total_removed: Total items removed
            - dry_run: Whether this was a dry run
            - removed_task_ids: List of task IDs removed (preview in dry run)
            - message: Human-readable result message

    Examples:
        # Remove expired deleted tasks
        empty_trash()

        # Preview what would be removed
        empty_trash(dry_run=True)
    """
    from ai_todo.core.empty_trash import EmptyTrashManager

    try:
        manager = EmptyTrashManager(CURRENT_TODO_PATH)
        result = manager.empty_trash(dry_run=dry_run)

        # Format user-friendly message
        if result.total_removed == 0:
            message = "ℹ️  No expired deleted tasks found."
        elif result.dry_run:
            message = (
                f"🔍 Would remove {result.total_removed} expired task(s): "
                f"{result.tasks_removed} root, {result.subtasks_removed} subtasks"
            )
        else:
            message = f"🗑️  Removed {result.total_removed} expired task(s)"

        return {
            "tasks_removed": result.tasks_removed,
            "subtasks_removed": result.subtasks_removed,
            "total_removed": result.total_removed,
            "dry_run": result.dry_run,
            "removed_task_ids": result.removed_task_ids,
            "message": message,
        }
    except Exception as e:
        raise ValueError(f"Empty trash operation failed: {e}") from e


@mcp.tool()
def undo_task(task_id: str) -> str:
    """Reopen (undo) a completed task."""
    return _capture_output(undo_command, task_id, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def start_task(task_id: str) -> str:
    """Mark a task as in progress."""
    from ai_todo.cli.commands import start_command

    return _capture_output(start_command, task_id, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def stop_task(task_id: str) -> str:
    """Stop progress on a task."""
    from ai_todo.cli.commands import stop_command

    return _capture_output(stop_command, task_id, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def get_active_tasks() -> str:
    """Get a list of all currently active tasks (marked #inprogress)."""
    return _capture_output(
        list_command, tag="inprogress", incomplete_only=True, todo_path=CURRENT_TODO_PATH
    )


@mcp.prompt()
def active_context() -> str:
    """Get the current active context (in-progress tasks)."""
    return _capture_output(
        list_command, tag="inprogress", incomplete_only=True, todo_path=CURRENT_TODO_PATH
    )


# Phase 2: Description Management


@mcp.tool()
def set_description(task_id: str, description: str) -> str:
    """Set or clear a task's description (notes).

    This is idempotent - calling with the same description has no additional effect.

    Args:
        task_id: ID of the task
        description: The description text. Use "" (empty string) to clear.
    """
    if description == "":
        return _capture_output(delete_note_command, task_id, todo_path=CURRENT_TODO_PATH)
    else:
        # Check if task has existing notes - if so, update; otherwise add
        from ai_todo.cli.commands import get_manager

        manager = get_manager(CURRENT_TODO_PATH)
        task = manager.get_task(task_id)
        if task and task.notes:
            return _capture_output(
                update_note_command, task_id, description, todo_path=CURRENT_TODO_PATH
            )
        else:
            return _capture_output(note_command, task_id, description, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def set_tags(task_id: str, tags: list[str]) -> str:
    """Set a task's tags (replaces all existing tags).

    This is idempotent - calling with the same tags has no additional effect.

    Args:
        task_id: ID of the task
        tags: List of tags. Use [] (empty list) to clear all tags.
    """
    from ai_todo.cli.commands import get_manager, save_changes

    manager = get_manager(CURRENT_TODO_PATH)
    task = manager.get_task(task_id)
    if not task:
        return f"Error: Task {task_id} not found"

    # Set tags (replaces existing)
    task.tags = set(tags)
    save_changes(manager, CURRENT_TODO_PATH)

    if tags:
        tag_str = " ".join([f"`#{tag}`" for tag in sorted(tags)])
        return f"Set tags on #{task_id}: {tag_str}"
    else:
        return f"Cleared tags from #{task_id}"


# Phase 3: Task Display and Relationships


@mcp.tool()
def show_task(task_id: str) -> str:
    """Display task with subtasks, relationships, and notes."""
    return _capture_output(show_command, task_id, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def relate_task(task_id: str, rel_type: str, target_ids: list[str]) -> str:
    """Add task relationship (completed-by, depends-on, blocks, related-to, duplicate-of)."""
    return _capture_output(
        relate_command, task_id, rel_type, target_ids, todo_path=CURRENT_TODO_PATH
    )


# Phase 4: File Operations


@mcp.tool()
def lint() -> str:
    """Identify formatting issues (indentation, checkboxes)."""
    return _capture_output(lint_command, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def reformat(dry_run: bool = False) -> str:
    """Apply formatting fixes."""
    return _capture_output(reformat_command, dry_run, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def reorder() -> str:
    """Reorder subtasks to match reverse-chronological order (newest on top)."""
    return _capture_output(reorder_command, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def resolve_conflicts(dry_run: bool = False) -> str:
    """Detect and resolve duplicate task IDs."""
    return _capture_output(resolve_conflicts_command, dry_run, todo_path=CURRENT_TODO_PATH)


# Phase 5: Configuration and Setup


@mcp.tool()
def show_config() -> str:
    """Show current configuration."""
    return _capture_output(config_command, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def detect_coordination() -> str:
    """Detect available coordination options based on system."""
    return _capture_output(detect_coordination_tool_command, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def setup_coordination(coord_type: str) -> str:
    """Set up coordination service (github-issues, counterapi)."""
    return _capture_output(
        setup_coordination_tool_command,
        coord_type,
        interactive=False,
        todo_path=CURRENT_TODO_PATH,
    )


@mcp.tool()
def switch_mode(mode: str, force: bool = False, renumber: bool = False) -> str:
    """Switch numbering mode (single-user, multi-user, branch, enhanced)."""
    return _capture_output(
        switch_mode_tool_command, mode, force, renumber, todo_path=CURRENT_TODO_PATH
    )


# Phase 6: Info


@mcp.tool()
def version() -> str:
    """Return the current ai-todo version."""
    from ai_todo import __version__

    return f"ai-todo version {__version__}"


@mcp.tool()
def check_update() -> str:
    """Check if an ai-todo update is available, respecting version constraints.

    In development mode, suggests using 'restart' tool instead of version checking.
    """
    from pathlib import Path

    from ai_todo.core.updater import check_for_updates, is_dev_mode

    # In dev mode, version checks are irrelevant
    if is_dev_mode():
        from ai_todo import __version__

        return (
            f"Development mode (version {__version__})\n"
            "Version checks are not meaningful in dev mode.\n"
            "Use 'update' tool with restart=True to reload code changes."
        )

    # Get project root from TODO path
    project_root = Path(CURRENT_TODO_PATH).parent
    info = check_for_updates(project_root)
    return info.message


@mcp.tool()
def update(restart: bool = True) -> str:
    """Update ai-todo to the latest version and optionally restart.

    In development mode, this just restarts the server to pick up code changes.
    In production mode, updates via uv and optionally restarts.

    Args:
        restart: If True, restart the MCP server after update to apply changes.
                 The host (e.g., Cursor) will automatically reconnect.
    """
    from pathlib import Path

    from ai_todo.core.updater import is_dev_mode, perform_update, restart_server

    # In dev mode, skip version checks entirely - just restart if requested
    if is_dev_mode():
        if restart:
            import threading

            def delayed_restart():
                import time

                time.sleep(0.5)
                restart_server()

            threading.Thread(target=delayed_restart, daemon=True).start()
            return "Development mode: Restarting MCP server to pick up code changes..."
        else:
            return "Development mode: Use restart=True to reload code changes."

    # Production mode: perform actual update
    project_root = Path(CURRENT_TODO_PATH).parent
    success, message = perform_update(restart=restart, project_root=project_root)

    if success and restart:
        import threading

        def delayed_restart():
            import time

            time.sleep(0.5)
            restart_server()

        threading.Thread(target=delayed_restart, daemon=True).start()

    return message


# Phase 7: Tamper Detection


@mcp.tool()
def accept_tamper(reason: str) -> str:
    """Accept external changes to TODO.md."""
    from ai_todo.cli.tamper_ops import tamper_accept_command

    return _capture_output(tamper_accept_command, reason, todo_path=CURRENT_TODO_PATH)


# =============================================================================
# MCP Resources - Read-only data endpoints for IDE integration
# =============================================================================


def _task_to_dict(task) -> dict:
    """Convert a Task object to a JSON-serializable dictionary."""
    return {
        "id": task.id,
        "description": task.description,
        "status": task.status.value,
        "tags": sorted(task.tags) if task.tags else [],
        "notes": task.notes if task.notes else [],
        "is_subtask": "." in task.id,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
    }


def _get_open_tasks_data(todo_path: str) -> dict:
    """Get open tasks data (internal helper for testing).

    Returns dict with tasks list, count, filter, and timestamp.
    """
    from ai_todo.cli.commands import get_manager
    from ai_todo.core.task import IN_PROGRESS_TAG

    manager = get_manager(todo_path)
    tasks = manager.list_tasks()

    # Filter to open tasks: pending status OR has inprogress tag
    open_tasks = [
        t for t in tasks if t.status.value == "pending" or IN_PROGRESS_TAG in (t.tags or set())
    ]

    # Only include root tasks (not subtasks)
    root_tasks = [t for t in open_tasks if "." not in t.id]

    # Add subtask count for each root task
    result_tasks = []
    for task in root_tasks:
        task_dict = _task_to_dict(task)
        subtasks = [t for t in open_tasks if t.id.startswith(f"{task.id}.")]
        task_dict["subtask_count"] = len(subtasks)
        result_tasks.append(task_dict)

    return {
        "tasks": result_tasks,
        "count": len(result_tasks),
        "filter": "open",
        "timestamp": datetime.now().isoformat(),
    }


def _get_active_tasks_data(todo_path: str) -> dict:
    """Get active tasks data (internal helper for testing).

    Returns dict with tasks list, count, filter, and timestamp.
    """
    from ai_todo.cli.commands import get_manager
    from ai_todo.core.task import IN_PROGRESS_TAG

    manager = get_manager(todo_path)
    tasks = manager.list_tasks()

    # Filter to active tasks (has inprogress tag)
    active_tasks = [t for t in tasks if IN_PROGRESS_TAG in (t.tags or set())]

    result_tasks = [_task_to_dict(t) for t in active_tasks]

    return {
        "tasks": result_tasks,
        "count": len(result_tasks),
        "filter": "active",
        "timestamp": datetime.now().isoformat(),
    }


def _get_task_data(task_id: str, todo_path: str) -> dict:
    """Get task data (internal helper for testing).

    Returns dict with task, subtasks, relationships, and timestamp.
    """
    from ai_todo.cli.commands import get_manager
    from ai_todo.core.file_ops import FileOps

    file_ops = FileOps(todo_path)
    file_ops.read_tasks()  # Initialize file_ops with task data
    manager = get_manager(todo_path)

    task = manager.get_task(task_id)
    if not task:
        return {"error": f"Task #{task_id} not found", "timestamp": datetime.now().isoformat()}

    # Get subtasks
    subtasks = manager.get_subtasks(task_id)
    subtask_dicts = [_task_to_dict(s) for s in sorted(subtasks, key=lambda t: t.id)]

    # Get relationships
    relationships = file_ops.get_relationships(task_id) or {}

    return {
        "task": _task_to_dict(task),
        "subtasks": subtask_dicts,
        "relationships": relationships,
        "timestamp": datetime.now().isoformat(),
    }


def _get_config_data(todo_path: str) -> dict:
    """Get config data (internal helper for testing).

    Returns dict with numbering, security, coordination, and timestamp.
    """
    from ai_todo.core.config import Config
    from ai_todo.core.file_ops import FileOps

    # Get file_ops for paths
    file_ops = FileOps(todo_path)
    config_path = file_ops.config_dir / "config.yaml"
    config = Config(str(config_path))

    # Get next task ID
    next_id = None
    try:
        serial_path = file_ops.config_dir / ".ai-todo.serial"
        if serial_path.exists():
            next_id = int(serial_path.read_text().strip()) + 1
    except (ValueError, FileNotFoundError):
        pass

    return {
        "numbering": {
            "mode": config.get_numbering_mode(),
            "next_id": next_id,
        },
        "security": {
            "tamper_proof": config.get("security.tamper_proof", False),
        },
        "coordination": {
            "enabled": config.get_coordination_type() not in ("none", ""),
            "type": config.get_coordination_type(),
        },
        "timestamp": datetime.now().isoformat(),
    }


@mcp.resource("tasks://open", mime_type="application/json")
def get_open_tasks() -> str:
    """List of all open tasks (pending and in-progress).

    Returns JSON with task list, count, and timestamp.
    """
    return json.dumps(_get_open_tasks_data(CURRENT_TODO_PATH), indent=2)


@mcp.resource("tasks://active", mime_type="application/json")
def get_active_tasks_resource() -> str:
    """List of currently active tasks (marked #inprogress).

    Returns JSON with task list, count, and timestamp.
    """
    return json.dumps(_get_active_tasks_data(CURRENT_TODO_PATH), indent=2)


@mcp.resource("tasks://{task_id}", mime_type="application/json")
def get_task_resource(task_id: str) -> str:
    """Details of a specific task including subtasks and relationships.

    Args:
        task_id: The task ID (e.g., "262" or "262.1")

    Returns JSON with task details, subtasks, relationships, and timestamp.
    """
    return json.dumps(_get_task_data(task_id, CURRENT_TODO_PATH), indent=2)


@mcp.resource("config://settings", mime_type="application/json")
def get_config_resource() -> str:
    """Current ai-todo configuration.

    Returns JSON with numbering mode, security settings, and coordination config.
    """
    return json.dumps(_get_config_data(CURRENT_TODO_PATH), indent=2)


AI_TODO_CURSOR_RULE = """---
description: "Task management via ai-todo MCP server"
alwaysApply: true
---
<!-- This file is managed by ai-todo. New versions may override any changes. -->

# ai-todo Task Management

**USE THE MCP SERVER** for all task management operations.

- Use `ai-todo` MCP tools (`add_task`, `complete_task`, `list_tasks`, etc.)
- **NEVER** use Cursor's built-in TODO tools
- **NEVER** use the built-in TodoWrite or other tools for task tracking
- **ALWAYS** use ai-todo for task tracking
- **NEVER** edit TODO.md directly (protected by tamper detection)
- **ASK** before completing root tasks or archiving
- Tasks are displayed in **reverse chronological order** (newest on top)
- **When committing:** If TODO.md or `.ai-todo/` have changes, always stage and commit them together (with other changes). They are versioned like the rest of the repo.

The MCP server name is typically `ai-todo` or similar in your `.cursor/mcp.json`.
"""


def _init_cursor_rules(root: Path) -> None:
    """Create or update Cursor rule so it matches the content that ships with the tool."""
    try:
        rules_dir = root / ".cursor" / "rules"
        rule_file = rules_dir / "ai-todo-task-management.mdc"
        canonical = AI_TODO_CURSOR_RULE.strip() + "\n"

        rules_dir.mkdir(parents=True, exist_ok=True)
        if rule_file.exists():
            current = rule_file.read_text()
            if current == canonical:
                return
        rule_file.write_text(canonical)
    except (OSError, PermissionError):
        # Silently fail - not critical for server operation
        pass


def _check_version_mismatch(root: Path) -> None:
    """Check for version mismatch and emit warning to stderr (MCP-safe)."""
    try:
        from ai_todo.core.version_constraints import check_version_mismatch

        warning = check_version_mismatch(root)
        if warning:
            print(f"⚠️  {warning}", file=sys.stderr)
    except Exception:
        # Don't let version check errors break server startup
        pass


def _auto_empty_trash(todo_path: str):
    """Auto-run empty trash on server startup (silent)."""
    from ai_todo.core.empty_trash import EmptyTrashManager

    try:
        manager = EmptyTrashManager(todo_path)
        manager.empty_trash(dry_run=False)
        # Silent operation - FileOps handles logging automatically
    except Exception:
        # Fail silently - don't block server startup
        pass


def run_server(root_path: str = "."):
    """Run the MCP server."""
    global CURRENT_TODO_PATH
    root = Path(root_path).resolve()
    CURRENT_TODO_PATH = str(root / "TODO.md")

    # Initialize Cursor rules if needed
    _init_cursor_rules(root)

    # Check for version mismatch (warning to stderr, MCP-safe)
    _check_version_mismatch(root)

    # Auto-run empty trash on startup (silent)
    _auto_empty_trash(CURRENT_TODO_PATH)

    # Run the server using stdio transport
    mcp.run(transport="stdio")


async def main():
    """Entry point for direct execution (legacy)."""
    # Default to current directory if run directly
    run_server(".")


if __name__ == "__main__":
    asyncio.run(main())
