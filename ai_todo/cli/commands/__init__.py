import os
import re
import subprocess
from pathlib import Path

from ai_todo.cli.config_ops import (
    detect_coordination_command,
    list_mode_backups_command,
    rollback_mode_command,
    setup_coordination_command,
    setup_wizard_command,
    show_config_command,
    switch_mode_command,
)
from ai_todo.cli.system_ops import (
    create_backup,
    list_backups_command,
    rollback_command,
    update_command,
    view_log_command,
)
from ai_todo.cli.utility_ops import (
    report_bug_command,
    uninstall_command,
    version_command,
)
from ai_todo.core.config import Config
from ai_todo.core.coordination import CoordinationManager
from ai_todo.core.file_ops import FileOps
from ai_todo.core.task import Task, TaskManager, TaskStatus

# Global file_ops cache to preserve relationships across operations
_file_ops_cache: dict[str, FileOps] = {}


def get_manager(todo_path: str = "TODO.md") -> TaskManager:
    """Initialize core components and return TaskManager."""
    file_ops = FileOps(todo_path)
    tasks = file_ops.read_tasks()
    # Cache file_ops to preserve relationships
    _file_ops_cache[todo_path] = file_ops
    return TaskManager(tasks)


def save_changes(manager: TaskManager, todo_path: str = "TODO.md") -> None:
    """Save tasks back to file, preserving relationships."""
    # Use cached file_ops if available to preserve relationships
    file_ops = _file_ops_cache.get(todo_path)
    if file_ops is None:
        file_ops = FileOps(todo_path)
        file_ops.read_tasks()  # Read to get relationships and original blank line state
        # Cache it for future operations
        _file_ops_cache[todo_path] = file_ops
    else:
        # Re-read to get latest file state (in case file was modified externally)
        # Phase 13: Structure is now preserved via snapshot, no state restoration needed
        file_ops.read_tasks()
    tasks = manager.list_tasks()
    # Phase 13: Structure preservation is handled automatically by snapshot
    file_ops.write_tasks(tasks)


