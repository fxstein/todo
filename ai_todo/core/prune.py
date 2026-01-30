"""Prune functionality for removing old archived tasks from TODO.md."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ai_todo.core.file_ops import FileOps
from ai_todo.core.task import Task, TaskStatus
from ai_todo.utils.git import get_task_archive_date


@dataclass
class PruneResult:
    """Result of a prune operation."""

    tasks_pruned: int
    subtasks_pruned: int
    archive_path: str | None
    dry_run: bool
    pruned_task_ids: list[str]

    @property
    def total_pruned(self) -> int:
        """Total number of items pruned (tasks + subtasks)."""
        return self.tasks_pruned + self.subtasks_pruned


class PruneManager:
    """Manage prune operations on TODO.md archived tasks."""

    def __init__(self, todo_path: str = "TODO.md"):
        """
        Initialize PruneManager with TODO.md path.

        Args:
            todo_path: Path to TODO.md file
        """
        self.todo_path = todo_path
        self.file_ops = FileOps(todo_path)

    @staticmethod
    def _task_id_sort_key(task_id: str) -> tuple[int, ...]:
        """
        Convert task ID to sortable tuple for numeric sorting.

        Args:
            task_id: Task ID (e.g., "9", "10", "10.1", "100")

        Returns:
            Tuple of integers for numeric comparison

        Examples:
            "9" -> (9,)
            "10" -> (10,)
            "10.1" -> (10, 1)
            "100" -> (100,)

        This ensures correct numeric ordering: 9, 10, 10.1, 10.2, 100
        instead of lexicographic ordering: 10, 10.1, 10.2, 100, 9
        """
        try:
            return tuple(int(part) for part in task_id.split("."))
        except ValueError:
            # Fallback for non-numeric IDs (shouldn't happen in practice)
            return (0,)

    def identify_tasks_to_prune(
        self,
        tasks: list[Task],
        days: int | None = None,
        older_than: str | None = None,
        from_task: str | None = None,
    ) -> list[Task]:
        """
        Identify archived tasks matching prune criteria.

        Args:
            tasks: All tasks from TODO.md
            days: Prune tasks older than N days
            older_than: Prune tasks archived before YYYY-MM-DD
            from_task: Prune tasks from #1 to #from_task

        Returns:
            List of tasks to prune (includes subtasks)

        Algorithm:
            1. Filter for archived tasks only (status == ARCHIVED)
            2. Apply age filter (days or older_than)
            3. OR apply range filter (from_task)
            4. Include all subtasks of matching parent tasks
            5. Return deduplicated list
        """
        # Filter to archived tasks only
        archived_tasks = [t for t in tasks if t.status == TaskStatus.ARCHIVED]

        if not archived_tasks:
            return []

        # Apply filters
        if from_task:
            # Range-based pruning: #1 to #from_task
            return self._filter_by_task_range(archived_tasks, from_task)
        elif days is not None:
            # Age-based pruning: older than N days
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
            return self._filter_by_age(archived_tasks, cutoff_date)
        elif older_than:
            # Date-based pruning: before specific date
            # Parse as naive, then make UTC-aware at midnight
            cutoff_date = datetime.strptime(older_than, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            return self._filter_by_age(archived_tasks, cutoff_date)
        else:
            # Default: 30 days
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
            return self._filter_by_age(archived_tasks, cutoff_date)

    def _filter_by_age(self, tasks: list[Task], cutoff_date: datetime) -> list[Task]:
        """
        Filter tasks older than cutoff date.

        Args:
            tasks: List of archived tasks
            cutoff_date: Cutoff datetime (must be timezone-aware in UTC)

        Returns:
            List of tasks to prune
        """
        to_prune = []

        for task in tasks:
            # Skip subtasks - they'll be included with parent
            if "." in task.id:
                continue

            # Get archive date
            archive_date = get_task_archive_date(task.id, self.todo_path)

            if archive_date is None:
                # No date found - skip this task
                continue

            # Normalize both dates to UTC timezone-aware datetime for comparison
            # If archive_date is timezone-aware, convert to UTC
            # If archive_date is naive, assume it's already in UTC
            if archive_date.tzinfo is not None:
                archive_date_utc = archive_date.astimezone(timezone.utc)
            else:
                # Naive datetime - assume it's already UTC
                archive_date_utc = archive_date.replace(tzinfo=timezone.utc)

            # cutoff_date should already be UTC-aware from identify_tasks_to_prune
            # But ensure it's UTC for safety
            if cutoff_date.tzinfo is not None:
                cutoff_date_utc = cutoff_date.astimezone(timezone.utc)
            else:
                # Naive datetime - assume it's UTC
                cutoff_date_utc = cutoff_date.replace(tzinfo=timezone.utc)

            # Check if older than cutoff
            if archive_date_utc < cutoff_date_utc:
                to_prune.append(task)
                # Include all subtasks
                subtasks = [t for t in tasks if t.id.startswith(f"{task.id}.")]
                to_prune.extend(subtasks)

        return to_prune

    def _filter_by_task_range(self, tasks: list[Task], from_task: str) -> list[Task]:
        """
        Filter tasks from #1 to #from_task (inclusive).

        Args:
            tasks: List of archived tasks
            from_task: Maximum task ID to prune

        Returns:
            List of tasks to prune
        """
        try:
            max_id = int(from_task)
        except ValueError:
            return []

        to_prune = []

        for task in tasks:
            # Skip subtasks - they'll be included with parent
            if "." in task.id:
                continue

            # Root task only
            try:
                if int(task.id) <= max_id:
                    to_prune.append(task)
                    # Include all subtasks
                    subtasks = [t for t in tasks if t.id.startswith(f"{task.id}.")]
                    to_prune.extend(subtasks)
            except ValueError:
                continue

        return to_prune

    def create_archive_backup(
        self,
        tasks_to_prune: list[Task],
        days: int | None = None,
        older_than: str | None = None,
        from_task: str | None = None,
    ) -> str:
        """
        Create archive backup file before pruning.

        Args:
            tasks_to_prune: Tasks being pruned
            days: Retention period in days (if used)
            older_than: Date filter (if used)
            from_task: Task range filter (if used)

        Returns:
            Path to created archive file

        Format:
            .ai-todo/archives/TODO_ARCHIVE_YYYY-MM-DD.md
        """
        # Create archives directory
        config_dir = Path(self.todo_path).parent / ".ai-todo"
        archives_dir = config_dir / "archives"
        archives_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y-%m-%d")
        archive_file = archives_dir / f"TODO_ARCHIVE_{timestamp}.md"

        # Handle filename conflicts
        counter = 1
        while archive_file.exists():
            archive_file = archives_dir / f"TODO_ARCHIVE_{timestamp}_{counter}.md"
            counter += 1

        # Count tasks and subtasks
        root_tasks = [t for t in tasks_to_prune if "." not in t.id]
        subtasks = [t for t in tasks_to_prune if "." in t.id]

        # Determine pruning criteria description
        if from_task:
            criteria_desc = f"tasks from #1 to #{from_task}"
            retention_label = "Task Range"
            retention_value = f"#1 to #{from_task}"
        elif older_than:
            criteria_desc = f"tasks archived before {older_than}"
            retention_label = "Date Filter"
            retention_value = f"Before {older_than}"
        else:
            criteria_desc = f"tasks archived more than {days} days ago"
            retention_label = "Retention Period"
            retention_value = f"{days} days"

        # Generate archive content
        content = f"""# Archived Tasks - Pruned on {timestamp}

