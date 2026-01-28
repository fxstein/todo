"""Unit tests for prune functionality."""

import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ai_todo.core.prune import PruneManager, PruneResult
from ai_todo.core.task import Task, TaskStatus
from ai_todo.utils.git import get_task_archive_date, parse_archive_date_from_metadata


class TestGitHistoryParsing:
    """Test git history analysis functions."""

    def test_get_task_archive_date_from_git_log(self):
        """Test parsing archive date from git log."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            todo_path = f.name
            f.write("# TODO\n")

        try:
            # Mock subprocess to return a date
            with patch("ai_todo.utils.git.subprocess.run") as mock_run:
                mock_result = MagicMock()
                mock_result.returncode = 0
                mock_result.stdout = "2026-01-15 10:30:45 -0800\n"
                mock_run.return_value = mock_result

                result = get_task_archive_date("129", todo_path)

                assert result is not None
                assert result.year == 2026
                assert result.month == 1
                assert result.day == 15

                # Verify git command uses extended-regexp for OR logic
                mock_run.assert_called_once()
                call_args = mock_run.call_args[0][0]
                assert "--extended-regexp" in call_args
                assert "--grep=archive.*129|#129" in call_args
        finally:
            Path(todo_path).unlink()

    def test_get_task_archive_date_no_git_history(self):
        """Test fallback when git history unavailable."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            todo_path = f.name
            f.write("- [x] **#129** Test task (2026-01-15)\n")

        try:
            # Mock subprocess to return no results
            with patch("ai_todo.utils.git.subprocess.run") as mock_run:
                mock_result = MagicMock()
                mock_result.returncode = 0
                mock_result.stdout = ""
                mock_run.return_value = mock_result

                result = get_task_archive_date("129", todo_path)

                assert result is not None
                assert result.year == 2026
                assert result.month == 1
                assert result.day == 15
        finally:
            Path(todo_path).unlink()

    def test_parse_archive_date_from_metadata(self):
        """Test parsing archive date from task metadata."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            todo_path = f.name
            f.write("- [x] **#129** Test task (2026-01-28)\n")
            f.write("- [x] **#130** Another task (2025-12-15)\n")

        try:
            result129 = parse_archive_date_from_metadata("129", todo_path)
            assert result129 is not None
            assert result129.year == 2026
            assert result129.month == 1
            assert result129.day == 28

            result130 = parse_archive_date_from_metadata("130", todo_path)
            assert result130 is not None
            assert result130.year == 2025
            assert result130.month == 12
            assert result130.day == 15
        finally:
            Path(todo_path).unlink()

    def test_parse_archive_date_task_not_found(self):
        """Test parsing when task ID not found."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            todo_path = f.name
            f.write("- [x] **#129** Test task (2026-01-28)\n")

        try:
            result = parse_archive_date_from_metadata("999", todo_path)
            assert result is None
        finally:
            Path(todo_path).unlink()