def _resolve_git_root(cwd: str) -> str | None:
    try:
        superproject = subprocess.run(
            ["git", "rev-parse", "--show-superproject-working-tree"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        if superproject.returncode == 0:
            candidate = superproject.stdout.strip()
            if candidate:
                return candidate
        gitdir = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        if gitdir.returncode == 0:
            gitdir_path = gitdir.stdout.strip()
            if gitdir_path:
                gitdir_real = (Path(cwd) / gitdir_path).resolve()
                if gitdir_real.is_file():
                    try:
                        gitdir_line = gitdir_real.read_text().splitlines()[0].strip()
                    except (OSError, IndexError):
                        gitdir_line = ""
                    if gitdir_line.startswith("gitdir:"):
                        gitdir_value = gitdir_line.split("gitdir:", 1)[1].strip()
                        gitdir_real = (Path(cwd) / gitdir_value).resolve()
                marker = str(Path(".git") / "modules") + os.sep
                gitdir_real_str = str(gitdir_real)
                if marker in gitdir_real_str:
                    super_root = gitdir_real_str.split(marker, 1)[0].rstrip("/")
                    if super_root:
                        return super_root
        toplevel = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        if toplevel.returncode == 0:
            candidate = toplevel.stdout.strip()
            if candidate:
                return candidate
    except OSError:
        return None
    return None


def _resolve_root(
    cwd: str, root_override: str | None = None, env_override: str | None = None
) -> tuple[str, str]:
    if root_override:
        return str(Path(root_override).resolve()), "--root"
    if env_override:
        return str(Path(env_override).resolve()), "env"
    git_root = _resolve_git_root(cwd)
    if git_root:
        return git_root, "git"
    return cwd, "cwd"


def show_root_command(root_override: str | None = None) -> None:
    cwd = os.getcwd()
    env_override = os.getenv("TODO_AI_ROOT")
    root, source = _resolve_root(cwd, root_override=root_override, env_override=env_override)
    print(f"Resolved root: {root} (source: {source})")


def add_command(description: str, tags: list[str], todo_path: str = "TODO.md"):
    """Add a new task."""
    # Use cached file_ops if available, otherwise create new one
    file_ops = _file_ops_cache.get(todo_path)
    if file_ops is None:
        file_ops = FileOps(todo_path)
        file_ops.read_tasks()
        _file_ops_cache[todo_path] = file_ops
    else:
        # Re-read to get latest state
        file_ops.read_tasks()

    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)

    # ID Generation
    config_dir = Path(todo_path).parent / ".ai-todo"
    if not config_dir.exists():
        config_dir = Path(todo_path).parent / ".todo.ai"
    config_path = config_dir / "config.yaml"
    config = Config(str(config_path))
    coord_manager = CoordinationManager(config)
    new_id = coord_manager.get_next_task_id(manager, file_ops)

    # Create task
    task = manager.add_task(description, tags, task_id=new_id)

    # CRITICAL: New tasks must appear at the TOP of the Tasks section
    # Reorder tasks to put newly added task first
    all_tasks = manager.list_tasks()
    reordered_tasks = [task] + [t for t in all_tasks if t.id != task.id]

    # Phase 14: Structure preservation is handled automatically by snapshot
    # No manual file editing needed
    file_ops.write_tasks(reordered_tasks)

    # Update serial file with new task ID
    # Extract numeric part from task ID
    task_id_num = new_id
    if "-" in task_id_num:
        task_id_num = task_id_num.split("-")[-1]
    if "." in task_id_num:
        task_id_num = task_id_num.split(".")[0]
    try:
        serial_value = int(task_id_num)
        file_ops.set_serial(serial_value)
    except ValueError:
        pass

    # Format output with tags
    tag_str = " ".join([f"`#{tag}`" for tag in sorted(task.tags)]) if task.tags else ""
    output = f"Added: #{task.id} {task.description}"
    if tag_str:
        output += f" {tag_str}"
    print(output)


def _insert_subtask_after_parent(tasks: list[Task], parent_id: str, subtask: Task) -> list[Task]:
    """Insert a subtask immediately after its parent (newest on top)."""
    parent_index = None

    for index, task in enumerate(tasks):
        if task.id == parent_id:
            parent_index = index
            break  # Found parent, stop searching

    if parent_index is not None:
        insert_at = parent_index + 1
    else:
        insert_at = len(tasks)

    return tasks[:insert_at] + [subtask] + tasks[insert_at:]


def add_subtask_command(
    parent_id: str, description: str, tags: list[str], todo_path: str = "TODO.md"
):
    """Add a subtask to an existing task."""
    file_ops = _file_ops_cache.get(todo_path)
    if file_ops is None:
        file_ops = FileOps(todo_path)
        tasks = file_ops.read_tasks()
        _file_ops_cache[todo_path] = file_ops
    else:
        tasks = file_ops.read_tasks()

    manager = TaskManager(tasks)
    try:
        parent = manager.get_task(parent_id)
        if not parent:
            raise ValueError(f"Parent task {parent_id} not found")

        # Check nesting depth (allow 3 levels: task → subtask → sub-subtask)
        if parent.id.count(".") >= 2:
            raise ValueError("Maximum nesting depth is 3 levels (task.subtask.sub-subtask)")

        config_dir = Path(todo_path).parent / ".ai-todo"
        if not config_dir.exists():
            config_dir = Path(todo_path).parent / ".todo.ai"
        config_path = config_dir / "config.yaml"
        config = Config(str(config_path))
        coord_manager = CoordinationManager(config)
        subtask_id = coord_manager.get_next_subtask_id(parent_id, manager)

        subtask = manager.add_subtask(parent_id, description, tags, task_id=subtask_id)
        ordered_tasks = _insert_subtask_after_parent(tasks, parent_id, subtask)
        file_ops.write_tasks(ordered_tasks)

        # Format output with tags
        tag_str = " ".join([f"`#{tag}`" for tag in sorted(subtask.tags)]) if subtask.tags else ""
        output = f"Added subtask: #{subtask.id} {subtask.description}"
        if tag_str:
            output += f" {tag_str}"
        print(output)
    except ValueError as e:
        print(f"Error: {e}")


def list_command(
    tag: str | None = None,
    incomplete_only: bool = False,
    parents_only: bool = False,
    has_subtasks: bool = False,
    todo_path: str = "TODO.md",
):
    """List tasks with optional filters."""
    manager = get_manager(todo_path)
    tasks = manager.list_tasks()

    # Filter by status (only pending tasks)
    if incomplete_only:
        tasks = [t for t in tasks if t.status.value == "pending"]

    # Filter by tag
    if tag:
        tasks = [t for t in tasks if tag in (t.tags or [])]

    # Filter by subtask presence
    if has_subtasks:
        subtask_ids = {t.id.rsplit(".", 1)[0] for t in tasks if "." in t.id}
        tasks = [t for t in tasks if t.id in subtask_ids]

    # Filter to only parent tasks
    if parents_only:
        tasks = [t for t in tasks if "." not in t.id]

    # Display tasks
    for task in tasks:
        checkbox = "[x]" if task.status.value != "pending" else "[ ]"
        indent = "  " * (task.id.count("."))
        tag_str = " ".join([f"`#{tag}`" for tag in sorted(task.tags)]) if task.tags else ""
        description = task.description
        if tag_str:
            description = f"{description} {tag_str}".strip()
        print(f"{indent}- {checkbox} **#{task.id}** {description}")


def complete_command(task_ids: list[str], with_subtasks: bool = False, todo_path: str = "TODO.md"):
    """Mark task(s) as completed."""
    manager = get_manager(todo_path)

    # Expand task IDs (ranges, with-subtasks, etc.)
    expanded_ids = expand_task_ids(task_ids, with_subtasks, todo_path)

    completed_tasks = []
    for task_id in expanded_ids:
        try:
            task = manager.complete_task(task_id)
            if task:
                completed_tasks.append(task)
        except ValueError as e:
            print(f"Error: {e}")

    if completed_tasks:
        save_changes(manager, todo_path)
        # Output format: "Completed: #X Task Description" for each task
        for task in completed_tasks:
            print(f"Completed: #{task.id} {task.description}")


def modify_command(
    task_id: str, description: str, tags: list[str] | None = None, todo_path: str = "TODO.md"
):
    """Modify a task's description and/or tags."""
    manager = get_manager(todo_path)
    try:
        # Get existing task to preserve tags if not explicitly changing them
        existing_task = manager.get_task(task_id)
        if not existing_task:
            raise ValueError(f"Task {task_id} not found")

        # Extract tags from description if they're in backticks (format: `#tag`)
        tag_pattern = re.compile(r"`#([a-zA-Z0-9_-]+)`")
        found_tags = tag_pattern.findall(description)

        # Remove tags from description
        description = tag_pattern.sub("", description).strip()

        # Combine tags from description and explicit tags argument
        # CRITICAL: If no new tags provided, preserve existing tags
        if tags:
            all_tags: list[str] | None = list(set(found_tags + tags))
        elif found_tags:
            all_tags = found_tags
        else:
            # No new tags - preserve existing tags
            all_tags = list(existing_task.tags) if existing_task.tags else None

        task = manager.modify_task(task_id, description, all_tags)
        save_changes(manager, todo_path)

        # Format output with tags
        tag_str = " ".join([f"`#{tag}`" for tag in sorted(task.tags)]) if task.tags else ""
        output = f"Modified: #{task.id} {task.description}"
        if tag_str:
            output += f" {tag_str}"
        print(output)
    except ValueError as e:
        print(f"Error: {e}")


def start_command(task_id: str, todo_path: str = "TODO.md"):
    """Mark a task as in progress."""
    manager = get_manager(todo_path)
    try:
        task = manager.start_task(task_id)
        save_changes(manager, todo_path)
        print(f"Started task #{task.id}: {task.description}")
    except ValueError as e:
        print(f"Error: {e}")


def stop_command(task_id: str, todo_path: str = "TODO.md"):
    """Stop progress on a task."""
    manager = get_manager(todo_path)
    try:
        task = manager.stop_task(task_id)
        save_changes(manager, todo_path)
        print(f"Stopped task #{task.id}: {task.description}")
    except ValueError as e:
        print(f"Error: {e}")


def delete_command(task_ids: list[str], with_subtasks: bool = True, todo_path: str = "TODO.md"):
    """Soft delete task(s) to Deleted section (includes subtasks by default)."""
    manager = get_manager(todo_path)

    # Expand task IDs
    expanded_ids = expand_task_ids(task_ids, with_subtasks, todo_path)

    deleted_count = 0
    for task_id in expanded_ids:
        try:
            task = manager.delete_task(task_id)
            if task:
                deleted_count += 1
        except ValueError as e:
            print(f"Error: {e}")

    if deleted_count > 0:
        save_changes(manager, todo_path)
        print(f"Deleted {deleted_count} task(s)")

        # Auto-run empty trash after deletion (silent)
        try:
            from ai_todo.core.empty_trash import EmptyTrashManager

            trash_mgr = EmptyTrashManager(todo_path)
            trash_mgr.empty_trash(dry_run=False)
            # Silent operation - FileOps handles logging automatically
        except Exception:
            # Fail silently - don't block delete operation
            pass


def archive_command(
    task_ids: list[str],
    reason: str | None = None,
    with_subtasks: bool = True,  # Default to True for archive
    todo_path: str = "TODO.md",
):
    """Move task(s) to Archived Tasks section."""
    manager = get_manager(todo_path)

    # Note: Archive cooldown is now handled session-based in MCP server (server.py)
    # The file-based approach was broken because completed_at is set to datetime.now()
    # when parsing, not the actual completion time.

    # Expand task IDs (with subtasks by default)
    expanded_ids = expand_task_ids(task_ids, with_subtasks, todo_path)

    archived_count = 0
    # Process in reverse order so parent ends up on top (newest) in Archived Tasks
    for task_id in reversed(expanded_ids):
        try:
            task = manager.archive_task(task_id)
            if task and reason:
                # Add reason as note
                manager.add_note_to_task(task_id, f"Reason: {reason}")
            if task:
                archived_count += 1
        except ValueError as e:
            print(f"Error: {e}")

    if archived_count > 0:
        save_changes(manager, todo_path)
        print(f"Archived {archived_count} task(s)")


def restore_command(task_ids: list[str], todo_path: str = "TODO.md"):
    """Restore task(s) from Deleted or Archived Tasks to active Tasks.

    Args:
        task_ids: List of task IDs to restore (1 to n items)
        todo_path: Path to TODO.md file
    """
    restored_count = 0
    for task_id in task_ids:
        try:
            _restore_single_task(task_id, todo_path)
            restored_count += 1
        except ValueError as e:
            print(f"Error restoring {task_id}: {e}")

    if restored_count == 0 and len(task_ids) > 0:
        import sys

        sys.exit(1)


def _restore_single_task(task_id: str, todo_path: str = "TODO.md"):
    """Restore a single task from Deleted or Archived Tasks to active Tasks."""
    manager = get_manager(todo_path)

    # Read file state BEFORE restore
    file_ops = FileOps(todo_path)
    file_ops.read_tasks()

    task = manager.restore_task(task_id)

    # CRITICAL: Positioning depends on whether this is a root task or subtask
    all_tasks = manager.list_tasks()

    # Check if this is a subtask (contains a dot in the ID)
    if "." in task_id:
        # Subtask: Insert after parent
        parent_id = task_id.rsplit(".", 1)[0]
        tasks_without_restored = [t for t in all_tasks if t.id != task.id]

        # Find parent index
        parent_index = -1
        for i, t in enumerate(tasks_without_restored):
            if t.id == parent_id:
                parent_index = i
                break

        if parent_index != -1:
            # Insert after parent
            reordered_tasks = (
                tasks_without_restored[: parent_index + 1]
                + [task]
                + tasks_without_restored[parent_index + 1 :]
            )
        else:
            # Parent not found, put at top as fallback
            reordered_tasks = [task] + tasks_without_restored
    else:
        # Root task: Put at the TOP of the Tasks section
        reordered_tasks = [task] + [t for t in all_tasks if t.id != task.id]

    # Phase 14: Structure preservation is handled automatically by snapshot
    # No manual file editing needed
    file_ops.write_tasks(reordered_tasks)

    print(f"Restored task #{task.id} to Tasks section")

    # Idempotent/Self-healing restore: Check for missing subtasks and restore them
    # This handles cases where a previous restore failed or was incomplete
    subtasks = manager.get_subtasks(task_id)
    restored_subtasks = []
    for subtask in subtasks:
        # Check if subtask is "missing" (not in Tasks section)
        # A subtask is missing if it is ARCHIVED or DELETED
        if subtask.status in (TaskStatus.ARCHIVED, TaskStatus.DELETED):
            subtask.restore()
            restored_subtasks.append(subtask)

    if restored_subtasks:
        # Re-write tasks to save restored subtasks
        # CRITICAL: Use reordered_tasks (with parent at top), not a fresh fetch
        # If we re-fetch from manager, we lose the top position!

        # 1. Remove restored subtasks from their current position in reordered_tasks
        tasks_without_subtasks = [t for t in reordered_tasks if t not in restored_subtasks]

        # 2. Find parent index
        parent_index = -1
        for i, t in enumerate(tasks_without_subtasks):
            if t.id == task_id:
                parent_index = i
                break

        # 3. Insert subtasks after parent
        if parent_index != -1:
            final_tasks = (
                tasks_without_subtasks[: parent_index + 1]
                + sorted(
                    restored_subtasks,
                    key=lambda t: [int(x) for x in t.id.split(".")],
                    reverse=True,
                )
                + tasks_without_subtasks[parent_index + 1 :]
            )
            file_ops.write_tasks(final_tasks)
            print(f"  Also restored {len(restored_subtasks)} subtask(s)")


def undo_command(task_id: str, todo_path: str = "TODO.md"):
    """Reopen (undo) a completed task."""
    manager = get_manager(todo_path)
    try:
        task = manager.undo_task(task_id)
        save_changes(manager, todo_path)
        print(f"Reopened task #{task.id}")
    except ValueError as e:
        print(f"Error: {e}")


def note_command(task_id: str, note_text: str, todo_path: str = "TODO.md"):
    """Add a note to a task."""
    manager = get_manager(todo_path)
    try:
        task = manager.add_note_to_task(task_id, note_text)
        save_changes(manager, todo_path)
        print(f"Added note to task #{task.id}")
    except ValueError as e:
        print(f"Error: {e}")


def delete_note_command(task_id: str, todo_path: str = "TODO.md"):
    """Delete all notes from a task."""
    manager = get_manager(todo_path)
    try:
        task = manager.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        if not task.notes:
            print(f"Task #{task_id} has no notes to delete")
            return

        manager.delete_notes_from_task(task_id)
        save_changes(manager, todo_path)
        print(f"Deleted notes from task #{task_id}")
    except ValueError as e:
        print(f"Error: {e}")


def update_note_command(task_id: str, new_note_text: str, todo_path: str = "TODO.md"):
    """Replace all notes for a task with new text."""
    manager = get_manager(todo_path)
    try:
        task = manager.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        if not task.notes:
            print(f"Error: Task #{task_id} has no notes to update")
            print(f"Hint: Use 'note {task_id} \"text\"' to add notes")
            return

        # Show preview (matching shell script behavior)
        old_count = len(task.notes)
        new_count = len(new_note_text.split("\n"))
        print(f"Task #{task_id} currently has {old_count} note(s).")
        print(f"New note will have {new_count} line(s).")

        task = manager.update_notes_for_task(task_id, new_note_text)
        save_changes(manager, todo_path)
        print(f"Updated notes for task #{task.id}")
    except ValueError as e:
        print(f"Error: {e}")


def _get_checkbox(status_value: str) -> str:
    """Get the appropriate checkbox for a task status."""
    if status_value == "pending":
        return "[ ]"
    elif status_value == "deleted":
        return "[D]"
    else:  # completed, archived
        return "[x]"


def show_command(task_id: str, todo_path: str = "TODO.md"):
    """Display task with subtasks, relationships, and notes."""
    file_ops = FileOps(todo_path)
    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)

    task = manager.get_task(task_id)
    if not task:
        print(f"Error: Task #{task_id} not found")
        return

    # Display task line
    checkbox = _get_checkbox(task.status.value)
    indent = "  " * (task.id.count("."))
    tag_str = " ".join([f"`#{tag}`" for tag in sorted(task.tags)]) if task.tags else ""
    description = task.description
    if tag_str:
        description = f"{description} {tag_str}".strip()
    print(f"{indent}- {checkbox} **#{task.id}** {description}")

    # Display notes
    for note in task.notes:
        print(f"{indent}  > {note}")

    # Display subtasks
    subtasks = manager.get_subtasks(task_id)
    if subtasks:
        for subtask in sorted(subtasks, key=lambda t: t.id):
            sub_checkbox = _get_checkbox(subtask.status.value)
            sub_indent = "  " * (subtask.id.count("."))
            sub_tag_str = (
                " ".join([f"`#{tag}`" for tag in sorted(subtask.tags)]) if subtask.tags else ""
            )
            sub_description = subtask.description
            if sub_tag_str:
                sub_description = f"{sub_description} {sub_tag_str}".strip()
            print(f"{sub_indent}- {sub_checkbox} **#{subtask.id}** {sub_description}")
            for note in subtask.notes:
                print(f"{sub_indent}  > {note}")

    # Display relationships
    relationships = file_ops.get_relationships(task_id)
    if relationships:
        for rel_type, targets in sorted(relationships.items()):
            # Format relationship type
            formatted_type = rel_type.replace("-", " ").title()
            targets_str = " ".join(targets)
            print(f"  ↳ {formatted_type}: {targets_str}")
    else:
        print("  (No relationships)")


