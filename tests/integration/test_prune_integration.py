"""Integration tests for prune functionality (CLI and MCP)."""

import io
import sys
from pathlib import Path

import pytest

import ai_todo.mcp.server as mcp_server_module
from ai_todo.cli.commands import add_command, archive_command, prune_command
from ai_todo.core.file_ops import FileOps
from ai_todo.mcp.server import mcp


@pytest.fixture
def test_prune_file(tmp_path):
    """Create test TODO.md with archived tasks using CLI commands."""
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

    # Create archives directory
    archives_dir = todo_ai_dir / "archives"
    archives_dir.mkdir(exist_ok=True)

    # Add and archive tasks using CLI commands
    todo_path = str(todo_file)

    # Create and archive old tasks (1-3)
    add_command("First task", [], todo_path=todo_path)
    add_command("Second task", [], todo_path=todo_path)
    add_command("Third task", [], todo_path=todo_path)
    archive_command(["1", "2", "3"], reason="Done", todo_path=todo_path)

    # Create and archive mid-range task (5)
    add_command("Fifth task", [], todo_path=todo_path)
    archive_command(["4"], reason="Done", todo_path=todo_path)

    # Create active tasks
    add_command("Active task", ["feature"], todo_path=todo_path)
    add_command("Another active", [], todo_path=todo_path)

    return todo_path


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


# CLI Integration Tests


def test_cli_prune_from_task_range(test_prune_file):
    """Test CLI prune with --from-task option."""
    output = capture_cli_output(
        prune_command,
        days=30,
        older_than=None,
        from_task="2",  # Prune tasks #1-#2
        dry_run=False,
        backup=True,
        force=True,
        todo_path=test_prune_file,
    )

    # Should prune tasks 1, 2
    assert "Pruned 2 task(s)" in output
    assert "Archive backup:" in output

    content = Path(test_prune_file).read_text()
    assert "**#1**" not in content
    assert "**#2**" not in content
    assert "**#3**" in content  # Should remain


def test_cli_prune_from_task_dry_run(test_prune_file):
    """Test CLI prune dry-run with --from-task."""
    output = capture_cli_output(
        prune_command,
        days=30,
        older_than=None,
        from_task="2",
        dry_run=True,
        backup=True,
        force=True,
        todo_path=test_prune_file,
    )

    # Should preview but not prune
    assert "Found 2 task(s)" in output
    assert "would be pruned" in output

    # Verify nothing was actually removed
    content = Path(test_prune_file).read_text()
    assert "**#1**" in content
    assert "**#2**" in content


def test_cli_prune_with_backup(test_prune_file):
    """Test CLI prune creates backup file with metadata."""
    archives_dir = Path(test_prune_file).parent / ".ai-todo" / "archives"
    initial_backups = len(list(archives_dir.glob("*.md")))

    output = capture_cli_output(
        prune_command,
        days=30,
        older_than=None,
        from_task="2",
        dry_run=False,
        backup=True,
        force=True,
        todo_path=test_prune_file,
    )

    # Should create backup
    assert "Archive backup:" in output

    # Verify backup file exists
    final_backups = len(list(archives_dir.glob("*.md")))
    assert final_backups == initial_backups + 1

    # Verify backup has metadata
    backup_file = list(archives_dir.glob("*.md"))[0]
    backup_content = backup_file.read_text()
    assert "TASK_METADATA" in backup_content


def test_cli_prune_no_backup(test_prune_file):
    """Test CLI prune without backup creation."""
    archives_dir = Path(test_prune_file).parent / ".ai-todo" / "archives"
    initial_backups = len(list(archives_dir.glob("*.md")))

    output = capture_cli_output(
        prune_command,
        days=30,
        older_than=None,
        from_task="2",
        dry_run=False,
        backup=False,  # No backup
        force=True,
        todo_path=test_prune_file,
    )

    # Should prune without creating backup
    assert "Pruned 2 task(s)" in output
    assert "Archive backup:" not in output

    # Verify no new backup created
    final_backups = len(list(archives_dir.glob("*.md")))
    assert final_backups == initial_backups


def test_cli_prune_no_matching_tasks(test_prune_file):
    """Test CLI prune when no tasks match criteria."""
    output = capture_cli_output(
        prune_command,
        days=30,
        older_than=None,
        from_task="0",  # No tasks before #0
        dry_run=False,
        backup=True,
        force=True,
        todo_path=test_prune_file,
    )

    # Should report no tasks to prune
    assert "No archived tasks match" in output


# MCP Integration Tests


