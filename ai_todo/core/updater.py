"""Self-update functionality for ai-todo.

Provides version checking against PyPI and update mechanisms via uv.
Supports both production (installed via uv/pip) and development (editable) modes.
Respects version constraints from pyproject.toml or global config.
"""

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
    target_version: str | None = (
        None  # Version to update to (may differ from latest if constrained)
    )
    constraint_info: str | None = None  # Info about active constraint

    @property
    def message(self) -> str:
        """Human-readable update status message."""
        constraint_msg = f" ({self.constraint_info})" if self.constraint_info else ""

        if self.is_dev_mode:
            if self.update_available:
                return (
                    f"Update available: {self.current_version} -> {self.latest_version}\n"
                    f"Running in development mode. Use 'git pull' to update, then restart."
                )
            return f"Running in development mode at version {self.current_version} (latest: {self.latest_version})"
        else:
            if self.update_available:
                if self.target_version and self.target_version != self.latest_version:
                    return (
                        f"Update available: {self.current_version} -> {self.target_version}{constraint_msg}\n"
                        f"(Latest is {self.latest_version}, but constrained)"
                    )
                return f"Update available: {self.current_version} -> {self.latest_version}{constraint_msg}"
            if self.constraint_info:
                return f"ai-todo is up to date (version {self.current_version}){constraint_msg}"
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


def check_for_updates(project_root: Path | None = None) -> UpdateInfo:
    """Check if an update is available, respecting version constraints.

    Args:
        project_root: Project root directory to check for pyproject.toml constraints.

    Returns:
        UpdateInfo with current/latest versions and update availability.
    """
    from ai_todo.core.version_constraints import get_effective_constraint

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

    # Check for version constraints
    constraint = get_effective_constraint(project_root)
    constraint_info: str | None = None
    target_version: str | None = latest

    if constraint:
        constraint_info = f"constraint: {constraint.raw}"

        # If pinned, no updates allowed
        if constraint.pinned:
            return UpdateInfo(
                current_version=current,
                latest_version=latest,
                is_dev_mode=dev_mode,
                update_available=False,
                constraint_info=f"pinned to {constraint.pinned}",
            )

        # Check if latest satisfies constraint
        if not constraint.satisfies(latest):
            # Latest doesn't satisfy constraint - find best version that does
            # For now, just report that we can't update beyond constraint
            target_version = None
            constraint_info = f"latest {latest} exceeds constraint {constraint.raw}"

    # Compare versions
    try:
        current_tuple = parse_version(current)
        latest_tuple = parse_version(latest)
        update_available = latest_tuple > current_tuple

        # If constrained and latest exceeds constraint, check if we're at max allowed
        if constraint and target_version is None:
            update_available = False
    except (ValueError, IndexError):
        update_available = False

    return UpdateInfo(
        current_version=current,
        latest_version=latest,
        is_dev_mode=dev_mode,
        update_available=update_available,
        target_version=target_version if update_available else None,
        constraint_info=constraint_info,
    )


def perform_update(restart: bool = True, project_root: Path | None = None) -> tuple[bool, str]:
    """Perform the update using uv, respecting version constraints.

    Args:
        restart: If True, exit the process after update to trigger restart by host.
        project_root: Project root directory to check for pyproject.toml constraints.

    Returns:
        Tuple of (success, message).
    """
    info = check_for_updates(project_root)

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
        msg = f"ai-todo is already at the latest version ({info.current_version})"
        if info.constraint_info:
            msg += f"\n({info.constraint_info})"
        if restart:
            return (True, msg + "\nRestarting...")
        else:
            return (True, msg)

    # Determine target version
    target = info.target_version or info.latest_version

    # Try to update using uv
    try:
        # Build the install command with optional version constraint
        cmd = ["uv", "pip", "install", "--upgrade", f"ai-todo=={target}"]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode == 0:
            msg = f"Successfully updated ai-todo: {info.current_version} -> {target}"
            if info.constraint_info:
                msg += f"\n({info.constraint_info})"
            if restart:
                msg += "\nRestarting to apply update..."
            return (True, msg)
        else:
            return (
                False,
                f"Update failed: {result.stderr}\nTry manually: uv pip install ai-todo=={target}",
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


def restart_server(exit_code: int = 1) -> None:
    """Exit the server process to trigger restart by host.

    For MCP servers, we must fully exit so the host (Cursor) spawns
    a completely new process with proper MCP initialization handshake.

    Note: Must use os._exit() because sys.exit() from a daemon thread
    only terminates that thread, not the whole process.

    Args:
        exit_code: Exit code to use.
    """
    import os
    import sys

    # Flush all output buffers to ensure response is fully sent
    sys.stdout.flush()
    sys.stderr.flush()

    # Force exit entire process - sys.exit() doesn't work from daemon threads
    os._exit(exit_code)
