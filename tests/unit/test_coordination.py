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

    assert manager.generate_next_task_id(10) == "16"


def test_github_coordination_local_ahead(manager, mock_config, mock_github_client):
    mock_config.get_numbering_mode.return_value = "single-user"
    mock_config.get_coordination_type.return_value = "github-issues"
    mock_config.get.return_value = 123

    # Remote is behind
    mock_github_client.get_issue_comments.return_value = [{"body": "Next task number: 5"}]

    assert manager.generate_next_task_id(10) == "11"


def test_github_coordination_failure(manager, mock_config, mock_github_client):
    mock_config.get_numbering_mode.return_value = "single-user"
    mock_config.get_coordination_type.return_value = "github-issues"
    mock_config.get.return_value = 123

    # API failure
    mock_github_client.get_issue_comments.side_effect = Exception("API Error")

    # Should fallback to local increment
    assert manager.generate_next_task_id(10) == "11"
