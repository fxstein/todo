from collections.abc import Callable
from datetime import datetime
from pathlib import Path


class MigrationRegistry:
    """Manages migration execution."""

    def __init__(self, config_dir: str = ".ai-todo"):
        self.config_dir = Path(config_dir)
        self.migrations_dir = self.config_dir / "migrations"
        self.state_file = self.migrations_dir / "state.yaml"
        self._migrations: dict[str, Callable] = {}

        # Ensure directories exist
        if not self.migrations_dir.exists():
            self.migrations_dir.mkdir(parents=True, exist_ok=True)

    def register_migration(self, migration_id: str, func: Callable) -> None:
        """Register a migration function."""
        self._migrations[migration_id] = func

    def get_applied_migrations(self) -> list[str]:
        """Get list of already applied migration IDs."""
        if not self.state_file.exists():
            return []

        import yaml

        try:
            content = self.state_file.read_text(encoding="utf-8")
            data = yaml.safe_load(content) or {}
            applied = data.get("applied", [])
            return [str(item) for item in applied] if applied else []
        except Exception as e:
            print(f"Warning: Failed to load migration state: {e}")
            return []

    def _save_state(self, applied: list[str]) -> None:
        """Save applied migrations state."""
        import yaml

        data = {"applied": applied, "last_updated": datetime.now().isoformat()}
        self.state_file.write_text(yaml.dump(data), encoding="utf-8")

    def run_pending_migrations(self) -> list[str]:
        """Run all pending migrations."""
        applied = self.get_applied_migrations()
        executed = []

        # Sort migrations by ID (assuming lexicographical order works for now)
        # IDs should be something like "001_initial", "002_update_x"
        sorted_ids = sorted(self._migrations.keys())

        for mid in sorted_ids:
            if mid not in applied:
                print(f"Running migration: {mid}")
                try:
                    self._migrations[mid]()
                    applied.append(mid)
                    executed.append(mid)
                except Exception as e:
                    print(f"Error running migration {mid}: {e}")
                    raise e

        if executed:
            self._save_state(applied)

        return executed
