"""MCP server for ai-todo."""

import asyncio
import io
import sys
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
def add_task(description: str, tags: list[str] | None = None) -> str:
    """Add a new task to TODO.md."""
    if tags is None:
        tags = []
    return _capture_output(add_command, description, tags, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def add_subtask(parent_id: str, description: str, tags: list[str] | None = None) -> str:
    """Add a subtask to an existing task."""
    if tags is None:
        tags = []
    return _capture_output(
        add_subtask_command, parent_id, description, tags, todo_path=CURRENT_TODO_PATH
    )


@mcp.tool()
def complete_task(task_id: str, with_subtasks: bool = False) -> str:
    """Mark a task as complete."""
    return _capture_output(complete_command, [task_id], with_subtasks, todo_path=CURRENT_TODO_PATH)


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
def modify_task(task_id: str, description: str, tags: list[str] | None = None) -> str:
    """Modify a task's description and/or tags."""
    if tags is None:
        tags = []
    return _capture_output(modify_command, task_id, description, tags, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def delete_task(task_id: str, with_subtasks: bool = True) -> str:
    """Delete a task and its subtasks (move to Deleted section)."""
    return _capture_output(delete_command, [task_id], with_subtasks, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def archive_task(task_id: str, reason: str | None = None, with_subtasks: bool = False) -> str:
    """Archive a task (move to Recently Completed section)."""
    # Note: archive_command doesn't support with_subtasks yet in CLI signature used here
    return _capture_output(archive_command, [task_id], reason, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def restore_task(task_id: str) -> str:
    """Restore a task from Deleted or Recently Completed back to Tasks section."""
    return _capture_output(restore_command, task_id, todo_path=CURRENT_TODO_PATH)


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


# Phase 2: Note Management


@mcp.tool()
def add_note(task_id: str, note_text: str) -> str:
    """Add a note to a task."""
    return _capture_output(note_command, task_id, note_text, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def delete_note(task_id: str) -> str:
    """Delete all notes from a task."""
    return _capture_output(delete_note_command, task_id, todo_path=CURRENT_TODO_PATH)


@mcp.tool()
def update_note(task_id: str, new_note_text: str) -> str:
    """Replace existing notes with new text."""
    return _capture_output(update_note_command, task_id, new_note_text, todo_path=CURRENT_TODO_PATH)


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


# Phase 7: Tamper Detection


@mcp.tool()
def accept_tamper(reason: str) -> str:
    """Accept external changes to TODO.md."""
    from ai_todo.cli.tamper_ops import tamper_accept_command

    return _capture_output(tamper_accept_command, reason, todo_path=CURRENT_TODO_PATH)


AI_TODO_CURSOR_RULE = """---
description: "Task management via ai-todo MCP server"
alwaysApply: true
---
# ai-todo Task Management

**USE THE MCP SERVER** for all task management operations.

- Use `ai-todo` MCP tools (`add_task`, `complete_task`, `list_tasks`, etc.)
- **NEVER** use Cursor's built-in TODO tools
- **NEVER** edit TODO.md directly (protected by tamper detection)
- **ASK** before completing root tasks or archiving

The MCP server name is typically `ai-todo` or similar in your `.cursor/mcp.json`.
"""


def _init_cursor_rules(root: Path) -> None:
    """Initialize Cursor rules if they don't exist."""
    try:
        rules_dir = root / ".cursor" / "rules"
        rule_file = rules_dir / "ai-todo-task-management.mdc"

        # Only create if the file doesn't exist
        if rule_file.exists():
            return

        rules_dir.mkdir(parents=True, exist_ok=True)
        rule_file.write_text(AI_TODO_CURSOR_RULE.strip() + "\n")
    except (OSError, PermissionError):
        # Silently fail - not critical for server operation
        pass


def run_server(root_path: str = "."):
    """Run the MCP server."""
    global CURRENT_TODO_PATH
    root = Path(root_path).resolve()
    CURRENT_TODO_PATH = str(root / "TODO.md")

    # Initialize Cursor rules if needed
    _init_cursor_rules(root)

    # Run the server using stdio transport
    mcp.run(transport="stdio")


async def main():
    """Entry point for direct execution (legacy)."""
    # Default to current directory if run directly
    run_server(".")


if __name__ == "__main__":
    asyncio.run(main())
