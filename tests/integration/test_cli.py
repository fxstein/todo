import pytest
from click.testing import CliRunner
from todo_ai.cli.main import cli
from todo_ai.core.task import TaskStatus

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def isolated_cli(runner, tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        yield runner

def test_add_command(isolated_cli):
    result = isolated_cli.invoke(cli, ['add', 'Test task', '#tag1'])
    assert result.exit_code == 0
    assert "Added: #1 Test task" in result.output

def test_list_command(isolated_cli):
    isolated_cli.invoke(cli, ['add', 'Task 1'])
    result = isolated_cli.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert "[ ] #1 Task 1" in result.output

def test_complete_command(isolated_cli):
    isolated_cli.invoke(cli, ['add', 'Task 1'])
    result = isolated_cli.invoke(cli, ['complete', '1'])
    assert result.exit_code == 0
    assert "Completed: #1 Task 1" in result.output
    
    # Verify list update
    result = isolated_cli.invoke(cli, ['list'])
    assert "[x] #1 Task 1" in result.output

