import re
from pathlib import Path

from todo_ai.core.config import Config
from todo_ai.core.coordination import CoordinationManager
from todo_ai.core.file_ops import FileOps
from todo_ai.core.task import TaskManager

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
        file_ops.read_tasks()  # Read to get relationships
    tasks = manager.list_tasks()
    file_ops.write_tasks(tasks)


def add_command(description: str, tags: list[str], todo_path: str = "TODO.md"):
    """Add a new task."""
    file_ops = FileOps(todo_path)
    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)

    # ID Generation
    config = Config(str(file_ops.config_dir / "config.yaml"))
    coordination = CoordinationManager(config)

    # Get current state
    stored_serial = file_ops.get_serial()

    # Find max integer ID from existing tasks
    current_max = 0
    for task in tasks:
        if task.id.isdigit():
            current_max = max(current_max, int(task.id))

    # Generate next ID based on mode
    next_id_str = coordination.generate_next_task_id(current_max, stored_serial)

    # Update serial file for next time
    # If next_id is numeric, set serial to next_id (Last Used)
    if next_id_str.isdigit():
        file_ops.set_serial(int(next_id_str))

    task = manager.add_task(description, tags, task_id=next_id_str)
    file_ops.write_tasks(manager.list_tasks())
    print(f"Added: #{task.id} {task.description}")


def add_subtask_command(
    parent_id: str, description: str, tags: list[str], todo_path: str = "TODO.md"
):
    """Add a subtask."""
    manager = get_manager(todo_path)
    try:
        # Subtasks don't use global serial, they are nested under parent
        task = manager.add_subtask(parent_id, description, tags)
        save_changes(manager, todo_path)
        print(f"Added subtask: #{task.id} {task.description}")
    except ValueError as e:
        print(f"Error: {e}")


def complete_command(task_ids: list[str], with_subtasks: bool = False, todo_path: str = "TODO.md"):
    """Complete task(s)."""
    manager = get_manager(todo_path)
    try:
        # Expand ranges and optionally add subtasks
        expanded_ids = expand_task_ids(task_ids, with_subtasks, todo_path)

        completed_tasks = []
        for task_id in expanded_ids:
            try:
                task = manager.complete_task(task_id)
                completed_tasks.append(task)
            except ValueError as e:
                print(f"Warning: {e}")

        if not completed_tasks:
            print("Error: No tasks were completed")
            return

        save_changes(manager, todo_path)
        if len(completed_tasks) == 1:
            print(f"Completed: #{completed_tasks[0].id} {completed_tasks[0].description}")
        else:
            print(f"Completed {len(completed_tasks)} task(s)")
    except Exception as e:
        print(f"Error: {e}")


def list_command(status: str | None = None, tag: str | None = None, todo_path: str = "TODO.md"):
    """List tasks."""
    manager = get_manager(todo_path)

    # Print Header (similar to shell script)
    config_dir = Path(todo_path).parent / ".todo.ai"
    config = Config(str(config_dir / "config.yaml"))
    mode = config.get_numbering_mode()
    coord = config.get_coordination_type()
    issue = config.get("coordination.issue_number")
    coord_str = f"GitHub Issues (#{issue})" if issue else (coord or "None")
    print(f"📋 Mode: {mode} | Coordinator: {coord_str}")
    print()

    filters = {}
    if status:
        filters["status"] = status
    if tag:
        filters["tag"] = tag

    tasks = manager.list_tasks(filters)
    if not tasks:
        # Shell script usually prints nothing or specific message?
        # Standardize: No tasks found.
        # But shell script might just show header.
        return

    for task in tasks:
        checkbox = "[x]" if task.status.value != "pending" else "[ ]"

        # Indentation
        depth = task.id.count(".")
        indent = "  " * depth

        print(f"{indent}- {checkbox} **#{task.id}** {task.description}")

        # Notes
        for note in task.notes:
            print(f"{indent}  > {note}")


def expand_task_range(task_id: str) -> list[str]:
    """Expand a task range (e.g., '104.3-104.10') into a list of task IDs."""
    # Match patterns like: 104.3-104.10 or 122.3-10
    range_pattern = re.compile(r"^(\d+)\.(\d+)-(\d+)\.(\d+)$")
    short_range_pattern = re.compile(r"^(\d+)\.(\d+)-(\d+)$")

    match = range_pattern.match(task_id)
    if match:
        parent1, start, parent2, end = match.groups()
        if parent1 == parent2:
            return [f"{parent1}.{i}" for i in range(int(start), int(end) + 1)]
        return [task_id]  # Invalid range, return as-is

    match = short_range_pattern.match(task_id)
    if match:
        parent, start, end = match.groups()
        if int(start) <= int(end):
            return [f"{parent}.{i}" for i in range(int(start), int(end) + 1)]
        return [task_id]  # Invalid range, return as-is

    return [task_id]  # Not a range, return as-is