def relate_command(
    task_id: str,
    rel_type: str,
    target_ids: list[str],
    todo_path: str = "TODO.md",
):
    """Add a task relationship."""
    file_ops = FileOps(todo_path)
    tasks = file_ops.read_tasks()  # This also parses relationships
    manager = TaskManager(tasks)

    # Verify task exists
    task = manager.get_task(task_id)
    if not task:
        print(f"Error: Task #{task_id} not found")
        return

    # Validate relationship type
    valid_types = ["completed-by", "depends-on", "blocks", "related-to", "duplicate-of"]
    if rel_type not in valid_types:
        print(f"Error: Invalid relationship type '{rel_type}'")
        print(f"Valid types: {', '.join(valid_types)}")
        return

    # Add relationship
    file_ops.add_relationship(task_id, rel_type, target_ids)
    file_ops.write_tasks(tasks)  # Write back to preserve relationships

    targets_str = " ".join(target_ids)
    print(f"Added relationship: #{task_id} {rel_type} {targets_str}")


# Helper functions for task ID expansion
def expand_task_range(task_id: str) -> list[str]:
    """Expand a task range like '104.3-104.10' into a list of task IDs."""
    if "-" not in task_id:
        return [task_id]

    start_str, end_str = task_id.split("-", 1)
    # Extract base and numbers
    # Pattern: "104.3" -> base="104", num=3
    start_match = re.match(r"^([0-9]+(?:\.\d+)?)\.?(\d+)?$", start_str)
    end_match = re.match(r"^([0-9]+(?:\.\d+)?)\.?(\d+)?$", end_str)

    if not start_match or not end_match:
        return [task_id]  # Invalid range, return as-is

    start_base = start_match.group(1)
    start_num = int(start_match.group(2) or 0)
    end_base = end_match.group(1)
    end_num = int(end_match.group(2) or 0)

    # If bases don't match, can't expand
    if start_base != end_base:
        return [task_id]

    result = []
    for num in range(start_num, end_num + 1):
        result.append(f"{start_base}.{num}")
    return result


