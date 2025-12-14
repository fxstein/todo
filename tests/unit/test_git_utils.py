import subprocess
from unittest.mock import patch

from todo_ai.utils import git


@patch("subprocess.check_output")
def test_get_git_root(mock_subprocess):
    mock_subprocess.return_value = "/path/to/repo\n"
    assert git.get_git_root() == "/path/to/repo"


@patch("subprocess.check_output")
def test_get_current_branch(mock_subprocess):
    mock_subprocess.return_value = "feature/test\n"
    assert git.get_current_branch() == "feature/test"


@patch("subprocess.check_output")
def test_git_failure(mock_subprocess):
    mock_subprocess.side_effect = subprocess.CalledProcessError(1, "cmd")
    assert git.get_git_root() is None
    assert git.get_current_branch() == "main"
    assert git.get_user_name() == "user"
