import pytest

from todo_ai.core.task import IN_PROGRESS_TAG, Task, TaskManager, TaskStatus


def test_start_task():
    task = Task(id="1", description="Test task")
    manager = TaskManager([task])

    manager.start_task("1")

    assert IN_PROGRESS_TAG in task.tags
    assert task.status == TaskStatus.PENDING


def test_start_task_idempotent():
    task = Task(id="1", description="Test task", tags={IN_PROGRESS_TAG})
    manager = TaskManager([task])

    manager.start_task("1")

    assert IN_PROGRESS_TAG in task.tags
    assert len(task.tags) == 1


def test_start_task_invalid_status():
    task = Task(id="1", description="Test task", status=TaskStatus.COMPLETED)
    manager = TaskManager([task])

    with pytest.raises(ValueError, match="is not pending"):
        manager.start_task("1")


def test_stop_task():
    task = Task(id="1", description="Test task", tags={IN_PROGRESS_TAG})
    manager = TaskManager([task])

    manager.stop_task("1")

    assert IN_PROGRESS_TAG not in task.tags


def test_stop_task_idempotent():
    task = Task(id="1", description="Test task")
    manager = TaskManager([task])

    manager.stop_task("1")

    assert IN_PROGRESS_TAG not in task.tags


def test_complete_removes_inprogress_tag():
    task = Task(id="1", description="Test task", tags={IN_PROGRESS_TAG})
    manager = TaskManager([task])

    manager.complete_task("1")

    assert IN_PROGRESS_TAG not in task.tags
    assert task.status == TaskStatus.COMPLETED


def test_archive_removes_inprogress_tag():
    task = Task(id="1", description="Test task", tags={IN_PROGRESS_TAG})
    manager = TaskManager([task])

    manager.archive_task("1")

    assert IN_PROGRESS_TAG not in task.tags
    assert task.status == TaskStatus.ARCHIVED


def test_delete_removes_inprogress_tag():
    task = Task(id="1", description="Test task", tags={IN_PROGRESS_TAG})
    manager = TaskManager([task])

    manager.delete_task("1")

    assert IN_PROGRESS_TAG not in task.tags
    assert task.status == TaskStatus.DELETED
