# Prune Function Design Document

**Task:** #267.2 [AIT-2] Implement --prune function to remove archived tasks
**Linear Issue:** https://linear.app/fxstein/issue/AIT-2
**Analysis Document:** docs/design/prune_function_analysis.md
**Date:** 2026-01-28
**Status:** Design - Awaiting Review

## Executive Summary

This document specifies the technical design for implementing a prune function to remove old archived tasks from TODO.md based on git history analysis. The design follows the ai-todo architecture patterns, integrates with existing FileOps infrastructure, and provides both CLI and MCP interfaces.

**Key Design Decisions:**
- Git log parsing with completion date fallback for archive date detection
- Archive backup to `.ai-todo/archives/` before pruning (default ON)
- FileOps integration for all TODO.md operations
- Dry-run mode for safe previews
- MCP-CLI parity for consistency

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Prune Command (CLI/MCP)                  │
│  - Argument parsing & validation                             │
│  - User confirmation (CLI only)                              │
│  - Progress messages                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Prune Core Logic                            │
│  ai_todo/core/prune.py (NEW)                                │
│  - Task filtering by age/range                               │
│  - Archive backup creation                                   │
│  - FileOps integration                                       │
└────────┬─────────────────────────┬──────────────────────────┘
         │                         │
         ▼                         ▼
┌────────────────────┐    ┌───────────────────────────────────┐
│  Git History       │    │  Archive Backup                   │
│  ai_todo/utils/    │    │  .ai-todo/archives/               │
│  git.py (EXTEND)   │    │  TODO_ARCHIVE_YYYY-MM-DD.md       │
│  - Parse git log   │    │  - Standard TODO.md format        │
│  - Extract dates   │    │  - Metadata header                │
│  - Fallback logic  │    │  - Restoration-ready              │
└────────────────────┘    └───────────────────────────────────┘
```

## Component Specifications

### 1. Git History Analysis

**File:** `ai_todo/utils/git.py` (extend existing)

#### Function: `get_task_archive_date(task_id: str, todo_path: str) -> datetime | None`

**Purpose:** Determine when a task was archived by parsing git history.

**Algorithm:**
1. Search git log for commits mentioning task archive
2. Extract commit timestamp as archive date
3. Fall back to parsing archived task metadata if git unavailable
4. Return None if date cannot be determined

**Implementation:**
```python
def get_task_archive_date(task_id: str, todo_path: str) -> datetime | None:
    """
    Get the archive date for a task by parsing git history.

    Args:
        task_id: Task ID (e.g., "129", "129.1")
        todo_path: Path to TODO.md file

    Returns:
        datetime of when task was archived, or None if not found

    Algorithm:
        1. Try git log: git log --all --grep="archive.*{task_id}" --format="%ai" -- TODO.md
        2. Parse most recent matching commit timestamp
        3. If no git match, fall back to parsing task metadata (2026-01-28)
        4. Return None if neither method succeeds
    """
    # Try git log first
    try:
        result = subprocess.run(
            [
                "git", "log",
                "--all",
                f"--grep=archive.*{task_id}",
                "--grep=#{task_id}",  # Also match commit messages with task references
                "--format=%ai",
                "--",
                todo_path
            ],
            capture_output=True,
            text=True,
            cwd=str(Path(todo_path).parent),
            check=False
        )

        if result.returncode == 0 and result.stdout.strip():
            # Parse first (most recent) date
            date_str = result.stdout.strip().split('\n')[0]
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
        pattern = rf'\[x\]\s+\*\*#{re.escape(task_id)}\*\*.*\((\d{{4}}-\d{{2}}-\d{{2}})\)'
        match = re.search(pattern, content)

        if match:
            date_str = match.group(1)
            return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        pass

    return None
```

#### Function: `get_git_log_entries(task_id: str, todo_path: str) -> list[GitLogEntry]`

**Purpose:** Get all git log entries mentioning a task (for debugging/advanced features).

**Data Structure:**
```python
@dataclass
class GitLogEntry:
    """Represents a git log entry."""
    commit_hash: str
    author: str
    date: datetime
    message: str
```

**Implementation:**
```python
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
                "git", "log",
                "--all",
                f"--grep=#{task_id}",
                "--format=%H%x00%an%x00%ai%x00%s",
                "--",
                todo_path
            ],
            capture_output=True,
            text=True,
            cwd=str(Path(todo_path).parent),
            check=False
        )

        if result.returncode != 0 or not result.stdout.strip():
            return []

        entries = []
        for line in result.stdout.strip().split('\n'):
            parts = line.split('\x00')
            if len(parts) == 4:
                commit_hash, author, date_str, message = parts
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %z")
                entries.append(GitLogEntry(
                    commit_hash=commit_hash,
                    author=author,
                    date=date,
                    message=message
                ))

        return entries
    except Exception:
        return []