def expand_task_ids(
    task_ids: list[str], with_subtasks: bool = False, todo_path: str = "TODO.md"
) -> list[str]:
    """Expand task IDs, handling ranges and optionally including subtasks."""
    expanded = []
    for task_id in task_ids:
        # Expand ranges
        range_tasks = expand_task_range(task_id)
        expanded.extend(range_tasks)

    # If with_subtasks, add all subtasks
    if with_subtasks:
        manager = get_manager(todo_path)
        final_expanded = []
        for task_id in expanded:
            final_expanded.append(task_id)
            subtasks = manager.get_subtasks(task_id)
            final_expanded.extend([st.id for st in subtasks])
        return final_expanded

    return expanded


def modify_command(
    task_id: str, description: str, tags: list[str] | None = None, todo_path: str = "TODO.md"
):
    """Modify a task's description and/or tags."""
    manager = get_manager(todo_path)
    try:
        # Extract tags from description if they're in backticks (format: `#tag`)
        tag_pattern = re.compile(r"`#([a-zA-Z0-9_-]+)`")
        found_tags = tag_pattern.findall(description)

        # Remove tags from description
        description = tag_pattern.sub("", description).strip()

        # Combine tags from description and explicit tags argument
        if tags:
            all_tags: list[str] | None = list(set(found_tags + tags))
        else:
            all_tags = found_tags if found_tags else None

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


def delete_command(
    task_ids: list[str],
    with_subtasks: bool = False,
    todo_path: str = "TODO.md",
):
    """Delete task(s) - move to Deleted section."""
    manager = get_manager(todo_path)
    try:
        # Expand ranges and optionally add subtasks
        expanded_ids = expand_task_ids(task_ids, with_subtasks, todo_path)

        deleted_tasks = []
        for task_id in expanded_ids:
            try:
                task = manager.delete_task(task_id)
                deleted_tasks.append(task)
            except ValueError as e:
                print(f"Warning: {e}")

        if not deleted_tasks:
            print("Error: No tasks were deleted")
            return

        save_changes(manager, todo_path)
        if len(deleted_tasks) == 1:
            print(f"Deleted: #{deleted_tasks[0].id} {deleted_tasks[0].description}")
        else:
            print(f"Deleted {len(deleted_tasks)} task(s)")
    except Exception as e:
        print(f"Error: {e}")


def archive_command(
    task_ids: list[str],
    reason: str | None = None,
    with_subtasks: bool = False,
    todo_path: str = "TODO.md",
):
    """Archive task(s) - move to Recently Completed section."""
    manager = get_manager(todo_path)
    try:
        # Expand ranges and optionally add subtasks
        expanded_ids = expand_task_ids(task_ids, with_subtasks, todo_path)

        archived_tasks = []
        for task_id in expanded_ids:
            try:
                task = manager.get_task(task_id)
                if not task:
                    print(f"Warning: Task {task_id} not found")
                    continue

                # Check if task is incomplete and no reason provided
                if task.status.value == "pending" and not reason:
                    print(
                        f"Error: Task #{task_id} is not completed. "
                        "To archive incomplete tasks, provide --reason"
                    )
                    continue

                task = manager.archive_task(task_id)
                archived_tasks.append(task)
            except ValueError as e:
                print(f"Warning: {e}")

        if not archived_tasks:
            print("Error: No tasks were archived")
            return

        save_changes(manager, todo_path)
        if len(archived_tasks) == 1:
            print(f"Archived: #{archived_tasks[0].id} {archived_tasks[0].description}")
        else:
            print(f"Archived {len(archived_tasks)} task(s)")
    except Exception as e:
        print(f"Error: {e}")


def restore_command(task_id: str, todo_path: str = "TODO.md"):
    """Restore a task from Deleted or Recently Completed back to Tasks section."""
    manager = get_manager(todo_path)
    try:
        task = manager.restore_task(task_id)
        save_changes(manager, todo_path)
        print(f"Restored: #{task.id} {task.description}")
    except ValueError as e:
        print(f"Error: {e}")


def undo_command(task_id: str, todo_path: str = "TODO.md"):
    """Reopen (undo) a completed task."""
    manager = get_manager(todo_path)
    try:
        task = manager.undo_task(task_id)
        save_changes(manager, todo_path)
        print(f"Reopened: #{task.id} {task.description}")
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
            print(f"Error: Task #{task_id} has no notes to delete")
            return

        # Show confirmation (matching shell script behavior)
        note_count = len(task.notes)
        print(f"Task #{task_id} has {note_count} note(s).")
        reply = input(f"Delete all notes from task #{task_id}? (y/N) ")

        if reply.strip().lower() != "y":
            print("Cancelled - notes not deleted")
            return

        task = manager.delete_notes_from_task(task_id)
        save_changes(manager, todo_path)
        print(f"Deleted notes from task #{task.id}")
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
        reply = input(f"Replace notes for task #{task_id}? (y/N) ")

        if reply.strip().lower() != "y":
            print("Cancelled - notes not updated")
            return

        task = manager.update_notes_for_task(task_id, new_note_text)
        save_changes(manager, todo_path)
        print(f"Updated notes for task #{task.id}")
    except ValueError as e:
        print(f"Error: {e}")


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
    checkbox = "[x]" if task.status.value != "pending" else "[ ]"
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
            sub_checkbox = "[x]" if subtask.status.value != "pending" else "[ ]"
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
