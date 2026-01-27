"""Version constraint handling for ai-todo self-update feature.

Provides:
- GlobalConfig: User-level config at ~/.config/ai-todo/config.yaml
- Version constraint parsing and validation using PEP 440 specifiers
- Project pyproject.toml constraint detection
"""

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from ai_todo import __version__


@dataclass
class VersionConstraint:
    """Parsed version constraint with optional min/max bounds."""

    raw: str  # Original constraint string (e.g., ">=3.0.0,<4.0.0")
    min_version: tuple[int, ...] | None = None
    max_version: tuple[int, ...] | None = None
    min_inclusive: bool = True
    max_inclusive: bool = False
    pinned: str | None = None  # Exact version if pinned (e.g., "==3.0.2")
    allow_prerelease: bool = False

    def satisfies(self, version: str) -> bool:
        """Check if a version string satisfies this constraint."""
        try:
            ver_tuple = parse_version(version)
        except (ValueError, IndexError):
            return False

        # Pinned version check
        if self.pinned:
            try:
                pinned_tuple = parse_version(self.pinned)
                return ver_tuple == pinned_tuple
            except (ValueError, IndexError):
                return False

        # Check minimum
        if self.min_version:
            if self.min_inclusive:
                if ver_tuple < self.min_version:
                    return False
            else:
                if ver_tuple <= self.min_version:
                    return False

        # Check maximum
        if self.max_version:
            if self.max_inclusive:
                if ver_tuple > self.max_version:
                    return False
            else:
                if ver_tuple >= self.max_version:
                    return False

        return True


def parse_version(version: str) -> tuple[int, ...]:
    """Parse a version string into a comparable tuple.

    Handles versions like "3.0.2", "3.0.2b1", "3.0.2rc1".
    """
    # Remove any beta/rc/alpha suffixes for comparison
    base_version = re.split(r"[a-zA-Z]", version)[0]
    parts = base_version.split(".")
    return tuple(int(p) for p in parts if p.isdigit())


def parse_constraint(constraint_str: str) -> VersionConstraint:
    """Parse a PEP 440 version constraint string.

    Examples:
        "==3.0.2" -> pinned to 3.0.2
        ">=3.0.0" -> minimum 3.0.0
        ">=3.0.0,<4.0.0" -> range [3.0.0, 4.0.0)
        "<4.0.0" -> maximum (exclusive) 4.0.0
    """
    constraint = VersionConstraint(raw=constraint_str)

    # Split by comma for multiple constraints
    parts = [p.strip() for p in constraint_str.split(",")]

    for part in parts:
        if part.startswith("=="):
            constraint.pinned = part[2:].strip()
        elif part.startswith(">="):
            constraint.min_version = parse_version(part[2:].strip())
            constraint.min_inclusive = True
        elif part.startswith(">"):
            constraint.min_version = parse_version(part[1:].strip())
            constraint.min_inclusive = False
        elif part.startswith("<="):
            constraint.max_version = parse_version(part[2:].strip())
            constraint.max_inclusive = True
        elif part.startswith("<"):
            constraint.max_version = parse_version(part[1:].strip())
            constraint.max_inclusive = False
        elif part.startswith("!="):
            # Not equal - we don't fully support this, just ignore
            pass
        elif part.startswith("~="):
            # Compatible release - treat as >= with implicit <
            ver = part[2:].strip()
            ver_parts = ver.split(".")
            constraint.min_version = parse_version(ver)
            constraint.min_inclusive = True
            # ~=3.0 means >=3.0,<4.0
            if len(ver_parts) >= 2:
                major = int(ver_parts[0])
                constraint.max_version = (major + 1,)
                constraint.max_inclusive = False

    return constraint


def get_global_config_path() -> Path:
    """Get the global config path following XDG conventions."""
    if xdg_config := os.environ.get("XDG_CONFIG_HOME"):
        return Path(xdg_config) / "ai-todo" / "config.yaml"
    return Path.home() / ".config" / "ai-todo" / "config.yaml"


class GlobalConfig:
    """User-level global configuration for ai-todo.

    Stored at ~/.config/ai-todo/config.yaml (or XDG_CONFIG_HOME).
    Used for system-global tool installs where no project pyproject.toml applies.
    """

    def __init__(self, config_path: Path | None = None):
        self.config_path = config_path or get_global_config_path()
        self._data: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            return

        try:
            content = self.config_path.read_text(encoding="utf-8")
            self._data = yaml.safe_load(content) or {}
        except Exception:
            self._data = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)."""
        keys = key.split(".")
        value = self._data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """Set configuration value by key (supports dot notation)."""
        keys = key.split(".")
        target = self._data

        for k in keys[:-1]:
            if k not in target or not isinstance(target[k], dict):
                target[k] = {}
            target = target[k]

        target[keys[-1]] = value
        self._save()

    def _save(self) -> None:
        """Save configuration to YAML file."""
        if not self.config_path.parent.exists():
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            content = yaml.dump(self._data, default_flow_style=False)
            self.config_path.write_text(content, encoding="utf-8")
        except Exception as e:
            print(f"Error saving global config: {e}", file=sys.stderr)

    def get_version_constraint(self) -> VersionConstraint | None:
        """Get the configured version constraint for updates."""
        constraint_str = self.get("update.version_constraint")
        if constraint_str:
            try:
                return parse_constraint(str(constraint_str))
            except (ValueError, IndexError):
                return None
        return None

    def get_allow_prerelease(self) -> bool:
        """Check if prerelease versions are allowed."""
        return bool(self.get("update.allow_prerelease", False))


def get_project_constraint(project_root: Path) -> VersionConstraint | None:
    """Read ai-todo version constraint from project's pyproject.toml.

    Returns None if ai-todo is not listed as a dependency.
    """
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        return None

    try:
        content = pyproject_path.read_text(encoding="utf-8")

        # Simple regex to find ai-todo in dependencies
        # Matches: "ai-todo>=3.0.0,<4.0.0" or "ai-todo" or ai-todo = ">=3.0.0"
        patterns = [
            r'"ai-todo([^"]*)"',  # "ai-todo>=3.0.0,<4.0.0"
            r"'ai-todo([^']*)'",  # 'ai-todo>=3.0.0,<4.0.0'
            r"ai-todo\s*=\s*[\"']([^\"']+)[\"']",  # ai-todo = ">=3.0.0"
        ]

        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                constraint_str = match.group(1).strip()
                if constraint_str:
                    return parse_constraint(constraint_str)
                # ai-todo with no constraint means any version
                return None

    except Exception:
        pass

    return None


def check_version_mismatch(project_root: Path) -> str | None:
    """Check if current version mismatches project constraint.

    Returns warning message if mismatch, None if OK or no constraint.
    """
    constraint = get_project_constraint(project_root)
    if constraint is None:
        return None

    current = __version__
    if not constraint.satisfies(current):
        return (
            f"Warning: ai-todo {current} doesn't match project constraint {constraint.raw}\n"
            f"Consider using project-local install: uv add ai-todo"
        )

    return None


def get_effective_constraint(project_root: Path | None = None) -> VersionConstraint | None:
    """Get the effective version constraint based on precedence.

    Precedence (highest to lowest):
    1. Project pyproject.toml (if ai-todo is a dependency)
    2. User-level ~/.config/ai-todo/config.yaml
    3. None (upgrade to latest)
    """
    # Check project constraint first
    if project_root:
        project_constraint = get_project_constraint(project_root)
        if project_constraint:
            return project_constraint

    # Fall back to global config
    global_config = GlobalConfig()
    return global_config.get_version_constraint()
