"""Unit tests for MCP resources."""

from unittest.mock import MagicMock, patch

from ai_todo.core.task import Task, TaskStatus


class TestTaskToDict:
    """Tests for _task_to_dict helper function."""

    def test_basic_task_conversion(self):
        """Test converting a basic task to dict."""
        from ai_todo.mcp.server import _task_to_dict

        task = Task(
            id="42",
            description="Test task",
            status=TaskStatus.PENDING,
            tags={"bug", "feature"},
            notes=["Note 1", "Note 2"],
        )
        result = _task_to_dict(task)

        assert result["id"] == "42"
        assert result["description"] == "Test task"
        assert result["status"] == "pending"
        assert result["tags"] == ["bug", "feature"]  # Sorted
        assert result["notes"] == ["Note 1", "Note 2"]
        assert result["is_subtask"] is False

    def test_subtask_detection(self):
        """Test that subtasks are correctly identified."""
        from ai_todo.mcp.server import _task_to_dict

        task = Task(id="42.1", description="Subtask")
        result = _task_to_dict(task)
        assert result["is_subtask"] is True

        root_task = Task(id="42", description="Root task")
        result = _task_to_dict(root_task)
        assert result["is_subtask"] is False

    def test_empty_tags_and_notes(self):
        """Test task with no tags or notes."""
        from ai_todo.mcp.server import _task_to_dict

        task = Task(id="1", description="Simple task")
        result = _task_to_dict(task)

        assert result["tags"] == []
        assert result["notes"] == []


class TestGetOpenTasksData:
    """Tests for _get_open_tasks_data helper function."""

    @patch("ai_todo.cli.commands.get_manager")
    def test_returns_open_tasks(self, mock_get_manager):
        """Test that open tasks helper returns pending tasks."""
        from ai_todo.mcp.server import _get_open_tasks_data

        mock_manager = MagicMock()
        mock_manager.list_tasks.return_value = [
            Task(id="1", description="Pending task", status=TaskStatus.PENDING),
            Task(id="2", description="Completed task", status=TaskStatus.COMPLETED),
            Task(id="3", description="In progress", status=TaskStatus.PENDING, tags={"inprogress"}),
        ]
        mock_get_manager.return_value = mock_manager

        result = _get_open_tasks_data("TODO.md")

        assert result["filter"] == "open"
        assert result["count"] == 2  # Only pending/in-progress root tasks
        assert len(result["tasks"]) == 2
        assert "timestamp" in result

    @patch("ai_todo.cli.commands.get_manager")
    def test_excludes_subtasks_from_count(self, mock_get_manager):
        """Test that subtasks are not included in main list but counted."""
        from ai_todo.mcp.server import _get_open_tasks_data

        mock_manager = MagicMock()
        mock_manager.list_tasks.return_value = [
            Task(id="1", description="Root task", status=TaskStatus.PENDING),
            Task(id="1.1", description="Subtask 1", status=TaskStatus.PENDING),
            Task(id="1.2", description="Subtask 2", status=TaskStatus.PENDING),
        ]
        mock_get_manager.return_value = mock_manager

        result = _get_open_tasks_data("TODO.md")

        assert result["count"] == 1  # Only root task in count
        assert len(result["tasks"]) == 1
        assert result["tasks"][0]["id"] == "1"
        assert result["tasks"][0]["subtask_count"] == 2


class TestGetActiveTasksData:
    """Tests for _get_active_tasks_data helper function."""

    @patch("ai_todo.cli.commands.get_manager")
    def test_returns_only_inprogress_tasks(self, mock_get_manager):
        """Test that active resource returns only in-progress tasks."""
        from ai_todo.mcp.server import _get_active_tasks_data

        mock_manager = MagicMock()
        mock_manager.list_tasks.return_value = [
            Task(id="1", description="Not started", status=TaskStatus.PENDING),
            Task(id="2", description="Active", status=TaskStatus.PENDING, tags={"inprogress"}),
            Task(
                id="3",
                description="Also active",
                status=TaskStatus.PENDING,
                tags={"inprogress", "bug"},
            ),
        ]
        mock_get_manager.return_value = mock_manager

        result = _get_active_tasks_data("TODO.md")

        assert result["filter"] == "active"
        assert result["count"] == 2
        assert len(result["tasks"]) == 2


class TestGetTaskData:
    """Tests for _get_task_data helper function."""

    @patch("ai_todo.core.file_ops.FileOps")
    @patch("ai_todo.cli.commands.get_manager")
    def test_returns_task_with_subtasks(self, mock_get_manager, mock_file_ops_class):
        """Test that task helper returns task with subtasks."""
        from ai_todo.mcp.server import _get_task_data

        task = Task(id="1", description="Root task", status=TaskStatus.PENDING)
        subtask = Task(id="1.1", description="Subtask", status=TaskStatus.COMPLETED)

        mock_manager = MagicMock()
        mock_manager.get_task.return_value = task
        mock_manager.get_subtasks.return_value = [subtask]
        mock_get_manager.return_value = mock_manager

        mock_file_ops = MagicMock()
        mock_file_ops.read_tasks.return_value = [task, subtask]
        mock_file_ops.get_relationships.return_value = {"depends-on": ["2"]}
        mock_file_ops_class.return_value = mock_file_ops

        result = _get_task_data("1", "TODO.md")

        assert result["task"]["id"] == "1"
        assert len(result["subtasks"]) == 1
        assert result["subtasks"][0]["id"] == "1.1"
        assert result["relationships"] == {"depends-on": ["2"]}

    @patch("ai_todo.core.file_ops.FileOps")
    @patch("ai_todo.cli.commands.get_manager")
    def test_returns_error_for_nonexistent_task(self, mock_get_manager, mock_file_ops_class):
        """Test that task helper returns error for missing task."""
        from ai_todo.mcp.server import _get_task_data

        mock_manager = MagicMock()
        mock_manager.get_task.return_value = None
        mock_get_manager.return_value = mock_manager

        mock_file_ops = MagicMock()
        mock_file_ops.read_tasks.return_value = []
        mock_file_ops_class.return_value = mock_file_ops

        result = _get_task_data("999", "TODO.md")

        assert "error" in result
        assert "999" in result["error"]


class TestGetConfigData:
    """Tests for _get_config_data helper function."""

    @patch("ai_todo.core.config.Config")
    @patch("ai_todo.core.file_ops.FileOps")
    def test_returns_config_settings(self, mock_file_ops_class, mock_config_class):
        """Test that config helper returns settings."""
        from ai_todo.mcp.server import _get_config_data

        # Mock Config
        mock_config = MagicMock()
        mock_config.get_numbering_mode.return_value = "single-user"
        mock_config.get.side_effect = lambda key, default=None: {
            "security.tamper_proof": True,
            "coordination.enabled": False,
        }.get(key, default)
        mock_config.get_coordination_type.return_value = "none"
        mock_config_class.return_value = mock_config

        # Mock FileOps
        mock_config_dir = MagicMock()
        serial_path = MagicMock()
        serial_path.exists.return_value = False
        mock_config_dir.__truediv__ = MagicMock(return_value=serial_path)

        mock_file_ops = MagicMock()
        mock_file_ops.config_dir = mock_config_dir
        mock_file_ops_class.return_value = mock_file_ops

        result = _get_config_data("TODO.md")

        assert result["numbering"]["mode"] == "single-user"
        assert result["security"]["tamper_proof"] is True
        assert result["coordination"]["enabled"] is False
        assert "timestamp" in result
