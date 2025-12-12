import pytest
from datetime import datetime
from todo_ai.core.task import Task, TaskStatus

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
    assert task.status == TaskStatus.PENDING
    assert task.completed_at is None
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

