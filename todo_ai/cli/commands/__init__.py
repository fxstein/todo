from typing import List
from todo_ai.core.task import TaskManager
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
    file_ops = FileOps()
    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)
    
    # ID Generation
    config = Config()
    coordination = CoordinationManager(config)
    last_serial = file_ops.get_last_serial()
    
    # Generate next ID based on mode
    # Note: generate_next_task_id expects current_max_serial
    next_id = coordination.generate_next_task_id(last_serial)
    
    # Check if we need to increment serial file
    # Logic: if ID contains the next serial (last_serial + 1), update file
    # Simplified: Always increment if we generated a new ID
    # But generate_next_task_id assumes we pass it the MAX serial, and it returns MAX+1 formatted
    
    # Update serial file
    file_ops.increment_serial()
    
    task = manager.add_task(description, tags, task_id=next_id)
    file_ops.write_tasks(manager.list_tasks())
    print(f"Added: #{task.id} {task.description}")

def add_subtask_command(parent_id: str, description: str, tags: List[str]):
    """Add a subtask."""
    manager = get_manager()
    try:
        # Subtasks don't use global serial, they are nested under parent
        task = manager.add_subtask(parent_id, description, tags)
        save_changes(manager)
        print(f"Added subtask: #{task.id} {task.description}")
    except ValueError as e:
        print(f"Error: {e}")

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
