from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Set

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
    tags: Set[str] = field(default_factory=set)
    notes: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None

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

    def mark_archived(self) -> None:
        """Mark task as archived."""
        self.status = TaskStatus.ARCHIVED
        self.archived_at = datetime.now()
        self.updated_at = datetime.now()

    def mark_deleted(self) -> None:
        """Mark task as deleted."""
        self.status = TaskStatus.DELETED
        self.updated_at = datetime.now()

    def restore(self) -> None:
        """Restore task to pending status."""
        self.status = TaskStatus.PENDING
        self.completed_at = None
        self.archived_at = None
        self.updated_at = datetime.now()

