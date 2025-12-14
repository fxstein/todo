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


def complete_command(task_id: str, todo_path: str = "TODO.md"):
    """Complete a task."""
    manager = get_manager(todo_path)
    try:
        task = manager.complete_task(task_id)
        save_changes(manager, todo_path)
        print(f"Completed: #{task.id} {task.description}")
    except ValueError as e:
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
