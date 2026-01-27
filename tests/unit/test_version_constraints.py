"""Unit tests for ai_todo.core.version_constraints module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from ai_todo.core.version_constraints import (
    GlobalConfig,
    check_version_mismatch,
    get_effective_constraint,
    get_global_config_path,
    get_project_constraint,
    parse_constraint,
    parse_version,
)


class TestParseVersion:
    """Tests for parse_version function."""

    def test_simple_version(self):
        assert parse_version("3.0.2") == (3, 0, 2)
        assert parse_version("1.0.0") == (1, 0, 0)
        assert parse_version("10.20.30") == (10, 20, 30)

    def test_two_part_version(self):
        assert parse_version("3.0") == (3, 0)
        assert parse_version("1.2") == (1, 2)

    def test_beta_version(self):
        assert parse_version("3.0.2b1") == (3, 0, 2)
        assert parse_version("1.0.0beta") == (1, 0, 0)

    def test_rc_version(self):
        assert parse_version("3.0.2rc1") == (3, 0, 2)

    def test_alpha_version(self):
        assert parse_version("3.0.2a1") == (3, 0, 2)


class TestParseConstraint:
    """Tests for parse_constraint function."""

    def test_exact_pin(self):
        c = parse_constraint("==3.0.2")
        assert c.pinned == "3.0.2"
        assert c.min_version is None
        assert c.max_version is None

    def test_minimum_only(self):
        c = parse_constraint(">=3.0.0")
        assert c.pinned is None
        assert c.min_version == (3, 0, 0)
        assert c.min_inclusive is True
        assert c.max_version is None

    def test_maximum_only(self):
        c = parse_constraint("<4.0.0")
        assert c.pinned is None
        assert c.min_version is None
        assert c.max_version == (4, 0, 0)
        assert c.max_inclusive is False

    def test_range_constraint(self):
        c = parse_constraint(">=3.0.0,<4.0.0")
        assert c.pinned is None
        assert c.min_version == (3, 0, 0)
        assert c.min_inclusive is True
        assert c.max_version == (4, 0, 0)
        assert c.max_inclusive is False

    def test_inclusive_max(self):
        c = parse_constraint(">=3.0.0,<=3.9.9")
        assert c.min_version == (3, 0, 0)
        assert c.max_version == (3, 9, 9)
        assert c.max_inclusive is True

    def test_exclusive_min(self):
        c = parse_constraint(">3.0.0")
        assert c.min_version == (3, 0, 0)
        assert c.min_inclusive is False

    def test_compatible_release(self):
        c = parse_constraint("~=3.0")
        assert c.min_version == (3, 0)
        assert c.min_inclusive is True
        assert c.max_version == (4,)
        assert c.max_inclusive is False


class TestVersionConstraintSatisfies:
    """Tests for VersionConstraint.satisfies method."""

    def test_pinned_exact_match(self):
        c = parse_constraint("==3.0.2")
        assert c.satisfies("3.0.2") is True
        assert c.satisfies("3.0.1") is False
        assert c.satisfies("3.0.3") is False

    def test_minimum_constraint(self):
        c = parse_constraint(">=3.0.0")
        assert c.satisfies("3.0.0") is True
        assert c.satisfies("3.0.1") is True
        assert c.satisfies("4.0.0") is True
        assert c.satisfies("2.9.9") is False

    def test_maximum_constraint(self):
        c = parse_constraint("<4.0.0")
        assert c.satisfies("3.9.9") is True
        assert c.satisfies("3.0.0") is True
        assert c.satisfies("4.0.0") is False
        assert c.satisfies("4.0.1") is False

    def test_range_constraint(self):
        c = parse_constraint(">=3.0.0,<4.0.0")
        assert c.satisfies("3.0.0") is True
        assert c.satisfies("3.5.0") is True
        assert c.satisfies("3.9.9") is True
        assert c.satisfies("2.9.9") is False
        assert c.satisfies("4.0.0") is False
        assert c.satisfies("4.0.1") is False

    def test_exclusive_min(self):
        c = parse_constraint(">3.0.0")
        assert c.satisfies("3.0.0") is False
        assert c.satisfies("3.0.1") is True

    def test_inclusive_max(self):
        c = parse_constraint("<=3.9.9")
        assert c.satisfies("3.9.9") is True
        assert c.satisfies("3.9.10") is False


class TestGlobalConfig:
    """Tests for GlobalConfig class."""

    def test_load_nonexistent(self):
        """Test loading config from nonexistent file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "nonexistent" / "config.yaml"
            config = GlobalConfig(config_path)
            assert config.get("update.version_constraint") is None

    def test_set_and_get(self):
        """Test setting and getting values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = GlobalConfig(config_path)

            config.set("update.version_constraint", ">=3.0.0,<4.0.0")
            assert config.get("update.version_constraint") == ">=3.0.0,<4.0.0"

    def test_get_version_constraint(self):
        """Test getting parsed version constraint."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = GlobalConfig(config_path)

            config.set("update.version_constraint", ">=3.0.0,<4.0.0")
            constraint = config.get_version_constraint()

            assert constraint is not None
            assert constraint.min_version == (3, 0, 0)
            assert constraint.max_version == (4, 0, 0)

    def test_get_allow_prerelease(self):
        """Test getting allow_prerelease setting."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = GlobalConfig(config_path)

            assert config.get_allow_prerelease() is False

            config.set("update.allow_prerelease", True)
            assert config.get_allow_prerelease() is True


class TestGetGlobalConfigPath:
    """Tests for get_global_config_path function."""

    def test_default_path(self):
        """Test default config path (no XDG override)."""
        # Mock Path.home() to avoid Windows environment issues
        # and clear XDG_CONFIG_HOME to test default behavior
        with patch("pathlib.Path.home", return_value=Path("/home/testuser")):
            with patch.dict("os.environ", {"XDG_CONFIG_HOME": ""}, clear=False):
                path = get_global_config_path()
                assert path == Path("/home/testuser/.config/ai-todo/config.yaml")

    def test_xdg_override(self):
        """Test XDG_CONFIG_HOME override."""
        with patch.dict("os.environ", {"XDG_CONFIG_HOME": "/custom/config"}):
            path = get_global_config_path()
            assert path == Path("/custom/config/ai-todo/config.yaml")


class TestGetProjectConstraint:
    """Tests for get_project_constraint function."""

    def test_no_pyproject(self):
        """Test when pyproject.toml doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = get_project_constraint(Path(tmpdir))
            assert result is None

    def test_ai_todo_with_constraint(self):
        """Test extracting constraint from pyproject.toml."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pyproject = Path(tmpdir) / "pyproject.toml"
            pyproject.write_text("""
