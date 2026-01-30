"""Empty trash functionality for removing expired deleted tasks from TODO.md."""

from dataclasses import dataclass
from datetime import datetime, timezone

from ai_todo.core.file_ops import FileOps
from ai_todo.core.task import Task, TaskStatus


@dataclass
class EmptyTrashResult:
    """Result of an empty trash operation."""

    tasks_removed: int
    subtasks_removed: int
    dry_run: bool
    removed_task_ids: list[str]

    @property
    def total_removed(self) -> int:
        """Total number of items removed (tasks + subtasks)."""
        return self.tasks_removed + self.subtasks_removed


class EmptyTrashManager:
    """Manage empty trash operations on deleted tasks."""

    def __init__(self, todo_path: str = "TODO.md"):
        """
        Initialize EmptyTrashManager with TODO.md path.

        Args:
            todo_path: Path to TODO.md file
        """
        self.todo_path = todo_path
        self.file_ops = FileOps(todo_path)

    def identify_expired_deleted_tasks(self, tasks: list[Task]) -> list[Task]:
        """
        Identify deleted tasks where expires_at < current_date.

        Only processes tasks in the "Deleted Tasks" section with status DELETED
        and a valid expires_at timestamp. Uses timezone-aware UTC comparisons.

        Args:
            tasks: All tasks from TODO.md

        Returns:
            List of expired deleted tasks (includes root + subtasks)
        """
        current_date = datetime.now(timezone.utc)
        expired = []

        for task in tasks:
            # Must be deleted with expiration date
            if task.status != TaskStatus.DELETED:
                continue
            if task.expires_at is None:
                continue

            # Normalize expires_at to UTC if needed
            expires = task.expires_at
            if expires.tzinfo is not None:
                expires_utc = expires.astimezone(timezone.utc)
            else:
                # Naive datetime - assume it's already UTC
                expires_utc = expires.replace(tzinfo=timezone.utc)

            # Check if expired
            if expires_utc < current_date:
                expired.append(task)

        return expired

    def empty_trash(self, dry_run: bool = False) -> EmptyTrashResult:
        """
        Permanently remove expired deleted tasks (30-day retention).

        This operation removes tasks from the "Deleted Tasks" section where
        the expiration date (expires_at) has passed. This is permanent deletion
        with no backup option.

        Args:
            dry_run: If True, only report what would be removed

        Returns:
            EmptyTrashResult with operation details

        Algorithm:
            1. Read all tasks via FileOps
            2. Identify expired deleted tasks
            3. If dry_run, return preview result
            4. Remove expired tasks from task list
            5. Write remaining tasks via FileOps
            6. Return result
        """
        # Read tasks
        tasks = self.file_ops.read_tasks()

        # Identify expired deleted tasks
        expired_tasks = self.identify_expired_deleted_tasks(tasks)

        # Count root vs subtasks
        root_count = sum(1 for t in expired_tasks if "." not in t.id)
        subtask_count = len(expired_tasks) - root_count
        task_ids = [t.id for t in expired_tasks]

        # Dry run: return preview
        if dry_run:
            return EmptyTrashResult(root_count, subtask_count, True, task_ids)

        # No tasks to remove
        if not expired_tasks:
            return EmptyTrashResult(0, 0, False, [])

        # Remove expired tasks
        expired_ids = {t.id for t in expired_tasks}
        remaining_tasks = [t for t in tasks if t.id not in expired_ids]

        # Write changes via FileOps (handles logging automatically)
        self.file_ops.write_tasks(remaining_tasks)

        return EmptyTrashResult(root_count, subtask_count, False, task_ids)
