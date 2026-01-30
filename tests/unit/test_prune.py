"""Unit tests for prune functionality."""

import re
import tempfile
from datetime import datetime, timedelta, timezone
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

    def test_get_task_archive_date_escapes_subtask_dots(self):
        """Test that subtask IDs with dots are properly escaped in regex."""
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

                # Test with subtask ID containing dots
                result = get_task_archive_date("129.1", todo_path)

                assert result is not None

                # Verify dot is escaped in git grep pattern
                mock_run.assert_called_once()
                call_args = mock_run.call_args[0][0]
                # The dot should be escaped as \. in the pattern
                assert r"--grep=archive.*129\.1|#129\.1" in call_args
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

    def test_task_id_sort_key(self, temp_todo_file):
        """Test numeric task ID sorting."""
        manager = PruneManager(temp_todo_file)

        # Test basic task IDs
        assert manager._task_id_sort_key("9") == (9,)
        assert manager._task_id_sort_key("10") == (10,)
        assert manager._task_id_sort_key("100") == (100,)

        # Test subtask IDs
        assert manager._task_id_sort_key("10.1") == (10, 1)
        assert manager._task_id_sort_key("10.2") == (10, 2)
        assert manager._task_id_sort_key("10.10") == (10, 10)

        # Verify correct ordering
        task_ids = ["100", "10", "10.2", "10.10", "9", "10.1", "2"]
        sorted_ids = sorted(task_ids, key=manager._task_id_sort_key)
        expected = ["2", "9", "10", "10.1", "10.2", "10.10", "100"]
        assert sorted_ids == expected

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

        # Critical: Verify no duplicate task IDs in result
        result_ids = [t.id for t in result]
        assert len(result_ids) == len(set(result_ids)), "Duplicate task IDs found in result!"

    def test_filter_by_task_range_no_duplicates(self, temp_todo_file):
        """Test that subtasks are not added twice when filtering by task range."""
        manager = PruneManager(temp_todo_file)

        # Create tasks with multiple subtasks to test duplicate bug
        tasks = [
            Task(id="50", description="Root 50", status=TaskStatus.ARCHIVED, tags=set()),
            Task(id="50.1", description="Subtask 50.1", status=TaskStatus.ARCHIVED, tags=set()),
            Task(id="50.2", description="Subtask 50.2", status=TaskStatus.ARCHIVED, tags=set()),
            Task(id="50.3", description="Subtask 50.3", status=TaskStatus.ARCHIVED, tags=set()),
            Task(id="100", description="Root 100", status=TaskStatus.ARCHIVED, tags=set()),
            Task(id="100.1", description="Subtask 100.1", status=TaskStatus.ARCHIVED, tags=set()),
            Task(id="100.2", description="Subtask 100.2", status=TaskStatus.ARCHIVED, tags=set()),
            Task(id="150", description="Root 150", status=TaskStatus.ARCHIVED, tags=set()),
        ]

        # Filter with from_task=100 (should include #1-#100)
        result = manager._filter_by_task_range(tasks, "100")

        # Count task IDs
        result_ids = [t.id for t in result]

        # Verify no duplicates
        assert len(result_ids) == len(set(result_ids)), f"Duplicate IDs found: {result_ids}"

        # Verify correct tasks included
        expected_ids = {"50", "50.1", "50.2", "50.3", "100", "100.1", "100.2"}
        actual_ids = set(result_ids)
        assert actual_ids == expected_ids, f"Expected {expected_ids}, got {actual_ids}"

        # Verify task 150 is NOT included (above range)
        assert "150" not in actual_ids

        # Verify exact count (7 tasks total: 2 root + 5 subtasks)
        assert len(result_ids) == 7

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

    def test_identify_tasks_older_than_not_overridden(self, temp_todo_file, sample_archived_tasks):
        """Test that older_than parameter is not overridden by default days."""
        manager = PruneManager(temp_todo_file)

        with patch("ai_todo.core.prune.get_task_archive_date") as mock_get_date:

            def get_date(task_id, _path):
                for task in sample_archived_tasks:
                    if task.id == task_id:
                        return task.completed_at
                return None

            mock_get_date.side_effect = get_date

            # Use older_than without specifying days (days=None)
            # Should use older_than cutoff, not default 30 days
            result = manager.identify_tasks_to_prune(
                sample_archived_tasks, days=None, older_than="2025-12-20"
            )

            # Should include only tasks older than 2025-12-20
            # Task 100 (60 days old ~= 2025-11-30), 102 (45 days old ~= 2025-12-15)
            # but NOT 101 (10 days old ~= 2026-01-19)
            task_ids = {t.id for t in result}
            assert "100" in task_ids
            assert "102" in task_ids
            assert "101" not in task_ids

    def test_identify_tasks_from_task_not_overridden(self, temp_todo_file, sample_archived_tasks):
        """Test that from_task parameter is not overridden by default days."""
        manager = PruneManager(temp_todo_file)

        # Use from_task without specifying days (days=None)
        # Should use task range, not default 30 days
        result = manager.identify_tasks_to_prune(sample_archived_tasks, days=None, from_task="101")

        # Should include tasks 100 and 101, but NOT 102
        task_ids = {t.id for t in result}
        assert "100" in task_ids
        assert "101" in task_ids
        assert "102" not in task_ids

    def test_filter_by_age_timezone_aware(self, temp_todo_file):
        """Test that timezone-aware archive dates are handled correctly."""
        manager = PruneManager(temp_todo_file)

        # Create tasks with different timezone scenarios
        tasks = [
            # Task archived 60 days ago in PST (timezone.utc-8)
            Task(
                id="100",
                description="Task in PST",
                status=TaskStatus.ARCHIVED,
                tags=set(),
                completed_at=datetime.now(timezone.utc) - timedelta(days=60),
            ),
            # Task archived 10 days ago in EST (timezone.utc-5)
            Task(
                id="101",
                description="Task in EST",
                status=TaskStatus.ARCHIVED,
                tags=set(),
                completed_at=datetime.now(timezone.utc) - timedelta(days=10),
            ),
        ]

        with patch("ai_todo.core.prune.get_task_archive_date") as mock_get_date:

            def get_date(task_id, _path):
                if task_id == "100":
                    # Return timezone-aware datetime in PST
                    from datetime import timezone as tz

                    pst = tz(timedelta(hours=-8))
                    return (datetime.now(timezone.utc) - timedelta(days=60)).astimezone(pst)
                elif task_id == "101":
                    # Return timezone-aware datetime in EST
                    from datetime import timezone as tz

                    est = tz(timedelta(hours=-5))
                    return (datetime.now(timezone.utc) - timedelta(days=10)).astimezone(est)
                return None

            mock_get_date.side_effect = get_date

            # Filter with 30-day cutoff (timezone.utc)
            cutoff = datetime.now(timezone.utc) - timedelta(days=30)
            result = manager._filter_by_age(tasks, cutoff)

            # Should include only task 100 (60 days old), not 101 (10 days old)
            task_ids = {t.id for t in result}
            assert "100" in task_ids
            assert "101" not in task_ids

    def test_filter_by_age_mixed_timezone_naive_aware(self, temp_todo_file):
        """Test handling of mixed naive and timezone-aware archive dates."""
        manager = PruneManager(temp_todo_file)

        tasks = [
            Task(
                id="100",
                description="Task with aware date",
                status=TaskStatus.ARCHIVED,
                tags=set(),
            ),
            Task(
                id="101",
                description="Task with naive date",
                status=TaskStatus.ARCHIVED,
                tags=set(),
            ),
        ]

        with patch("ai_todo.core.prune.get_task_archive_date") as mock_get_date:

            def get_date(task_id, _path):
                if task_id == "100":
                    # Return timezone-aware datetime (60 days ago in UTC)
                    return datetime.now(timezone.utc) - timedelta(days=60)
                elif task_id == "101":
                    # Return naive datetime (10 days ago, assumed UTC)
                    return datetime.now() - timedelta(days=10)
                return None

            mock_get_date.side_effect = get_date

            # Filter with 30-day cutoff (timezone.utc-aware)
            cutoff = datetime.now(timezone.utc) - timedelta(days=30)
            result = manager._filter_by_age(tasks, cutoff)

            # Should include only task 100 (60 days old)
            task_ids = {t.id for t in result}
            assert "100" in task_ids
            assert "101" not in task_ids

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

    def test_archive_backup_numeric_task_id_sorting(self, temp_todo_file):
        """Test that task IDs are sorted numerically, not lexicographically."""
        manager = PruneManager(temp_todo_file)

        # Create tasks with IDs that would be incorrectly ordered by string sort
        tasks = [
            Task(
                id="100",
                description="Task 100",
                status=TaskStatus.ARCHIVED,
                tags=set(),
                created_at=datetime.now(timezone.utc),
            ),
            Task(
                id="9",
                description="Task 9",
                status=TaskStatus.ARCHIVED,
                tags=set(),
                created_at=datetime.now(timezone.utc),
            ),
            Task(
                id="10",
                description="Task 10",
                status=TaskStatus.ARCHIVED,
                tags=set(),
                created_at=datetime.now(timezone.utc),
            ),
            Task(
                id="10.1",
                description="Subtask 10.1",
                status=TaskStatus.ARCHIVED,
                tags=set(),
                created_at=datetime.now(timezone.utc),
            ),
            Task(
                id="10.10",
                description="Subtask 10.10",
                status=TaskStatus.ARCHIVED,
                tags=set(),
                created_at=datetime.now(timezone.utc),
            ),
            Task(
                id="10.2",
                description="Subtask 10.2",
                status=TaskStatus.ARCHIVED,
                tags=set(),
                created_at=datetime.now(timezone.utc),
            ),
            Task(
                id="2",
                description="Task 2",
                status=TaskStatus.ARCHIVED,
                tags=set(),
                created_at=datetime.now(timezone.utc),
            ),
        ]

        archive_path = manager.create_archive_backup(tasks, days=30)
        content = Path(archive_path).read_text()

        # Extract task IDs from TASK_METADATA section
        # Pattern: <!-- TASK_METADATA ... task_id:timestamp ... -->
        metadata_match = re.search(r"<!-- TASK_METADATA\n(.*?)\n-->", content, re.DOTALL)
        assert metadata_match, "TASK_METADATA section not found"

        metadata_content = metadata_match.group(1)
        metadata_lines = [line.strip() for line in metadata_content.split("\n") if line.strip()]
        # Skip the comment line
        metadata_lines = [line for line in metadata_lines if not line.startswith("#")]

        # Extract task IDs from metadata
        task_ids_in_metadata = [line.split(":")[0] for line in metadata_lines]

        # Verify numeric ordering
        expected_order = ["2", "9", "10", "10.1", "10.2", "10.10", "100"]
        assert task_ids_in_metadata == expected_order, (
            f"Expected {expected_order}, got {task_ids_in_metadata}"
        )

        # Also verify task content ordering (check for ##Pruned Tasks section)
        # Extract task IDs from the pruned tasks section
        pruned_section = re.search(r"## Pruned Tasks\n\n(.*?)\n---", content, re.DOTALL)
        assert pruned_section, "Pruned Tasks section not found"

        # Find all task IDs in the section
        task_id_matches = re.findall(r"\*\*#(\d+(?:\.\d+)?)\*\*", pruned_section.group(1))

        # Verify numeric ordering in task content
        # Note: Subtasks appear under their parent, so order is: 2, 9, 10, 10.1, 10.2, 10.10, 100
        expected_content_order = ["2", "9", "10", "10.1", "10.2", "10.10", "100"]
        assert task_id_matches == expected_content_order, (
            f"Expected {expected_content_order}, got {task_id_matches}"
        )

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
