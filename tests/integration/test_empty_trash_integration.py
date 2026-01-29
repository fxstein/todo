"""Integration tests for empty trash functionality (CLI and MCP)."""

import io
import sys
from datetime import UTC, datetime, timedelta

import pytest

import ai_todo.mcp.server as mcp_server_module
from ai_todo.cli.commands import (
    add_command,
    add_subtask_command,
    archive_command,
    delete_command,
    empty_trash_command,
)
from ai_todo.core.file_ops import FileOps
from ai_todo.mcp.server import mcp


@pytest.fixture
def test_empty_trash_file(tmp_path):
    """Create test TODO.md with deleted tasks."""
    todo_file = tmp_path / "TODO.md"
    todo_file.write_text(
        """# TODO

## Tasks

## Recently Completed

## Deleted Tasks

**Repository:** https://github.com/fxstein/ai-todo
""",
        encoding="utf-8",
    )

    # Create .ai-todo directory
    todo_ai_dir = tmp_path / ".ai-todo"
    todo_ai_dir.mkdir(exist_ok=True)
    (todo_ai_dir / ".ai-todo.serial").write_text("0", encoding="utf-8")
    (todo_ai_dir / "config.yaml").write_text(
        """numbering_mode: single-user
coordination_type: none
security:
  tamper_proof: off
""",
        encoding="utf-8",
    )

    # Create state directory
    state_dir = todo_ai_dir / "state"
    state_dir.mkdir(exist_ok=True)

    return str(todo_file)


def capture_cli_output(func, *args, **kwargs) -> str:
    """Capture CLI command output."""
    old_stdout = sys.stdout
    sys.stdout = captured = io.StringIO()
    try:
        func(*args, **kwargs)
        return captured.getvalue()
    finally:
        sys.stdout = old_stdout


def call_mcp_tool(tool_name: str, arguments: dict, todo_path: str):
    """Call MCP tool directly."""
    mcp_server_module.CURRENT_TODO_PATH = todo_path

    tool = mcp._tool_manager._tools.get(tool_name)
    if not tool:
        raise ValueError(f"Unknown tool: {tool_name}")

    return tool.fn(**arguments)


def manually_set_task_expiration(todo_path: str, task_id: str, expires_days_ago: int):
    """Manually set task expiration date for testing."""
    file_ops = FileOps(todo_path)
    tasks = file_ops.read_tasks()

    for task in tasks:
        if task.id == task_id:
            task.expires_at = datetime.now(UTC) - timedelta(days=expires_days_ago)
            break

    file_ops.write_tasks(tasks)


# CLI Integration Tests


def test_cli_empty_trash_basic(test_empty_trash_file):
    """Test basic CLI empty trash operation."""
    # Create and delete a task
    add_command("Task to delete", [], todo_path=test_empty_trash_file)
    delete_command(["1"], with_subtasks=True, todo_path=test_empty_trash_file)

    # Manually set expiration to past
    manually_set_task_expiration(test_empty_trash_file, "1", expires_days_ago=1)

    # Run empty trash
    output = capture_cli_output(empty_trash_command, todo_path=test_empty_trash_file)

    assert "Removed" in output
    assert "1" in output or "expired" in output

    # Verify task was removed
    file_ops = FileOps(test_empty_trash_file)
    tasks = file_ops.read_tasks()
    task_ids = {t.id for t in tasks}
    assert "1" not in task_ids


def test_cli_empty_trash_dry_run(test_empty_trash_file):
    """Test CLI empty trash dry run mode."""
    # Create and delete a task
    add_command("Task to delete", [], todo_path=test_empty_trash_file)
    delete_command(["1"], with_subtasks=True, todo_path=test_empty_trash_file)

    # Manually set expiration to past
    manually_set_task_expiration(test_empty_trash_file, "1", expires_days_ago=1)

    # Run dry run
    output = capture_cli_output(empty_trash_command, dry_run=True, todo_path=test_empty_trash_file)

    assert "Would remove" in output
    assert "1" in output

    # Verify task was NOT removed
    file_ops = FileOps(test_empty_trash_file)
    tasks = file_ops.read_tasks()
    task_ids = {t.id for t in tasks}
    assert "1" in task_ids  # Still there


