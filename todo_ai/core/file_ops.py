import re
from datetime import datetime
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
        self.metadata_lines: list[str] = []
        self.relationships: dict[
            str, dict[str, list[str]]
        ] = {}  # task_id -> {rel_type -> [targets]}
        self.tasks_header_format: str | None = None  # Preserve original Tasks section header format
        self.deleted_task_formats: dict[
            str, str
        ] = {}  # task_id -> original checkbox format (" ", "D", "x")
        self.has_original_header: bool = (
            False  # Track if file had a header before first task section
        )
        self.tasks_header_has_blank_line: bool = (
            False  # Track if original file had blank line after Tasks header
        )
        self.tasks_had_blank_between: bool = (
            False  # Track if original file had blank lines between tasks in Tasks section
        )

        # Ensure config directory exists
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)

    def read_tasks(self) -> list[Task]:
        """Read tasks from TODO.md."""
        if not self.todo_path.exists():
            self.header_lines = []
            self.footer_lines = []
            self.metadata_lines = []
            self.relationships = {}
            return []

        # Reset relationships before parsing
        self.relationships = {}
        content = self.todo_path.read_text(encoding="utf-8")
        return self._parse_markdown(content)

    def write_tasks(self, tasks: list[Task], preserve_blank_line_state: bool = True) -> None:
        """Write tasks to TODO.md.

        Args:
            tasks: List of tasks to write
            preserve_blank_line_state: If True, check current file state before writing
                to preserve blank line format (helps match shell script behavior)
        """
        # Before writing, check current file state for blank line after ## Tasks
        # This helps match shell script behavior (e.g., restore inserts directly)
        if preserve_blank_line_state and self.todo_path.exists() and self.tasks_header_format:
            try:
                current_content = self.todo_path.read_text(encoding="utf-8")
                current_lines = current_content.splitlines()
                for i, line in enumerate(current_lines):
                    if (
                        line == self.tasks_header_format
                        or line.strip() == self.tasks_header_format.strip()
                    ):
                        if i + 1 < len(current_lines):
                            next_line = current_lines[i + 1]
                            # If current file has no blank line (task follows directly),
                            # don't add one (matches shell restore/add behavior)
                            if next_line.strip().startswith("- ["):
                                self.tasks_header_has_blank_line = False
                                break
                            elif next_line.strip() == "":
                                # Check if line after blank is a task
                                if i + 2 < len(current_lines) and current_lines[
                                    i + 2
                                ].strip().startswith("- ["):
                                    self.tasks_header_has_blank_line = True
                                    break
                        break
            except Exception:
                # If we can't read the file, use existing detection
                pass

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

    def get_relationships(self, task_id: str) -> dict[str, list[str]]:
        """Get all relationships for a task."""
        return self.relationships.get(task_id, {})

    def add_relationship(self, task_id: str, rel_type: str, target_ids: list[str]) -> None:
        """Add a relationship for a task."""
        if task_id not in self.relationships:
            self.relationships[task_id] = {}
        # Replace existing relationship of this type
        self.relationships[task_id][rel_type] = target_ids

    def _parse_markdown(self, content: str) -> list[Task]:
        """Parse TODO.md content into Task objects."""
        tasks = []
        lines = content.splitlines()

        current_task: Task | None = None
        current_section = "Header"  # Start in Header mode
        seen_tasks_section = False  # Track if we've seen any task section

        self.header_lines = []
        self.footer_lines = []
        self.metadata_lines = []
        self.relationships = {}  # Will be populated during parsing

        # Regex patterns
        # Match [ ], [x], or [D] checkboxes
        task_pattern = re.compile(r"^\s*-\s*\[([ xD])\]\s*\*\*#([0-9\.]+)\*\*\s*(.*)$")
        tag_pattern = re.compile(r"`#([a-zA-Z0-9_-]+)`")
        section_pattern = re.compile(r"^##\s+(.*)$")
        # Also match single # for "Tasks" section (common format)
        single_section_pattern = re.compile(r"^#\s+Tasks\s*$")
        relationship_pattern = re.compile(r"^([0-9\.]+):([a-z-]+):(.+)$")

        # Sections that contain tasks
        TASK_SECTIONS = {"Tasks", "Recently Completed", "Deleted Tasks"}
        in_relationships_section = False
        in_metadata_section = False
        in_metadata_section = False

        for line_idx, line in enumerate(lines):
            line_stripped = line.strip()

            # Check for single # Tasks section (common format)
            single_section_match = single_section_pattern.match(line)
            if single_section_match:
                # Preserve the original header line format
                self.tasks_header_format = line
                # If this is the first line (no header), mark that we had no original header
                if not seen_tasks_section and len(self.header_lines) == 0:
                    self.has_original_header = False
                # Check if next line is blank (preserve blank line format)
                if line_idx + 1 < len(lines):
                    next_line = lines[line_idx + 1]
                    if next_line.strip() == "":
                        self.tasks_header_has_blank_line = True
                # Don't add to header_lines - it's the tasks section header, not a header line
                # We'll write it separately in _generate_markdown
                current_section = "Tasks"
                seen_tasks_section = True
                current_task = None
                in_metadata_section = False
                continue

            # Check for section header
            section_match = section_pattern.match(line)
            if section_match:
                section_name = section_match.group(1).strip()
                if section_name in TASK_SECTIONS:
                    # If this is the first section and we're still in Header, mark no original header
                    if (
                        current_section == "Header"
                        and section_name == "Tasks"
                        and len(self.header_lines) == 0
                    ):
                        self.has_original_header = False
                    # Check if this is Tasks section and next line is blank or a task
                    if section_name == "Tasks":
                        self.tasks_header_format = line
                        # Reset blank line detection - we'll check the next line
                        self.tasks_header_has_blank_line = False
                        if line_idx + 1 < len(lines):
                            next_line = lines[line_idx + 1]
                            if next_line.strip() == "":
                                self.tasks_header_has_blank_line = True
                            # If next line is a task (starts with "- ["), no blank line after header
                            elif next_line.strip().startswith("- ["):
                                self.tasks_header_has_blank_line = False
                    current_section = section_name
                    seen_tasks_section = True
                    current_task = None
                    in_metadata_section = False
                    continue
                elif section_name == "Task Metadata":
                    in_metadata_section = True
                    self.metadata_lines.append(line)
                    continue
                else:
                    # Unknown section? Treat as footer if we've already seen tasks?
                    # Or treat as content if in Header?
                    # For now, if we are past "Tasks", any unknown section might be footer
                    if current_section != "Header" and not in_metadata_section:
                        current_section = "Footer"

            # Check for Footer start via separator
            if (
                line_stripped == "------------------"
                and current_section != "Header"
                and not in_metadata_section
            ):
                current_section = "Footer"

            # Check for relationships section directly (even without Task Metadata header)
            if line_stripped == "<!-- TASK RELATIONSHIPS":
                in_relationships_section = True
                in_metadata_section = True
                self.metadata_lines.append(line)
                continue

            # Handle metadata section
            if in_metadata_section:
                # Check for Task Metadata section
                if line_stripped == "<!-- TASK RELATIONSHIPS":
                    in_relationships_section = True
                    self.metadata_lines.append(line)
                    continue

                if in_relationships_section:
                    if line_stripped == "-->":
                        in_relationships_section = False
                        self.metadata_lines.append(line)
                        continue
                    # Parse relationship line: task_id:rel_type:targets
                    rel_match = relationship_pattern.match(line_stripped)
                    if rel_match:
                        task_id, rel_type, targets = rel_match.groups()
                        if task_id not in self.relationships:
                            self.relationships[task_id] = {}
                        # Targets can be space-separated list
                        target_list = [t.strip() for t in targets.split() if t.strip()]
                        self.relationships[task_id][rel_type] = target_list
                    self.metadata_lines.append(line)
                    continue
                else:
                    # Other metadata lines (descriptions, etc.)
                    self.metadata_lines.append(line)
                    continue

            # Handle Header
            if current_section == "Header":
                self.header_lines.append(line)
                self.has_original_header = True
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

                # Extract tags and remove them from description
                tags = set()
                tag_matches = tag_pattern.findall(description)
                for tag in tag_matches:
                    tags.add(tag)

                # Remove tags from description (format: `#tag`)
                if tag_matches:
                    description = tag_pattern.sub("", description).strip()

                # Parse archive date if present: (YYYY-MM-DD) at end of description
                archived_at = None
                archive_date_match = re.search(r" \(([0-9]{4}-[0-9]{2}-[0-9]{2})\)$", description)
                if archive_date_match and current_section == "Recently Completed":
                    try:
                        archived_at = datetime.strptime(archive_date_match.group(1), "%Y-%m-%d")
                        # Remove date from description
                        description = re.sub(
                            r" \(([0-9]{4}-[0-9]{2}-[0-9]{2})\)$", "", description
                        ).strip()
                    except ValueError:
                        pass

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

                # Check for [D] checkbox (deleted tasks) - overrides status
                if completed_char.upper() == "D":
                    status = TaskStatus.DELETED

                # Parse deletion metadata if present: (deleted YYYY-MM-DD, expires YYYY-MM-DD)
                deleted_at = None
                expires_at = None
                if status == TaskStatus.DELETED or current_section == "Deleted Tasks":
                    deletion_match = re.search(
                        r"\(deleted ([0-9]{4}-[0-9]{2}-[0-9]{2}), expires ([0-9]{4}-[0-9]{2}-[0-9]{2})\)",
                        description,
                    )
                    if deletion_match:
                        try:
                            deleted_at = datetime.strptime(deletion_match.group(1), "%Y-%m-%d")
                            expires_at = datetime.strptime(deletion_match.group(2), "%Y-%m-%d")
                            # Remove deletion metadata from description
                            description = re.sub(
                                r" *\(deleted [0-9]{4}-[0-9]{2}-[0-9]{2}, expires [0-9]{4}-[0-9]{2}-[0-9]{2}\)",
                                "",
                                description,
                            ).strip()
                            status = TaskStatus.DELETED
                        except ValueError:
                            pass

                task = Task(id=task_id, description=description.strip(), status=status, tags=tags)
                if deleted_at:
                    task.deleted_at = deleted_at
                if expires_at:
                    task.expires_at = expires_at
                if archived_at:
                    task.archived_at = archived_at
                # Preserve original checkbox format for deleted tasks (for tasks already in Deleted section)
                if status == TaskStatus.DELETED and current_section == "Deleted Tasks":
                    self.deleted_task_formats[task_id] = completed_char
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
        # Archived tasks: sort by archive date (most recent first), then by ID (reverse)
        archived_tasks.sort(
            key=lambda t: (
                t.archived_at if t.archived_at else datetime.min,
                -int(t.id.split(".")[0]) if t.id.split(".")[0].isdigit() else 0,
            ),
            reverse=True,
        )
        # Deleted tasks: sort by deletion date (most recent first), then by ID (reverse)
        # Tasks without deletion date go last
        deleted_tasks.sort(
            key=lambda t: (
                t.deleted_at if t.deleted_at else datetime.min,
                -int(t.id.split(".")[0]) if t.id.split(".")[0].isdigit() else 0,
            ),
            reverse=True,
        )

        lines = []

        # 1. Header (use preserved or default)
        if self.header_lines:
            lines.extend(self.header_lines)
            # Ensure spacing before Tasks section if header doesn't end with blank line
            if lines and lines[-1].strip() != "":
                lines.append("")
        elif not self.tasks_header_format and self.has_original_header:
            # Only add default header if file had an original header (not if it started with Tasks section)
            lines = [
                "# todo.ai ToDo List",
                "",
                "> **⚠️ IMPORTANT: This file should ONLY be edited through the `todo.ai` script!**",
                "",
            ]
            # Ensure spacing before Tasks
            if lines and lines[-1].strip() != "":
                lines.append("")
        # If tasks_header_format exists and no other header, file started with Tasks section - preserve that

        # 2. Tasks Section - preserve original format if found
        if self.tasks_header_format:
            lines.append(self.tasks_header_format)
            # Match shell script behavior:
            # - If original had blank line, preserve it (always add blank line if tasks exist)
            # - If original had no blank line (e.g., after restore inserted directly), don't add one
            # BUT: shell restore inserts directly, but preserves existing blank lines between tasks
            # So if we detect no blank line after header but there are multiple tasks,
            # the blank line was between tasks, not after header
            if self.tasks_header_has_blank_line and active_tasks:
                # Original had blank line - preserve it
                lines.append("")
            # If original had no blank line, don't add one (matches shell restore behavior)
            # The blank line between tasks will be preserved by the existing file structure
        else:
            lines.append("## Tasks")
            # Add blank line after Tasks header if there are tasks (shell script format)
            if active_tasks:
                lines.append("")

        def format_task(t: Task) -> str:
            # Determine checkbox
            if t.status == TaskStatus.DELETED:
                # Use preserved format if available, otherwise use [D] for newly deleted tasks
                if t.id in self.deleted_task_formats:
                    checkbox = self.deleted_task_formats[t.id]  # Preserve original format
                elif t.deleted_at and t.expires_at:
                    checkbox = "D"  # Use [D] for newly deleted tasks with metadata
                else:
                    checkbox = " "  # Preserve [ ] for old deleted tasks without metadata
            elif t.status != TaskStatus.PENDING:
                checkbox = "x"
            else:
                checkbox = " "

            indent = "  " * (t.id.count("."))

            # Format description with tags
            description = t.description
            if t.tags:
                tag_str = " ".join([f"`#{tag}`" for tag in sorted(t.tags)])
                description = f"{description} {tag_str}".strip()

            line = f"{indent}- [{checkbox}] **#{t.id}** {description}"

            # Add deletion metadata for deleted tasks (shell script format)
            if t.status == TaskStatus.DELETED and t.deleted_at and t.expires_at:
                delete_date = t.deleted_at.strftime("%Y-%m-%d")
                expire_date = t.expires_at.strftime("%Y-%m-%d")
                line += f" (deleted {delete_date}, expires {expire_date})"

            for note in t.notes:
                line += f"\n{indent}  > {note}"
            return line

        # Add tasks
        # Check if we need to preserve blank lines between tasks (for restore/add operations)
        preserve_task_blanks = False
        if not self.tasks_header_has_blank_line and len(active_tasks) > 1:
            # No blank line after header, but multiple tasks - check if original had blanks between
            # This happens when restore/add inserts directly but preserves existing structure
            if self.todo_path.exists():
                try:
                    current_content = self.todo_path.read_text(encoding="utf-8")
                    current_lines = current_content.splitlines()
                    in_tasks = False
                    task_count = 0
                    for i, line in enumerate(current_lines):
                        if line == self.tasks_header_format or (
                            self.tasks_header_format
                            and line.strip() == self.tasks_header_format.strip()
                        ):
                            in_tasks = True
                            continue
                        if in_tasks and line.strip().startswith("- ["):
                            task_count += 1
                            # Check if there's a blank line after this task (before next task or section)
                            if i + 1 < len(current_lines):
                                next_line = current_lines[i + 1]
                                if next_line.strip() == "":
                                    # Check if line after blank is another task
                                    if i + 2 < len(current_lines) and current_lines[
                                        i + 2
                                    ].strip().startswith("- ["):
                                        preserve_task_blanks = True
                                        break
                        elif in_tasks and line.strip().startswith("## "):
                            # Hit next section, stop checking
                            break
                except Exception:
                    pass

        for i, t in enumerate(active_tasks):
            lines.append(format_task(t))
            # Add blank line between tasks if we're preserving them (for restore/add operations)
            if preserve_task_blanks and i < len(active_tasks) - 1:
                lines.append("")

        # Add blank line after Tasks section if there are tasks AND other sections exist
        # (shell script format - only add blank line if there are sections after Tasks)
        if active_tasks and (archived_tasks or deleted_tasks):
            lines.append("")

        # 3. Recently Completed Section
        if archived_tasks:
            lines.append("## Recently Completed")
            for t in archived_tasks:
                task_line = format_task(t)
                # Add archive date if present (shell script format)
                if t.archived_at:
                    archive_date = t.archived_at.strftime("%Y-%m-%d")
                    # Insert date before notes (if any) or at end
                    if "\n" in task_line:
                        # Has notes - insert date before first note line
                        parts = task_line.split("\n", 1)
                        task_line = f"{parts[0]} ({archive_date})\n{parts[1]}"
                    else:
                        task_line = f"{task_line} ({archive_date})"
                lines.append(task_line)
            lines.append("")

        # 4. Deleted Tasks Section
        if deleted_tasks:
            # Add blank line before Deleted Tasks section if Recently Completed section exists
            if archived_tasks and lines and lines[-1].strip() != "":
                lines.append("")
            lines.append("## Deleted Tasks")
            for t in deleted_tasks:
                lines.append(format_task(t))

        # 5. Task Metadata Section (if relationships exist or section was present)
        if self.relationships or self.metadata_lines:
            if lines[-1].strip() != "":
                lines.append("")
            # If we have relationships, write them
            if self.relationships:
                # Check if metadata section header exists in preserved lines
                has_metadata_header = any(
                    "## Task Metadata" in line for line in self.metadata_lines
                )
                if not has_metadata_header:
                    lines.append("## Task Metadata")
                    lines.append("")
                    lines.append("Task relationships and dependencies (managed by todo.ai tool).")
                    lines.append("View with: `./todo.ai show <task-id>`")
                    lines.append("")
                lines.append("<!-- TASK RELATIONSHIPS")
                # Write relationships
                for task_id in sorted(self.relationships.keys()):
                    for rel_type in sorted(self.relationships[task_id].keys()):
                        targets = " ".join(self.relationships[task_id][rel_type])
                        lines.append(f"{task_id}:{rel_type}:{targets}")
                lines.append("-->")
            else:
                # Preserve existing metadata section if no relationships
                if self.metadata_lines:
                    lines.extend(self.metadata_lines)

        # 6. Footer (use preserved)
        if self.footer_lines:
            # Ensure spacing
            if lines[-1].strip() != "":
                lines.append("")
            lines.extend(self.footer_lines)

        return "\n".join(lines) + "\n"