def expand_task_ids(
    task_ids: list[str], with_subtasks: bool = False, todo_path: str = "TODO.md"
) -> list[str]:
    """Expand task IDs including ranges and optionally subtasks."""
    expanded = []
    manager = get_manager(todo_path)

    for task_id in task_ids:
        # Expand ranges
        if "-" in task_id:
            expanded.extend(expand_task_range(task_id))
        else:
            expanded.append(task_id)

    # Add subtasks if requested
    if with_subtasks:
        final_expanded = []
        for task_id in expanded:
            final_expanded.append(task_id)
            # Get subtasks
            subtasks = manager.get_subtasks(task_id)
            for subtask in subtasks:
                final_expanded.append(subtask.id)
        return final_expanded

    return expanded


def lint_command(todo_path: str = "TODO.md"):
    """Identify formatting issues (indentation, checkboxes, orphaned subtasks, duplicates)."""
    print("🔍 Checking TODO.md for formatting issues...")
    print("")

    file_ops = FileOps(todo_path)
    file_ops.read_tasks()  # Parse relationships

    issues_found = 0

    # Read file content for line-by-line analysis
    todo_file = Path(todo_path)
    if not todo_file.exists():
        print(f"Error: {todo_path} not found")
        return

    content = todo_file.read_text(encoding="utf-8")
    lines = content.splitlines()

    # Track which section we're in
    in_tasks = False
    skip_line = False

    # Check for spacing issues
    print("📏 Checking spacing:")
    spacing_issues = 0
    last_line_was_blank = False
    last_line_was_task = False
    last_task_was_root = False

    for _i, line in enumerate(lines):
        line_stripped = line.strip()

        # Detect section headers
        if line_stripped == "## Tasks":
            in_tasks = True
            skip_line = False
            last_line_was_blank = False
            last_line_was_task = False
            continue
        elif line_stripped == "## Archived Tasks" or line_stripped == "## Recently Completed":
            in_tasks = False
            skip_line = True
        elif line_stripped == "## Deleted Tasks":
            in_tasks = False
            skip_line = True
        elif line_stripped.startswith("## "):
            in_tasks = False
            skip_line = True
        elif line_stripped == "---":
            continue

        if skip_line:
            continue

        if in_tasks:
            # Check for blank line
            if not line_stripped:
                last_line_was_blank = True
                last_line_was_task = False
                continue

            # Check for task
            is_task = re.match(r"^\s*- \[.*\] ", line)
            if is_task:
                is_root = re.match(r"^- \[.*\] ", line) is not None

                # Rule 1: Root tasks must be separated by 1 blank line (unless first task)
                if is_root:
                    if last_line_was_task and not last_line_was_blank:
                        # Previous line was a task, and no blank line
                        print(f"  ❌ Missing blank line before root task: {line_stripped}")
                        spacing_issues += 1
                        issues_found += 1

                # Rule 2: Subtasks must NOT have blank lines between them
                if not is_root:
                    if last_line_was_blank and last_task_was_root is False:
                        # Previous was subtask (or note), and we have a blank line
                        # Wait, we need to know if previous was subtask of SAME parent?
                        # Simplified: No blank lines before subtasks
                        print(f"  ❌ Unexpected blank line before subtask: {line_stripped}")
                        spacing_issues += 1
                        issues_found += 1

                last_line_was_blank = False
                last_line_was_task = True
                last_task_was_root = is_root
                continue

            # Check for note
            if line_stripped.startswith(">"):
                last_line_was_blank = False
                # Notes are part of the task block
                continue

    if spacing_issues == 0:
        print("  ✅ Spacing is correct")
    else:
        print(f"  📊 Found {spacing_issues} spacing issues")
    print("")

    # Check for indentation issues
    print("📋 Checking indentation:")
    indent_issues = 0

    # Check for ordering issues
    print("📉 Checking subtask ordering:")
    order_issues = 0
    last_parent_id = None
    last_sub_num = None

    for line in lines:
        line_stripped = line.strip()

        # Detect section headers
        if line_stripped == "## Tasks":
            in_tasks = True
            skip_line = False
        elif line_stripped == "## Archived Tasks" or line_stripped == "## Recently Completed":
            in_tasks = False
            skip_line = True
        elif line_stripped == "## Deleted Tasks":
            in_tasks = False
            skip_line = True
        elif line_stripped.startswith("## "):
            in_tasks = False
            skip_line = True
        elif line_stripped == "---":
            # Ignore separators
            continue

        if skip_line:
            continue

        # Only check tasks in the "Tasks" section
        if in_tasks:
            # Check for subtasks not indented (should start with "  -")
            if re.match(r"^- \[.*\] \*\*#[0-9]+\.[0-9]+\*\* ", line):
                print(f"  ❌ Subtask not indented: {line}")
                indent_issues += 1
                issues_found += 1

            # Check for out-of-order subtasks (Task #198.1)
            # Match subtasks: "  - [ ] **#1.2** Description"
            subtask_match = re.match(r"^  - \[.*\] \*\*#([0-9]+)\.([0-9]+)\*\* ", line)
            if subtask_match:
                current_parent_id = subtask_match.group(1)
                current_sub_num = int(subtask_match.group(2))

                # If we are in a subtask block (same parent)
                if last_parent_id == current_parent_id:
                    # Check if current subtask number is smaller than previous (should be descending)
                    # Reverse chronological: 1.2 then 1.1
                    # So current (1.1) should be < previous (1.2).

                    if last_sub_num is not None and current_sub_num > last_sub_num:
                        print(
                            f"  ❌ Out-of-order subtask: #{current_parent_id}.{current_sub_num} appears after #{current_parent_id}.{last_sub_num} (should be reverse chronological)"
                        )
                        order_issues += 1
                        issues_found += 1
                else:
                    # New parent block, reset
                    last_parent_id = current_parent_id

                last_sub_num = current_sub_num
            else:
                # Not a subtask line, reset tracking
                last_parent_id = None
                last_sub_num = None

    if indent_issues == 0:
        print("  ✅ All subtasks properly indented")
    else:
        print(f"  📊 Found {indent_issues} indentation issues")

    if order_issues == 0:
        print("  ✅ All subtasks properly ordered (newest first)")
    else:
        print(f"  📊 Found {order_issues} subtask ordering issues")
    print("")

    # Check for malformed checkboxes
    print("☑️  Checking checkboxes:")
    checkbox_issues = 0

    # Reset section tracking
    in_tasks = False
    skip_line = False

    for line in lines:
        line_stripped = line.strip()

        # Detect section headers
        if line_stripped == "## Tasks":
            in_tasks = True
            skip_line = False
        elif line_stripped == "## Archived Tasks" or line_stripped == "## Recently Completed":
            in_tasks = False
            skip_line = True
        elif line_stripped == "## Deleted Tasks":
            in_tasks = False
            skip_line = True
        elif line_stripped.startswith("## "):
            in_tasks = False
            skip_line = True
        elif line_stripped == "---":
            continue

        if skip_line:
            continue

        # Only check tasks in the "Tasks" section
        if in_tasks:
            # Check for malformed checkbox patterns
            if re.match(r"^- \[.*\] ", line) or re.match(r"^  - \[.*\] ", line):
                if re.search(r"\[  \]|\[   \]|\[    \]|\[\]", line):
                    print(f"  ❌ Malformed checkbox: {line}")
                    checkbox_issues += 1
                    issues_found += 1

    if checkbox_issues == 0:
        print("  ✅ All checkboxes properly formatted")
    else:
        print(f"  📊 Found {checkbox_issues} checkbox issues")
    print("")

    # Check for orphaned subtasks
    print("🔗 Checking for orphaned subtasks:")
    orphan_issues = 0
    seen_parents = set()

    # First pass: collect all parent task IDs (only in Tasks section)
    in_tasks = False
    skip_line = False

    for line in lines:
        line_stripped = line.strip()

        if line_stripped == "## Tasks":
            in_tasks = True
            skip_line = False
        elif line_stripped == "## Archived Tasks" or line_stripped == "## Recently Completed":
            in_tasks = False
            skip_line = True
        elif line_stripped == "## Deleted Tasks":
            in_tasks = False
            skip_line = True
        elif line_stripped.startswith("## "):
            in_tasks = False
            skip_line = True
        elif line_stripped == "---":
            continue

        if skip_line:
            continue

        if in_tasks:
            # Match parent tasks (not subtasks - no dot in ID)
            match = re.match(r"^- \[.*\] \*\*#([0-9]+)\*\* ", line)
            if match:
                parent_id = match.group(1)
                seen_parents.add(parent_id)

    # Second pass: check all subtasks have parents
    in_tasks = False
    skip_line = False

    for line in lines:
        line_stripped = line.strip()

        if line_stripped == "## Tasks":
            in_tasks = True
            skip_line = False
        elif line_stripped == "## Archived Tasks" or line_stripped == "## Recently Completed":
            in_tasks = False
            skip_line = True
        elif line_stripped == "## Deleted Tasks":
            in_tasks = False
            skip_line = True
        elif line_stripped.startswith("## "):
            in_tasks = False
            skip_line = True
        elif line_stripped == "---":
            continue

        if skip_line:
            continue

        if in_tasks:
            # Match subtasks (have dot in ID)
            match = re.match(r"^  - \[.*\] \*\*#([0-9]+)\.([0-9]+)\*\* ", line)
            if match:
                parent_id = match.group(1)
                subtask_id = f"{match.group(1)}.{match.group(2)}"
                if parent_id not in seen_parents:
                    print(f"  ❌ Orphaned subtask #{subtask_id} (parent #{parent_id} not found)")
                    orphan_issues += 1
                    issues_found += 1

    if orphan_issues == 0:
        print("  ✅ No orphaned subtasks")
    else:
        print(f"  📊 Found {orphan_issues} orphaned subtasks")
    print("")

    # Check for duplicate task IDs
    print("🔢 Checking for duplicate task IDs:")
    duplicate_issues = 0
    task_ids_seen: dict[str, list[int]] = {}  # task_id -> list of line numbers

    in_tasks = False
    skip_line = False
    line_num = 0

    for line in lines:
        line_num += 1
        line_stripped = line.strip()

        if line_stripped == "## Tasks":
            in_tasks = True
            skip_line = False
        elif line_stripped == "## Archived Tasks" or line_stripped == "## Recently Completed":
            in_tasks = False
            skip_line = True
        elif line_stripped == "## Deleted Tasks":
            in_tasks = False
            skip_line = True
        elif line_stripped.startswith("## "):
            in_tasks = False
            skip_line = True
        elif line_stripped == "---":
            continue

        if skip_line:
            continue

        # Match task IDs in format: **#task_id**
        match = re.search(r"\*\*#([0-9]+(?:\.[0-9]+)?)\*\*", line)
        if match:
            task_id = match.group(1)
            if task_id not in task_ids_seen:
                task_ids_seen[task_id] = []
            task_ids_seen[task_id].append(line_num)

    # Report duplicates
    for task_id, line_nums in task_ids_seen.items():
        if len(line_nums) > 1:
            print(
                f"  ❌ Duplicate task ID #{task_id} found on lines: {', '.join(map(str, line_nums))}"
            )
            duplicate_issues += 1
            issues_found += 1

    if duplicate_issues == 0:
        print("  ✅ No duplicate task IDs")
    else:
        print(f"  📊 Found {duplicate_issues} duplicate task ID(s)")
    print("")

    # Summary
    if issues_found == 0:
        print("✅ No formatting issues found!")
    else:
        print(f"📊 Total issues found: {issues_found}")