```

### 2. Prune Core Logic

**File:** `ai_todo/core/prune.py` (NEW)

#### Class: `PruneManager`

**Purpose:** Encapsulate prune logic and state.

**Implementation:**
```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from ai_todo.core.file_ops import FileOps
from ai_todo.core.task import Task, TaskManager, TaskStatus
from ai_todo.utils.git import get_task_archive_date


@dataclass
class PruneResult:
    """Result of a prune operation."""
    tasks_pruned: int
    subtasks_pruned: int
    archive_path: str | None
    dry_run: bool
    pruned_task_ids: list[str]

    @property
    def total_pruned(self) -> int:
        return self.tasks_pruned + self.subtasks_pruned


class PruneManager:
    """Manage prune operations on TODO.md archived tasks."""

    def __init__(self, todo_path: str = "TODO.md"):
        """Initialize PruneManager with TODO.md path."""
        self.todo_path = todo_path
        self.file_ops = FileOps(todo_path)

    def identify_tasks_to_prune(
        self,
        tasks: list[Task],
        days: int | None = None,
        older_than: str | None = None,
        from_task: str | None = None
    ) -> list[Task]:
        """
        Identify archived tasks matching prune criteria.

        Args:
            tasks: All tasks from TODO.md
            days: Prune tasks older than N days
            older_than: Prune tasks archived before YYYY-MM-DD
            from_task: Prune tasks from #1 to #from_task

        Returns:
            List of tasks to prune (includes subtasks)

        Algorithm:
            1. Filter for archived tasks only (status == ARCHIVED)
            2. Apply age filter (days or older_than)
            3. OR apply range filter (from_task)
            4. Include all subtasks of matching parent tasks
            5. Return deduplicated list
        """
        # Filter to archived tasks only
        archived_tasks = [t for t in tasks if t.status == TaskStatus.ARCHIVED]

        if not archived_tasks:
            return []

        # Apply filters
        if from_task:
            # Range-based pruning: #1 to #from_task
            return self._filter_by_task_range(archived_tasks, from_task)
        elif days is not None:
            # Age-based pruning: older than N days
            cutoff_date = datetime.now() - timedelta(days=days)
            return self._filter_by_age(archived_tasks, cutoff_date)
        elif older_than:
            # Date-based pruning: before specific date
            cutoff_date = datetime.strptime(older_than, "%Y-%m-%d")
            return self._filter_by_age(archived_tasks, cutoff_date)
        else:
            # Default: 30 days
            cutoff_date = datetime.now() - timedelta(days=30)
            return self._filter_by_age(archived_tasks, cutoff_date)

    def _filter_by_age(self, tasks: list[Task], cutoff_date: datetime) -> list[Task]:
        """Filter tasks older than cutoff date."""
        to_prune = []

        for task in tasks:
            # Skip subtasks - they'll be included with parent
            if "." in task.id:
                continue

            # Get archive date
            archive_date = get_task_archive_date(task.id, self.todo_path)

            if archive_date is None:
                # No date found - skip this task
                continue

            # Check if older than cutoff
            if archive_date < cutoff_date:
                to_prune.append(task)
                # Include all subtasks
                subtasks = [t for t in tasks if t.id.startswith(f"{task.id}.")]
                to_prune.extend(subtasks)

        return to_prune

    def _filter_by_task_range(self, tasks: list[Task], from_task: str) -> list[Task]:
        """Filter tasks from #1 to #from_task (inclusive)."""
        try:
            max_id = int(from_task)
        except ValueError:
            return []

        to_prune = []

        for task in tasks:
            # Extract numeric part of task ID
            if "." in task.id:
                # Subtask - check parent ID
                parent_id = task.id.split(".")[0]
                try:
                    if int(parent_id) <= max_id:
                        to_prune.append(task)
                except ValueError:
                    continue
            else:
                # Root task
                try:
                    if int(task.id) <= max_id:
                        to_prune.append(task)
                        # Include all subtasks
                        subtasks = [t for t in tasks if t.id.startswith(f"{task.id}.")]
                        to_prune.extend(subtasks)
                except ValueError:
                    continue

        return to_prune

    def create_archive_backup(
        self,
        tasks_to_prune: list[Task],
        retention_days: int
    ) -> str:
        """
        Create archive backup file before pruning.

        Args:
            tasks_to_prune: Tasks being pruned
            retention_days: Retention period used for pruning

        Returns:
            Path to created archive file

        Format:
            .ai-todo/archives/TODO_ARCHIVE_YYYY-MM-DD.md
        """
        # Create archives directory
        config_dir = Path(self.todo_path).parent / ".ai-todo"
        archives_dir = config_dir / "archives"
        archives_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y-%m-%d")
        archive_file = archives_dir / f"TODO_ARCHIVE_{timestamp}.md"

        # Handle filename conflicts
        counter = 1
        while archive_file.exists():
            archive_file = archives_dir / f"TODO_ARCHIVE_{timestamp}_{counter}.md"
            counter += 1

        # Count tasks and subtasks
        root_tasks = [t for t in tasks_to_prune if "." not in t.id]
        subtasks = [t for t in tasks_to_prune if "." in t.id]

        # Generate archive content
        content = f"""# Archived Tasks - Pruned on {timestamp}

This file contains tasks pruned from TODO.md on {timestamp}.
These tasks were archived more than {retention_days} days ago.

**Prune Statistics:**
- Tasks Pruned: {len(root_tasks)} root tasks
- Subtasks Pruned: {len(subtasks)} subtasks
- Total: {len(tasks_to_prune)} items
- Retention Period: {retention_days} days
- Original TODO.md: {self.todo_path}

## Pruned Tasks

"""

        # Add tasks in standard TODO.md format
        for task in tasks_to_prune:
            # Skip subtasks - they'll be included under parent
            if "." in task.id:
                continue

            # Add root task
            content += self._format_task(task)

            # Add subtasks
            task_subtasks = [t for t in tasks_to_prune if t.id.startswith(f"{task.id}.") and t.id.count(".") == task.id.count(".") + 1]
            for subtask in sorted(task_subtasks, key=lambda t: t.id):
                content += self._format_task(subtask)

            content += "\n"

        # Add footer
        content += f"""---
**Prune Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Retention Period:** {retention_days} days
**Tasks Pruned:** {len(root_tasks)} tasks, {len(subtasks)} subtasks
**Original TODO.md:** {self.todo_path}
"""

        # Write archive file
        archive_file.write_text(content, encoding="utf-8")

        return str(archive_file)

    def _format_task(self, task: Task) -> str:
        """Format task for archive file (standard TODO.md format)."""
        indent = "  " * task.id.count(".")
        checkbox = "[x]"  # Archived tasks are completed
        tags = " ".join(f"`#{tag}`" for tag in sorted(task.tags)) if task.tags else ""

        line = f"{indent}- {checkbox} **#{task.id}** {task.description}"
        if tags:
            line += f" {tags}"

        # Add completion date if available
        if task.completed_at:
            date_str = task.completed_at.strftime("%Y-%m-%d")
            line += f" ({date_str})"

        line += "\n"

        # Add notes
        for note in task.notes:
            line += f"{indent}  > {note}\n"

        return line

    def prune_tasks(
        self,
        days: int = 30,
        older_than: str | None = None,
        from_task: str | None = None,
        dry_run: bool = False,
        backup: bool = True
    ) -> PruneResult:
        """
        Prune archived tasks from TODO.md.

        Args:
            days: Prune tasks older than N days (default: 30)
            older_than: Prune tasks before YYYY-MM-DD
            from_task: Prune tasks from #1 to #from_task
            dry_run: Preview without making changes
            backup: Create archive backup (default: True)

        Returns:
            PruneResult with operation details

        Algorithm:
            1. Read all tasks via FileOps
            2. Identify tasks to prune (via identify_tasks_to_prune)
            3. If dry_run, return preview result
            4. If backup, create archive backup (fail if backup fails)
            5. Remove pruned tasks from task list
            6. Write remaining tasks via FileOps
            7. Return result
        """
        # Read tasks
        tasks = self.file_ops.read_tasks()

        # Identify tasks to prune
        to_prune = self.identify_tasks_to_prune(
            tasks,
            days=days,
            older_than=older_than,
            from_task=from_task
        )

        # Count root tasks vs subtasks
        root_tasks = [t for t in to_prune if "." not in t.id]
        subtasks = [t for t in to_prune if "." in t.id]

        # Dry run - return preview
        if dry_run:
            return PruneResult(
                tasks_pruned=len(root_tasks),
                subtasks_pruned=len(subtasks),
                archive_path=None,
                dry_run=True,
                pruned_task_ids=[t.id for t in to_prune]
            )

        # No tasks to prune
        if not to_prune:
            return PruneResult(
                tasks_pruned=0,
                subtasks_pruned=0,
                archive_path=None,
                dry_run=False,
                pruned_task_ids=[]
            )

        # Create backup
        archive_path = None
        if backup:
            archive_path = self.create_archive_backup(to_prune, days)

        # Remove pruned tasks
        pruned_ids = {t.id for t in to_prune}
        remaining_tasks = [t for t in tasks if t.id not in pruned_ids]

        # Write changes via FileOps
        self.file_ops.write_tasks(remaining_tasks)

        return PruneResult(
            tasks_pruned=len(root_tasks),
            subtasks_pruned=len(subtasks),
            archive_path=archive_path,
            dry_run=False,
            pruned_task_ids=[t.id for t in to_prune]
        )
