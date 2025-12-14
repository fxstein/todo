import os
from unittest.mock import MagicMock, patch

import pytest

from todo_ai.core.github_client import GitHubClient


@pytest.fixture
def github_client():
    return GitHubClient(token="test_token")


@patch("subprocess.check_output")
def test_get_repo_info_ssh(mock_subprocess, github_client):
    mock_subprocess.return_value = "git@github.com:owner/repo.git"
    owner, repo = github_client._get_repo_info()
    assert owner == "owner"
    assert repo == "repo"


@patch("subprocess.check_output")
def test_get_repo_info_https(mock_subprocess, github_client):
    mock_subprocess.return_value = "https://github.com/owner/repo.git"
    owner, repo = github_client._get_repo_info()
    assert owner == "owner"
    assert repo == "repo"


@patch("subprocess.check_output")
def test_get_headers_from_gh(mock_subprocess):
    # Mock gh not being available in env vars, but available via subprocess
    with patch.dict(os.environ, {}, clear=True):
        with patch("shutil.which") as mock_which:
            mock_which.return_value = "/usr/bin/gh"
            mock_subprocess.return_value = "gh_token"

            client = GitHubClient()
            headers = client._get_headers()
            assert headers["Authorization"] == "token gh_token"


@patch("requests.post")
@patch("todo_ai.core.github_client.GitHubClient._get_repo_info")
def test_create_issue(mock_repo_info, mock_post, github_client):
    mock_repo_info.return_value = ("owner", "repo")
    mock_response = MagicMock()
    mock_response.json.return_value = {"number": 1, "title": "Test Issue"}
    mock_post.return_value = mock_response

    issue = github_client.create_issue("Test Issue", "Body", ["bug"])

    assert issue["number"] == 1
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs["json"]["title"] == "Test Issue"
    assert kwargs["json"]["labels"] == ["bug"]


@patch("requests.get")
@patch("todo_ai.core.github_client.GitHubClient._get_repo_info")
def test_get_issue(mock_repo_info, mock_get, github_client):
    mock_repo_info.return_value = ("owner", "repo")
    mock_response = MagicMock()
    mock_response.json.return_value = {"number": 1, "title": "Test Issue"}
    mock_get.return_value = mock_response

    issue = github_client.get_issue(1)

    assert issue["number"] == 1
    mock_get.assert_called_with(
        "https://api.github.com/repos/owner/repo/issues/1", headers=github_client._get_headers()
    )


@patch("requests.get")
@patch("todo_ai.core.github_client.GitHubClient._get_repo_info")
def test_get_issue_comments(mock_repo_info, mock_get, github_client):
    mock_repo_info.return_value = ("owner", "repo")
    mock_response = MagicMock()
    # Return a list of comments
    mock_response.json.return_value = [
        {"id": 1, "body": "Comment 1"},
        {"id": 2, "body": "Next task number: 10"},
    ]
    mock_get.return_value = mock_response

    comments = github_client.get_issue_comments(123)

    assert len(comments) == 2
    assert comments[1]["body"] == "Next task number: 10"
    mock_get.assert_called_with(
        "https://api.github.com/repos/owner/repo/issues/123/comments",
        headers=github_client._get_headers(),
    )