def reformat_command(dry_run: bool = False, todo_path: str = "TODO.md"):
    """Apply formatting fixes (with --dry-run option)."""
    if dry_run:
        print("🔍 DRY RUN: Showing what would be fixed...")
        # For dry run, we can't easily show diffs without generating the file
        # So we'll just say we would reformat
        print("  🔄 Would reformat TODO.md to enforce standards (indentation, spacing, headers)")
        print("  💡 Run './todo.ai --reformat' to apply these fixes")
        return

    print("🔧 Applying formatting fixes...")

    try:
        # Simply reading and writing through FileOps enforces all standards
        file_ops = FileOps(todo_path)
        tasks = file_ops.read_tasks()
        file_ops.write_tasks(tasks)
        print("✅ Reformatted TODO.md")
    except Exception as e:
        print(f"Error reformatting file: {e}")


def reorder_command(todo_path: str = "TODO.md"):
    """Reorder subtasks to match reverse-chronological order (newest on top)."""
    print("🔧 Reordering subtasks...")
    print("")

    try:
        file_ops = FileOps(todo_path)
        tasks = file_ops.read_tasks()

        # We need to reorder subtasks in the list
        # 1. Identify root tasks and their subtasks
        root_tasks = []
        subtasks_map: dict[str, list[Task]] = {}  # parent_id -> list[Task]

        for task in tasks:
            if "." in task.id:
                parent_id = task.id.rsplit(".", 1)[0]
                if parent_id not in subtasks_map:
                    subtasks_map[parent_id] = []
                subtasks_map[parent_id].append(task)
            else:
                root_tasks.append(task)

        # 2. Reconstruct list with sorted subtasks
        new_task_list = []
        for root_task in root_tasks:
            new_task_list.append(root_task)
            if root_task.id in subtasks_map:
                # Sort subtasks descending by ID (newest on top)
                sorted_subtasks = sorted(
                    subtasks_map[root_task.id],
                    key=lambda t: [int(x) for x in t.id.split(".")],
                    reverse=True,
                )
                new_task_list.extend(sorted_subtasks)

        # 3. Write back
        file_ops.write_tasks(new_task_list)
        print("✅ Reordered subtasks (newest on top)")

    except Exception as e:
        print(f"Error reordering tasks: {e}")