```

### 3. CLI Command

**File:** `ai_todo/cli/commands/__init__.py` (extend)

#### Function: `prune_command(...)`

**Purpose:** CLI interface for prune operation.

**Implementation:**
```python
def prune_command(
    days: int = 30,
    older_than: str | None = None,
    from_task: str | None = None,
    dry_run: bool = False,
    backup: bool = True,
    force: bool = False,
    todo_path: str = "TODO.md"
):
    """
    Prune old archived tasks from TODO.md.

    Args:
        days: Prune tasks older than N days (default: 30)
        older_than: Prune tasks before YYYY-MM-DD
        from_task: Prune tasks from #1 to #from_task
        dry_run: Preview without making changes
        backup: Create archive backup (default: True)
        force: Skip confirmation prompts
        todo_path: Path to TODO.md
    """
    from ai_todo.core.prune import PruneManager

    prune_mgr = PruneManager(todo_path)

    # Run prune (dry-run first to preview)
    preview_result = prune_mgr.prune_tasks(
        days=days,
        older_than=older_than,
        from_task=from_task,
        dry_run=True,
        backup=False
    )

    # No tasks to prune
    if preview_result.total_pruned == 0:
        print("ℹ️  No archived tasks match the prune criteria.")
        return

    # Display preview
    print(f"🔍 Found {preview_result.tasks_pruned} task(s) and {preview_result.subtasks_pruned} subtask(s) to prune")
    print(f"   Total: {preview_result.total_pruned} items")
    print("")

    # Dry run - show preview and exit
    if dry_run:
        print("📋 Tasks that would be pruned:")
        for task_id in preview_result.pruned_task_ids[:10]:  # Show first 10
            print(f"   - #{task_id}")
        if len(preview_result.pruned_task_ids) > 10:
            print(f"   ... and {len(preview_result.pruned_task_ids) - 10} more")
        print("")
        print("💡 Run without --dry-run to prune these tasks")
        return

    # Confirmation prompt (unless --force)
    if not force:
        print("⚠️  This will permanently remove these tasks from TODO.md")
        if backup:
            print("   (A backup will be created in .ai-todo/archives/)")
        response = input("\nContinue? [y/N]: ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            return

    # Perform actual prune
    print("")
    print("🔧 Pruning tasks...")

    result = prune_mgr.prune_tasks(
        days=days,
        older_than=older_than,
        from_task=from_task,
        dry_run=False,
        backup=backup
    )

    # Display result
    print(f"✅ Pruned {result.tasks_pruned} task(s) and {result.subtasks_pruned} subtask(s)")

    if result.archive_path:
        print(f"📦 Archive backup: {result.archive_path}")

    print("")
```

**CLI Integration (in `ai_todo/cli/main.py`):**
```python
# Add to argument parser
prune_parser = subparsers.add_parser(
    "prune",
    help="Prune old archived tasks"
)
prune_parser.add_argument(
    "--days",
    type=int,
    default=30,
    help="Prune tasks older than N days (default: 30)"
)
prune_parser.add_argument(
    "--older-than",
    type=str,
    help="Prune tasks before YYYY-MM-DD"
)
prune_parser.add_argument(
    "--from-task",
    type=str,
    help="Prune tasks from #1 to #ID"
)
prune_parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Preview without making changes"
)
prune_parser.add_argument(
    "--no-backup",
    action="store_true",
    help="Skip archive backup creation"
)
prune_parser.add_argument(
    "--force",
    action="store_true",
    help="Skip confirmation prompts"
)
prune_parser.set_defaults(func=prune_command_wrapper)