def test_cli_empty_trash_no_expired_tasks(test_empty_trash_file):
    """Test CLI empty trash with no expired tasks."""
    # Create and delete a recent task (not expired)
    add_command("Recent delete", [], todo_path=test_empty_trash_file)
    delete_command(["1"], with_subtasks=True, todo_path=test_empty_trash_file)

    # Run empty trash
    output = capture_cli_output(empty_trash_command, todo_path=test_empty_trash_file)

    assert "No expired" in output or "found" in output.lower()

    # Verify task still exists
    file_ops = FileOps(test_empty_trash_file)
    tasks = file_ops.read_tasks()
    task_ids = {t.id for t in tasks}
    assert "1" in task_ids


def test_cli_empty_trash_with_subtasks(test_empty_trash_file):
    """Test empty trash removes subtasks with parent."""
    # Create parent task with subtask
    add_command("Parent task", [], todo_path=test_empty_trash_file)
    add_subtask_command("1", "Subtask", [], todo_path=test_empty_trash_file)

    # Delete both
    delete_command(["1"], with_subtasks=True, todo_path=test_empty_trash_file)

    # Set expiration to past
    manually_set_task_expiration(test_empty_trash_file, "1", expires_days_ago=1)
    manually_set_task_expiration(test_empty_trash_file, "1.1", expires_days_ago=1)

    # Run empty trash
    result_output = capture_cli_output(empty_trash_command, todo_path=test_empty_trash_file)

    assert "2" in result_output or "Removed" in result_output

    # Verify both removed
    file_ops = FileOps(test_empty_trash_file)
    tasks = file_ops.read_tasks()
    task_ids = {t.id for t in tasks}
    assert "1" not in task_ids
    assert "1.1" not in task_ids


# MCP Integration Tests


def test_mcp_empty_trash_basic(test_empty_trash_file):
    """Test basic MCP empty_trash tool."""
    # Create and delete a task
    call_mcp_tool("add_task", {"title": "Task to delete"}, test_empty_trash_file)
    call_mcp_tool("delete_task", {"task_ids": ["1"]}, test_empty_trash_file)

    # Set expiration to past
    manually_set_task_expiration(test_empty_trash_file, "1", expires_days_ago=1)

    # Run empty trash
    result = call_mcp_tool("empty_trash", {}, test_empty_trash_file)

    assert result["total_removed"] == 1
    assert result["tasks_removed"] == 1
    assert result["subtasks_removed"] == 0
    assert "1" in result["removed_task_ids"]
    assert result["dry_run"] is False
    assert "Removed" in result["message"]


def test_mcp_empty_trash_dry_run(test_empty_trash_file):
    """Test MCP empty_trash tool dry run mode."""
    # Create and delete a task
    call_mcp_tool("add_task", {"title": "Task to delete"}, test_empty_trash_file)
    call_mcp_tool("delete_task", {"task_ids": ["1"]}, test_empty_trash_file)

    # Set expiration to past
    manually_set_task_expiration(test_empty_trash_file, "1", expires_days_ago=1)

    # Run dry run
    result = call_mcp_tool("empty_trash", {"dry_run": True}, test_empty_trash_file)

    assert result["dry_run"] is True
    assert result["total_removed"] == 1
    assert "Would remove" in result["message"]

    # Verify task NOT removed
    file_ops = FileOps(test_empty_trash_file)
    tasks = file_ops.read_tasks()
    task_ids = {t.id for t in tasks}
    assert "1" in task_ids


def test_mcp_cli_parity(test_empty_trash_file):
    """Test that MCP and CLI produce consistent results."""
    # Setup: Create and delete 2 tasks
    add_command("Task 1", [], todo_path=test_empty_trash_file)
    add_command("Task 2", [], todo_path=test_empty_trash_file)
    delete_command(["1", "2"], with_subtasks=True, todo_path=test_empty_trash_file)

    # Set expiration to past
    manually_set_task_expiration(test_empty_trash_file, "1", expires_days_ago=1)
    manually_set_task_expiration(test_empty_trash_file, "2", expires_days_ago=1)

    # Test dry run parity
    mcp_result = call_mcp_tool("empty_trash", {"dry_run": True}, test_empty_trash_file)

    # CLI dry run
    cli_output = capture_cli_output(
        empty_trash_command, dry_run=True, todo_path=test_empty_trash_file
    )

    # Both should report 2 tasks
    assert mcp_result["total_removed"] == 2
    assert "2" in cli_output  # Should show count


