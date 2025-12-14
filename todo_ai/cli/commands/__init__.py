import re
from pathlib import Path

from todo_ai.core.config import Config
from todo_ai.core.coordination import CoordinationManager
from todo_ai.core.file_ops import FileOps
from todo_ai.core.task import TaskManager


def get_manager(todo_path: str = "TODO.md") -> TaskManager:
    """Initialize core components and return TaskManager."""
    file_ops = FileOps(todo_path)
    tasks = file_ops.read_tasks()
    return TaskManager(tasks)


def save_changes(manager: TaskManager, todo_path: str = "TODO.md") -> None:
    """Save tasks back to file."""
    file_ops = FileOps(todo_path)
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
