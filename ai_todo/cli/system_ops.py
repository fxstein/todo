"""System operations commands for todo.ai."""

import re
import shutil
from datetime import datetime
from pathlib import Path


def view_log_command(
    filter_text: str | None = None, lines: int | None = None, todo_path: str = "TODO.md"
) -> None:
    """View TODO operation log (with --filter and --lines options)."""
    # Check new location first, then legacy
    config_dir = Path(todo_path).parent / ".ai-todo"
    if not config_dir.exists():
        config_dir = Path(todo_path).parent / ".todo.ai"
    log_file = config_dir / ".ai-todo.log"
    if not log_file.exists():
        log_file = config_dir / ".todo.ai.log"

    if not log_file.exists():
        print("No log file found")
        return

    print("📋 TODO Tool Log")
    print("=================")
    print("")

    content = log_file.read_text(encoding="utf-8")
    log_lines = [line for line in content.splitlines() if line.strip() and not line.startswith("#")]

    if filter_text:
        print(f"Filtering by: {filter_text}")
        print("")
        filtered = [line for line in log_lines if filter_text.lower() in line.lower()]
        log_lines = filtered

    if lines:
        log_lines = log_lines[:lines]
    else:
        log_lines = log_lines[:50]  # Default to 50 lines

    for line in log_lines:
        print(line)


def update_command() -> None:
    """Update todo.ai to latest version."""
    print("🔄 Updating todo.ai...")
    print("")
    print("Note: For Python package installations, use:")
    print("  pip install --upgrade ai-todo")
    print("  # or")
    print("  uv pip install --upgrade ai-todo")
    print("")
    print("For shell script installations, visit:")
    print("  https://github.com/fxstein/ai-todo")


def list_backups_command(todo_path: str = "TODO.md") -> None:
    """List available backup versions."""
    config_dir = Path(todo_path).parent / ".ai-todo"
    if not config_dir.exists():
        config_dir = Path(todo_path).parent / ".todo.ai"
    backups_dir = config_dir / "backups"

    if not backups_dir.exists():
        print("No backups available")
        return

    # Find all backup files (format: todo.ai.TIMESTAMP)
    backup_files = sorted(
        backups_dir.glob("todo.ai.*"), key=lambda p: p.stat().st_mtime, reverse=True
    )

    if not backup_files:
        print("No backups available")
        return

    print("Available backups:")
    print("")

    for index, backup in enumerate(backup_files, 1):
        filename = backup.name
        timestamp = filename.replace("todo.ai.", "")
        try:
            # Try to extract version from backup file
            content = backup.read_text(encoding="utf-8", errors="ignore")
            version_match = re.search(r'VERSION="([^"]+)"', content)
            version = version_match.group(1) if version_match else "unknown"
        except Exception:
            version = "unknown"

        # Get file modification time
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        date_str = mtime.strftime("%Y-%m-%d %H:%M:%S")

        if index == 1:
            print(f"  [{index}] {timestamp} (v{version}) - {date_str} [LATEST]")
        else:
            print(f"  [{index}] {timestamp} (v{version}) - {date_str}")

    print("")
    print("Use './todo.ai rollback [index|timestamp]' to restore a backup")


def rollback_command(target: str | None = None, todo_path: str = "TODO.md") -> None:
    """Rollback to previous version (by index or timestamp)."""
    config_dir = Path(todo_path).parent / ".ai-todo"
    if not config_dir.exists():
        config_dir = Path(todo_path).parent / ".todo.ai"
    backups_dir = config_dir / "backups"

    if not backups_dir.exists():
        print("Error: No backups available")
        return

    backup_files = sorted(
        backups_dir.glob("todo.ai.*"), key=lambda p: p.stat().st_mtime, reverse=True
    )

    if not backup_files:
        print("Error: No backups available")
        return

    target_backup: Path | None = None

    if not target:
        # Default: rollback to latest backup
        target_backup = backup_files[0]
    elif target.isdigit():
        # Index specified
        index = int(target)
        if 1 <= index <= len(backup_files):
            target_backup = backup_files[index - 1]
        else:
            print("Error: Invalid backup index. Use './todo.ai backups' to see available backups")
            return
    else:
        # Timestamp or version specified
        for backup in backup_files:
            filename = backup.name
            timestamp = filename.replace("todo.ai.", "")
            if timestamp == target:
                target_backup = backup
                break

            # Also check version
            try:
                content = backup.read_text(encoding="utf-8", errors="ignore")
                version_match = re.search(r'VERSION="([^"]+)"', content)
                if version_match and version_match.group(1) == target:
                    target_backup = backup
                    break
            except Exception:
                pass

        if not target_backup:
            print(f"Error: No backup found matching '{target}'")
            print("Use './todo.ai backups' to see available backups")
            return

    if not target_backup or not target_backup.exists():
        print("Error: Backup file not found")
        return

    # Extract version from backup
    try:
        content = target_backup.read_text(encoding="utf-8", errors="ignore")
        version_match = re.search(r'VERSION="([^"]+)"', content)
        backup_version = version_match.group(1) if version_match else "unknown"
    except Exception:
        backup_version = "unknown"

    # Get current version
    try:
        from ai_todo import __version__

        current_version = __version__
    except Exception:
        current_version = "unknown"

    backup_name = target_backup.name

    print("⚠️  Rollback Warning:")
    print(f"   Current version: {current_version}")
    print(f"   Backup version:  {backup_version}")
    print(f"   Backup file:     {backup_name}")
    print("")
    print("This will replace the current script with the backup version.")
    print("Continue? (y/N)")
    reply = input().strip()
    if reply.lower() != "y":
        print("Rollback cancelled")
        return

    # Note: For Python package, rollback doesn't make sense in the same way
    # This is mainly for shell script installations
    print("Note: For Python package installations, rollback should be done via:")
    print("  pip install ai-todo==<version>")
    print("  # or")
    print("  uv pip install ai-todo==<version>")


def create_backup(todo_path: str = "TODO.md") -> str | None:
    """Create a backup of TODO.md before major operations."""
    todo_file = Path(todo_path)
    if not todo_file.exists():
        return None

    config_dir = todo_file.parent / ".ai-todo"
    if not config_dir.exists():
        config_dir = todo_file.parent / ".todo.ai"
    backups_dir = config_dir / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_name = f"todo.ai.{timestamp}"
    backup_path = backups_dir / backup_name

    try:
        shutil.copy2(todo_file, backup_path)
        return backup_name
    except Exception as e:
        print(f"Warning: Failed to create backup: {e}")
        return None