# Safety Tests


def test_safety_only_deletes_from_deleted_section(test_empty_trash_file):
    """Test that only tasks in Deleted Tasks section are affected."""
    # Create tasks in different sections
    add_command("Active task", [], todo_path=test_empty_trash_file)  # #1 - Active
    add_command("To archive", [], todo_path=test_empty_trash_file)  # #2
    add_command("To delete", [], todo_path=test_empty_trash_file)  # #3

    # Archive one, delete one
    archive_command(["2"], reason="Done", todo_path=test_empty_trash_file)
    delete_command(["3"], with_subtasks=True, todo_path=test_empty_trash_file)

    # Set ALL tasks to have expired dates (simulate malformed data)
    # But only deleted tasks should be affected
    manually_set_task_expiration(test_empty_trash_file, "3", expires_days_ago=1)

    # Run empty trash
    empty_trash_command(todo_path=test_empty_trash_file)

    # Verify only deleted task removed
    file_ops = FileOps(test_empty_trash_file)
    tasks = file_ops.read_tasks()
    task_ids = {t.id for t in tasks}

    assert "1" in task_ids  # Active task untouched
    assert "2" in task_ids  # Archived task untouched
    assert "3" not in task_ids  # Deleted task removed


def test_safety_never_touches_archived_tasks(test_empty_trash_file):
    """Test that archived tasks are never removed."""
    # Create and archive tasks
    add_command("Task 1", [], todo_path=test_empty_trash_file)
    add_command("Task 2", [], todo_path=test_empty_trash_file)
    archive_command(["1", "2"], reason="Done", todo_path=test_empty_trash_file)

    # Run empty trash (should do nothing)
    output = capture_cli_output(empty_trash_command, todo_path=test_empty_trash_file)

    assert "No expired" in output

    # Verify tasks still there
    file_ops = FileOps(test_empty_trash_file)
    tasks = file_ops.read_tasks()
    task_ids = {t.id for t in tasks}
    assert "1" in task_ids
    assert "2" in task_ids


def test_safety_never_touches_active_tasks(test_empty_trash_file):
    """Test that active tasks are never removed."""
    # Create active tasks
    add_command("Active 1", [], todo_path=test_empty_trash_file)
    add_command("Active 2", [], todo_path=test_empty_trash_file)

    # Run empty trash (should do nothing)
    output = capture_cli_output(empty_trash_command, todo_path=test_empty_trash_file)

    assert "No expired" in output

    # Verify tasks still there
    file_ops = FileOps(test_empty_trash_file)
    tasks = file_ops.read_tasks()
    task_ids = {t.id for t in tasks}
    assert "1" in task_ids
    assert "2" in task_ids


def test_subtasks_removed_with_parent(test_empty_trash_file):
    """Test that subtasks are removed when parent is expired."""
    # Create parent with subtask
    add_command("Parent task", [], todo_path=test_empty_trash_file)
    add_subtask_command("1", "Subtask", [], todo_path=test_empty_trash_file)

    # Delete both
    delete_command(["1"], with_subtasks=True, todo_path=test_empty_trash_file)

    # Set expiration to past
    manually_set_task_expiration(test_empty_trash_file, "1", expires_days_ago=1)
    manually_set_task_expiration(test_empty_trash_file, "1.1", expires_days_ago=1)

    # Run empty trash
    result = call_mcp_tool("empty_trash", {}, test_empty_trash_file)

    assert result["total_removed"] == 2
    assert result["tasks_removed"] == 1
    assert result["subtasks_removed"] == 1

    # Verify both removed
    file_ops = FileOps(test_empty_trash_file)
    tasks = file_ops.read_tasks()
    task_ids = {t.id for t in tasks}
    assert "1" not in task_ids
    assert "1.1" not in task_ids