def prune_command_wrapper(args):
    """Wrapper to call prune_command with parsed args."""
    prune_command(
        days=args.days,
        older_than=args.older_than,
        from_task=args.from_task,
        dry_run=args.dry_run,
        backup=not args.no_backup,
        force=args.force,
        todo_path=args.todo_path
    )
```

### 4. MCP Integration

**File:** `ai_todo/mcp/server.py` (extend)

#### MCP Tool: `prune_tasks`

**Purpose:** MCP interface for prune operation (parity with CLI).

**Implementation:**
```python
@mcp.tool()
def prune_tasks(
    days: int = 30,
    older_than: str | None = None,
    from_task: str | None = None,
    dry_run: bool = False,
    backup: bool = True,
) -> dict:
    """
    Prune old archived tasks from TODO.md.

    Args:
        days: Prune tasks older than N days (default: 30)
        older_than: Prune tasks before YYYY-MM-DD (format: YYYY-MM-DD)
        from_task: Prune tasks from #1 to #ID (numeric task ID)
        dry_run: Preview without making changes (default: False)
        backup: Create archive backup (default: True)

    Returns:
        dict with keys:
            - tasks_pruned: Number of root tasks pruned
            - subtasks_pruned: Number of subtasks pruned
            - total_pruned: Total items pruned
            - archive_path: Path to backup archive (if created)
            - dry_run: Whether this was a dry run
            - pruned_task_ids: List of task IDs pruned (preview in dry run)

    Examples:
        # Prune tasks older than 30 days (default)
        prune_tasks()

        # Prune tasks older than 60 days
        prune_tasks(days=60)

        # Prune tasks before specific date
        prune_tasks(older_than="2025-10-01")

        # Prune tasks from #1 to #50
        prune_tasks(from_task="50")

        # Preview what would be pruned
        prune_tasks(dry_run=True)

        # Prune without backup (not recommended)
        prune_tasks(backup=False)
    """
    from ai_todo.core.prune import PruneManager

    todo_path = get_todo_path()
    prune_mgr = PruneManager(todo_path)

    try:
        result = prune_mgr.prune_tasks(
            days=days,
            older_than=older_than,
            from_task=from_task,
            dry_run=dry_run,
            backup=backup
        )

        return {
            "tasks_pruned": result.tasks_pruned,
            "subtasks_pruned": result.subtasks_pruned,
            "total_pruned": result.total_pruned,
            "archive_path": result.archive_path,
            "dry_run": result.dry_run,
            "pruned_task_ids": result.pruned_task_ids
        }
    except Exception as e:
        raise ValueError(f"Prune operation failed: {e}")