[project]
dependencies = [
    "ai-todo>=3.0.0,<4.0.0",
    "other-package>=1.0",
]
""")
            result = get_project_constraint(Path(tmpdir))
            assert result is not None
            assert result.min_version == (3, 0, 0)
            assert result.max_version == (4, 0, 0)

    def test_ai_todo_no_constraint(self):
        """Test when ai-todo is listed without version constraint."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pyproject = Path(tmpdir) / "pyproject.toml"
            pyproject.write_text("""
[project]
dependencies = [
    "ai-todo",
]
""")
            result = get_project_constraint(Path(tmpdir))
            # No constraint specified means any version is OK
            assert result is None

    def test_ai_todo_not_in_deps(self):
        """Test when ai-todo is not a dependency."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pyproject = Path(tmpdir) / "pyproject.toml"
            pyproject.write_text("""
[project]
dependencies = [
    "other-package>=1.0",
]
""")
            result = get_project_constraint(Path(tmpdir))
            assert result is None


class TestCheckVersionMismatch:
    """Tests for check_version_mismatch function."""

    def test_no_mismatch(self):
        """Test when version satisfies constraint."""
        with tempfile.TemporaryDirectory() as tmpdir:
            pyproject = Path(tmpdir) / "pyproject.toml"
            # Use a constraint that includes the current version
            pyproject.write_text("""
[project]
dependencies = [
    "ai-todo>=1.0.0",
]
""")
            result = check_version_mismatch(Path(tmpdir))
            assert result is None

    def test_no_constraint(self):
        """Test when no constraint exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = check_version_mismatch(Path(tmpdir))
            assert result is None


class TestGetEffectiveConstraint:
    """Tests for get_effective_constraint function."""

    def test_project_takes_precedence(self):
        """Test that project constraint takes precedence over global."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create project pyproject.toml
            pyproject = Path(tmpdir) / "pyproject.toml"
            pyproject.write_text("""
[project]
dependencies = [
    "ai-todo>=3.0.0,<4.0.0",
]
""")
            # Create global config with different constraint
            global_config_path = Path(tmpdir) / "global_config.yaml"
            global_config_path.write_text("update:\n  version_constraint: '==2.0.0'\n")

            with patch(
                "ai_todo.core.version_constraints.get_global_config_path",
                return_value=global_config_path,
            ):
                result = get_effective_constraint(Path(tmpdir))

            # Should use project constraint, not global
            assert result is not None
            assert result.min_version == (3, 0, 0)
            assert result.max_version == (4, 0, 0)

    def test_falls_back_to_global(self):
        """Test fallback to global config when no project constraint."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # No pyproject.toml
            global_config_path = Path(tmpdir) / "global_config.yaml"
            global_config_path.write_text("update:\n  version_constraint: '>=2.0.0'\n")

            with patch(
                "ai_todo.core.version_constraints.get_global_config_path",
                return_value=global_config_path,
            ):
                result = get_effective_constraint(Path(tmpdir))

            assert result is not None
            assert result.min_version == (2, 0, 0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
