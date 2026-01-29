import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class GitLogEntry:
    """Represents a git log entry."""

    commit_hash: str
    author: str
    date: datetime
    message: str


def get_git_root() -> str | None:
    """Get the root directory of the git repository."""
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
        return root
    except subprocess.CalledProcessError:
        return None


def get_current_branch() -> str:
    """Get current git branch name."""
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
        ).strip()
        return branch
    except subprocess.CalledProcessError:
        return "main"


def get_user_name() -> str:
    """Get git user name."""
    try:
        name = subprocess.check_output(["git", "config", "user.name"], text=True).strip()
        return name
    except subprocess.CalledProcessError:
        return "user"


def get_user_email() -> str:
    """Get git user email."""
    try:
        email = subprocess.check_output(["git", "config", "user.email"], text=True).strip()
        return email
    except subprocess.CalledProcessError:
        return ""


def is_git_repo() -> bool:
    """Check if current directory is inside a git repository."""
    return get_git_root() is not None


def get_task_archive_date(task_id: str, todo_path: str) -> datetime | None:
    """
    Get the archive date for a task by parsing git history.

    Args:
        task_id: Task ID (e.g., "129", "129.1")
        todo_path: Path to TODO.md file

    Returns:
        datetime of when task was archived, or None if not found

    Algorithm:
        1. Try git log: search for commits mentioning task archive
        2. Parse most recent matching commit timestamp
        3. If no git match, fall back to parsing task metadata (YYYY-MM-DD)
        4. Return None if neither method succeeds
    """
    # Try git log first
    try:
        # Escape task_id for regex (e.g., "129.1" -> "129\.1")
        escaped_task_id = re.escape(task_id)
        # Use extended regex with OR (|) to match EITHER pattern
        result = subprocess.run(
            [
                "git",
                "log",
                "--all",
                "--extended-regexp",
                f"--grep=archive.*{escaped_task_id}|#{escaped_task_id}",
                "--format=%ai",
                "--",
                todo_path,
            ],
            capture_output=True,
            text=True,
            cwd=str(Path(todo_path).parent),
            check=False,
        )

        if result.returncode == 0 and result.stdout.strip():
            # Parse first (most recent) date
            date_str = result.stdout.strip().split("\n")[0]
            # Format: "2026-01-28 10:30:45 -0800"
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %z")
    except Exception:
        pass  # Fall through to fallback

    # Fallback: Parse metadata from archived task line
    return parse_archive_date_from_metadata(task_id, todo_path)


def parse_archive_date_from_metadata(task_id: str, todo_path: str) -> datetime | None:
    """
    Parse archive date from task metadata line.

    Format: - [x] **#129** Task description (2026-01-28)

    Args:
        task_id: Task ID
        todo_path: Path to TODO.md

    Returns:
        datetime of archive date, or None if not found
    """
    try:
        content = Path(todo_path).read_text(encoding="utf-8")
        # Look for archived task with ID
        # Pattern matches: [x] **#129** ... (2026-01-28)
        pattern = rf"\[x\]\s+\*\*#{re.escape(task_id)}\*\*.*\((\d{{4}}-\d{{2}}-\d{{2}})\)"
        match = re.search(pattern, content)

        if match:
            date_str = match.group(1)
            # Parse as naive datetime (no timezone)
            return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        pass

    return None


def get_git_log_entries(task_id: str, todo_path: str) -> list[GitLogEntry]:
    """
    Get all git log entries mentioning a task.

    Args:
        task_id: Task ID
        todo_path: Path to TODO.md

    Returns:
        List of GitLogEntry objects, newest first
    """
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--all",
                f"--grep=#{task_id}",
                "--format=%H%x00%an%x00%ai%x00%s",
                "--",
                todo_path,
            ],
            capture_output=True,
            text=True,
            cwd=str(Path(todo_path).parent),
            check=False,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return []

        entries = []
        for line in result.stdout.strip().split("\n"):
            parts = line.split("\x00")
            if len(parts) == 4:
                commit_hash, author, date_str, message = parts
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %z")
                entries.append(
                    GitLogEntry(commit_hash=commit_hash, author=author, date=date, message=message)
                )

        return entries
    except Exception:
        return []
