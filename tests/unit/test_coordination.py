from unittest.mock import MagicMock, patch

import pytest

from ai_todo.core.config import Config
from ai_todo.core.coordination import CoordinationManager


@pytest.fixture
def mock_config():
    config = MagicMock(spec=Config)
    config.get_numbering_mode.return_value = "single-user"
    config.get_coordination_type.return_value = "none"
    config.get.return_value = None
    return config


@pytest.fixture
def mock_github_client():
    client = MagicMock()
    return client


@pytest.fixture
def manager(mock_config, mock_github_client):
    return CoordinationManager(mock_config, mock_github_client)


def test_single_user_simple(manager, mock_config):
    mock_config.get_numbering_mode.return_value = "single-user"
    mock_config.get_coordination_type.return_value = "none"

    assert manager.generate_next_task_id(10) == "11"


def test_multi_user(manager, mock_config):
    mock_config.get_numbering_mode.return_value = "multi-user"

    with patch("ai_todo.core.coordination.CoordinationManager._get_github_user_id") as mock_user:
        mock_user.return_value = "devuser"
        # stored=20, current=10 -> max=20 -> next=21
        assert manager.generate_next_task_id(10, stored_serial=20) == "devuser-21"


def test_branch_mode(manager, mock_config):
    mock_config.get_numbering_mode.return_value = "branch"

    with patch("ai_todo.core.coordination.CoordinationManager._get_branch_name") as mock_branch:
        mock_branch.return_value = "feature"
        # stored=5, current=10 -> max=10 -> next=11
        assert manager.generate_next_task_id(10, stored_serial=5) == "feature-11"


def test_enhanced_mode(manager, mock_config):
    mock_config.get_numbering_mode.return_value = "enhanced"
    # Should behave like single-user (max(stored, current) + 1)
    # stored=10, current=5 -> max=10 -> next=11
    assert manager.generate_next_task_id(5, stored_serial=10) == "11"


def test_github_coordination(manager, mock_config, mock_github_client):
    mock_config.get_numbering_mode.return_value = "single-user"
    mock_config.get_coordination_type.return_value = "github-issues"
    mock_config.get.return_value = 123  # issue number

    # Remote is ahead
    mock_github_client.get_issue_comments.return_value = [{"body": "Next task number: 15"}]

    result = manager.generate_next_task_id(10)
    assert result == "16"

    # Verify it posts the new task number back to GitHub
    mock_github_client.create_issue_comment.assert_called_once_with(123, "Next task number: 16")


def test_github_coordination_local_ahead(manager, mock_config, mock_github_client):
    mock_config.get_numbering_mode.return_value = "single-user"
    mock_config.get_coordination_type.return_value = "github-issues"
    mock_config.get.return_value = 123

    # Remote is behind
    mock_github_client.get_issue_comments.return_value = [{"body": "Next task number: 5"}]

    result = manager.generate_next_task_id(10)
    assert result == "11"

    # Verify it posts the new task number back to GitHub
    mock_github_client.create_issue_comment.assert_called_once_with(123, "Next task number: 11")


def test_github_coordination_failure(manager, mock_config, mock_github_client):
    mock_config.get_numbering_mode.return_value = "single-user"
    mock_config.get_coordination_type.return_value = "github-issues"
    mock_config.get.return_value = 123

    # API failure on read
    mock_github_client.get_issue_comments.side_effect = Exception("API Error")

    # Should fallback to local increment
    assert manager.generate_next_task_id(10) == "11"

    # Should not have called create_issue_comment since read failed
    mock_github_client.create_issue_comment.assert_not_called()


def test_github_coordination_post_failure(manager, mock_config, mock_github_client):
    """Test that task creation succeeds even if posting to GitHub fails."""
    mock_config.get_numbering_mode.return_value = "single-user"
    mock_config.get_coordination_type.return_value = "github-issues"
    mock_config.get.return_value = 123

    mock_github_client.get_issue_comments.return_value = [{"body": "Next task number: 15"}]
    mock_github_client.create_issue_comment.side_effect = Exception("Post failed")

    # Should still return the correct task ID even if post fails
    result = manager.generate_next_task_id(10)
    assert result == "16"