```

## Edge Cases & Error Handling

### 1. No Archived Tasks
**Scenario:** TODO.md has no archived tasks.
**Behavior:** Display message "No archived tasks found. Nothing to prune." and exit gracefully.

### 2. No Git Repository
**Scenario:** TODO.md is not in a git repository.
**Behavior:**
- Log warning: "Git history unavailable, using completion dates"
- Fall back to parsing completion dates from task metadata
- Continue operation normally

### 3. Tasks Without Archive Dates
**Scenario:** Archived task has no parseable date (neither git log nor metadata).
**Behavior:**
- Skip these tasks
- Log warning: "Skipped N tasks without archive dates"
- Continue with remaining tasks

### 4. All Tasks Match Criteria
**Scenario:** Prune would remove all archived tasks.
**Behavior:**
- Display count of tasks to prune
- Require explicit confirmation (even with --force, show warning)
- Proceed if confirmed

### 5. Backup Creation Fails
**Scenario:** Unable to create archive backup file (disk full, permissions, etc.).
**Behavior:**
- **ABORT** prune operation
- Display error: "Failed to create backup archive: [error]"
- Do NOT modify TODO.md
- Exit with error code 1

### 6. FileOps Tamper Detection
**Scenario:** TODO.md has been modified externally (tamper detected).
**Behavior:**
- FileOps will raise exception
- Display error: "TODO.md has been modified externally. Run --accept-tamper first."
- Exit with error code 1

### 7. Invalid Date Format (older_than)
**Scenario:** User provides invalid date format.
**Behavior:**
- Validate date format before running
- Display error: "Invalid date format. Use YYYY-MM-DD."
- Exit with error code 1

### 8. Invalid Task ID (from_task)
**Scenario:** User provides non-numeric task ID.
**Behavior:**
- Validate task ID format before running
- Display error: "Invalid task ID. Must be numeric."
- Exit with error code 1

### 9. Empty Prune Result
**Scenario:** No tasks match the prune criteria.
**Behavior:**
- Display message: "No archived tasks older than N days found."
- No backup created, no changes made
- Exit successfully

### 10. Interrupted Operation
**Scenario:** User presses Ctrl+C during prune.
**Behavior:**
- Catch KeyboardInterrupt
- Display: "Operation cancelled by user."
- FileOps ensures atomicity (changes are committed only at end)
- Exit gracefully

## Backwards Compatibility

### 1. TODO.md Format
**Guarantee:** Prune does not change TODO.md format.
- Uses FileOps read/write exclusively
- Preserves all TODO.md sections and formatting
- Only removes archived tasks (minimal change)

### 2. Existing Commands
**Guarantee:** No existing commands are modified.
- Archive command unchanged
- Restore command unchanged
- All existing CLI/MCP tools work as before

### 3. Configuration
**Guarantee:** No new configuration required.
- Prune uses default `.ai-todo/` directory structure
- Creates `archives/` subdirectory automatically
- No config file changes needed

### 4. Git History
**Guarantee:** Git history is preserved.
- Prune operation creates a git-committable change
- Archive backups are version-controlled (if committed)
- No history rewriting or destructive git operations

## Testing Strategy

### Unit Tests (`tests/unit/test_prune.py`)

#### Test: Git History Parsing
```python
def test_get_task_archive_date_from_git():
    """Test git log parsing for archive date."""
    # Setup: Create mock git log output
    # Test: Call get_task_archive_date()
    # Assert: Correct datetime returned

