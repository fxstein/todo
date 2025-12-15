import os
import re
import subprocess
from pathlib import Path

from todo_ai.cli.config_ops import (
    detect_coordination_command,
    list_mode_backups_command,
    rollback_mode_command,
    setup_coordination_command,
    setup_wizard_command,
    show_config_command,
    switch_mode_command,
)
from todo_ai.cli.system_ops import (
    create_backup,
    list_backups_command,
    rollback_command,
    update_command,
    view_log_command,
)
from todo_ai.cli.utility_ops import (
    report_bug_command,
    uninstall_command,
    version_command,
)
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
    # Phase 13: Get blank line state from snapshot instead of old state variables
    original_had_blank_after_header = (
        file_ops._structure_snapshot.blank_after_tasks_header
        if file_ops._structure_snapshot
        else False
    )

    manager = TaskManager(tasks)

    # ID Generation
    config_path = Path(todo_path).parent / ".todo.ai" / "config.yaml"
    config = Config(str(config_path))
    coord_manager = CoordinationManager(config)
    new_id = coord_manager.get_next_task_id(manager, file_ops)

    # Create task
    task = manager.add_task(description, tags, task_id=new_id)

    # Phase 13: Structure preservation is handled by snapshot automatically
    # Manual file editing will be removed in Phase 14
    file_ops.write_tasks(manager.list_tasks(), preserve_blank_line_state=False)

    # After writing, if original had blank after header, ensure blank line between first two tasks
    # This matches shell script behavior: preserves original structure
    if original_had_blank_after_header and len(manager.list_tasks()) >= 2:
        content = Path(todo_path).read_text(encoding="utf-8")
        lines = content.splitlines()

        # Find ## Tasks header
        tasks_header_idx = None
        for i, line in enumerate(lines):
            if line.strip() == "## Tasks" or line.strip() == "# Tasks":
                tasks_header_idx = i
                break

        if tasks_header_idx is not None:
            # Find first two tasks after header
            first_task_idx = None
            second_task_idx = None
            for i in range(tasks_header_idx + 1, len(lines)):
                if lines[i].strip().startswith("- ["):
                    if first_task_idx is None:
                        first_task_idx = i
                    elif second_task_idx is None:
                        second_task_idx = i
                        break

            # If we have two tasks and no blank line between them, add one
            if first_task_idx is not None and second_task_idx is not None:
                # Check if there's already a blank line between them
                has_blank_between = False
                for j in range(first_task_idx + 1, second_task_idx):
                    if lines[j].strip() == "":
                        has_blank_between = True
                        break

                if not has_blank_between:
                    # Insert blank line before second task
                    lines.insert(second_task_idx, "")
                    Path(todo_path).write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Phase 13: Structure preservation is handled automatically by snapshot

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


def add_subtask_command(
    parent_id: str, description: str, tags: list[str], todo_path: str = "TODO.md"
):
    """Add a subtask to an existing task."""
    file_ops = FileOps(todo_path)
    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)
    try:
        parent = manager.get_task(parent_id)
        if not parent:
            raise ValueError(f"Parent task {parent_id} not found")

        # Check nesting depth
        if parent.id.count(".") >= 1:
            raise ValueError("Maximum nesting depth is 2 levels (task.subtask)")

        config_path = Path(todo_path).parent / ".todo.ai" / "config.yaml"
        config = Config(str(config_path))
        coord_manager = CoordinationManager(config)
        subtask_id = coord_manager.get_next_subtask_id(parent_id, manager)

        subtask = manager.add_subtask(parent_id, description, tags, task_id=subtask_id)
        save_changes(manager, todo_path)

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


def delete_command(task_ids: list[str], with_subtasks: bool = False, todo_path: str = "TODO.md"):
    """Soft delete task(s) to Deleted section."""
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


def archive_command(
    task_ids: list[str],
    reason: str | None = None,
    todo_path: str = "TODO.md",
):
    """Move task(s) to Recently Completed section."""
    manager = get_manager(todo_path)

    # Expand task IDs (no with_subtasks for archive - it archives individually)
    expanded_ids = expand_task_ids(task_ids, False, todo_path)

    archived_count = 0
    for task_id in expanded_ids:
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