def resolve_conflicts_command(dry_run: bool = False, todo_path: str = "TODO.md"):
    """Detect and resolve duplicate task IDs (with --dry-run option)."""
    if dry_run:
        print("🔍 DRY RUN: Showing what would be fixed...")
    else:
        print("🔧 Resolving task ID conflicts...")
    print("")

    todo_file = Path(todo_path)
    if not todo_file.exists():
        print(f"Error: {todo_path} not found")
        return

    # Step 1: Detect duplicate task IDs
    content = todo_file.read_text(encoding="utf-8")
    lines = content.splitlines()

    task_ids: dict[str, list[int]] = {}  # task_id -> list of line numbers
    line_num = 0

    for line in lines:
        line_num += 1
        # Match task IDs in format: **#task_id**
        match = re.search(r"\*\*#([0-9]+(?:\.[0-9]+)?)\*\*", line)
        if match:
            task_id = match.group(1)
            if task_id not in task_ids:
                task_ids[task_id] = []
            task_ids[task_id].append(line_num)

    # Find duplicates
    duplicates: dict[str, list[int]] = {}
    for task_id, line_nums in task_ids.items():
        if len(line_nums) > 1:
            duplicates[task_id] = line_nums

    if not duplicates:
        print("✅ No duplicate task IDs found")
        return

    print(f"📊 Found {len(duplicates)} duplicate task ID(s):")
    for dup_id, line_nums in duplicates.items():
        print(f"  - #{dup_id} (lines: {', '.join(map(str, line_nums))})")
    print("")

    # Step 2: Create mapping from old duplicate IDs to new IDs
    # Strategy: Keep first occurrence, renumber subsequent ones
    id_mapping: dict[tuple[int, str], str] = {}  # (line_num, old_id) -> new_id

    # Get all existing task IDs to avoid conflicts
    all_task_ids = set(task_ids.keys())

    for dup_id, line_nums in duplicates.items():
        # Keep first occurrence, renumber the rest
        for occurrence_index, dup_line_num in enumerate(line_nums[1:], 1):
            # Generate new ID
            # Extract numeric part
            if re.match(r"^([0-9]+)(\.([0-9]+))?$", dup_id):
                match = re.match(r"^([0-9]+)(\.([0-9]+))?$", dup_id)
                if match:
                    numeric_part = match.group(1)
                    subtask_part = match.group(3)

                    if subtask_part:
                        # Subtask - preserve parent, increment subtask number
                        parent_num = numeric_part
                        subtask_num = int(subtask_part)
                        new_subtask_num = subtask_num + occurrence_index
                        new_id = f"{parent_num}.{new_subtask_num}"
                    else:
                        # Main task - find highest number and increment
                        highest_num = 0
                        for existing_id in all_task_ids:
                            if re.match(r"^([0-9]+)(\.([0-9]+))?$", existing_id):
                                m = re.match(r"^([0-9]+)(\.([0-9]+))?$", existing_id)
                                if m and not m.group(3):  # Main task only
                                    num = int(m.group(1))
                                    if num > highest_num:
                                        highest_num = num
                        new_id = str(highest_num + occurrence_index)
            else:
                # Fallback: append occurrence index
                new_id = f"{dup_id}-dup{occurrence_index}"

            # Make sure new_id doesn't conflict
            conflict_index = 0
            while new_id in all_task_ids:
                conflict_index += 1
                if re.match(r"^([0-9]+)(\.([0-9]+))?$", dup_id):
                    match = re.match(r"^([0-9]+)(\.([0-9]+))?$", dup_id)
                    if match:
                        numeric_part = match.group(1)
                        subtask_part = match.group(3)
                        if subtask_part:
                            parent_num = numeric_part
                            subtask_num = int(subtask_part)
                            new_subtask_num = subtask_num + occurrence_index + conflict_index
                            new_id = f"{parent_num}.{new_subtask_num}"
                        else:
                            new_id = str(int(new_id) + 1)
                else:
                    new_id = f"{dup_id}-dup{occurrence_index}-{conflict_index}"

            all_task_ids.add(new_id)
            id_mapping[(dup_line_num, dup_id)] = new_id

    # Step 3: Apply renumbering
    if dry_run:
        print("📋 Would renumber the following tasks:")
        for (line_num, old_id), new_id in sorted(id_mapping.items()):
            task_line = lines[line_num - 1] if line_num <= len(lines) else ""
            print(f"  Line {line_num}: #{old_id} → #{new_id}")
            print(f"    {task_line}")
        print("")
        print("💡 Run './todo.ai resolve-conflicts' to apply these changes")
    else:
        # Create backup before making changes
        backup_name = create_backup(todo_path)
        if backup_name:
            print(f"💾 Backup created: {backup_name}")
            print("")

        # Apply changes
        new_lines = []
        line_num = 0

        for line in lines:
            line_num += 1
            new_line = line
            line_changed = False

            # Check if this line needs renumbering
            for (dup_line_num, old_id), new_id in id_mapping.items():
                if line_num == dup_line_num:
                    # Replace task ID in line
                    new_line = re.sub(rf"\*\*#{re.escape(old_id)}\*\*", f"**#{new_id}**", new_line)
                    line_changed = True
                    print(f"  ✅ Renumbered: Line {line_num}: #{old_id} → #{new_id}")
                    break

            # Also update references to old IDs in relationships, notes, etc.
            if not line_changed:
                for (_, old_id), new_id in id_mapping.items():
                    # Replace references (e.g., in relationships: #old_id or old_id:)
                    new_line = re.sub(
                        rf"#{re.escape(old_id)}([^0-9a-z-]|$)", rf"#{new_id}\1", new_line
                    )
                    new_line = re.sub(
                        rf":{re.escape(old_id)}([^0-9a-z-]|$)", rf":{new_id}\1", new_line
                    )
                    new_line = re.sub(
                        rf"{re.escape(old_id)}:([^0-9a-z-]|$)", rf"{new_id}:\1", new_line
                    )

            new_lines.append(new_line)

        # Write changes
        todo_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

        conflicts_resolved = len(id_mapping)
        print("")
        if conflicts_resolved > 0:
            print(f"✅ Resolved {conflicts_resolved} conflict(s)")
        else:
            print("✅ No conflicts found")


