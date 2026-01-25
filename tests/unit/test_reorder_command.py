"""Unit tests for reorder_command."""

from pathlib import Path

import pytest

from todo_ai.cli.commands import reorder_command
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


def test_reorder_subtasks(test_todo_file):
    """Test that reorder_command sorts subtasks in reverse chronological order."""
    # 1. Setup: Create tasks in chronological order (simulating old buggy behavior)
    # We can't use add_subtask_command because we fixed it to insert at top!
    # So we manually write the file content to simulate the "wrong" order.

    Path(test_todo_file).write_text(
        """# TODO

## Tasks

- [ ] **#1** Parent task
  - [ ] **#1.1** Oldest subtask
  - [ ] **#1.2** Middle subtask
  - [ ] **#1.3** Newest subtask

## Recently Completed

## Deleted Tasks
""",
        encoding="utf-8",
    )

    # Verify initial state (chronological)
    file_ops = FileOps(test_todo_file)
    tasks = file_ops.read_tasks()
    assert len(tasks) == 4
    assert tasks[1].id == "1.1"
    assert tasks[2].id == "1.2"
    assert tasks[3].id == "1.3"

    # 2. Action: Run reorder command
    reorder_command(todo_path=test_todo_file)

    # 3. Verification
    tasks = file_ops.read_tasks()

    # Expected order: 1, 1.3, 1.2, 1.1
    assert tasks[0].id == "1"
    assert tasks[1].id == "1.3"
    assert tasks[2].id == "1.2"
    assert tasks[3].id == "1.1"


def test_reorder_preserves_notes(test_todo_file):
    """Test that reorder_command preserves notes attached to subtasks."""
    Path(test_todo_file).write_text(
        """# TODO

## Tasks

- [ ] **#1** Parent task
  - [ ] **#1.1** Oldest subtask
    > Note for 1.1
  - [ ] **#1.2** Newest subtask
    > Note for 1.2

## Recently Completed
""",
        encoding="utf-8",
    )

    reorder_command(todo_path=test_todo_file)

    content = Path(test_todo_file).read_text()

    # Check order
    lines = content.splitlines()
    # Find indices
    idx_1_2 = -1
    idx_1_1 = -1

    for i, line in enumerate(lines):
        if "**#1.2**" in line:
            idx_1_2 = i
        if "**#1.1**" in line:
            idx_1_1 = i

    assert idx_1_2 < idx_1_1, "1.2 should appear before 1.1"

    # Check notes are still attached (immediately following their task)
    assert lines[idx_1_2 + 1].strip() == "> Note for 1.2"
    assert lines[idx_1_1 + 1].strip() == "> Note for 1.1"