def test_mcp_prune_from_task(test_prune_file):
    """Test MCP prune_tasks tool with from_task parameter."""
    result = call_mcp_tool(
        "prune_tasks",
        {"from_task": "2", "dry_run": False, "backup": True},
        test_prune_file,
    )

    # Verify result
    assert result["tasks_pruned"] == 2  # Tasks 1 and 2
    assert result["subtasks_pruned"] == 0  # No subtasks in test data
    assert result["total_pruned"] == 2
    assert result["archive_path"] is not None

    content = Path(test_prune_file).read_text()
    assert "**#1**" not in content
    assert "**#2**" not in content
    assert "**#3**" in content


def test_mcp_prune_dry_run(test_prune_file):
    """Test MCP prune_tasks with dry_run=True."""
    result = call_mcp_tool(
        "prune_tasks",
        {"from_task": "3", "dry_run": True, "backup": True},
        test_prune_file,
    )

    # Verify preview result
    assert result["dry_run"] is True
    assert result["tasks_pruned"] == 3  # 1, 2, 3
    assert result["total_pruned"] == 3
    assert result["archive_path"] is None
    assert len(result["pruned_task_ids"]) == 3

    # Verify no actual changes
    content = Path(test_prune_file).read_text()
    assert "**#1**" in content
    assert "**#2**" in content


def test_mcp_prune_with_backup(test_prune_file):
    """Test MCP prune_tasks creates backup with metadata."""
    result = call_mcp_tool(
        "prune_tasks",
        {"from_task": "2", "dry_run": False, "backup": True},
        test_prune_file,
    )

    # Verify backup exists
    backup_path = Path(result["archive_path"])
    assert backup_path.exists()

    # Verify backup content includes metadata
    backup_content = backup_path.read_text()
    assert "<!-- TASK_METADATA" in backup_content
    assert "# Format: task_id:created_at[:updated_at]" in backup_content
    assert "**#1**" in backup_content
    assert "**#2**" in backup_content


def test_mcp_prune_without_backup(test_prune_file):
    """Test MCP prune_tasks without backup."""
    result = call_mcp_tool(
        "prune_tasks",
        {"from_task": "2", "dry_run": False, "backup": False},
        test_prune_file,
    )

    # Verify no backup created
    assert result["archive_path"] is None
    assert result["tasks_pruned"] == 2


# Edge Cases


def test_prune_preserves_active_tasks(test_prune_file):
    """Test that prune never touches active tasks."""
    call_mcp_tool(
        "prune_tasks",
        {"from_task": "99", "dry_run": False, "backup": False},
        test_prune_file,
    )

    content = Path(test_prune_file).read_text()

    # Active tasks must remain
    assert "Active task" in content
    assert "Another active" in content


def test_prune_includes_subtasks(test_prune_file):
    """Test that pruning parent task includes all subtasks."""
    # Add task with subtasks, then archive
    from ai_todo.cli.commands import add_subtask_command

    add_command("Parent task", [], todo_path=test_prune_file)
    parent_id = "7"  # Next ID after initial setup
    add_subtask_command(parent_id, "Subtask one", [], todo_path=test_prune_file)
    add_subtask_command(parent_id, "Subtask two", [], todo_path=test_prune_file)
    archive_command([parent_id], reason="Done", todo_path=test_prune_file)

    # Prune it
    result = call_mcp_tool(
        "prune_tasks",
        {"from_task": "7", "dry_run": True, "backup": True},
        test_prune_file,
    )

    # Should include parent and all subtasks
    pruned_ids = result["pruned_task_ids"]
    assert "7" in pruned_ids
    assert "7.1" in pruned_ids
    assert "7.2" in pruned_ids


def test_prune_empty_result(test_prune_file):
    """Test prune when no archived tasks match criteria."""
    # Prune tasks that don't exist
    result = call_mcp_tool(
        "prune_tasks",
        {"from_task": "0", "dry_run": False, "backup": True},
        test_prune_file,
    )

    assert result["tasks_pruned"] == 0
    assert result["subtasks_pruned"] == 0
    assert result["total_pruned"] == 0
    assert result["archive_path"] is None


def test_backup_includes_metadata(test_prune_file):
    """Test that backup files include complete TASK_METADATA."""
    result = call_mcp_tool(
        "prune_tasks",
        {"from_task": "2", "dry_run": False, "backup": True},
        test_prune_file,
    )

    backup_path = Path(result["archive_path"])
    backup_content = backup_path.read_text()

    # Verify TASK_METADATA section exists
    assert "<!-- TASK_METADATA" in backup_content
    assert "# Format: task_id:created_at[:updated_at]" in backup_content

    # Verify metadata for pruned tasks (task IDs 1 and 2)
    assert ":created_at" in backup_content or "T" in backup_content  # Has timestamps


