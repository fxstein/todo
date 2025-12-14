import re
from pathlib import Path

from todo_ai.core.task import Task, TaskStatus


class FileOps:
    """Handles file operations for TODO.md and .todo.ai directory."""

    def __init__(self, todo_path: str = "TODO.md"):
        self.todo_path = Path(todo_path)
        self.config_dir = self.todo_path.parent / ".todo.ai"
        self.serial_path = self.config_dir / ".todo.ai.serial"

        # State to preserve file structure
        self.header_lines: list[str] = []
        self.footer_lines: list[str] = []

        # Ensure config directory exists
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)

    def read_tasks(self) -> list[Task]:
        """Read tasks from TODO.md."""
        if not self.todo_path.exists():
            self.header_lines = []
            self.footer_lines = []
            return []

        content = self.todo_path.read_text(encoding="utf-8")
        return self._parse_markdown(content)

    def write_tasks(self, tasks: list[Task]) -> None:
        """Write tasks to TODO.md."""
        content = self._generate_markdown(tasks)
        self.todo_path.write_text(content, encoding="utf-8")

    def get_serial(self) -> int:
        """Get the current serial number from file."""
        if not self.serial_path.exists():
            return 0

        try:
            return int(self.serial_path.read_text().strip())
        except ValueError:
            return 0

    def set_serial(self, value: int) -> None:
        """Set the serial number in file."""
        self.serial_path.write_text(str(value))

    def _parse_markdown(self, content: str) -> list[Task]:
        """Parse TODO.md content into Task objects."""
        tasks = []
        lines = content.splitlines()

        current_task: Task | None = None
        current_section = "Header"  # Start in Header mode

        self.header_lines = []
        self.footer_lines = []

        # Regex patterns
        task_pattern = re.compile(r"^\s*-\s*\[([ x])\]\s*\*\*#([0-9\.]+)\*\*\s*(.*)$")
        tag_pattern = re.compile(r"`#([a-zA-Z0-9_-]+)`")
        section_pattern = re.compile(r"^##\s+(.*)$")

        # Sections that contain tasks
        TASK_SECTIONS = {"Tasks", "Recently Completed", "Deleted Tasks"}

        for line in lines:
            line_stripped = line.strip()

            # Check for section header
            section_match = section_pattern.match(line)
            if section_match:
                section_name = section_match.group(1).strip()
                if section_name in TASK_SECTIONS:
                    current_section = section_name
                    current_task = None
                    continue
                else:
                    # Unknown section? Treat as footer if we've already seen tasks?
                    # Or treat as content if in Header?
                    # For now, if we are past "Tasks", any unknown section might be footer
                    if current_section != "Header":
                        current_section = "Footer"

            # Check for Footer start via separator
            if line_stripped == "------------------" and current_section != "Header":
                current_section = "Footer"

            # Handle Header
            if current_section == "Header":
                self.header_lines.append(line)
                continue

            # Handle Footer
            if current_section == "Footer":
                self.footer_lines.append(line)
                continue

            # Handle Task Sections
            # Check for task/subtask
            task_match = task_pattern.match(line)

            if task_match:
                completed_char, task_id, description = task_match.groups()

                # Extract tags
                tags = set()
                tag_matches = tag_pattern.findall(description)
                for tag in tag_matches:
                    tags.add(tag)

                # Determine status
                status = TaskStatus.PENDING
                if completed_char.lower() == "x":
                    if current_section == "Recently Completed":
                        status = TaskStatus.ARCHIVED
                    elif current_section == "Deleted Tasks":
                        status = TaskStatus.DELETED
                    else:
                        status = TaskStatus.COMPLETED
                elif current_section == "Deleted Tasks":
                    status = TaskStatus.DELETED

                task = Task(id=task_id, description=description.strip(), status=status, tags=tags)
                tasks.append(task)
                current_task = task
                continue

            # Check for notes
            if current_task and line_stripped.startswith(">"):
                note_content = line_stripped[1:].strip()
                current_task.add_note(note_content)
                continue

            # Ignore empty lines inside task sections to clean up output?
            # Or preserve? If we ignore, we generate standard spacing.
            pass

        return tasks

    def _generate_markdown(self, tasks: list[Task]) -> str:
        """Generate TODO.md content from Task objects."""
        # Organize tasks by section
        active_tasks = []
        archived_tasks = []
        deleted_tasks = []

        for task in tasks:
            if task.status == TaskStatus.PENDING:
                active_tasks.append(task)
            elif task.status == TaskStatus.COMPLETED:
                active_tasks.append(task)
            elif task.status == TaskStatus.ARCHIVED:
                archived_tasks.append(task)
            elif task.status == TaskStatus.DELETED:
                deleted_tasks.append(task)

        # Sort tasks
        def sort_key(t):
            parts = [int(p) for p in t.id.split(".")]
            return parts

        active_tasks.sort(key=sort_key)
        archived_tasks.sort(key=sort_key, reverse=True)
        deleted_tasks.sort(key=sort_key, reverse=True)

        lines = []

        # 1. Header (use preserved or default)
        if self.header_lines:
            lines.extend(self.header_lines)
        else:
            lines = [
                "# todo.ai ToDo List",
                "",
                "> **⚠️ IMPORTANT: This file should ONLY be edited through the `todo.ai` script!**",
                "",
            ]

        # Ensure spacing before Tasks
        if lines and lines[-1].strip() != "":
            lines.append("")

        # 2. Tasks Section
        lines.append("## Tasks")

        def format_task(t: Task) -> str:
            checkbox = (
                "x" if t.status != TaskStatus.PENDING and t.status != TaskStatus.DELETED else " "
            )
            if t.status == TaskStatus.DELETED:
                checkbox = " "

            indent = "  " * (t.id.count("."))
            line = f"{indent}- [{checkbox}] **#{t.id}** {t.description}"

            for note in t.notes:
                line += f"\n{indent}  > {note}"
            return line

        for t in active_tasks:
            lines.append(format_task(t))

        lines.append("")

        # 3. Recently Completed Section
        lines.append("## Recently Completed")
        for t in archived_tasks:
            lines.append(format_task(t))

        lines.append("")

        # 4. Deleted Tasks Section
        lines.append("## Deleted Tasks")
        for t in deleted_tasks:
            lines.append(format_task(t))

        # 5. Footer (use preserved)
        if self.footer_lines:
            # Ensure spacing
            if lines[-1].strip() != "":
                lines.append("")
            lines.extend(self.footer_lines)

        return "\n".join(lines) + "\n"