def test_get_task_archive_date_fallback():
    """Test fallback to metadata parsing."""
    # Setup: Mock no git history
    # Test: Call get_task_archive_date()
    # Assert: Falls back to metadata parsing

def test_parse_archive_date_from_metadata():
    """Test metadata date parsing."""
    # Setup: Create archived task with (2026-01-28)
    # Test: Parse date
    # Assert: Correct datetime returned
```

#### Test: Task Filtering
```python
def test_filter_by_age():
    """Test age-based filtering."""
    # Setup: Create tasks with various archive dates
    # Test: Filter with 30-day cutoff
    # Assert: Only old tasks returned

def test_filter_by_task_range():
    """Test range-based filtering."""
    # Setup: Create tasks #1-#100
    # Test: Filter with from_task="50"
    # Assert: Tasks #1-#50 returned

def test_include_subtasks():
    """Test subtask inclusion."""
    # Setup: Parent task #10 with subtasks #10.1, #10.2
    # Test: Filter includes parent
    # Assert: All subtasks also included
```

#### Test: Archive Backup
```python
def test_create_archive_backup():
    """Test archive backup creation."""
    # Setup: Tasks to prune
    # Test: create_archive_backup()
    # Assert: File created with correct format

def test_archive_backup_filename_collision():
    """Test handling of filename conflicts."""
    # Setup: Existing archive file
    # Test: Create another on same date
    # Assert: Incremented filename used
```

### Integration Tests (`tests/integration/test_prune.py`)

#### Test: End-to-End CLI Prune
```python
def test_prune_cli_default():
    """Test CLI prune with defaults."""
    # Setup: TODO.md with old archived tasks
    # Run: ./todo.ai prune --force
    # Assert: Tasks pruned, backup created

def test_prune_cli_dry_run():
    """Test CLI dry-run mode."""
    # Setup: TODO.md with old archived tasks
    # Run: ./todo.ai prune --dry-run
    # Assert: Preview shown, no changes made

def test_prune_cli_custom_days():
    """Test CLI with --days option."""
    # Setup: TODO.md with tasks of various ages
    # Run: ./todo.ai prune --days 60 --force
    # Assert: Only tasks older than 60 days pruned
```

#### Test: End-to-End MCP Prune
```python
def test_prune_mcp_default():
    """Test MCP prune_tasks with defaults."""
    # Setup: TODO.md with old archived tasks
    # Call: prune_tasks()
    # Assert: Tasks pruned, result correct

def test_prune_mcp_dry_run():
    """Test MCP dry-run mode."""
    # Setup: TODO.md with old archived tasks
    # Call: prune_tasks(dry_run=True)
    # Assert: Preview returned, no changes made
```

#### Test: MCP-CLI Parity
```python
def test_mcp_cli_parity():
    """Test that MCP and CLI produce identical results."""
    # Setup: TODO.md with old archived tasks
    # Run: CLI prune in temp directory A
    # Run: MCP prune in temp directory B
    # Assert: Both directories have identical TODO.md and archive files
```

### Edge Case Tests
```python
def test_no_archived_tasks():
    """Test prune with no archived tasks."""
    # Setup: TODO.md with only active tasks
    # Run: Prune command
    # Assert: Message displayed, no changes

def test_backup_creation_failure():
    """Test handling of backup failure."""
    # Setup: Mock backup creation to fail
    # Run: Prune command
    # Assert: Operation aborted, TODO.md unchanged

def test_tamper_detection():
    """Test handling of tamper detection."""
    # Setup: Modify TODO.md externally
    # Run: Prune command
    # Assert: Error displayed, operation aborted
