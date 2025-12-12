import re
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from todo_ai.core.task import Task, TaskStatus

class FileOps:
    """Handles file operations for TODO.md and .todo.ai directory."""
    
    def __init__(self, todo_path: str = "TODO.md"):
        self.todo_path = Path(todo_path)
        self.config_dir = self.todo_path.parent / ".todo.ai"
        self.serial_path = self.config_dir / ".todo.ai.serial"
        
        # Ensure config directory exists
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)

    def read_tasks(self) -> List[Task]:
        """Read tasks from TODO.md."""
        if not self.todo_path.exists():
            return []
            
        content = self.todo_path.read_text(encoding="utf-8")
        return self._parse_markdown(content)

    def write_tasks(self, tasks: List[Task]) -> None:
        """Write tasks to TODO.md."""
        content = self._generate_markdown(tasks)
        self.todo_path.write_text(content, encoding="utf-8")

    def get_next_serial(self) -> int:
        """Get and increment the serial number."""
        if not self.serial_path.exists():
            self.serial_path.write_text("1")
            return 1
            
        try:
            current = int(self.serial_path.read_text().strip())
        except ValueError:
            current = 0
            
        next_serial = current + 1
        self.serial_path.write_text(str(next_serial))
        return next_serial

    def _parse_markdown(self, content: str) -> List[Task]:
        """Parse TODO.md content into Task objects."""
        tasks = []
        lines = content.splitlines()
        
        current_task: Optional[Task] = None
        current_section = "Tasks"  # Default section
        
        # Regex patterns
        task_pattern = re.compile(r'^\s*-\s*\[([ x])\]\s*\*\*#([0-9\.]+)\*\*\s*(.*)$')
        subtask_pattern = re.compile(r'^\s*-\s*\[([ x])\]\s*\*\*#([0-9\.]+)\*\*\s*(.*)$') # Same as task for now
        tag_pattern = re.compile(r'`#([a-zA-Z0-9_-]+)`')
        section_pattern = re.compile(r'^##\s+(.*)$')
        
        for line in lines:
            line_stripped = line.strip()
            
            # Check for section header
            section_match = section_pattern.match(line)
            if section_match:
                current_section = section_match.group(1).strip()
                current_task = None
                continue
                
            # Check for task/subtask
            # Note: We rely on indentation/logic to distinguish, but for flat parsing 
            # we just grab the ID. The regex handles indentation in the prefix \s*
            task_match = task_pattern.match(line)
            
            if task_match:
                completed_char, task_id, description = task_match.groups()
                
                # Extract tags
                tags = set()
                tag_matches = tag_pattern.findall(description)
                for tag in tag_matches:
                    tags.add(tag)
                    # Remove tag from description for cleaner storage? 
                    # Existing shell script keeps them in description text but valid tags are marked.
                    # We'll keep them in description to preserve original text format.
                
                # Determine status based on checkbox and section
                status = TaskStatus.PENDING
                if completed_char.lower() == 'x':
                    if current_section == "Recently Completed":
                        status = TaskStatus.ARCHIVED
                    elif current_section == "Deleted Tasks":
                        status = TaskStatus.DELETED
                    else:
                        status = TaskStatus.COMPLETED
                elif current_section == "Deleted Tasks":
                     status = TaskStatus.DELETED
                
                # Create task object
                task = Task(
                    id=task_id,
                    description=description.strip(),
                    status=status,
                    tags=tags
                )
                tasks.append(task)
                current_task = task
                continue
            
            # Check for notes (lines starting with >)
            if current_task and line_stripped.startswith(">"):
                note_content = line_stripped[1:].strip()
                current_task.add_note(note_content)
                
        return tasks

    def _generate_markdown(self, tasks: List[Task]) -> str:
        """Generate TODO.md content from Task objects."""
        # Organize tasks by section
        active_tasks = []
        completed_tasks = [] # In "Tasks" section but checked
        archived_tasks = []  # In "Recently Completed"
        deleted_tasks = []   # In "Deleted Tasks"
        
        for task in tasks:
            if task.status == TaskStatus.PENDING:
                active_tasks.append(task)
            elif task.status == TaskStatus.COMPLETED:
                active_tasks.append(task) # Completed but not archived yet
            elif task.status == TaskStatus.ARCHIVED:
                archived_tasks.append(task)
            elif task.status == TaskStatus.DELETED:
                deleted_tasks.append(task)
        
        # Sort tasks by ID (numerical/hierarchical)
        def sort_key(t):
            parts = [int(p) for p in t.id.split('.')]
            return parts

        active_tasks.sort(key=sort_key)
        archived_tasks.sort(key=sort_key, reverse=True) # Usually recent first
        deleted_tasks.sort(key=sort_key, reverse=True)
        
        lines = ["# todo.ai ToDo List", "", 
                 "> **⚠️ IMPORTANT: This file should ONLY be edited through the `todo.ai` script!**", 
                 "", "## Tasks"]
        
        def format_task(t: Task) -> str:
            checkbox = "x" if t.status != TaskStatus.PENDING and t.status != TaskStatus.DELETED else " "
            # Handle deleted status which might have unchecked box in some conventions, 
            # but usually deleted tasks are just listed. 
            # Existing script: deleted tasks often have [ ] or [x] depending on state when deleted?
            # Let's standardize: Deleted = [ ] usually unless it was completed then deleted.
            # For simplicity, if status is DELETED, we check if it was completed before?
            # The Task model has completed_at. 
            # For now, let's just use [ ] for deleted pending, [x] for deleted completed if we track that.
            # Simplified: PENDING=[ ], COMPLETED=[x], ARCHIVED=[x], DELETED=[ ] (usually)
            
            if t.status == TaskStatus.DELETED:
                 # Check if it looks completed in description or logic? 
                 # Default to [ ] for deleted items to differentiate from archived
                 checkbox = " "
            
            # Indentation for subtasks
            indent = "  " * (t.id.count('.'))
            
            line = f"{indent}- [{checkbox}] **#{t.id}** {t.description}"
            
            # Add notes
            for note in t.notes:
                line += f"\n{indent}  > {note}"
                
            return line

        for t in active_tasks:
            lines.append(format_task(t))
            
        lines.append("")
        lines.append("## Recently Completed")
        for t in archived_tasks:
            lines.append(format_task(t))
            
        lines.append("")
        lines.append("## Deleted Tasks")
        for t in deleted_tasks:
            lines.append(format_task(t))
            
        return "\n".join(lines) + "\n"