class TestPruneManager:
    """Test PruneManager class."""

    @pytest.fixture
    def temp_todo_file(self):
        """Create a temporary TODO.md file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            todo_path = f.name
            f.write("# TODO\n\n## Tasks\n\n## Archived Tasks\n")
        yield todo_path
        Path(todo_path).unlink(missing_ok=True)

    @pytest.fixture
    def sample_archived_tasks(self):
        """Create sample archived tasks with various dates."""
        tasks = []

        # Old task (60 days ago)
        old_task = Task(
            id="100",
            description="Old task",
            status=TaskStatus.ARCHIVED,
            tags=set(),
            completed_at=datetime.now() - timedelta(days=60),
        )
        tasks.append(old_task)

        # Recent task (10 days ago)
        recent_task = Task(
            id="101",
            description="Recent task",
            status=TaskStatus.ARCHIVED,
            tags=set(),
            completed_at=datetime.now() - timedelta(days=10),
        )
        tasks.append(recent_task)

        # Task with subtasks (45 days ago)
        parent_task = Task(
            id="102",
            description="Parent task",
            status=TaskStatus.ARCHIVED,
            tags=set(),
            completed_at=datetime.now() - timedelta(days=45),
        )
        subtask1 = Task(
            id="102.1",
            description="Subtask 1",
            status=TaskStatus.ARCHIVED,
            tags=set(),
            completed_at=datetime.now() - timedelta(days=45),
        )
        subtask2 = Task(
            id="102.2",
            description="Subtask 2",
            status=TaskStatus.ARCHIVED,
            tags=set(),
            completed_at=datetime.now() - timedelta(days=45),
        )
        tasks.extend([parent_task, subtask1, subtask2])

        # Active task (should not be pruned)
        active_task = Task(
            id="103",
            description="Active task",
            status=TaskStatus.PENDING,
            tags=set(),
        )
        tasks.append(active_task)

        return tasks

    def test_prune_manager_initialization(self, temp_todo_file):
        """Test PruneManager initialization."""
        manager = PruneManager(temp_todo_file)
        assert manager.todo_path == temp_todo_file
        assert manager.file_ops is not None

    def test_filter_by_age(self, temp_todo_file, sample_archived_tasks):
        """Test filtering tasks by age."""
        manager = PruneManager(temp_todo_file)

        # Mock get_task_archive_date to use completed_at
        with patch("ai_todo.core.prune.get_task_archive_date") as mock_get_date:

            def get_date(task_id, _path):
                for task in sample_archived_tasks:
                    if task.id == task_id:
                        return task.completed_at
                return None

            mock_get_date.side_effect = get_date

            # Filter with 30-day cutoff
            cutoff = datetime.now() - timedelta(days=30)
            archived = [t for t in sample_archived_tasks if t.status == TaskStatus.ARCHIVED]
            result = manager._filter_by_age(archived, cutoff)

            # Should include task 100 (60 days) and 102 (45 days) + subtasks
            task_ids = {t.id for t in result}
            assert "100" in task_ids  # Old task
            assert "102" in task_ids  # Parent task
            assert "102.1" in task_ids  # Subtask 1
            assert "102.2" in task_ids  # Subtask 2
            assert "101" not in task_ids  # Recent task (10 days)

    def test_filter_by_task_range(self, temp_todo_file, sample_archived_tasks):
        """Test filtering tasks by task ID range."""
        manager = PruneManager(temp_todo_file)

        archived = [t for t in sample_archived_tasks if t.status == TaskStatus.ARCHIVED]
        result = manager._filter_by_task_range(archived, "101")

        # Should include task 100, 101, and their subtasks
        task_ids = {t.id for t in result}
        assert "100" in task_ids
        assert "101" in task_ids
        assert "102" not in task_ids  # Above range

    def test_identify_tasks_to_prune_default(self, temp_todo_file, sample_archived_tasks):
        """Test identify_tasks_to_prune with default 30-day retention."""
        manager = PruneManager(temp_todo_file)

        with patch("ai_todo.core.prune.get_task_archive_date") as mock_get_date:

            def get_date(task_id, _path):
                for task in sample_archived_tasks:
                    if task.id == task_id:
                        return task.completed_at
                return None

            mock_get_date.side_effect = get_date

            result = manager.identify_tasks_to_prune(sample_archived_tasks)

            # Should prune old tasks (>30 days)
            task_ids = {t.id for t in result}
            assert "100" in task_ids  # 60 days old
            assert "102" in task_ids  # 45 days old
            assert "101" not in task_ids  # 10 days old

    def test_identify_tasks_to_prune_no_archived(self, temp_todo_file):
        """Test identify_tasks_to_prune with no archived tasks."""
        manager = PruneManager(temp_todo_file)

        active_tasks = [
            Task(id="1", description="Task 1", status=TaskStatus.PENDING, tags=set()),
            Task(id="2", description="Task 2", status=TaskStatus.PENDING, tags=set()),
        ]

        result = manager.identify_tasks_to_prune(active_tasks)
        assert len(result) == 0

    def test_create_archive_backup(self, temp_todo_file, sample_archived_tasks):
        """Test archive backup creation."""
        manager = PruneManager(temp_todo_file)

        # Get only archived tasks to prune
        to_prune = [t for t in sample_archived_tasks if t.id in ["100", "102", "102.1", "102.2"]]

        archive_path = manager.create_archive_backup(to_prune, days=30)

        # Verify archive file was created
        assert Path(archive_path).exists()

        # Verify archive content
        content = Path(archive_path).read_text()
        assert "# Archived Tasks - Pruned on" in content
        assert "Tasks Pruned: 2 root tasks" in content
        assert "Subtasks Pruned: 2 subtasks" in content
        assert "**#100**" in content
        assert "**#102**" in content

        # Verify TASK_METADATA is included
        assert "<!-- TASK_METADATA" in content
        assert "# Format: task_id:created_at[:updated_at]" in content
        assert "100:" in content  # Metadata for task 100
        assert "102:" in content  # Metadata for task 102
        assert "102.1:" in content  # Metadata for subtask
        assert "102.2:" in content  # Metadata for subtask

        # Cleanup
        Path(archive_path).unlink()

    def test_create_archive_backup_with_older_than(self, temp_todo_file, sample_archived_tasks):
        """Test archive backup with older_than parameter."""
        manager = PruneManager(temp_todo_file)
        to_prune = [t for t in sample_archived_tasks if t.id in ["100", "102"]]

        archive_path = manager.create_archive_backup(to_prune, older_than="2025-10-01")

        content = Path(archive_path).read_text()
        assert "archived before 2025-10-01" in content
        assert "Date Filter: Before 2025-10-01" in content
        assert "Retention Period:" not in content

        Path(archive_path).unlink()

    def test_create_archive_backup_with_from_task(self, temp_todo_file, sample_archived_tasks):
        """Test archive backup with from_task parameter."""
        manager = PruneManager(temp_todo_file)
        to_prune = [t for t in sample_archived_tasks if t.id in ["100", "102"]]

        archive_path = manager.create_archive_backup(to_prune, from_task="150")

        content = Path(archive_path).read_text()
        assert "tasks from #1 to #150" in content
        assert "Task Range: #1 to #150" in content
        assert "Retention Period:" not in content

        Path(archive_path).unlink()

    def test_prune_tasks_dry_run(self, temp_todo_file, sample_archived_tasks):
        """Test prune_tasks in dry-run mode."""
        manager = PruneManager(temp_todo_file)

        # Mock file_ops.read_tasks to return sample tasks
        with patch.object(manager.file_ops, "read_tasks", return_value=sample_archived_tasks):
            with patch("ai_todo.core.prune.get_task_archive_date") as mock_get_date:

                def get_date(task_id, _path):
                    for task in sample_archived_tasks:
                        if task.id == task_id:
                            return task.completed_at
                    return None

                mock_get_date.side_effect = get_date

                result = manager.prune_tasks(days=30, dry_run=True)

                assert isinstance(result, PruneResult)
                assert result.dry_run is True
                assert result.archive_path is None
                assert result.tasks_pruned > 0
                assert len(result.pruned_task_ids) > 0

    def test_prune_tasks_with_backup(self, temp_todo_file, sample_archived_tasks):
        """Test prune_tasks with backup creation."""
        manager = PruneManager(temp_todo_file)

        # Mock file_ops methods
        with patch.object(manager.file_ops, "read_tasks", return_value=sample_archived_tasks):
            with patch.object(manager.file_ops, "write_tasks") as mock_write:
                with patch("ai_todo.core.prune.get_task_archive_date") as mock_get_date:

                    def get_date(task_id, _path):
                        for task in sample_archived_tasks:
                            if task.id == task_id:
                                return task.completed_at
                        return None

                    mock_get_date.side_effect = get_date

                    result = manager.prune_tasks(days=30, backup=True)

                    assert isinstance(result, PruneResult)
                    assert result.dry_run is False
                    assert result.archive_path is not None
                    assert Path(result.archive_path).exists()
                    assert result.tasks_pruned > 0

                    # Verify write_tasks was called
                    assert mock_write.called

                    # Cleanup
                    Path(result.archive_path).unlink()

    def test_prune_tasks_no_backup(self, temp_todo_file, sample_archived_tasks):
        """Test prune_tasks without backup creation."""
        manager = PruneManager(temp_todo_file)

        with patch.object(manager.file_ops, "read_tasks", return_value=sample_archived_tasks):
            with patch.object(manager.file_ops, "write_tasks"):
                with patch("ai_todo.core.prune.get_task_archive_date") as mock_get_date:

                    def get_date(task_id, _path):
                        for task in sample_archived_tasks:
                            if task.id == task_id:
                                return task.completed_at
                        return None

                    mock_get_date.side_effect = get_date

                    result = manager.prune_tasks(days=30, backup=False)

                    assert result.archive_path is None

    def test_prune_tasks_no_matches(self, temp_todo_file):
        """Test prune_tasks when no tasks match criteria."""
        manager = PruneManager(temp_todo_file)

        # Only recent tasks
        recent_tasks = [
            Task(
                id="1",
                description="Recent",
                status=TaskStatus.ARCHIVED,
                tags=set(),
                completed_at=datetime.now() - timedelta(days=5),
            )
        ]

        with patch.object(manager.file_ops, "read_tasks", return_value=recent_tasks):
            with patch("ai_todo.core.prune.get_task_archive_date") as mock_get_date:
                mock_get_date.return_value = datetime.now() - timedelta(days=5)

                result = manager.prune_tasks(days=30)

                assert result.tasks_pruned == 0
                assert result.subtasks_pruned == 0
                assert result.archive_path is None


class TestPruneResult:
    """Test PruneResult dataclass."""

    def test_prune_result_total_pruned(self):
        """Test total_pruned property."""
        result = PruneResult(
            tasks_pruned=5,
            subtasks_pruned=10,
            archive_path="/path/to/archive",
            dry_run=False,
            pruned_task_ids=["1", "2", "3"],
        )

        assert result.total_pruned == 15

    def test_prune_result_dry_run(self):
        """Test dry run result."""
        result = PruneResult(
            tasks_pruned=3,
            subtasks_pruned=5,
            archive_path=None,
            dry_run=True,
            pruned_task_ids=["1", "2", "3"],
        )

        assert result.dry_run is True
        assert result.archive_path is None
        assert len(result.pruned_task_ids) == 3
