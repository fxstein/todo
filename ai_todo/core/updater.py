"""Self-update functionality for ai-todo.

Provides version checking against PyPI and update mechanisms via uv.
Supports both production (installed via uv/pip) and development (editable) modes.
"""

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from ai_todo import __version__


@dataclass
class UpdateInfo:
    """Information about an available update."""

    current_version: str
    latest_version: str
    is_dev_mode: bool
    update_available: bool

    @property
    def message(self) -> str:
        """Human-readable update status message."""
        if self.is_dev_mode:
            if self.update_available:
                return (
                    f"Update available: {self.current_version} -> {self.latest_version}\n"
                    f"Running in development mode. Use 'git pull' to update, then restart."
                )
            return f"Running in development mode at version {self.current_version} (latest: {self.latest_version})"
        else:
            if self.update_available:
                return f"Update available: {self.current_version} -> {self.latest_version}"
            return f"ai-todo is up to date (version {self.current_version})"


def is_dev_mode() -> bool:
    """Check if ai-todo is installed in development/editable mode.

    Detects editable installs by checking if the package directory
    is outside the site-packages directory.
    """
    try:
        # Get the directory where ai_todo is installed
        import ai_todo

        package_dir = Path(ai_todo.__file__).parent.resolve()

        # Get site-packages directories
        site_packages = [Path(p).resolve() for p in sys.path if "site-packages" in p]

        # If package is not in any site-packages, it's likely editable/dev mode
        for sp in site_packages:
            try:
                package_dir.relative_to(sp)
                return False  # Package is in site-packages, not dev mode
            except ValueError:
                continue

        # Also check for .egg-link file (legacy editable installs)
        for path_item in sys.path:
            egg_link = Path(path_item) / "ai-todo.egg-link"
            if egg_link.exists():
                return True

        # If not in site-packages, assume dev mode
        return True
    except Exception:
        return False


def get_latest_version() -> str | None:
    """Fetch the latest version from PyPI.

    Returns:
        Latest version string, or None if unable to fetch.
    """
    import json

    try:
        with urlopen("https://pypi.org/pypi/ai-todo/json", timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            version = data.get("info", {}).get("version")
            return str(version) if version else None
    except (URLError, TimeoutError, json.JSONDecodeError, KeyError):
        return None


def parse_version(version: str) -> tuple[int, ...]:
    """Parse a version string into a comparable tuple.

    Handles versions like "3.0.2", "3.0.2b1", "3.0.2rc1".
    """
    # Remove any beta/rc/alpha suffixes for comparison
    # "3.0.2b1" -> "3.0.2", "3.0.2rc1" -> "3.0.2"
    import re

    base_version = re.split(r"[a-zA-Z]", version)[0]
    parts = base_version.split(".")
    return tuple(int(p) for p in parts if p.isdigit())


def check_for_updates() -> UpdateInfo:
    """Check if an update is available.

    Returns:
        UpdateInfo with current/latest versions and update availability.
    """
    current = __version__
    latest = get_latest_version()
    dev_mode = is_dev_mode()

    if latest is None:
        # Can't check, assume up to date
        return UpdateInfo(
            current_version=current,
            latest_version=current,
            is_dev_mode=dev_mode,
            update_available=False,
        )

    # Compare versions
    try:
        current_tuple = parse_version(current)
        latest_tuple = parse_version(latest)
        update_available = latest_tuple > current_tuple
    except (ValueError, IndexError):
        update_available = False

    return UpdateInfo(
        current_version=current,
        latest_version=latest,
        is_dev_mode=dev_mode,
        update_available=update_available,
    )


def perform_update(restart: bool = True) -> tuple[bool, str]:
    """Perform the update using uv.

    Args:
        restart: If True, exit the process after update to trigger restart by host.

    Returns:
        Tuple of (success, message).
    """
    info = check_for_updates()

    if info.is_dev_mode:
        if restart:
            return (
                True,
                f"Development mode detected. Restarting to pick up code changes...\n"
                f"Current version: {info.current_version}",
            )
        else:
            return (
                False,
                f"Development mode detected. Use 'git pull' to update code.\n"
                f"Current version: {info.current_version}",
            )

    if not info.update_available:
        if restart:
            return (True, f"Already at latest version ({info.current_version}). Restarting...")
        else:
            return (True, f"ai-todo is already at the latest version ({info.current_version})")

    # Try to update using uv
    try:
        # First, try uv pip install --upgrade
        result = subprocess.run(
            ["uv", "pip", "install", "--upgrade", "ai-todo"],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode == 0:
            return (
                True,
                f"Successfully updated ai-todo: {info.current_version} -> {info.latest_version}\n"
                + ("Restarting to apply update..." if restart else ""),
            )
        else:
            # Try alternative: uvx with version
            return (
                False,
                f"Update failed: {result.stderr}\nTry manually: uv pip install --upgrade ai-todo",
            )

    except FileNotFoundError:
        return (
            False,
            "uv not found. Install uv or manually update:\n  pip install --upgrade ai-todo",
        )
    except subprocess.TimeoutExpired:
        return (False, "Update timed out. Try again later.")
    except Exception as e:
        return (False, f"Update failed: {e}")


def restart_server() -> None:
    """Exit the server process to trigger restart by host.

    For MCP servers using stdio transport, exiting cleanly causes
    the host (e.g., Cursor) to detect the exit and restart the server.
    """
    # Use os._exit to avoid any cleanup that might hang
    # Exit code 0 indicates clean shutdown
    os._exit(0)
