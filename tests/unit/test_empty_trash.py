"""Unit tests for empty trash functionality."""

import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from ai_todo.core.empty_trash import EmptyTrashManager, EmptyTrashResult
from ai_todo.core.task import Task, TaskStatus


class TestEmptyTrashManager:
    """Test EmptyTrashManager class."""

    @pytest.fixture
    def temp_todo_file(self):
        """Create a temporary TODO.md file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            todo_path = f.name
            f.write("# TODO\n\n## Tasks\n\n## Archived Tasks\n\n## Deleted Tasks\n")
        yield todo_path
        Path(todo_path).unlink(missing_ok=True)

    @pytest.fixture
    def sample_deleted_tasks(self):
        """Create sample deleted tasks with various expiration dates."""
        tasks = []

        # Expired task (deleted 60 days ago, expires 30 days ago)
        task1 = Task(
            id="100",
            description="Old deleted task",
            status=TaskStatus.DELETED,
            deleted_at=datetime.now(UTC) - timedelta(days=60),
            expires_at=datetime.now(UTC) - timedelta(days=30),
        )
        tasks.append(task1)

        # Expired task with subtask (deleted 40 days ago, expires 10 days ago)
        task2 = Task(
            id="101",
            description="Expired parent task",
            status=TaskStatus.DELETED,
            deleted_at=datetime.now(UTC) - timedelta(days=40),
            expires_at=datetime.now(UTC) - timedelta(days=10),
        )
        task2_1 = Task(
            id="101.1",
            description="Expired subtask",
            status=TaskStatus.DELETED,
            deleted_at=datetime.now(UTC) - timedelta(days=40),
            expires_at=datetime.now(UTC) - timedelta(days=10),
        )
        tasks.extend([task2, task2_1])

        # Not expired task (deleted 10 days ago, expires in 20 days)
        task3 = Task(
            id="102",
            description="Recent deleted task",
            status=TaskStatus.DELETED,
            deleted_at=datetime.now(UTC) - timedelta(days=10),
            expires_at=datetime.now(UTC) + timedelta(days=20),
        )
        tasks.append(task3)

        # Pending task (should never be touched)
        task4 = Task(
            id="103",
            description="Pending task",
            status=TaskStatus.PENDING,
        )
        tasks.append(task4)

        # Archived task (should never be touched)
        task5 = Task(
            id="104",
            description="Archived task",
            status=TaskStatus.ARCHIVED,
            completed_at=datetime.now(UTC) - timedelta(days=40),
        )
        tasks.append(task5)

        # Deleted task without expires_at (malformed, should be skipped)
        task6 = Task(
            id="105",
            description="Deleted without expiration",
            status=TaskStatus.DELETED,
            deleted_at=datetime.now(UTC) - timedelta(days=40),
            expires_at=None,
        )
        tasks.append(task6)

        return tasks

    def test_identify_expired_deleted_tasks_basic(self, sample_deleted_tasks):
        """Test basic filtering of expired deleted tasks."""
        manager = EmptyTrashManager()
        expired = manager.identify_expired_deleted_tasks(sample_deleted_tasks)

        # Should find 3 expired tasks: #100, #101, #101.1
        assert len(expired) == 3
        expired_ids = {t.id for t in expired}
        assert expired_ids == {"100", "101", "101.1"}

    def test_identify_expired_deleted_tasks_timezone_aware(self):
        """Test handling of timezone-aware expires_at."""
        manager = EmptyTrashManager()

        # Task with timezone-aware expires_at
        task = Task(
            id="200",
            description="Timezone test",
            status=TaskStatus.DELETED,
            deleted_at=datetime.now(UTC) - timedelta(days=40),
            expires_at=datetime.now(UTC) - timedelta(days=10),
        )

        expired = manager.identify_expired_deleted_tasks([task])
        assert len(expired) == 1
        assert expired[0].id == "200"

    def test_identify_expired_deleted_tasks_naive_datetime(self):
        """Test handling of naive (no timezone) expires_at."""
        manager = EmptyTrashManager()

        # Task with naive expires_at (assume UTC)
        naive_date = datetime.now() - timedelta(days=10)  # No timezone
        task = Task(
            id="201",
            description="Naive datetime test",
            status=TaskStatus.DELETED,
            deleted_at=datetime.now(UTC) - timedelta(days=40),
            expires_at=naive_date,
        )

        expired = manager.identify_expired_deleted_tasks([task])
        assert len(expired) == 1
        assert expired[0].id == "201"

    def test_identify_expired_deleted_tasks_missing_expires_at(self, sample_deleted_tasks):
        """Test that tasks without expires_at are skipped."""
        manager = EmptyTrashManager()
        expired = manager.identify_expired_deleted_tasks(sample_deleted_tasks)

        # Task #105 has no expires_at, should be skipped
        expired_ids = {t.id for t in expired}
        assert "105" not in expired_ids

    def test_identify_expired_deleted_tasks_not_expired(self, sample_deleted_tasks):
        """Test that non-expired tasks are not included."""
        manager = EmptyTrashManager()
        expired = manager.identify_expired_deleted_tasks(sample_deleted_tasks)

        # Task #102 not expired yet
        expired_ids = {t.id for t in expired}
        assert "102" not in expired_ids

    def test_identify_expired_deleted_tasks_only_deleted_status(self, sample_deleted_tasks):
        """Test that only DELETED status tasks are processed."""
        manager = EmptyTrashManager()
        expired = manager.identify_expired_deleted_tasks(sample_deleted_tasks)

        # Pending (#103) and Archived (#104) should never be included
        expired_ids = {t.id for t in expired}
        assert "103" not in expired_ids  # Pending
        assert "104" not in expired_ids  # Archived

    def test_empty_trash_dry_run(self, temp_todo_file, sample_deleted_tasks):
        """Test dry run mode returns preview without removing."""
        manager = EmptyTrashManager(temp_todo_file)

        # Mock read_tasks to return sample tasks
        manager.file_ops.read_tasks = lambda: sample_deleted_tasks

        result = manager.empty_trash(dry_run=True)

        assert result.dry_run is True
        assert result.total_removed == 3  # 2 root + 1 subtask
        assert result.tasks_removed == 2  # #100, #101
        assert result.subtasks_removed == 1  # #101.1
        assert set(result.removed_task_ids) == {"100", "101", "101.1"}

    def test_empty_trash_no_expired_tasks(self, temp_todo_file):
        """Test behavior when no expired tasks exist."""
        manager = EmptyTrashManager(temp_todo_file)

        # Create non-expired deleted task
        task = Task(
            id="200",
            description="Recent delete",
            status=TaskStatus.DELETED,
            deleted_at=datetime.now(UTC),
            expires_at=datetime.now(UTC) + timedelta(days=29),
        )

        manager.file_ops.read_tasks = lambda: [task]

        result = manager.empty_trash(dry_run=False)

        assert result.total_removed == 0
        assert result.tasks_removed == 0
        assert result.subtasks_removed == 0
        assert len(result.removed_task_ids) == 0

    def test_empty_trash_result_total_removed_property(self):
        """Test EmptyTrashResult.total_removed property."""
        result = EmptyTrashResult(
            tasks_removed=5,
            subtasks_removed=12,
            dry_run=False,
            removed_task_ids=["1", "2", "3"],
        )

        assert result.total_removed == 17  # 5 + 12

    def test_empty_trash_counts_root_and_subtasks_correctly(self, sample_deleted_tasks):
        """Test that root tasks and subtasks are counted separately."""
        manager = EmptyTrashManager()
        expired = manager.identify_expired_deleted_tasks(sample_deleted_tasks)

        root_count = sum(1 for t in expired if "." not in t.id)
        subtask_count = sum(1 for t in expired if "." in t.id)

        assert root_count == 2  # #100, #101
        assert subtask_count == 1  # #101.1
        assert root_count + subtask_count == 3
