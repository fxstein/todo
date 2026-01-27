"""Reproduction test for Issue #195: Archiving a task does not archive its subtasks.

Also includes tests for Issue #242: Archive/delete task ordering bug.
"""

import re

import pytest

from ai_todo.cli.commands import add_command, add_subtask_command, archive_command
from ai_todo.core.file_ops import FileOps


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

    # Create .ai-todo directory
    todo_ai_dir = tmp_path / ".ai-todo"
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


def test_archive_ordering_parent_before_subtasks(test_todo_file):
    """Test that archived parent appears before its subtasks in the file (Issue #242)."""
    # Setup: Add parent with multiple subtasks
    add_command("Parent task", [], todo_path=test_todo_file)
    add_subtask_command("1", "Subtask one", [], todo_path=test_todo_file)
    add_subtask_command("1", "Subtask two", [], todo_path=test_todo_file)

    # Archive parent (includes subtasks by default)
    archive_command(["1"], todo_path=test_todo_file)

    # Read file content and verify ordering
    with open(test_todo_file) as f:
        content = f.read()

    # Extract task IDs from archived section in order
    lines = content.split("\n")
    in_archived = False
    archived_ids = []
    for line in lines:
        if "## Archived Tasks" in line or "## Recently Completed" in line:
            in_archived = True
            continue
        if in_archived and line.startswith("## "):
            break
        match = re.search(r"\*\*#([0-9.]+)\*\*", line)
        if in_archived and match:
            archived_ids.append(match.group(1))

    # Parent should come before subtasks
    assert archived_ids == ["1", "1.2", "1.1"], f"Expected ['1', '1.2', '1.1'], got {archived_ids}"


def test_archive_ordering_multiple_parents(test_todo_file):
    """Test that multiple archived parent-subtask groups maintain correct ordering (Issue #242)."""
    # Setup: Add two parents with subtasks
    add_command("First parent", [], todo_path=test_todo_file)
    add_subtask_command("1", "First subtask 1", [], todo_path=test_todo_file)
    add_subtask_command("1", "First subtask 2", [], todo_path=test_todo_file)

    add_command("Second parent", [], todo_path=test_todo_file)
    add_subtask_command("2", "Second subtask 1", [], todo_path=test_todo_file)

    # Archive first parent, then second parent
    archive_command(["1"], todo_path=test_todo_file)
    archive_command(["2"], todo_path=test_todo_file)

    # Read file content and verify ordering
    with open(test_todo_file) as f:
        content = f.read()

    # Extract task IDs from archived section in order
    lines = content.split("\n")
    in_archived = False
    archived_ids = []
    for line in lines:
        if "## Archived Tasks" in line or "## Recently Completed" in line:
            in_archived = True
            continue
        if in_archived and line.startswith("## "):
            break
        match = re.search(r"\*\*#([0-9.]+)\*\*", line)
        if in_archived and match:
            archived_ids.append(match.group(1))

    # Second parent (most recently archived) should come first, with its subtasks
    # Then first parent with its subtasks
    assert archived_ids == ["2", "2.1", "1", "1.2", "1.1"], (
        f"Expected ['2', '2.1', '1', '1.2', '1.1'], got {archived_ids}"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
