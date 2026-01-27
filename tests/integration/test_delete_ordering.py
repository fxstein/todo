"""Tests for Issue #242: Delete task ordering bug - root task appears below subtasks."""

import re

import pytest

from ai_todo.cli.commands import add_command, add_subtask_command, delete_command


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


def test_delete_ordering_parent_before_subtasks(test_todo_file):
    """Test that deleted parent appears before its subtasks in the file (Issue #242)."""
    # Setup: Add parent with multiple subtasks
    add_command("Parent task", [], todo_path=test_todo_file)
    add_subtask_command("1", "Subtask one", [], todo_path=test_todo_file)
    add_subtask_command("1", "Subtask two", [], todo_path=test_todo_file)

    # Delete parent (includes subtasks by default)
    delete_command(["1"], todo_path=test_todo_file)

    # Read file content and verify ordering
    with open(test_todo_file) as f:
        content = f.read()

    # Extract task IDs from deleted section in order
    lines = content.split("\n")
    in_deleted = False
    deleted_ids = []
    for line in lines:
        if "## Deleted Tasks" in line:
            in_deleted = True
            continue
        if in_deleted and line.startswith("## "):
            break
        if in_deleted and line.strip() == "---":
            break
        match = re.search(r"\*\*#([0-9.]+)\*\*", line)
        if in_deleted and match:
            deleted_ids.append(match.group(1))

    # Parent should come before subtasks
    assert deleted_ids == ["1", "1.2", "1.1"], f"Expected ['1', '1.2', '1.1'], got {deleted_ids}"


def test_delete_ordering_multiple_parents(test_todo_file):
    """Test that multiple deleted parent-subtask groups maintain correct ordering (Issue #242)."""
    # Setup: Add two parents with subtasks
    add_command("First parent", [], todo_path=test_todo_file)
    add_subtask_command("1", "First subtask 1", [], todo_path=test_todo_file)
    add_subtask_command("1", "First subtask 2", [], todo_path=test_todo_file)

    add_command("Second parent", [], todo_path=test_todo_file)
    add_subtask_command("2", "Second subtask 1", [], todo_path=test_todo_file)

    # Delete first parent, then second parent
    delete_command(["1"], todo_path=test_todo_file)
    delete_command(["2"], todo_path=test_todo_file)

    # Read file content and verify ordering
    with open(test_todo_file) as f:
        content = f.read()

    # Extract task IDs from deleted section in order
    lines = content.split("\n")
    in_deleted = False
    deleted_ids = []
    for line in lines:
        if "## Deleted Tasks" in line:
            in_deleted = True
            continue
        if in_deleted and line.startswith("## "):
            break
        if in_deleted and line.strip() == "---":
            break
        match = re.search(r"\*\*#([0-9.]+)\*\*", line)
        if in_deleted and match:
            deleted_ids.append(match.group(1))

    # Second parent (most recently deleted) should come first, with its subtasks
    # Then first parent with its subtasks
    assert deleted_ids == ["2", "2.1", "1", "1.2", "1.1"], (
        f"Expected ['2', '2.1', '1', '1.2', '1.1'], got {deleted_ids}"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