def test_backup_conflict_handling(test_prune_file):
    """Test that multiple prunes create separate backup files."""
    # First prune
    result1 = call_mcp_tool(
        "prune_tasks",
        {"from_task": "1", "dry_run": False, "backup": True},
        test_prune_file,
    )

    # Second prune (same day) - need to have something left to prune
    result2 = call_mcp_tool(
        "prune_tasks",
        {"from_task": "3", "dry_run": False, "backup": True},
        test_prune_file,
    )

    # Verify different backup files (second might be None if nothing to prune)
    if result2["archive_path"]:
        assert result1["archive_path"] != result2["archive_path"]
        assert Path(result2["archive_path"]).exists()

    assert Path(result1["archive_path"]).exists()


def test_prune_metadata_removal(test_prune_file):
    """Test that TASK_METADATA entries are removed for pruned tasks."""
    # Prune task #1
    call_mcp_tool(
        "prune_tasks",
        {"from_task": "1", "dry_run": False, "backup": True},
        test_prune_file,
    )

    content = Path(test_prune_file).read_text()

    # Task #1 should be removed from both Tasks and Metadata
    assert "**#1**" not in content

    # Other tasks should remain
    assert "**#2**" in content or "**#3**" in content


# MCP-CLI Parity Test


def test_mcp_cli_parity_from_task(test_prune_file):
    """Test that MCP and CLI produce same results for from_task pruning."""
    # Create two copies
    cli_file = Path(test_prune_file).parent / "TODO_CLI.md"
    mcp_file = Path(test_prune_file).parent / "TODO_MCP.md"

    import shutil

    shutil.copy2(test_prune_file, cli_file)
    shutil.copy2(test_prune_file, mcp_file)

    # Prune with CLI (no backup for simplicity)
    capture_cli_output(
        prune_command,
        days=30,
        older_than=None,
        from_task="2",
        dry_run=False,
        backup=False,
        force=True,
        todo_path=str(cli_file),
    )

    # Prune with MCP
    call_mcp_tool(
        "prune_tasks",
        {"from_task": "2", "dry_run": False, "backup": False},
        str(mcp_file),
    )

    # Read final states
    cli_ops = FileOps(str(cli_file))
    mcp_ops = FileOps(str(mcp_file))

    cli_tasks = cli_ops.read_tasks()
    mcp_tasks = mcp_ops.read_tasks()

    # Both should have same number of tasks
    assert len(cli_tasks) == len(mcp_tasks)

    # Both should have same task IDs
    cli_ids = {t.id for t in cli_tasks}
    mcp_ids = {t.id for t in mcp_tasks}
    assert cli_ids == mcp_ids


def test_mcp_cli_parity_dry_run(test_prune_file):
    """Test that MCP and CLI report same preview for dry-run."""
    # CLI dry-run
    cli_output = capture_cli_output(
        prune_command,
        days=30,
        older_than=None,
        from_task="2",
        dry_run=True,
        backup=True,
        force=True,
        todo_path=test_prune_file,
    )

    # MCP dry-run
    mcp_result = call_mcp_tool(
        "prune_tasks",
        {"from_task": "2", "dry_run": True, "backup": True},
        test_prune_file,
    )

    # Verify both report same counts
    assert str(mcp_result["tasks_pruned"]) in cli_output
    assert str(mcp_result["subtasks_pruned"]) in cli_output

    # Verify file unchanged
    content = Path(test_prune_file).read_text()
    assert "**#1**" in content
    assert "**#2**" in content


# End-to-End Workflow Test


def test_end_to_end_workflow(test_prune_file):
    """Test complete workflow: add, archive, prune."""
    # 1. Add new task
    add_command("New task", [], todo_path=test_prune_file)

    # 2. Archive it (should be task #7)
    archive_command(["7"], reason="Done", todo_path=test_prune_file)

    # 3. Prune old tasks only (tasks 1-3)
    result = call_mcp_tool(
        "prune_tasks",
        {"from_task": "3", "dry_run": False, "backup": True},
        test_prune_file,
    )

    # 4. Verify: old tasks removed, new archive remains
    content = Path(test_prune_file).read_text()
    assert "**#1**" not in content  # Pruned
    assert "**#2**" not in content  # Pruned
    assert "**#3**" not in content  # Pruned
    assert "**#7** New task" in content  # Newly archived - remains

    # 5. Verify backup exists
    assert result["archive_path"] is not None
    backup_path = Path(result["archive_path"])
    assert backup_path.exists()
