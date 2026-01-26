"""Reproduction test for Issue #188: Subtask ordering inconsistency."""

import pytest

from ai_todo.cli.commands import add_command, add_subtask_command
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


def test_subtask_ordering_newest_on_top(test_todo_file):
    """Test that new subtasks are inserted at the TOP of the subtask list (immediately after parent)."""
    # 1. Setup: Add parent task
    add_command("Parent task", [], todo_path=test_todo_file)

    # 2. Add first subtask
    add_subtask_command("1", "Subtask One", [], todo_path=test_todo_file)

    # 3. Add second subtask
    add_subtask_command("1", "Subtask Two", [], todo_path=test_todo_file)

    # 4. Verify order
    file_ops = FileOps(test_todo_file)
    tasks = file_ops.read_tasks()

    # Expected order:
    # 1. Parent
    # 2. Subtask Two (Newest)
    # 3. Subtask One (Oldest)

    assert len(tasks) == 3
    assert tasks[0].id == "1"

    # This assertion should FAIL with current implementation
    # Current implementation: 1 -> 1.1 -> 1.2 (Chronological)
    # Desired implementation: 1 -> 1.2 -> 1.1 (Reverse Chronological)

    print(f"Task order: {[t.id for t in tasks]}")

    assert tasks[1].id == "1.2", f"Expected newest subtask (1.2) first, got {tasks[1].id}"
    assert tasks[2].id == "1.1", f"Expected oldest subtask (1.1) last, got {tasks[2].id}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