def edit_command(todo_path: str = "TODO.md"):
    """Open TODO.md in editor."""
    editor = os.environ.get("EDITOR", "nano")
    todo_file = Path(todo_path)

    if not todo_file.exists():
        print(f"Error: {todo_path} not found")
        return

    try:
        subprocess.run([editor, str(todo_file)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to open editor: {e}")
    except FileNotFoundError:
        print(f"Error: Editor '{editor}' not found. Set EDITOR environment variable.")


# Phase 5: System Operations
def log_command(
    filter_text: str | None = None, lines: int | None = None, todo_path: str = "TODO.md"
) -> None:
    """View TODO operation log (with --filter and --lines options)."""
    view_log_command(filter_text, lines, todo_path)


def update_tool_command() -> None:
    """Update todo.ai to latest version."""
    update_command()


def backups_command(todo_path: str = "TODO.md") -> None:
    """List available backup versions."""
    list_backups_command(todo_path)


def rollback_tool_command(target: str | None = None, todo_path: str = "TODO.md") -> None:
    """Rollback to previous version (by index or timestamp)."""
    rollback_command(target, todo_path)


# Phase 6: Configuration and Setup
def config_command(todo_path: str = "TODO.md") -> None:
    """Show current configuration."""
    show_config_command(todo_path)


def detect_coordination_tool_command(todo_path: str = "TODO.md") -> None:
    """Detect available coordination options based on system."""
    detect_coordination_command(todo_path)


def setup_coordination_tool_command(
    coord_type: str, interactive: bool = True, todo_path: str = "TODO.md"
) -> None:
    """Set up coordination service (github-issues, counterapi)."""
    setup_coordination_command(coord_type, interactive, todo_path)


def setup_wizard_tool_command(todo_path: str = "TODO.md") -> None:
    """Interactive setup wizard for mode and coordination."""
    setup_wizard_command(todo_path)


def switch_mode_tool_command(
    new_mode: str,
    force: bool = False,
    renumber: bool = False,
    todo_path: str = "TODO.md",
) -> None:
    """Switch numbering mode (single-user, multi-user, branch, enhanced) with --force and --renumber options."""
    switch_mode_command(new_mode, force, renumber, todo_path)


def list_mode_backups_tool_command(todo_path: str = "TODO.md") -> None:
    """List mode switch backups."""
    list_mode_backups_command(todo_path)


def rollback_mode_tool_command(backup_name: str, todo_path: str = "TODO.md") -> None:
    """Rollback from mode switch backup."""
    rollback_mode_command(backup_name, todo_path)


# Prune Command
def empty_trash_command(
    dry_run: bool = False,
    todo_path: str = "TODO.md",
):
    """
    Permanently remove expired deleted tasks (30-day retention).

    Args:
        dry_run: Preview without making changes
        todo_path: Path to TODO.md
    """
    from ai_todo.core.empty_trash import EmptyTrashManager

    manager = EmptyTrashManager(todo_path)
    result = manager.empty_trash(dry_run=dry_run)

    if result.total_removed == 0:
        print("ℹ️  No expired deleted tasks found.")
        return

    if dry_run:
        print(f"🔍 Would remove {result.total_removed} expired task(s):")
        print(f"   - Root tasks: {result.tasks_removed}")
        print(f"   - Subtasks: {result.subtasks_removed}")
        print(f"   - IDs: {', '.join(result.removed_task_ids[:10])}")
        if len(result.removed_task_ids) > 10:
            print(f"   ... and {len(result.removed_task_ids) - 10} more")
        print("")
        print("💡 Run without --dry-run to permanently remove these tasks")
    else:
        print(f"🗑️  Removed {result.total_removed} expired task(s)")
        print(f"   - Root tasks: {result.tasks_removed}")
        print(f"   - Subtasks: {result.subtasks_removed}")


def prune_command(
    days: int | None = None,
    older_than: str | None = None,
    from_task: str | None = None,
    dry_run: bool = False,
    backup: bool = True,
    force: bool = False,
    todo_path: str = "TODO.md",
):
    """
    Prune old archived tasks from TODO.md.

    Args:
        days: Prune tasks older than N days (default: 30 if no other filter)
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
        days=days, older_than=older_than, from_task=from_task, dry_run=True, backup=False
    )

    # No tasks to prune
    if preview_result.total_pruned == 0:
        print("ℹ️  No archived tasks match the prune criteria.")
        return

    # Display preview
    print(
        f"🔍 Found {preview_result.tasks_pruned} task(s) and "
        f"{preview_result.subtasks_pruned} subtask(s) to prune"
    )
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
        if response != "y":
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
        backup=backup,
    )

    # Display result
    print(f"✅ Pruned {result.tasks_pruned} task(s) and {result.subtasks_pruned} subtask(s)")

    if result.archive_path:
        print(f"📦 Archive backup: {result.archive_path}")

    print("")


# Phase 7: Utility Commands
def report_bug_tool_command(
    error_description: str,
    error_context: str | None = None,
    command: str | None = None,
) -> None:
    """Report bugs to GitHub Issues (with duplicate detection)."""
    report_bug_command(error_description, error_context, command)


def uninstall_tool_command(
    remove_data: bool = False,
    remove_rules: bool = False,
    force: bool = False,
) -> None:
    """Uninstall todo.ai (with --remove-data, --remove-rules, --all options)."""
    uninstall_command(remove_data, remove_rules, force)


def version_tool_command() -> None:
    """Show version information."""
    version_command()
