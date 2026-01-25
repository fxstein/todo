import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from todo_ai.core.task import Task, TaskStatus


@dataclass(frozen=True)
class FileStructureSnapshot:
    """Immutable snapshot of file structure captured from pristine file.

    This snapshot is captured ONCE when FileOps first reads a file, and
    is never modified, even if the file is re-read after modifications.
    This ensures consistent structure preservation across all operations.
    """

    # Tasks section header format
    tasks_header_format: str  # "# Tasks" or "## Tasks"

    # Blank line preservation
    blank_after_tasks_header: bool  # True if blank line after header
    blank_between_tasks: bool  # True if blank lines between tasks in Tasks section
    blank_after_tasks_section: bool  # True if blank line after Tasks (before other sections)

    # File sections
    header_lines: tuple[str, ...]  # Immutable tuple of header lines
    footer_lines: tuple[str, ...]  # Immutable tuple of footer lines

    # Metadata
    has_original_header: bool  # True if file had header before Tasks section
    metadata_lines: tuple[str, ...]  # HTML comments, relationships, etc.

    # Interleaved content (non-task lines in Tasks section)
    # Key: task_id (of preceding task), Value: tuple[str, ...] (lines of comments/whitespace)
    # Preserves user comments, notes, or other content between tasks
    interleaved_content: dict[str, tuple[str, ...]]

    # Original task order in Tasks section (to preserve order of existing tasks)
    # New tasks (not in this list) should appear first, then existing tasks in this order
    original_task_order: tuple[str, ...]


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
        # Interleaved content (non-task lines in Tasks section) - Phase 10
        # Key: task_id (of preceding task), Value: list[str] (lines of comments/whitespace)
        # Preserves user comments, notes, or other content between tasks
        self.interleaved_content: dict[str, list[str]] = {}

        # Phase 11: Structure snapshot - captured once, never modified
        self._structure_snapshot: FileStructureSnapshot | None = None
        self._snapshot_mtime: float = 0.0  # File modification time when snapshot was captured
        # Used to detect external file modifications (e.g., user edits in editor)
        # If file mtime > snapshot_mtime, snapshot is stale and must be recaptured

        # Ensure config directory exists
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)

    def read_tasks(self) -> list[Task]:
        """Read tasks from TODO.md.

        On first call, captures structure snapshot from pristine file.
        Subsequent calls can re-read tasks, but snapshot remains unchanged unless file is modified externally.
        """
        if not self.todo_path.exists():
            # No file - use default structure
            if self._structure_snapshot is None:
                self._structure_snapshot = self._create_default_snapshot()
            self.header_lines = []
            self.footer_lines = []
            self.metadata_lines = []
            self.relationships = {}
            return []

        # Check if file was modified externally (e.g., by user in editor)
        # If so, invalidate snapshot and recapture
        current_mtime = self.todo_path.stat().st_mtime
        if self._structure_snapshot is None or current_mtime > self._snapshot_mtime:
            self._structure_snapshot = self._capture_structure_snapshot()
            self._snapshot_mtime = current_mtime

        # Reset relationships before parsing (relationships can change)
        self.relationships = {}
        content = self.todo_path.read_text(encoding="utf-8")
        return self._parse_markdown(content)

    def write_tasks(self, tasks: list[Task]) -> None:
        """Write tasks to TODO.md using preserved structure snapshot.

        Args:
            tasks: List of tasks to write
        """
        # Phase 14: Ensure snapshot is available (should always be set by read_tasks())
        if self._structure_snapshot is None:
            # Fallback: read once to get snapshot
            self.read_tasks()

        if self._structure_snapshot is None:
            raise ValueError("Structure snapshot must be available for writing tasks")

        content = self._generate_markdown(tasks, self._structure_snapshot)
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
        self.interleaved_content = {}  # Reset interleaved content for each parse

        # Regex patterns
        # Match [ ], [x], or [D] checkboxes
        task_pattern = re.compile(r"^\s*-\s*\[([ xD])\]\s*\*\*#([0-9\.]+)\*\*\s*(.*)$")
        tag_pattern = re.compile(r"`#([a-zA-Z0-9_-]+)`")
        section_pattern = re.compile(r"^##\s+(.*)$")
        # Also match single # for "Tasks" section (common format)
        single_section_pattern = re.compile(r"^#\s+Tasks\s*$")
        relationship_pattern = re.compile(r"^([0-9\.]+):([a-z-]+):(.+)$")

        # Sections that contain tasks
        TASK_SECTIONS = {"Tasks", "Recently Completed", "Archived Tasks", "Deleted Tasks"}
        in_relationships_section = False
        in_metadata_section = False
        in_metadata_section = False

        for line in lines:
            line_stripped = line.strip()

            # Ignore separator lines
            if line_stripped == "---":
                continue

            # Check for single # Tasks section (common format)
            single_section_match = single_section_pattern.match(line)
            if single_section_match:
                # Preserve the original header line format
                self.tasks_header_format = line
                # If this is the first line (no header), mark that we had no original header
                if not seen_tasks_section and len(self.header_lines) == 0:
                    self.has_original_header = False
                # Blank line detection now handled by snapshot
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
                        # Blank line detection now handled by snapshot
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
                if archive_date_match and (
                    current_section == "Recently Completed" or current_section == "Archived Tasks"
                ):
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
                completed_at = None
                if completed_char.lower() == "x":
                    if (
                        current_section == "Recently Completed"
                        or current_section == "Archived Tasks"
                    ):
                        status = TaskStatus.ARCHIVED
                        # Fix for #204: Treat archived tasks as completed for restore purposes
                        # We use archived_at as completed_at if available, or current time
                        completed_at = archived_at or datetime.now()
                    elif current_section == "Deleted Tasks":
                        status = TaskStatus.DELETED
                    else:
                        status = TaskStatus.COMPLETED
                        completed_at = (
                            datetime.now()
                        )  # Approximate since we don't store separate completed_at in file
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
                if completed_at:
                    task.completed_at = completed_at
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

            # Phase 10: Capture interleaved content (non-task lines in Tasks section)
            # This includes comments or other markdown content between tasks
            # Note: Blank lines are handled by existing blank line logic, not captured here
            # (They will be handled properly in Phase 12 with the snapshot system)
            if current_section in TASK_SECTIONS and current_task and line_stripped:
                # We're in a task section and have a current task
                # This line is not a task, not a note, not a section header, not metadata, and not blank
                # Capture it as interleaved content keyed by the preceding task ID
                if current_task.id not in self.interleaved_content:
                    self.interleaved_content[current_task.id] = []
                self.interleaved_content[current_task.id].append(line)
                continue

            # Ignore empty lines inside task sections to clean up output?
            # Or preserve? If we ignore, we generate standard spacing.
            pass

        return tasks

    def _create_default_snapshot(self) -> FileStructureSnapshot:
        """Create a default structure snapshot for files that don't exist yet."""
        return FileStructureSnapshot(
            tasks_header_format="## Tasks",
            blank_after_tasks_header=True,
            blank_between_tasks=False,
            blank_after_tasks_section=False,
            header_lines=(),
            footer_lines=(),
            has_original_header=False,
            metadata_lines=(),
            interleaved_content={},
            original_task_order=(),
        )

    def _capture_structure_snapshot(self) -> FileStructureSnapshot:
        """Capture structure snapshot from pristine file.

        This is called ONCE when FileOps first reads a file, or when file is modified externally.
        The snapshot is immutable and never modified.
        """
        if not self.todo_path.exists():
            return self._create_default_snapshot()

        content = self.todo_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        # Parse structure elements
        header_lines: list[str] = []
        footer_lines: list[str] = []
        metadata_lines: list[str] = []
        tasks_header_format: str | None = None
        blank_after_tasks_header = False
        blank_between_tasks = False
        blank_after_tasks_section = False
        has_original_header = False
        interleaved_content: dict[str, list[str]] = {}  # Will be converted to tuple

        # Regex patterns
        task_pattern = re.compile(r"^\s*-\s*\[([ xD])\]\s*\*\*#([0-9\.]+)\*\*\s*(.*)$")
        section_pattern = re.compile(r"^##\s+(.*)$")
        single_section_pattern = re.compile(r"^#\s+Tasks\s*$")

        # Sections that contain tasks
        TASK_SECTIONS = {"Tasks", "Recently Completed", "Archived Tasks", "Deleted Tasks"}
        current_section = "Header"
        seen_tasks_section = False
        in_relationships_section = False
        in_metadata_section = False
        current_task_id: str | None = None
        tasks_in_section: list[str] = []  # Track task IDs to detect blank lines between

        for line_idx, line in enumerate(lines):
            line_stripped = line.strip()

            # Ignore separator lines
            if line_stripped == "---":
                continue

            # Check for single # Tasks section
            single_section_match = single_section_pattern.match(line)
            if single_section_match:
                tasks_header_format = line
                if not seen_tasks_section and len(header_lines) == 0:
                    has_original_header = False
                # Check if next line is blank
                if line_idx + 1 < len(lines):
                    next_line = lines[line_idx + 1]
                    if next_line.strip() == "":
                        blank_after_tasks_header = True
                current_section = "Tasks"
                seen_tasks_section = True
                current_task_id = None
                in_metadata_section = False
                continue

            # Check for section header
            section_match = section_pattern.match(line)
            if section_match:
                section_name = section_match.group(1).strip()
                if section_name in TASK_SECTIONS:
                    if (
                        current_section == "Header"
                        and section_name == "Tasks"
                        and len(header_lines) == 0
                    ):
                        has_original_header = False
                    if section_name == "Tasks":
                        tasks_header_format = line
                        blank_after_tasks_header = False
                        if line_idx + 1 < len(lines):
                            next_line = lines[line_idx + 1]
                            if next_line.strip() == "":
                                blank_after_tasks_header = True
                        tasks_in_section = []  # Reset for Tasks section
                    elif section_name == "Recently Completed" or section_name == "Archived Tasks":
                        # Check if there's a blank line before this section (after Tasks)
                        if current_section == "Tasks" and tasks_in_section:
                            if line_idx > 0 and lines[line_idx - 1].strip() == "":
                                blank_after_tasks_section = True
                    current_section = section_name
                    seen_tasks_section = True
                    current_task_id = None
                    in_metadata_section = False
                    continue
                elif section_name == "Task Metadata":
                    in_metadata_section = True
                    metadata_lines.append(line)
                    continue
                else:
                    if current_section != "Header" and not in_metadata_section:
                        current_section = "Footer"

            # Check for Footer start
            if (
                line_stripped == "------------------"
                and current_section != "Header"
                and not in_metadata_section
            ):
                current_section = "Footer"

            # Check for relationships section
            if line_stripped == "<!-- TASK RELATIONSHIPS":
                in_relationships_section = True
                in_metadata_section = True
                metadata_lines.append(line)
                continue

            # Handle metadata section
            if in_metadata_section:
                if line_stripped == "<!-- TASK RELATIONSHIPS":
                    in_relationships_section = True
                    metadata_lines.append(line)
                    continue
                if in_relationships_section:
                    if line_stripped == "-->":
                        in_relationships_section = False
                    metadata_lines.append(line)
                    continue
                else:
                    metadata_lines.append(line)
                    continue

            # Handle Header
            if current_section == "Header":
                header_lines.append(line)
                has_original_header = True
                continue

            # Handle Footer
            if current_section == "Footer":
                footer_lines.append(line)
                continue

            # Handle Task Sections - detect tasks and interleaved content
            task_match = task_pattern.match(line)
            if task_match:
                task_id = task_match.group(2)
                # Check for blank line between tasks
                if current_section == "Tasks" and tasks_in_section:
                    # Check if previous line was blank
                    if line_idx > 0 and lines[line_idx - 1].strip() == "":
                        blank_between_tasks = True
                if current_section == "Tasks":
                    tasks_in_section.append(task_id)
                current_task_id = task_id
                continue

            # Check for notes (blockquotes) - these are part of tasks, not interleaved
            if current_task_id and line_stripped.startswith(">"):
                continue

            # Phase 10: Capture interleaved content (non-task, non-note, non-blank lines)
            if current_section == "Tasks" and current_task_id and line_stripped:
                if current_task_id not in interleaved_content:
                    interleaved_content[current_task_id] = []
                interleaved_content[current_task_id].append(line)
                continue

        return FileStructureSnapshot(
            tasks_header_format=tasks_header_format or "## Tasks",
            blank_after_tasks_header=blank_after_tasks_header,
            blank_between_tasks=blank_between_tasks,
            blank_after_tasks_section=blank_after_tasks_section,
            header_lines=tuple(header_lines),
            footer_lines=tuple(footer_lines),
            has_original_header=has_original_header,
            metadata_lines=tuple(metadata_lines),
            interleaved_content={k: tuple(v) for k, v in interleaved_content.items()},
            original_task_order=tuple(tasks_in_section),
        )

    def _generate_markdown(
        self, tasks: list[Task], snapshot: FileStructureSnapshot | None = None
    ) -> str:
        """Generate TODO.md content from Task objects using structure snapshot.

        Args:
            tasks: List of tasks to generate markdown for
            snapshot: Structure snapshot to use. Must not be None (raises ValueError if None).
        """
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

        # CRITICAL: Do NOT reorder tasks here!
        # Tasks should be written in the exact order they appear in the tasks list.
        # The ADD operation handles putting new tasks at the top BEFORE calling write.
        # All other operations (modify, complete, undo) preserve existing order.
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

        lines: list[str] = []

        # Phase 13: Always use snapshot (no fallback)
        if snapshot is None:
            raise ValueError("Structure snapshot must be available for generation")

        # 1. Header (Enforced Standard)
        lines.extend(
            [
                "# todo.ai ToDo List",
                "",
                "> ⚠️ **MANAGED FILE**: Do not edit manually. Use `todo-ai` (CLI/MCP) or `todo.ai` to manage tasks.",
                "",
            ]
        )

        # 2. Tasks Section
        lines.append("## Tasks")
        # Enforce blank line after header if there are tasks
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

            # Strict indentation: 0, 2, 4 spaces
            indent_level = t.id.count(".")
            if indent_level > 2:
                indent_level = 2  # Max depth 2 (3 levels)
            indent = "  " * indent_level

            # Format description with tags
            description = t.description
            if t.tags:
                # Tags must be wrapped in backticks
                tag_str = " ".join(
                    [f"`{tag}`" if tag.startswith("#") else f"`#{tag}`" for tag in sorted(t.tags)]
                )
                description = f"{description} {tag_str}".strip()

            line = f"{indent}- [{checkbox}] **#{t.id}** {description}"

            # Add completed date for completed tasks
            if t.status == TaskStatus.COMPLETED and t.completed_at:
                completed_date = t.completed_at.strftime("%Y-%m-%d")
                line += f" ({completed_date})"

            # Add deletion metadata for deleted tasks
            if t.status == TaskStatus.DELETED and t.deleted_at and t.expires_at:
                delete_date = t.deleted_at.strftime("%Y-%m-%d")
                expire_date = t.expires_at.strftime("%Y-%m-%d")
                line += f" (deleted {delete_date}, expires {expire_date})"

            for note in t.notes:
                # Strict note formatting: indent + 2 spaces + > + space
                note_indent = indent + "  "
                line += f"\n{note_indent}> {note}"
            return line

        # Add active tasks
        for i, t in enumerate(active_tasks):
            lines.append(format_task(t))
            # Insert interleaved content if any
            if t.id in snapshot.interleaved_content:
                lines.extend(snapshot.interleaved_content[t.id])

            # Spacing Rules:
            # Root tasks: 1 blank line between them
            # Subtasks: 0 blank lines (handled by not adding one here)
            is_root = "." not in t.id
            is_last = i == len(active_tasks) - 1
            if is_root and not is_last:
                # Check if next task is also root
                next_task = active_tasks[i + 1]
                if "." not in next_task.id:
                    lines.append("")

        # 3. Archived Tasks Section
        if archived_tasks:
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append("## Archived Tasks")
            for t in archived_tasks:
                task_line = format_task(t)
                # Add archive date if present (shell script format)
                if t.archived_at:
                    archive_date = t.archived_at.strftime("%Y-%m-%d")
                    # Insert date before notes (if any) or at end
                    if "\n" in task_line:
                        # Has notes - insert date before first note line
                        parts = task_line.split("\n", 1)
                        # Check if date already exists (e.g. completed date)
                        if f"({archive_date})" not in parts[0]:
                            task_line = f"{parts[0]} ({archive_date})\n{parts[1]}"
                    else:
                        if f"({archive_date})" not in task_line:
                            task_line = f"{task_line} ({archive_date})"
                lines.append(task_line)

        # 4. Deleted Tasks Section
        if deleted_tasks:
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append("## Deleted Tasks")
            for t in deleted_tasks:
                lines.append(format_task(t))

        # 5. Task Metadata Section (if relationships exist or section was present)
        metadata_lines_to_use = snapshot.metadata_lines
        if self.relationships or metadata_lines_to_use:
            lines.append("")
            lines.append("---")
            lines.append("")
            # If we have relationships, write them
            if self.relationships:
                # Check if metadata section header exists in preserved lines
                has_metadata_header = any(
                    "## Task Metadata" in line for line in metadata_lines_to_use
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
                if metadata_lines_to_use:
                    lines.extend(metadata_lines_to_use)

        # 6. Footer (Enforced Standard)
        lines.extend(
            [
                "",
                "---",
                f"**todo-ai (mcp)** v3.0.0 | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ]
        )

        return "\n".join(lines) + "\n"