def test_subtask_removed_independently(test_empty_trash_file):
    """Test that expired subtask can be removed even if parent not expired."""
    # Create parent with 2 subtasks
    add_command("Parent", [], todo_path=test_empty_trash_file)
    add_subtask_command("1", "Subtask 1", [], todo_path=test_empty_trash_file)
    add_subtask_command("1", "Subtask 2", [], todo_path=test_empty_trash_file)

    # Delete all
    delete_command(["1"], with_subtasks=True, todo_path=test_empty_trash_file)

    # Set only one subtask to expired (parent and other subtask still valid)
    manually_set_task_expiration(test_empty_trash_file, "1.1", expires_days_ago=1)

    # Run empty trash
    result = call_mcp_tool("empty_trash", {}, test_empty_trash_file)

    assert result["total_removed"] == 1
    assert result["subtasks_removed"] == 1
    assert "1.1" in result["removed_task_ids"]

    # Verify only expired subtask removed
    file_ops = FileOps(test_empty_trash_file)
    tasks = file_ops.read_tasks()
    task_ids = {t.id for t in tasks}
    assert "1" in task_ids  # Parent still there
    assert "1.1" not in task_ids  # Expired subtask removed
    assert "1.2" in task_ids  # Other subtask still there


def test_logging_operations_logged(test_empty_trash_file, tmp_path):
    """Test that empty trash operations are logged."""
    # Create and delete task
    add_command("Task", [], todo_path=test_empty_trash_file)
    delete_command(["1"], with_subtasks=True, todo_path=test_empty_trash_file)

    # Set expiration to past
    manually_set_task_expiration(test_empty_trash_file, "1", expires_days_ago=1)

    # Run empty trash
    empty_trash_command(todo_path=test_empty_trash_file)

    # Check log file exists and has entries
    log_file = tmp_path / ".ai-todo" / ".ai-todo.log"
    assert log_file.exists()

    log_content = log_file.read_text()
    assert "UPDATE" in log_content  # FileOps logs UPDATE for write_tasks


def test_mcp_and_cli_identical_results(test_empty_trash_file):
    """Test that MCP and CLI produce identical results for same input."""
    # Create identical state twice
    add_command("Task 1", [], todo_path=test_empty_trash_file)
    add_command("Task 2", [], todo_path=test_empty_trash_file)
    delete_command(["1", "2"], with_subtasks=True, todo_path=test_empty_trash_file)

    # Set expiration
    manually_set_task_expiration(test_empty_trash_file, "1", expires_days_ago=1)
    manually_set_task_expiration(test_empty_trash_file, "2", expires_days_ago=1)

    # Test dry run results are consistent
    mcp_result = call_mcp_tool("empty_trash", {"dry_run": True}, test_empty_trash_file)

    assert mcp_result["tasks_removed"] == 2
    assert mcp_result["subtasks_removed"] == 0
    assert mcp_result["total_removed"] == 2
    assert len(mcp_result["removed_task_ids"]) == 2


def test_auto_empty_trash_after_delete(test_empty_trash_file):
    """Test that empty trash auto-runs after delete command."""
    # Create 2 tasks
    add_command("Old task", [], todo_path=test_empty_trash_file)
    add_command("New task", [], todo_path=test_empty_trash_file)

    # Delete and expire the first one
    delete_command(["1"], with_subtasks=True, todo_path=test_empty_trash_file)
    manually_set_task_expiration(test_empty_trash_file, "1", expires_days_ago=1)

    # Delete the second one (should auto-trigger empty trash and remove #1)
    delete_command(["2"], with_subtasks=True, todo_path=test_empty_trash_file)

    # Verify #1 was auto-removed but #2 is still there (not expired)
    file_ops = FileOps(test_empty_trash_file)
    tasks = file_ops.read_tasks()
    task_ids = {t.id for t in tasks}
    assert "1" not in task_ids  # Auto-removed by empty trash
    assert "2" in task_ids  # Just deleted, not expired yet


def test_empty_section_handling(test_empty_trash_file):
    """Test behavior with empty Deleted Tasks section."""
    # Run empty trash on file with no deleted tasks
    output = capture_cli_output(empty_trash_command, todo_path=test_empty_trash_file)

    assert "No expired" in output

    # Should complete without error
    file_ops = FileOps(test_empty_trash_file)
    tasks = file_ops.read_tasks()
    assert len(tasks) == 0
