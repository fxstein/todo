"""Unit tests for ai_todo.core.updater module."""

from unittest.mock import MagicMock, patch

import pytest

from ai_todo.core.updater import (
    UpdateInfo,
    check_for_updates,
    get_latest_version,
    is_dev_mode,
    parse_version,
    perform_update,
)


class TestParseVersion:
    """Tests for version parsing."""

    def test_simple_version(self):
        """Test parsing simple version strings."""
        assert parse_version("3.0.2") == (3, 0, 2)
        assert parse_version("1.0.0") == (1, 0, 0)
        assert parse_version("10.20.30") == (10, 20, 30)

    def test_beta_version(self):
        """Test parsing beta version strings."""
        assert parse_version("3.0.2b1") == (3, 0, 2)
        assert parse_version("1.0.0b14") == (1, 0, 0)

    def test_rc_version(self):
        """Test parsing release candidate version strings."""
        assert parse_version("3.0.2rc1") == (3, 0, 2)
        assert parse_version("2.0.0rc3") == (2, 0, 0)

    def test_alpha_version(self):
        """Test parsing alpha version strings."""
        assert parse_version("3.0.2a1") == (3, 0, 2)

    def test_version_comparison(self):
        """Test that parsed versions compare correctly."""
        assert parse_version("3.0.2") > parse_version("3.0.1")
        assert parse_version("3.1.0") > parse_version("3.0.9")
        assert parse_version("4.0.0") > parse_version("3.9.9")
        assert parse_version("3.0.2") == parse_version("3.0.2b1")  # Base version equal


class TestUpdateInfo:
    """Tests for UpdateInfo dataclass."""

    def test_message_dev_mode_update_available(self):
        """Test message when in dev mode with update available."""
        info = UpdateInfo(
            current_version="3.0.1",
            latest_version="3.0.2",
            is_dev_mode=True,
            update_available=True,
        )
        assert "Update available" in info.message
        assert "development mode" in info.message
        assert "git pull" in info.message

    def test_message_dev_mode_up_to_date(self):
        """Test message when in dev mode and up to date."""
        info = UpdateInfo(
            current_version="3.0.2",
            latest_version="3.0.2",
            is_dev_mode=True,
            update_available=False,
        )
        assert "development mode" in info.message
        assert "3.0.2" in info.message

    def test_message_production_update_available(self):
        """Test message when in production with update available."""
        info = UpdateInfo(
            current_version="3.0.1",
            latest_version="3.0.2",
            is_dev_mode=False,
            update_available=True,
        )
        assert "Update available" in info.message
        assert "3.0.1" in info.message
        assert "3.0.2" in info.message
        assert "development" not in info.message

    def test_message_production_up_to_date(self):
        """Test message when in production and up to date."""
        info = UpdateInfo(
            current_version="3.0.2",
            latest_version="3.0.2",
            is_dev_mode=False,
            update_available=False,
        )
        assert "up to date" in info.message
        assert "3.0.2" in info.message


class TestGetLatestVersion:
    """Tests for get_latest_version function."""

    def test_successful_fetch(self):
        """Test successful version fetch from PyPI."""
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"info": {"version": "3.0.5"}}'
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch("ai_todo.core.updater.urlopen", return_value=mock_response):
            version = get_latest_version()
            assert version == "3.0.5"

    def test_network_error(self):
        """Test handling of network errors."""
        from urllib.error import URLError

        with patch("ai_todo.core.updater.urlopen", side_effect=URLError("Network error")):
            version = get_latest_version()
            assert version is None

    def test_timeout_error(self):
        """Test handling of timeout errors."""
        with patch("ai_todo.core.updater.urlopen", side_effect=TimeoutError()):
            version = get_latest_version()
            assert version is None


class TestIsDevMode:
    """Tests for is_dev_mode function."""

    def test_detects_dev_mode(self):
        """Test that is_dev_mode returns a boolean."""
        # Just verify it returns a boolean without crashing
        result = is_dev_mode()
        assert isinstance(result, bool)

    def test_current_repo_is_dev_mode(self):
        """Test that running from repo is detected as dev mode."""
        # When running tests from the repo, should be in dev mode
        assert is_dev_mode() is True


class TestCheckForUpdates:
    """Tests for check_for_updates function."""

    def test_returns_update_info(self):
        """Test that check_for_updates returns UpdateInfo."""
        with patch("ai_todo.core.updater.get_latest_version", return_value="3.0.2"):
            info = check_for_updates()
            assert isinstance(info, UpdateInfo)
            assert info.current_version is not None

    def test_handles_pypi_failure(self):
        """Test handling when PyPI is unreachable."""
        with patch("ai_todo.core.updater.get_latest_version", return_value=None):
            info = check_for_updates()
            assert isinstance(info, UpdateInfo)
            assert info.update_available is False

    def test_detects_update_available(self):
        """Test detection of available update."""
        with (
            patch("ai_todo.core.updater.get_latest_version", return_value="99.0.0"),
            patch("ai_todo.core.updater.is_dev_mode", return_value=False),
        ):
            info = check_for_updates()
            assert info.update_available is True
            assert info.latest_version == "99.0.0"

    def test_detects_up_to_date(self):
        """Test detection when already at latest."""
        from ai_todo import __version__

        with patch("ai_todo.core.updater.get_latest_version", return_value=__version__):
            info = check_for_updates()
            assert info.update_available is False


class TestPerformUpdate:
    """Tests for perform_update function."""

    def test_dev_mode_with_restart(self):
        """Test update in dev mode with restart requested."""
        with patch("ai_todo.core.updater.is_dev_mode", return_value=True):
            success, message = perform_update(restart=True)
            assert success is True
            assert "Development mode" in message
            assert "Restarting" in message

    def test_dev_mode_without_restart(self):
        """Test update in dev mode without restart."""
        with patch("ai_todo.core.updater.is_dev_mode", return_value=True):
            success, message = perform_update(restart=False)
            assert success is False
            assert "Development mode" in message
            assert "git pull" in message

    def test_already_up_to_date(self):
        """Test update when already at latest version."""
        from ai_todo import __version__

        with (
            patch("ai_todo.core.updater.is_dev_mode", return_value=False),
            patch("ai_todo.core.updater.get_latest_version", return_value=__version__),
        ):
            success, message = perform_update(restart=False)
            assert success is True
            assert "latest version" in message

    def test_uv_not_found(self):
        """Test handling when uv is not installed."""
        with (
            patch("ai_todo.core.updater.is_dev_mode", return_value=False),
            patch("ai_todo.core.updater.get_latest_version", return_value="99.0.0"),
            patch("subprocess.run", side_effect=FileNotFoundError()),
        ):
            success, message = perform_update(restart=False)
            assert success is False
            assert "uv not found" in message


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
