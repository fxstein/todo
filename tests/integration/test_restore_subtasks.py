import os

from todo_ai.cli.main import add_command, add_subtask_command, archive_command, restore_command
from todo_ai.core.file_ops import FileOps
from todo_ai.core.task import TaskManager, TaskStatus


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

    # Parent should be pending
    assert manager.get_task("1").status == TaskStatus.PENDING

    # Subtask SHOULD be pending, but bug causes it to remain archived
    # We assert the CORRECT behavior here to fail until fixed
    assert manager.get_task("1.1").status == TaskStatus.PENDING, (
        "Subtask 1.1 should be restored with parent"
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
    assert manager.get_task("1").status == TaskStatus.PENDING
    assert manager.get_task("1.1").status == TaskStatus.ARCHIVED

    # Run restore command again on parent
    restore_command("1", todo_path=str(todo_file))

    # Verify fixed state
    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)
    assert manager.get_task("1").status == TaskStatus.PENDING
    assert manager.get_task("1.1").status == TaskStatus.PENDING, (
        "Subtask 1.1 should be restored by idempotent run"
    )
