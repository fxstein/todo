import shutil
from pathlib import Path

import pytest

TEST_DATA_DIR = Path(__file__).parent / "integration" / "test_data"


@pytest.fixture
def test_env(tmp_path):
    """
    Creates an isolated test environment with a copy of the test data.
    Returns the path to the temporary directory containing TODO.md and .ai-todo/.
    """
    # Source paths
    src_todo = TEST_DATA_DIR / "TODO.md"
    src_config_dir = TEST_DATA_DIR / ".ai-todo"

    # Destination paths
    dest_todo = tmp_path / "TODO.md"
    dest_config_dir = tmp_path / ".ai-todo"

    # Copy files
    if src_todo.exists():
        shutil.copy2(src_todo, dest_todo)

    if src_config_dir.exists():
        shutil.copytree(src_config_dir, dest_config_dir)

    return tmp_path