```

## Performance Considerations

### 1. Git Log Parsing
**Concern:** Git log parsing could be slow for large repositories.

**Mitigation:**
- Limit git log search to TODO.md file only (`-- TODO.md`)
- Use grep patterns to filter commits (`--grep`)
- Cache results for multiple task lookups in same operation
- Estimated performance: < 100ms for typical repository

### 2. Large Archive Sections
**Concern:** TODO.md with 1000+ archived tasks.

**Mitigation:**
- FileOps already handles large files efficiently
- Filtering is O(n) with n = number of tasks
- No complex algorithms or nested loops
- Estimated performance: < 1 second for 1000 tasks

### 3. Backup File Creation
**Concern:** Writing large archive backup files.

**Mitigation:**
- Single write operation (not incremental)
- Archive files are smaller than full TODO.md
- Filesystem buffering handles write efficiency
- Estimated performance: < 500ms for 100 tasks

## Security Considerations

### 1. File Operations
**Concern:** Malicious file path injection.

**Mitigation:**
- Use FileOps exclusively (validated paths)
- Archive directory is fixed (`.ai-todo/archives/`)
- No user-controlled file paths

### 2. Git Command Injection
**Concern:** Command injection via task IDs.

**Mitigation:**
- Task IDs are validated (numeric only)
- Use subprocess with array args (not shell=True)
- Escape special characters in grep patterns

### 3. Data Loss
**Concern:** Accidental deletion of tasks.

**Mitigation:**
- Backup created by default (requires --no-backup to disable)
- Confirmation prompts (requires --force to skip)
- Dry-run mode for previews
- Archive backups are version-controlled

## Documentation Requirements

### 1. CLI Help Text
```bash
$ ./todo.ai prune --help

Prune old archived tasks from TODO.md.

Usage:
  ./todo.ai prune [OPTIONS]

Options:
  --days N              Prune tasks older than N days (default: 30)
  --older-than DATE     Prune tasks before DATE (format: YYYY-MM-DD)
  --from-task ID        Prune tasks from #1 to #ID (numeric)
  --dry-run             Preview without making changes
  --no-backup           Skip archive backup creation (not recommended)
  --force               Skip confirmation prompts

Examples:
  # Prune tasks older than 30 days (default)
  ./todo.ai prune

  # Preview what would be pruned
  ./todo.ai prune --dry-run

  # Prune tasks older than 60 days
  ./todo.ai prune --days 60

  # Prune tasks before specific date
  ./todo.ai prune --older-than 2025-10-01

  # Prune tasks from #1 to #50
  ./todo.ai prune --from-task 50

Backup Location:
  Archive backups are saved to .ai-todo/archives/TODO_ARCHIVE_YYYY-MM-DD.md

Notes:
  - By default, a backup is created before pruning
  - Prune only affects tasks in the "Archived Tasks" section
  - Git history is used to determine archive dates when available
```

### 2. MCP Tool Documentation
**File:** `docs/mcp.md` (extend)

```markdown
## prune_tasks

Prune old archived tasks from TODO.md.

**Parameters:**
- `days` (int, optional): Prune tasks older than N days. Default: 30.
- `older_than` (str, optional): Prune tasks before YYYY-MM-DD.
- `from_task` (str, optional): Prune tasks from #1 to #ID (numeric).
- `dry_run` (bool, optional): Preview without making changes. Default: False.
- `backup` (bool, optional): Create archive backup. Default: True.

**Returns:**
```json
{
  "tasks_pruned": 5,
  "subtasks_pruned": 12,
  "total_pruned": 17,
  "archive_path": ".ai-todo/archives/TODO_ARCHIVE_2026-01-28.md",
  "dry_run": false,
  "pruned_task_ids": ["1", "2", "3", "4", "5"]
}
```

**Examples:**
```javascript
// Prune tasks older than 30 days (default)
const result = await prune_tasks();

// Preview what would be pruned
const preview = await prune_tasks({ dry_run: true });

// Prune tasks older than 60 days
const result = await prune_tasks({ days: 60 });

// Prune tasks before specific date
const result = await prune_tasks({ older_than: "2025-10-01" });

// Prune tasks from #1 to #50
const result = await prune_tasks({ from_task: "50" });
```

**Notes:**
- Archive backups are created by default in `.ai-todo/archives/`
- Only tasks in "Archived Tasks" section are affected
- Git history is used for date detection when available
```

### 3. README Examples
**File:** `README.md` (extend)

```markdown
### Prune Old Archived Tasks

Remove old archived tasks to keep TODO.md clean:

```bash
# Prune tasks older than 30 days (default)
./todo.ai prune

# Preview what would be pruned
./todo.ai prune --dry-run

# Prune tasks older than 60 days
./todo.ai prune --days 60

# Prune tasks before specific date
./todo.ai prune --older-than 2025-10-01

# Prune tasks from #1 to #50
./todo.ai prune --from-task 50
```

Archive backups are automatically created in `.ai-todo/archives/` before pruning.
```

### 4. CHANGELOG.md
```markdown
## [Unreleased]

