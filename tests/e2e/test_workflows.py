import pytest
import os
from click.testing import CliRunner
from todo_ai.cli.main import cli

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def isolated_cli(runner, test_env):
    """
    Runs CLI commands in an isolated environment with test data.
    Uses the test_env fixture which populates the tmp_path with TODO.md and config.
    """
    cwd = os.getcwd()
    os.chdir(test_env)
    try:
        yield runner
    finally:
        os.chdir(cwd)

def test_workflow_basic(isolated_cli):
    """Test basic add -> list -> complete workflow."""
    
    # 1. Add a task
    result = isolated_cli.invoke(cli, ['add', 'Buy milk', '#shopping'])
    assert result.exit_code == 0
    # Serial is 6 (Last Used), Max is 5. Next should be 7.
    assert "Added: #7 Buy milk" in result.output 
    
    # 2. List tasks
    result = isolated_cli.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert "#7 Buy milk" in result.output
    
    # 3. Complete task
    result = isolated_cli.invoke(cli, ['complete', '7'])
    assert result.exit_code == 0
    assert "Completed: #7 Buy milk" in result.output
    
    # 4. Verify completion
    result = isolated_cli.invoke(cli, ['list'])
    assert "[x] #7 Buy milk" in result.output

def test_workflow_subtasks(isolated_cli):
    """Test subtask creation and management."""
    
    # 1. Add parent task
    result = isolated_cli.invoke(cli, ['add', 'Parent Task'])
    assert result.exit_code == 0
    # Serial is 6 (Last Used). Next is 7.
    assert "Added: #7 Parent Task" in result.output
    
    # 2. Add subtask
    result = isolated_cli.invoke(cli, ['add-subtask', '7', 'Subtask 1'])
    assert result.exit_code == 0
    assert "Added subtask: #7.1 Subtask 1" in result.output
    
    # 3. Verify listing
    result = isolated_cli.invoke(cli, ['list'])
    assert "#7.1 Subtask 1" in result.output
    
    # 4. Complete subtask
    result = isolated_cli.invoke(cli, ['complete', '7.1'])
    assert result.exit_code == 0
    
    # 5. Verify completion
    result = isolated_cli.invoke(cli, ['list'])
    assert "[x] #7.1 Subtask 1" in result.output
