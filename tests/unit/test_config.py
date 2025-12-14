import pytest
import yaml

from todo_ai.core.config import Config


@pytest.fixture
def temp_config_file(tmp_path):
    config_dir = tmp_path / ".todo.ai"
    config_dir.mkdir()
    config_path = config_dir / "config.yaml"
    return config_path


def test_load_empty_config(temp_config_file):
    config = Config(str(temp_config_file))
    assert config.get("mode") is None
    assert config.get("mode", "default") == "default"


def test_load_existing_config(temp_config_file):
    data = {"mode": "multi-user", "coordination": {"type": "github-issues", "issue_number": 42}}
    temp_config_file.write_text(yaml.dump(data), encoding="utf-8")

    config = Config(str(temp_config_file))
    assert config.get("mode") == "multi-user"
    assert config.get("coordination.type") == "github-issues"
    assert config.get("coordination.issue_number") == 42
    assert config.get("nonexistent") is None


def test_set_and_save_config(temp_config_file):
    config = Config(str(temp_config_file))

    config.set("mode", "branch")
    config.set("coordination.type", "none")

    # Verify in memory
    assert config.get("mode") == "branch"
    assert config.get("coordination.type") == "none"

    # Verify file persistence
    new_config = Config(str(temp_config_file))
    assert new_config.get("mode") == "branch"
    assert new_config.get("coordination.type") == "none"


def test_helper_methods(temp_config_file):
    config = Config(str(temp_config_file))

    # Default values
    assert config.get_numbering_mode() == "single-user"
    assert config.get_coordination_type() == "none"

    # Set values
    config.set("mode", "enhanced")
    config.set("coordination.type", "counterapi")

    assert config.get_numbering_mode() == "enhanced"
    assert config.get_coordination_type() == "counterapi"
