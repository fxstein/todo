from pathlib import Path
from typing import Any

import yaml


class Config:
    """Manages ai-todo configuration."""

    # Data directory names
    NEW_DATA_DIR = ".ai-todo"
    OLD_DATA_DIR = ".todo.ai"

    def __init__(self, config_path: str = ".ai-todo/config.yaml"):
        self.config_path = Path(config_path)
        self._data: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            return

        try:
            content = self.config_path.read_text(encoding="utf-8")
            self._data = yaml.safe_load(content) or {}
        except Exception as e:
            # Fallback to empty config on error
            print(f"Warning: Failed to load config: {e}")
            self._data = {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        Supports dot notation for nested keys (e.g., "coordination.type").
        """
        keys = key.split(".")
        value = self._data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value by key.
        Supports dot notation for nested keys.
        Saves to file immediately.
        """
        keys = key.split(".")
        target = self._data

        # Traverse to the last dict
        for k in keys[:-1]:
            if k not in target or not isinstance(target[k], dict):
                target[k] = {}
            target = target[k]

        target[keys[-1]] = value
        self._save()

    def _save(self) -> None:
        """Save configuration to YAML file."""
        # Ensure directory exists
        if not self.config_path.parent.exists():
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            content = yaml.dump(self._data, default_flow_style=False)
            self.config_path.write_text(content, encoding="utf-8")
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_numbering_mode(self) -> str:
        """Get current numbering mode."""
        result = self.get("mode", "single-user")
        return str(result) if result is not None else "single-user"

    def get_coordination_type(self) -> str:
        """Get current coordination type."""
        result = self.get("coordination.type", "none")
        return str(result) if result is not None else "none"