def restore_command(task_id: str, todo_path: str = "TODO.md"):
    """Restore task from Deleted or Recently Completed to active Tasks."""
    from pathlib import Path

    manager = get_manager(todo_path)
    try:
        # Read file state BEFORE restore to detect original blank line structure
        file_ops = FileOps(todo_path)
        file_ops.read_tasks()
        # Phase 13: Get blank line state from snapshot instead of old state variables
        original_had_blank_after_header = (
            file_ops._structure_snapshot.blank_after_tasks_header
            if file_ops._structure_snapshot
            else False
        )

        task = manager.restore_task(task_id)

        # Phase 13: Structure preservation is handled by snapshot automatically
        # Manual file editing will be removed in Phase 14
        file_ops.write_tasks(manager.list_tasks(), preserve_blank_line_state=False)

        # After writing, if original had blank after header, ensure blank line between first two tasks
        # This matches shell script behavior: preserves original structure
        if original_had_blank_after_header:
            content = Path(todo_path).read_text(encoding="utf-8")
            lines = content.splitlines()

            # Find ## Tasks header
            tasks_header_idx = None
            for i, line in enumerate(lines):
                if line.strip() == "## Tasks" or line.strip() == "# Tasks":
                    tasks_header_idx = i
                    break

            if tasks_header_idx is not None:
                # Find first two tasks after header
                first_task_idx = None
                second_task_idx = None
                for i in range(tasks_header_idx + 1, len(lines)):
                    if lines[i].strip().startswith("- ["):
                        if first_task_idx is None:
                            first_task_idx = i
                        elif second_task_idx is None:
                            second_task_idx = i
                            break

                # If we have two tasks and no blank line between them, add one
                if first_task_idx is not None and second_task_idx is not None:
                    # Check if there's already a blank line between them
                    has_blank_between = False
                    for j in range(first_task_idx + 1, second_task_idx):
                        if lines[j].strip() == "":
                            has_blank_between = True
                            break

                    if not has_blank_between:
                        # Insert blank line before second task
                        lines.insert(second_task_idx, "")
                        Path(todo_path).write_text("\n".join(lines) + "\n", encoding="utf-8")

        print(f"Restored task #{task.id} to Tasks section")
    except ValueError as e:
        print(f"Error: {e}")


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

        reply = input(f"Delete all notes from task #{task_id}? (y/N) ")
        if reply.strip().lower() != "y":
            print("Cancelled - notes not deleted")
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

    # Check for indentation issues
    print("📋 Checking indentation:")
    indent_issues = 0

    for line in lines:
        line_stripped = line.strip()

        # Detect section headers
        if line_stripped == "## Tasks":
            in_tasks = True
            skip_line = False
        elif line_stripped == "## Recently Completed":
            in_tasks = False
            skip_line = True
        elif line_stripped == "## Deleted Tasks":
            in_tasks = False
            skip_line = True
        elif line_stripped.startswith("## "):
            in_tasks = False
            skip_line = True

        if skip_line:
            continue

        # Only check tasks in the "Tasks" section
        if in_tasks:
            # Check for subtasks not indented (should start with "  -")
            if re.match(r"^- \[.*\] \*\*#[0-9]+\.[0-9]+\*\* ", line):
                print(f"  ❌ Subtask not indented: {line}")
                indent_issues += 1
                issues_found += 1

    if indent_issues == 0:
        print("  ✅ All subtasks properly indented")
    else:
        print(f"  📊 Found {indent_issues} indentation issues")
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
        elif line_stripped == "## Recently Completed":
            in_tasks = False
            skip_line = True
        elif line_stripped == "## Deleted Tasks":
            in_tasks = False
            skip_line = True
        elif line_stripped.startswith("## "):
            in_tasks = False
            skip_line = True

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
        elif line_stripped == "## Recently Completed":
            in_tasks = False
            skip_line = True
        elif line_stripped == "## Deleted Tasks":
            in_tasks = False
            skip_line = True
        elif line_stripped.startswith("## "):
            in_tasks = False
            skip_line = True

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
        elif line_stripped == "## Recently Completed":
            in_tasks = False
            skip_line = True
        elif line_stripped == "## Deleted Tasks":
            in_tasks = False
            skip_line = True
        elif line_stripped.startswith("## "):
            in_tasks = False
            skip_line = True

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
        elif line_stripped == "## Recently Completed":
            in_tasks = False
            skip_line = True
        elif line_stripped == "## Deleted Tasks":
            in_tasks = False
            skip_line = True
        elif line_stripped.startswith("## "):
            in_tasks = False
            skip_line = True

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
    else:
        print("🔧 Applying formatting fixes...")
    print("")

    todo_file = Path(todo_path)
    if not todo_file.exists():
        print(f"Error: {todo_path} not found")
        return

    fixes_applied = 0

    # Fix indentation issues
    print("📋 Fixing indentation:")
    indent_fixes = 0

    content = todo_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    new_lines = []

    for line in lines:
        # Check for subtasks not indented (should start with "  -")
        if re.match(r"^- \[.*\] \*\*#[0-9]+\.[0-9]+\*\* ", line):
            fixed_line = f"  {line}"
            if dry_run:
                print(f"  🔄 Would fix: {line}")
                print(f"  ➡️  To:        {fixed_line}")
            else:
                print(f"  ✅ Fixed: {line}")
            new_lines.append(fixed_line)
            indent_fixes += 1
            fixes_applied += 1
        else:
            new_lines.append(line)

    if indent_fixes == 0:
        print("  ✅ No indentation issues found")
    else:
        if dry_run:
            print(f"  📊 Would fix {indent_fixes} indentation issues")
        else:
            print(f"  📊 Fixed {indent_fixes} indentation issues")
    print("")

    # Fix checkbox issues
    print("☑️  Fixing checkboxes:")
    checkbox_fixes = 0

    # Check if there are malformed checkboxes
    has_malformed = False
    for line in new_lines:
        if re.search(r"\[  \]|\[   \]|\[    \]|\[\]", line):
            has_malformed = True
            break

    if has_malformed:
        if dry_run:
            print("  🔄 Would fix malformed checkboxes:")
            for i, line in enumerate(new_lines, 1):
                if re.search(r"\[  \]|\[   \]|\[    \]|\[\]", line):
                    print(f"    Line {i}: {line}")
        else:
            # Normalize checkboxes
            normalized_lines = []
            for line in new_lines:
                # Fix various malformed patterns
                fixed = re.sub(r"\[  \]", "[ ]", line)
                fixed = re.sub(r"\[   \]", "[ ]", fixed)
                fixed = re.sub(r"\[    \]", "[ ]", fixed)
                fixed = re.sub(r"\[\]", "[ ]", fixed)
                # Fix any other malformed patterns with multiple spaces
                fixed = re.sub(r"\[[ ]+\]", "[ ]", fixed)
                normalized_lines.append(fixed)
            new_lines = normalized_lines
            print("  ✅ Fixed malformed checkboxes")
        checkbox_fixes += 1
        fixes_applied += 1

    if checkbox_fixes == 0:
        print("  ✅ No checkbox issues found")
    else:
        if dry_run:
            print(f"  📊 Would fix {checkbox_fixes} checkbox patterns")
        else:
            print(f"  📊 Fixed {checkbox_fixes} checkbox patterns")
    print("")

    # Write changes if not dry run
    if not dry_run and fixes_applied > 0:
        todo_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    # Summary
    if dry_run:
        print("💡 Run './todo.ai --reformat' to apply these fixes")
    elif fixes_applied > 0:
        print(f"🎉 Applied {fixes_applied} formatting fixes to TODO.md")
    else:
        print("🎉 No formatting issues found - TODO.md is already properly formatted!")


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