This file contains tasks pruned from TODO.md on {timestamp}.
These tasks are {criteria_desc}.

**Prune Statistics:**
- Tasks Pruned: {len(root_tasks)} root tasks
- Subtasks Pruned: {len(subtasks)} subtasks
- Total: {len(tasks_to_prune)} items
- {retention_label}: {retention_value}
- Original TODO.md: {self.todo_path}

## Pruned Tasks

"""

        # Add tasks in standard TODO.md format
        # Sort root tasks numerically for correct ordering
        root_tasks_sorted = sorted(
            [t for t in tasks_to_prune if "." not in t.id],
            key=lambda t: self._task_id_sort_key(t.id),
        )

        for task in root_tasks_sorted:
            # Add root task
            content += self._format_task(task)

            # Add subtasks
            task_subtasks = [
                t
                for t in tasks_to_prune
                if t.id.startswith(f"{task.id}.") and t.id.count(".") == task.id.count(".") + 1
            ]
            for subtask in sorted(task_subtasks, key=lambda t: self._task_id_sort_key(t.id)):
                content += self._format_task(subtask)

            content += "\n"

        # Add TASK_METADATA section for pruned tasks
        has_metadata = any(t.created_at is not None for t in tasks_to_prune)
        if has_metadata:
            content += "---\n\n## Task Metadata\n\n"
            content += "<!-- TASK_METADATA\n"
            content += "# Format: task_id:created_at[:updated_at]\n"

            for task in sorted(tasks_to_prune, key=lambda x: self._task_id_sort_key(x.id)):
                if task.created_at is not None:
                    created_str = task.created_at.isoformat()
                    if task.updated_at is not None and task.updated_at != task.created_at:
                        updated_str = task.updated_at.isoformat()
                        content += f"{task.id}:{created_str}:{updated_str}\n"
                    else:
                        content += f"{task.id}:{created_str}\n"

            content += "-->\n\n"

        # Add footer
        content += f"""---
