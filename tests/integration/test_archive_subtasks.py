"""Reproduction test for Issue #195: Archiving a task does not archive its subtasks."""

import pytest

from todo_ai.cli.commands import add_command, add_subtask_command, archive_command
from todo_ai.core.file_ops import FileOps


@pytest.fixture
def test_todo_file(tmp_path):
    """Create a test TODO.md file."""
    todo_file = tmp_path / "TODO.md"
    todo_file.write_text(
        """# TODO

## Tasks

## Recently Completed

## Deleted Tasks
""",
        encoding="utf-8",
    )

    # Create .todo.ai directory
    todo_ai_dir = tmp_path / ".todo.ai"
    todo_ai_dir.mkdir(exist_ok=True)
    (todo_ai_dir / "serial").write_text("0", encoding="utf-8")
    (todo_ai_dir / "config.yaml").write_text(
        "mode: single-user\ncoordination: none\n",
        encoding="utf-8",
    )

    return str(todo_file)


def test_archive_parent_archives_subtasks(test_todo_file):
    """Test that archiving a parent task automatically archives subtasks."""
    # 1. Setup: Add parent and subtask
    add_command("Parent task", [], todo_path=test_todo_file)
    add_subtask_command("1", "Subtask", [], todo_path=test_todo_file)

    # Verify setup
    file_ops = FileOps(test_todo_file)
    tasks = file_ops.read_tasks()
    assert len(tasks) == 2
    assert tasks[0].id == "1"
    assert tasks[1].id == "1.1"

    # 2. Action: Archive parent task
    # Should archive subtasks by default now
    archive_command(["1"], reason="Done", todo_path=test_todo_file)

    # 3. Verification
    tasks = file_ops.read_tasks()

    # Check what remains in Tasks section
    active_tasks = [t for t in tasks if t.status.value == "pending"]
    archived_tasks = [t for t in tasks if t.status.value == "archived"]

    # Subtask 1.1 should be archived along with parent
    assert len(active_tasks) == 0

    assert len(archived_tasks) == 2
    assert archived_tasks[0].id == "1"
    assert archived_tasks[1].id == "1.1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
