from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

IN_PROGRESS_TAG = "inprogress"


class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    DELETED = "deleted"


@dataclass
class Task:
    """
    Represents a single task with metadata.

    Attributes:
        id: Unique identifier for the task (e.g., "42" or "42.1")
        description: The task text content
        status: Current status of the task
        tags: Set of tags associated with the task (e.g., "bug", "feature")
        notes: List of notes attached to the task
        created_at: Timestamp when the task was created
        updated_at: Timestamp when the task was last modified
        completed_at: Timestamp when the task was completed (if applicable)
        archived_at: Timestamp when the task was archived (if applicable)
    """

    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    tags: set[str] = field(default_factory=set)
    notes: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
    archived_at: datetime | None = None
    deleted_at: datetime | None = None
    expires_at: datetime | None = None

    def add_tag(self, tag: str) -> None:
        """Add a tag to the task."""
        self.tags.add(tag)
        self.updated_at = datetime.now()

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the task."""
        self.tags.discard(tag)
        self.updated_at = datetime.now()

    def add_note(self, note: str) -> None:
        """Add a note to the task."""
        self.notes.append(note)
        self.updated_at = datetime.now()

    def mark_completed(self) -> None:
        """Mark task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()
        self.remove_tag(IN_PROGRESS_TAG)

    def mark_archived(self) -> None:
        """Mark task as archived."""
        self.status = TaskStatus.ARCHIVED
        self.archived_at = datetime.now()
        self.updated_at = datetime.now()
        self.remove_tag(IN_PROGRESS_TAG)
        # If task was completed, preserve completed_at
        if not self.completed_at and self.status == TaskStatus.ARCHIVED:
            # Task is being archived directly (not from completed state)
            pass

    def mark_deleted(self) -> None:
        """Mark task as deleted."""
        self.status = TaskStatus.DELETED
        self.deleted_at = datetime.now()
        # Set expiry to 30 days from deletion
        from datetime import timedelta

        self.expires_at = self.deleted_at + timedelta(days=30)
        self.updated_at = datetime.now()
        self.remove_tag(IN_PROGRESS_TAG)

    def restore(self) -> None:
        """Restore task to pending status, preserving completion status if applicable."""
        # Only reset to PENDING if it was DELETED or ARCHIVED (and not previously completed)
        # If it was completed before archiving, we want to keep it completed but move it back to Tasks section.

        # Check if completed_at is set (meaning it was completed before archiving)
        # Note: mark_archived preserves completed_at if it was already set
        if self.completed_at:
            self.status = TaskStatus.COMPLETED
        else:
            self.status = TaskStatus.PENDING

        self.archived_at = None
        self.deleted_at = None
        self.updated_at = datetime.now()


class TaskManager:
    """Core task management operations"""

    def __init__(self, tasks: list[Task] | None = None):
        self._tasks: dict[str, Task] = {t.id: t for t in tasks} if tasks else {}

    def get_task(self, task_id: str) -> Task | None:
        """Retrieve a task by ID."""
        return self._tasks.get(task_id)

    def add_task(
        self, description: str, tags: list[str] | None = None, task_id: str | None = None
    ) -> Task:
        """Add a new task."""
        if not task_id:
            # Fallback: Find max integer ID from existing tasks
            max_id = 0
            for tid in self._tasks:
                if tid.isdigit():
                    max_id = max(max_id, int(tid))
            task_id = str(max_id + 1)

        task = Task(id=task_id, description=description, tags=set(tags) if tags else set())
        self._tasks[task_id] = task
        return task

    def add_subtask(
        self,
        parent_id: str,
        description: str,
        tags: list[str] | None = None,
        task_id: str | None = None,
    ) -> Task:
        """Add a subtask to an existing task."""
        parent = self.get_task(parent_id)
        if not parent:
            raise ValueError(f"Parent task {parent_id} not found")

        if not task_id:
            # Find next subtask ID
            # Format: parent_id.sub_id (e.g. 1.1, 1.2)
            prefix = f"{parent_id}."
            max_sub = 0
            for tid in self._tasks:
                if tid.startswith(prefix):
                    suffix = tid[len(prefix) :]
                    if suffix.isdigit():
                        max_sub = max(max_sub, int(suffix))
            task_id = f"{prefix}{max_sub + 1}"

        task = Task(id=task_id, description=description, tags=set(tags) if tags else set())
        self._tasks[task_id] = task
        return task

    def complete_task(self, task_id: str) -> Task:
        """Mark a task as complete."""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        task.mark_completed()
        return task

    def delete_task(self, task_id: str) -> Task:
        """Mark a task as deleted."""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        task.mark_deleted()
        return task

    def archive_task(self, task_id: str) -> Task:
        """Mark a task as archived."""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        task.mark_archived()
        return task

    def restore_task(self, task_id: str) -> Task:
        """Restore a task to pending status."""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        task.restore()
        return task

    def modify_task(
        self, task_id: str, description: str | None = None, tags: list[str] | None = None
    ) -> Task:
        """Modify a task's description and/or tags."""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        if description is not None:
            task.description = description
            task.updated_at = datetime.now()

        if tags is not None:
            task.tags = set(tags)
            task.updated_at = datetime.now()

        return task

    def undo_task(self, task_id: str) -> Task:
        """Reopen (undo) a completed task."""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        if task.status != TaskStatus.COMPLETED:
            raise ValueError(f"Task {task_id} is not completed, cannot undo")

        # Explicitly clear completed_at to ensure it goes back to PENDING
        task.completed_at = None
        task.restore()
        return task

    def start_task(self, task_id: str) -> Task:
        """Mark a task as in progress."""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        if task.status != TaskStatus.PENDING:
            raise ValueError(f"Task {task_id} is not pending (status: {task.status.value})")

        task.add_tag(IN_PROGRESS_TAG)
        return task

    def stop_task(self, task_id: str) -> Task:
        """Stop progress on a task."""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        task.remove_tag(IN_PROGRESS_TAG)
        return task

    def get_subtasks(self, parent_id: str) -> list[Task]:
        """Get all subtasks of a parent task."""
        prefix = f"{parent_id}."
        return [task for task_id, task in self._tasks.items() if task_id.startswith(prefix)]

    def add_note_to_task(self, task_id: str, note: str) -> Task:
        """Add a note to a task. Handles multi-line notes by splitting on newlines."""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        # Handle multi-line notes - split by newlines and add each line
        for line in note.split("\n"):
            if line.strip():
                task.add_note(line.strip())
        return task

    def delete_notes_from_task(self, task_id: str) -> Task:
        """Delete all notes from a task."""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        if not task.notes:
            raise ValueError(f"Task {task_id} has no notes to delete")
        task.notes.clear()
        task.updated_at = datetime.now()
        return task

    def update_notes_for_task(self, task_id: str, new_note: str) -> Task:
        """Replace all notes for a task with a new note."""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        if not task.notes:
            raise ValueError(f"Task {task_id} has no notes to update")
        task.notes.clear()
        # Handle multi-line notes - split by newlines and add each line
        for line in new_note.split("\n"):
            if line.strip():
                task.notes.append(line.strip())
        task.updated_at = datetime.now()
        return task

    def list_tasks(self, filters: dict[str, Any] | None = None) -> list[Task]:
        """List tasks matching filters."""
        if not filters:
            return list(self._tasks.values())

        result = []
        for task in self._tasks.values():
            match = True

            if "status" in filters:
                if task.status != filters["status"]:
                    match = False

            if "tag" in filters:
                if filters["tag"] not in task.tags:
                    match = False

            if match:
                result.append(task)

        return result
