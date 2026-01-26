import os

import pytest

from ai_todo.cli.main import add_command, add_subtask_command, archive_command, restore_command
from ai_todo.core.file_ops import FileOps
from ai_todo.core.task import TaskManager, TaskStatus


@pytest.fixture(autouse=True)
def clean_env():
    """Clean up TODO_FILE environment variable after each test."""
    original = os.environ.get("TODO_FILE")
    yield
    if original is None:
        os.environ.pop("TODO_FILE", None)
    else:
        os.environ["TODO_FILE"] = original


def test_restore_subtasks_reproduction(tmp_path, capsys):
    """
    Reproduction test case for bug #204: Restoring a task does not restore its subtasks.
    """
    # Setup
    todo_file = tmp_path / "TODO.md"
    os.environ["TODO_FILE"] = str(todo_file)

    # Create parent and subtask
    add_command("Parent Task", ["#test"], todo_path=str(todo_file))
    add_subtask_command("1", "Subtask 1", ["#test"], todo_path=str(todo_file))

    # Verify initial state
    file_ops = FileOps(str(todo_file))
    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)
    assert len(tasks) == 2
    assert manager.get_task("1").status == TaskStatus.PENDING
    assert manager.get_task("1.1").status == TaskStatus.PENDING

    # Archive parent (should archive subtask too - fixed in #195)
    archive_command(["1"], todo_path=str(todo_file))

    # Verify archived state
    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)
    assert manager.get_task("1").status == TaskStatus.ARCHIVED
    assert manager.get_task("1.1").status == TaskStatus.ARCHIVED

    # Restore parent
    restore_command("1", todo_path=str(todo_file))

    # Verify final state - THIS IS EXPECTED TO FAIL CURRENTLY
    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)

    # Parent should be COMPLETED (since it was archived)
    assert manager.get_task("1").status == TaskStatus.COMPLETED

    # Subtask SHOULD be COMPLETED (since it was archived)
    assert manager.get_task("1.1").status == TaskStatus.COMPLETED, (
        "Subtask 1.1 should be restored with parent"
    )


def test_restore_subtasks_preserves_completion(tmp_path, capsys):
    """
    Test for #204.6: Restore should preserve completion status.
    """
    # Setup
    todo_file = tmp_path / "TODO.md"
    os.environ["TODO_FILE"] = str(todo_file)

    # Create parent and subtask
    add_command("Parent Task", ["#test"], todo_path=str(todo_file))
    add_subtask_command("1", "Subtask 1", ["#test"], todo_path=str(todo_file))

    # Complete subtask
    from ai_todo.cli.main import complete_command

    complete_command(["1.1"], todo_path=str(todo_file))

    # Verify initial state
    file_ops = FileOps(str(todo_file))
    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)
    assert manager.get_task("1").status == TaskStatus.PENDING
    assert manager.get_task("1.1").status == TaskStatus.COMPLETED

    # Archive parent (should archive subtask too)
    archive_command(["1"], todo_path=str(todo_file))

    # Restore parent
    restore_command("1", todo_path=str(todo_file))

    # Verify final state
    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)

    # Parent should be COMPLETED (since it was archived and we treat archived tasks as completed)
    assert manager.get_task("1").status == TaskStatus.COMPLETED

    # Subtask should be COMPLETED (not PENDING)
    assert manager.get_task("1.1").status == TaskStatus.COMPLETED, (
        "Subtask 1.1 should preserve COMPLETED status after restore"
    )


def test_restore_subtasks_idempotency(tmp_path, capsys):
    """
    Test for self-healing/idempotency requirement (#204.4).
    If parent is already restored but subtask is missing, running restore again should fix it.
    """
    # Setup
    todo_file = tmp_path / "TODO.md"
    os.environ["TODO_FILE"] = str(todo_file)

    # Create parent and subtask
    add_command("Parent Task", ["#test"], todo_path=str(todo_file))
    add_subtask_command("1", "Subtask 1", ["#test"], todo_path=str(todo_file))

    # Archive both
    archive_command(["1"], todo_path=str(todo_file))

    # Manually simulate broken state: Restore ONLY parent
    file_ops = FileOps(str(todo_file))
    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)
    parent = manager.get_task("1")
    parent.restore()
    # Subtask 1.1 remains ARCHIVED
    file_ops.write_tasks(manager.list_tasks())

    # Verify broken state
    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)
    # Parent is COMPLETED because we called restore() manually on it
    assert manager.get_task("1").status == TaskStatus.COMPLETED
    assert manager.get_task("1.1").status == TaskStatus.ARCHIVED

    # Run restore command again on parent
    restore_command("1", todo_path=str(todo_file))

    # Verify fixed state
    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)
    assert manager.get_task("1").status == TaskStatus.COMPLETED
    assert manager.get_task("1.1").status == TaskStatus.COMPLETED, (
        "Subtask 1.1 should be restored by idempotent run"
    )