**Prune Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**{retention_label}:** {retention_value}
**Tasks Pruned:** {len(root_tasks)} tasks, {len(subtasks)} subtasks
**Original TODO.md:** {self.todo_path}
"""

        # Write archive file
        archive_file.write_text(content, encoding="utf-8")

        return str(archive_file)

    def _format_task(self, task: Task) -> str:
        """
        Format task for archive file (standard TODO.md format).

        Args:
            task: Task to format

        Returns:
            Formatted task string
        """
        indent = "  " * task.id.count(".")
        checkbox = "[x]"  # Archived tasks are completed
        tags = " ".join(f"`#{tag}`" for tag in sorted(task.tags)) if task.tags else ""

        line = f"{indent}- {checkbox} **#{task.id}** {task.description}"
        if tags:
            line += f" {tags}"

        # Add completion date if available
        if task.completed_at:
            date_str = task.completed_at.strftime("%Y-%m-%d")
            line += f" ({date_str})"

        line += "\n"

        # Add notes
        for note in task.notes:
            line += f"{indent}  > {note}\n"

        return line

    def prune_tasks(
        self,
        days: int | None = None,
        older_than: str | None = None,
        from_task: str | None = None,
        dry_run: bool = False,
        backup: bool = True,
    ) -> PruneResult:
        """
        Prune archived tasks from TODO.md.

        Args:
            days: Prune tasks older than N days (default: 30 if no other filter)
            older_than: Prune tasks before YYYY-MM-DD
            from_task: Prune tasks from #1 to #from_task
            dry_run: Preview without making changes
            backup: Create archive backup (default: True)

        Returns:
            PruneResult with operation details

        Algorithm:
            1. Read all tasks via FileOps
            2. Identify tasks to prune (via identify_tasks_to_prune)
            3. If dry_run, return preview result
            4. If backup, create archive backup (fail if backup fails)
            5. Remove pruned tasks from task list
            6. Write remaining tasks via FileOps
            7. Return result
        """
        # Read tasks
        tasks = self.file_ops.read_tasks()

        # Identify tasks to prune
        to_prune = self.identify_tasks_to_prune(
            tasks, days=days, older_than=older_than, from_task=from_task
        )

        # Count root tasks vs subtasks
        root_tasks = [t for t in to_prune if "." not in t.id]
        subtasks = [t for t in to_prune if "." in t.id]

        # Dry run - return preview
        if dry_run:
            return PruneResult(
                tasks_pruned=len(root_tasks),
                subtasks_pruned=len(subtasks),
                archive_path=None,
                dry_run=True,
                pruned_task_ids=[t.id for t in to_prune],
            )

        # No tasks to prune
        if not to_prune:
            return PruneResult(
                tasks_pruned=0,
                subtasks_pruned=0,
                archive_path=None,
                dry_run=False,
                pruned_task_ids=[],
            )

        # Create backup
        archive_path = None
        if backup:
            archive_path = self.create_archive_backup(
                to_prune, days=days, older_than=older_than, from_task=from_task
            )

        # Remove pruned tasks
        pruned_ids = {t.id for t in to_prune}
        remaining_tasks = [t for t in tasks if t.id not in pruned_ids]

        # Write changes via FileOps
        self.file_ops.write_tasks(remaining_tasks)

        return PruneResult(
            tasks_pruned=len(root_tasks),
            subtasks_pruned=len(subtasks),
            archive_path=archive_path,
            dry_run=False,
            pruned_task_ids=[t.id for t in to_prune],
        )