### Added
- `prune` command to remove old archived tasks based on git history
- Archive backup system in `.ai-todo/archives/`
- MCP `prune_tasks` tool with CLI parity
- Git history analysis for accurate archive date detection
- Dry-run mode for safe preview of prune operations
```

## Implementation Plan

### Phase 1: Git History Analysis (Priority: P0)
**Time Estimate:** 2-3 hours

1. Extend `ai_todo/utils/git.py` with:
   - `get_task_archive_date(task_id, todo_path) -> datetime | None`
   - `parse_archive_date_from_metadata(task_id, todo_path) -> datetime | None`
   - `GitLogEntry` dataclass
   - `get_git_log_entries(task_id, todo_path) -> list[GitLogEntry]`

2. Write unit tests:
   - Test git log parsing
   - Test metadata fallback
   - Test edge cases (no git, invalid dates, etc.)

3. Manual testing:
   - Test with real TODO.md and git history
   - Verify date accuracy

**Deliverables:**
- Extended `git.py` with 4 new functions
- 10+ unit tests with 100% coverage
- Verified accuracy with real data

### Phase 2: Prune Core Logic (Priority: P0)
**Time Estimate:** 4-5 hours

1. Create `ai_todo/core/prune.py` with:
   - `PruneResult` dataclass
   - `PruneManager` class
   - All filtering methods
   - Archive backup creation
   - Main `prune_tasks()` method

2. Write unit tests:
   - Test task filtering (age, range, date)
   - Test subtask inclusion
   - Test archive backup creation
   - Test FileOps integration
   - Test edge cases

3. Integration testing:
   - Test with real TODO.md files
   - Verify backup format
   - Verify FileOps atomicity

**Deliverables:**
- Complete `prune.py` module (300-400 lines)
- 20+ unit tests with 100% coverage
- Integration tests passing

### Phase 3: CLI Command (Priority: P1)
**Time Estimate:** 2-3 hours

1. Add `prune_command()` to `ai_todo/cli/commands/__init__.py`
   - Argument handling
   - Progress messages
   - Confirmation prompts
   - Error handling

2. Integrate with `ai_todo/cli/main.py`:
   - Add argument parser
   - Add command registration
   - Add help text

3. Write CLI tests:
   - End-to-end CLI prune
   - Dry-run mode
   - Custom options
   - Error scenarios

**Deliverables:**
- CLI command implementation
- Argument parser integration
- 10+ CLI integration tests
- Help text and examples

### Phase 4: MCP Integration (Priority: P1)
**Time Estimate:** 2-3 hours

1. Add `prune_tasks()` tool to `ai_todo/mcp/server.py`
   - MCP tool decorator
   - Parameter validation
   - Result formatting
   - Error handling

2. Write MCP tests:
   - End-to-end MCP prune
   - Dry-run mode
   - Custom options
   - MCP-CLI parity

**Deliverables:**
- MCP tool implementation
- 10+ MCP integration tests
- Parity tests passing

### Phase 5: Testing & Verification (Priority: P0)
**Time Estimate:** 3-4 hours

1. Run full test suite:
   - All unit tests
   - All integration tests
   - Coverage report (target: 95%+)

2. Manual testing:
   - Real-world scenarios
   - Edge cases
   - Performance testing (1000+ tasks)

3. Linting:
   - Run `uv run ruff check`
   - Fix all issues

**Deliverables:**
- 95%+ code coverage
- All tests passing
- Zero lint errors
- Manual test report

### Phase 6: Documentation (Priority: P2)
**Time Estimate:** 2-3 hours

1. Update documentation:
   - `docs/cli.md` - CLI command
   - `docs/mcp.md` - MCP tool
   - `README.md` - Examples
   - `CHANGELOG.md` - Entry
   - Inline help text

2. Create examples:
   - `docs/examples/prune_usage.md`
   - Common scenarios
   - Best practices

**Deliverables:**
- Complete documentation
- Examples file
- Updated changelog

## Approval Checklist

Before proceeding to implementation, confirm:

- [ ] Design approach is sound (git log + fallback)
- [ ] FileOps integration is correct
- [ ] Edge cases are covered
- [ ] Error handling is comprehensive
- [ ] Testing strategy is sufficient
- [ ] Documentation plan is complete
- [ ] Performance is acceptable
- [ ] Security considerations addressed
- [ ] Backwards compatibility maintained
- [ ] MCP-CLI parity ensured

## References

- **Analysis Document:** `docs/design/prune_function_analysis.md`
- **Original Task:** #129 (TODO.md lines 105-108)
- **Linear Issue:** https://linear.app/fxstein/issue/AIT-2
- **Specification:** `docs/development/TODO_TOOL_IMPROVEMENTS.md` (section 3.4)
- **FileOps Class:** `ai_todo/core/file_ops.py`
- **Git Utilities:** `ai_todo/utils/git.py`
- **Archive Command:** `ai_todo/cli/commands/__init__.py` (lines 401-433)

---

**Design Completed:** 2026-01-28
**Designer:** AI Agent (Cursor)
**Status:** Awaiting Review
**Next Step:** Human approval before implementation
