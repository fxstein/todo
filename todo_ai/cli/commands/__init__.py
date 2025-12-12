from typing import List, Optional
from todo_ai.core.task import TaskManager, Task
from todo_ai.core.file_ops import FileOps
from todo_ai.core.config import Config
from todo_ai.core.coordination import CoordinationManager

def get_manager() -> TaskManager:
    """Initialize core components and return TaskManager."""
    # TODO: Load from config
    file_ops = FileOps()
    tasks = file_ops.read_tasks()
    return TaskManager(tasks)

def save_changes(manager: TaskManager) -> None:
    """Save tasks back to file."""
    file_ops = FileOps()
    tasks = manager.list_tasks()
    file_ops.write_tasks(tasks)

def add_command(description: str, tags: List[str]):
    """Add a new task."""
    manager = get_manager()
    task = manager.add_task(description, tags)
    save_changes(manager)
    print(f"Added: #{task.id} {task.description}")

def complete_command(task_id: str):
    """Complete a task."""
    manager = get_manager()
    try:
        task = manager.complete_task(task_id)
        save_changes(manager)
        print(f"Completed: #{task.id} {task.description}")
    except ValueError as e:
        print(f"Error: {e}")

def list_command(status: str = None, tag: str = None):
    """List tasks."""
    manager = get_manager()
    filters = {}
    if status:
        filters["status"] = status
    if tag:
        filters["tag"] = tag
        
    tasks = manager.list_tasks(filters)
    if not tasks:
        print("No tasks found.")
        return
        
    for task in tasks:
        checkbox = "[x]" if task.status.value != "pending" else "[ ]"
        print(f"{checkbox} #{task.id} {task.description}")

