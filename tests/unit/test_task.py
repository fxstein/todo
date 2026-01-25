from datetime import datetime

import pytest

from todo_ai.core.task import Task, TaskManager, TaskStatus

# ... (previous Task tests remain) ...


def test_task_creation():
    task = Task(id="1", description="Test task")
    assert task.id == "1"
    assert task.description == "Test task"
    assert task.status == TaskStatus.PENDING
    assert isinstance(task.created_at, datetime)
    assert len(task.tags) == 0
    assert len(task.notes) == 0


def test_task_status_changes():
    task = Task(id="1", description="Test task")

    # Complete
    task.mark_completed()
    assert task.status == TaskStatus.COMPLETED
    assert task.completed_at is not None

    # Archive
    task.mark_archived()
    assert task.status == TaskStatus.ARCHIVED
    assert task.archived_at is not None

    # Restore
    task.restore()
    assert task.status == TaskStatus.COMPLETED
    assert task.completed_at is not None
    assert task.archived_at is None


def test_task_tags():
    task = Task(id="1", description="Test task")

    task.add_tag("bug")
    assert "bug" in task.tags

    task.add_tag("feature")
    assert len(task.tags) == 2

    task.remove_tag("bug")
    assert "bug" not in task.tags
    assert len(task.tags) == 1


def test_task_notes():
    task = Task(id="1", description="Test task")

    task.add_note("Note 1")
    assert len(task.notes) == 1
    assert task.notes[0] == "Note 1"


# TaskManager Tests


@pytest.fixture
def task_manager():
    return TaskManager()


def test_manager_add_task(task_manager):
    task = task_manager.add_task("New task", tags=["tag1"])
    assert task.id == "1"
    assert task.description == "New task"
    assert "tag1" in task.tags

    task2 = task_manager.add_task("Second task")
    assert task2.id == "2"


def test_manager_add_subtask(task_manager):
    parent = task_manager.add_task("Parent")
    sub = task_manager.add_subtask(parent.id, "Subtask")

    assert sub.id == "1.1"
    assert sub.description == "Subtask"

    sub2 = task_manager.add_subtask(parent.id, "Subtask 2")
    assert sub2.id == "1.2"


def test_manager_add_subtask_nested(task_manager):
    parent = task_manager.add_task("Parent")
    sub = task_manager.add_subtask(parent.id, "Subtask")
    nested = task_manager.add_subtask(sub.id, "Nested")

    assert nested.id == "1.1.1"


def test_manager_operations(task_manager):
    task = task_manager.add_task("Task to modify")

    # Complete
    task_manager.complete_task(task.id)
    assert task.status == TaskStatus.COMPLETED

    # Archive
    task_manager.archive_task(task.id)
    assert task.status == TaskStatus.ARCHIVED

    # Restore
    task_manager.restore_task(task.id)
    assert task.status == TaskStatus.COMPLETED

    # Delete
    task_manager.delete_task(task.id)
    assert task.status == TaskStatus.DELETED


def test_manager_list_tasks(task_manager):
    t1 = task_manager.add_task("Task 1", tags=["tag1"])
    t2 = task_manager.add_task("Task 2", tags=["tag2"])
    task_manager.complete_task(t2.id)

    # All tasks
    all_tasks = task_manager.list_tasks()
    assert len(all_tasks) == 2

    # Filter by status
    pending = task_manager.list_tasks(filters={"status": TaskStatus.PENDING})
    assert len(pending) == 1
    assert pending[0].id == t1.id

    # Filter by tag
    tagged = task_manager.list_tasks(filters={"tag": "tag1"})
    assert len(tagged) == 1
    assert tagged[0].id == t1.id


def test_manager_modify_task(task_manager):
    task = task_manager.add_task("Original task", tags=["old"])

    # Modify description
    modified = task_manager.modify_task(task.id, "Updated task")
    assert modified.description == "Updated task"
    assert "old" in modified.tags

    # Modify tags
    modified = task_manager.modify_task(task.id, None, ["new", "tags"])
    assert modified.description == "Updated task"
    assert "new" in modified.tags
    assert "tags" in modified.tags
    assert "old" not in modified.tags

    # Modify both
    modified = task_manager.modify_task(task.id, "Final task", ["final"])
    assert modified.description == "Final task"
    assert "final" in modified.tags
    assert len(modified.tags) == 1


def test_manager_undo_task(task_manager):
    task = task_manager.add_task("Task to undo")

    # Complete it
    task_manager.complete_task(task.id)
    assert task.status == TaskStatus.COMPLETED

    # Undo it
    undone = task_manager.undo_task(task.id)
    assert undone.status == TaskStatus.PENDING
    assert undone.completed_at is None

    # Cannot undo non-completed task
    with pytest.raises(ValueError, match="not completed"):
        task_manager.undo_task(task.id)


def test_manager_get_subtasks(task_manager):
    parent = task_manager.add_task("Parent")
    sub1 = task_manager.add_subtask(parent.id, "Subtask 1")
    sub2 = task_manager.add_subtask(parent.id, "Subtask 2")
    other = task_manager.add_task("Other task")

    subtasks = task_manager.get_subtasks(parent.id)
    assert len(subtasks) == 2
    assert {s.id for s in subtasks} == {sub1.id, sub2.id}

    # Other task should not be included
    assert other.id not in {s.id for s in subtasks}


def test_manager_add_note_to_task(task_manager):
    task = task_manager.add_task("Task with note")
    task = task_manager.add_note_to_task(task.id, "Note 1")
    assert len(task.notes) == 1
    assert task.notes[0] == "Note 1"

    # Multi-line note
    task = task_manager.add_note_to_task(task.id, "Line 1\nLine 2\nLine 3")
    assert len(task.notes) == 4  # Original note + 3 new lines
    assert "Line 1" in task.notes
    assert "Line 2" in task.notes
    assert "Line 3" in task.notes


def test_manager_delete_notes_from_task(task_manager):
    task = task_manager.add_task("Task with notes")
    task.add_note("Note 1")
    task.add_note("Note 2")

    task = task_manager.delete_notes_from_task(task.id)
    assert len(task.notes) == 0

    # Should raise error if no notes
    with pytest.raises(ValueError, match="has no notes to delete"):
        task_manager.delete_notes_from_task(task.id)


def test_manager_update_notes_for_task(task_manager):
    task = task_manager.add_task("Task with notes")
    task.add_note("Old note 1")
    task.add_note("Old note 2")

    task = task_manager.update_notes_for_task(task.id, "New note")
    assert len(task.notes) == 1
    assert task.notes[0] == "New note"

    # Multi-line update
    task = task_manager.update_notes_for_task(task.id, "Line 1\nLine 2")
    assert len(task.notes) == 2
    assert task.notes[0] == "Line 1"
    assert task.notes[1] == "Line 2"

    # Should raise error if no notes
    task.notes.clear()
    with pytest.raises(ValueError, match="has no notes to update"):
        task_manager.update_notes_for_task(task.id, "New note")
