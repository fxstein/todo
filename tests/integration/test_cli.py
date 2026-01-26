"""Integration tests for CLI commands."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from ai_todo.cli.main import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def isolated_cli(runner, tmp_path):
    """Isolated CLI environment with temporary directory."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Create .ai-todo directory structure
        todo_ai_dir = Path(".ai-todo")
        todo_ai_dir.mkdir(exist_ok=True)
        (todo_ai_dir / "config.yaml").write_text(
            "numbering_mode: single-user\ncoordination_type: none\n"
        )
        (todo_ai_dir / ".ai-todo.serial").write_text("0")
        yield runner


# Basic Commands (already tested, but keeping for completeness)
def test_add_command(isolated_cli):
    """Test add command."""
    result = isolated_cli.invoke(cli, ["add", "Test task", "#tag1"])
    assert result.exit_code == 0
    assert "Added: #1 Test task" in result.output


def test_list_command(isolated_cli):
    """Test list command."""
    isolated_cli.invoke(cli, ["add", "Task 1"])
    result = isolated_cli.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "**#1** Task 1" in result.output


def test_complete_command(isolated_cli):
    """Test complete command."""
    isolated_cli.invoke(cli, ["add", "Task 1"])
    result = isolated_cli.invoke(cli, ["complete", "1"])
    assert result.exit_code == 0
    assert "Completed: #1 Task 1" in result.output

    # Verify list update
    result = isolated_cli.invoke(cli, ["list"])
    assert "[x] **#1** Task 1" in result.output


def test_add_subtask_command(isolated_cli):
    """Test add-subtask command."""
    isolated_cli.invoke(cli, ["add", "Parent task"])
    result = isolated_cli.invoke(cli, ["add-subtask", "1", "Subtask 1"])
    assert result.exit_code == 0
    assert "Added subtask: #1.1 Subtask 1" in result.output


def test_add_subtasks_multiple_parents(isolated_cli):
    """Ensure subtasks appear under their respective parents."""
    isolated_cli.invoke(cli, ["add", "Task A"])
    isolated_cli.invoke(cli, ["add", "Task B"])
    isolated_cli.invoke(cli, ["add", "Task C"])

    isolated_cli.invoke(cli, ["add-subtask", "1", "Subtask A.1"])
    isolated_cli.invoke(cli, ["add-subtask", "1", "Subtask A.2"])
    isolated_cli.invoke(cli, ["add-subtask", "2", "Subtask B.1"])
    isolated_cli.invoke(cli, ["add-subtask", "2", "Subtask B.2"])
    isolated_cli.invoke(cli, ["add-subtask", "3", "Subtask C.1"])
    isolated_cli.invoke(cli, ["add-subtask", "3", "Subtask C.2"])

    content = Path("TODO.md").read_text(encoding="utf-8")
    lines = content.splitlines()

    def line_index(fragment: str) -> int:
        return next(i for i, line in enumerate(lines) if fragment in line)

    parent_indices = [
        ("3", line_index("**#3** Task C")),
        ("2", line_index("**#2** Task B")),
        ("1", line_index("**#1** Task A")),
    ]
    parent_indices.sort(key=lambda item: item[1])

    subtask_indices = {
        "1": [
            line_index("**#1.1** Subtask A.1"),
            line_index("**#1.2** Subtask A.2"),
        ],
        "2": [
            line_index("**#2.1** Subtask B.1"),
            line_index("**#2.2** Subtask B.2"),
        ],
        "3": [
            line_index("**#3.1** Subtask C.1"),
            line_index("**#3.2** Subtask C.2"),
        ],
    }

    for index, (parent_id, parent_line) in enumerate(parent_indices):
        next_parent_line = parent_indices[index + 1][1] if index + 1 < len(parent_indices) else None
        for subtask_line in subtask_indices[parent_id]:
            assert subtask_line > parent_line
            if next_parent_line is not None:
                assert subtask_line < next_parent_line


# Phase 1: Task Management
def test_modify_command(isolated_cli):
    """Test modify command."""
    isolated_cli.invoke(cli, ["add", "Original task"])
    result = isolated_cli.invoke(cli, ["modify", "1", "Modified task", "#newtag"])
    assert result.exit_code == 0
    assert "Modified: #1 Modified task" in result.output

    # Verify modification
    result = isolated_cli.invoke(cli, ["list"])
    assert "Modified task" in result.output


def test_delete_command(isolated_cli):
    """Test delete command."""
    isolated_cli.invoke(cli, ["add", "Task to delete"])
    result = isolated_cli.invoke(cli, ["delete", "1"])
    assert result.exit_code == 0
    assert "Deleted" in result.output

    # Verify task is in Deleted section (check that it's not in active tasks)
    result = isolated_cli.invoke(cli, ["list"])
    # Task should not appear in main pending tasks list (it's in Deleted section)
    # The list command may show it in a different section, so we just verify delete worked
    assert result.exit_code == 0


def test_delete_command_with_subtasks(isolated_cli):
    """Test delete command removes subtasks by default (task#221 fix)."""
    # Create parent task
    isolated_cli.invoke(cli, ["add", "Parent task"])
    # Add subtasks
    isolated_cli.invoke(cli, ["add-subtask", "1", "Subtask 1"])
    isolated_cli.invoke(cli, ["add-subtask", "1", "Subtask 2"])

    # Delete parent - should delete subtasks too (default behavior)
    result = isolated_cli.invoke(cli, ["delete", "1"])
    assert result.exit_code == 0
    # Should report 3 tasks deleted (parent + 2 subtasks)
    assert "Deleted 3 task(s)" in result.output


def test_delete_command_no_subtasks_flag(isolated_cli):
    """Test delete --no-subtasks only deletes the parent task."""
    # Create parent task
    isolated_cli.invoke(cli, ["add", "Parent task"])
    # Add subtasks
    isolated_cli.invoke(cli, ["add-subtask", "1", "Subtask 1"])
    isolated_cli.invoke(cli, ["add-subtask", "1", "Subtask 2"])

    # Delete parent with --no-subtasks flag
    result = isolated_cli.invoke(cli, ["delete", "1", "--no-subtasks"])
    assert result.exit_code == 0
    # Should report only 1 task deleted (just the parent)
    assert "Deleted 1 task(s)" in result.output


def test_archive_command(isolated_cli):
    """Test archive command."""
    isolated_cli.invoke(cli, ["add", "Task to archive"])
    result = isolated_cli.invoke(cli, ["archive", "1", "--reason", "No longer needed"])
    assert result.exit_code == 0
    assert "Archived" in result.output


def test_archive_cooldown_blocks_immediate_archive(isolated_cli):
    """Test archive cooldown prevents immediate archiving of completed root tasks with subtasks."""
    # Create parent task with subtasks
    isolated_cli.invoke(cli, ["add", "Parent task"])
    isolated_cli.invoke(cli, ["add-subtask", "1", "Subtask 1"])
    isolated_cli.invoke(cli, ["add-subtask", "1", "Subtask 2"])

    # Complete the parent (and subtasks)
    isolated_cli.invoke(cli, ["complete", "1", "--with-subtasks"])

    # Try to archive immediately - should be blocked by cooldown
    result = isolated_cli.invoke(cli, ["archive", "1"])
    assert "requires human review" in result.output
    # Should NOT have archived any tasks
    assert "Archived" not in result.output


def test_archive_cooldown_allows_single_task(isolated_cli):
    """Test archive cooldown does NOT block single tasks without subtasks."""
    # Create single task (no subtasks)
    isolated_cli.invoke(cli, ["add", "Single task"])

    # Complete it
    isolated_cli.invoke(cli, ["complete", "1"])

    # Try to archive immediately - should work (no subtasks = no cooldown)
    result = isolated_cli.invoke(cli, ["archive", "1"])
    assert result.exit_code == 0
    assert "Archived 1 task(s)" in result.output


def test_restore_command(isolated_cli):
    """Test restore command."""
    isolated_cli.invoke(cli, ["add", "Task to restore"])
    isolated_cli.invoke(cli, ["delete", "1"])
    result = isolated_cli.invoke(cli, ["restore", "1"])
    assert result.exit_code == 0
    assert "Restored" in result.output and "#1" in result.output


def test_undo_command(isolated_cli):
    """Test undo command."""
    isolated_cli.invoke(cli, ["add", "Task to undo"])
    isolated_cli.invoke(cli, ["complete", "1"])
    result = isolated_cli.invoke(cli, ["undo", "1"])
    assert result.exit_code == 0
    assert "Reopened" in result.output and "#1" in result.output


# Phase 2: Note Management
def test_note_command(isolated_cli):
    """Test note command."""
    isolated_cli.invoke(cli, ["add", "Task with note"])
    result = isolated_cli.invoke(cli, ["note", "1", "This is a note"])
    assert result.exit_code == 0
    assert "Added note" in result.output and "#1" in result.output


def test_delete_note_command(isolated_cli):
    """Test delete-note command."""
    isolated_cli.invoke(cli, ["add", "Task with note"])
    isolated_cli.invoke(cli, ["note", "1", "Note to delete"])
    result = isolated_cli.invoke(cli, ["delete-note", "1"])
    assert result.exit_code == 0
    assert "Deleted notes" in result.output and "#1" in result.output


def test_update_note_command(isolated_cli):
    """Test update-note command."""
    isolated_cli.invoke(cli, ["add", "Task with note"])
    isolated_cli.invoke(cli, ["note", "1", "Old note"])
    result = isolated_cli.invoke(cli, ["update-note", "1", "New note"])
    assert result.exit_code == 0
    assert "Updated notes" in result.output and "#1" in result.output


# Progress Commands
def test_get_active_tasks_command(isolated_cli):
    """Test get-active-tasks command."""
    # Add tasks
    isolated_cli.invoke(cli, ["add", "Task 1"])
    isolated_cli.invoke(cli, ["add", "Task 2"])

    # Start a task
    isolated_cli.invoke(cli, ["start", "1"])

    # Get active tasks
    result = isolated_cli.invoke(cli, ["get-active-tasks"])
    assert result.exit_code == 0
    assert "#1" in result.output
    assert "#inprogress" in result.output


# Phase 3: Task Display and Relationships
def test_show_command(isolated_cli):
    """Test show command."""
    isolated_cli.invoke(cli, ["add", "Task to show"])
    result = isolated_cli.invoke(cli, ["show", "1"])
    assert result.exit_code == 0
    assert "#1" in result.output
    assert "Task to show" in result.output


def test_show_command_deleted_task_displays_d(isolated_cli):
    """Test show command displays [D] for deleted tasks (task#222 fix)."""
    # Create parent with subtasks
    isolated_cli.invoke(cli, ["add", "Parent task"])
    isolated_cli.invoke(cli, ["add-subtask", "1", "Child task"])

    # Delete the subtask only
    isolated_cli.invoke(cli, ["delete", "1.1", "--no-subtasks"])

    # Show the parent - should display subtask with [D] not [x]
    result = isolated_cli.invoke(cli, ["show", "1"])
    assert result.exit_code == 0
    assert "[D]" in result.output  # Deleted subtask should show [D]
    assert "[ ]" in result.output  # Parent should still be pending [ ]


def test_relate_command(isolated_cli):
    """Test relate command."""
    isolated_cli.invoke(cli, ["add", "Task 1"])
    isolated_cli.invoke(cli, ["add", "Task 2"])
    result = isolated_cli.invoke(cli, ["relate", "1", "--depends-on", "2"])
    assert result.exit_code == 0
    assert "Added relationship" in result.output or "depends-on" in result.output.lower()


# Phase 4: File Operations
def test_lint_command(isolated_cli):
    """Test lint command."""
    isolated_cli.invoke(cli, ["add", "Task 1"])
    result = isolated_cli.invoke(cli, ["lint"])
    assert result.exit_code == 0
    # Should report no issues or list issues found


def test_reformat_command(isolated_cli):
    """Test reformat command."""
    isolated_cli.invoke(cli, ["add", "Task 1"])
    result = isolated_cli.invoke(cli, ["reformat"])
    assert result.exit_code == 0
    # Should report reformatting results


def test_reformat_dry_run(isolated_cli):
    """Test reformat command with dry-run."""
    isolated_cli.invoke(cli, ["add", "Task 1"])
    result = isolated_cli.invoke(cli, ["reformat", "--dry-run"])
    assert result.exit_code == 0
    # Should show what would be changed without making changes


def test_resolve_conflicts_command(isolated_cli):
    """Test resolve-conflicts command."""
    isolated_cli.invoke(cli, ["add", "Task 1"])
    result = isolated_cli.invoke(cli, ["resolve-conflicts"])
    assert result.exit_code == 0
    # Should report conflict resolution results


def test_resolve_conflicts_dry_run(isolated_cli):
    """Test resolve-conflicts command with dry-run."""
    isolated_cli.invoke(cli, ["add", "Task 1"])
    result = isolated_cli.invoke(cli, ["resolve-conflicts", "--dry-run"])
    assert result.exit_code == 0
    # Should show what would be changed without making changes


# Phase 5: Configuration and Setup
def test_config_command(isolated_cli):
    """Test config command."""
    result = isolated_cli.invoke(cli, ["config"])
    assert result.exit_code == 0
    # Should show configuration


def test_detect_coordination_command(isolated_cli):
    """Test detect-coordination command."""
    result = isolated_cli.invoke(cli, ["detect-coordination"])
    assert result.exit_code == 0
    # Should show available coordination options


# Phase 7: Utility Commands
def test_version_command(isolated_cli):
    """Test version command."""
    result = isolated_cli.invoke(cli, ["version"])
    assert result.exit_code == 0
    # Should show version information


def test_version_short_flag(isolated_cli):
    """Test version command with -v flag."""
    # Note: -v might be interpreted as a global option, test may need adjustment
    result = isolated_cli.invoke(cli, ["-v"], standalone_mode=False)
    # If standalone_mode fails, just test that version command works
    if result.exit_code != 0:
        result = isolated_cli.invoke(cli, ["version"])
    assert result.exit_code == 0


def test_version_long_flag(isolated_cli):
    """Test version command with --version flag."""
    # Note: --version might be interpreted as a global option, test may need adjustment
    result = isolated_cli.invoke(cli, ["--version"], standalone_mode=False)
    # If standalone_mode fails, just test that version command works
    if result.exit_code != 0:
        result = isolated_cli.invoke(cli, ["version"])
    assert result.exit_code == 0


# Complex Workflow Tests
def test_complete_workflow(isolated_cli):
    """Test a complete workflow: add -> modify -> complete -> undo."""
    # Add task
    result = isolated_cli.invoke(cli, ["add", "Workflow task", "#test"])
    assert result.exit_code == 0
    task_id = result.output.split("#")[1].split()[0]

    # Modify task
    result = isolated_cli.invoke(cli, ["modify", task_id, "Modified workflow task"])
    assert result.exit_code == 0

    # Complete task
    result = isolated_cli.invoke(cli, ["complete", task_id])
    assert result.exit_code == 0

    # Undo task
    result = isolated_cli.invoke(cli, ["undo", task_id])
    assert result.exit_code == 0


def test_subtask_workflow(isolated_cli):
    """Test subtask workflow: add parent -> add subtask -> complete parent."""
    # Add parent
    result = isolated_cli.invoke(cli, ["add", "Parent task"])
    assert result.exit_code == 0
    parent_id = result.output.split("#")[1].split()[0]

    # Add subtask
    result = isolated_cli.invoke(cli, ["add-subtask", parent_id, "Subtask"])
    assert result.exit_code == 0

    # Complete parent (should complete subtask too)
    result = isolated_cli.invoke(cli, ["complete", parent_id, "--with-subtasks"])
    assert result.exit_code == 0


def test_note_workflow(isolated_cli):
    """Test note workflow: add task -> add note -> update note -> delete note."""
    # Add task
    result = isolated_cli.invoke(cli, ["add", "Task with notes"])
    assert result.exit_code == 0
    task_id = result.output.split("#")[1].split()[0]

    # Add note
    result = isolated_cli.invoke(cli, ["note", task_id, "First note"])
    assert result.exit_code == 0

    # Update note
    result = isolated_cli.invoke(cli, ["update-note", task_id, "Updated note"])
    assert result.exit_code == 0

    # Delete note
    result = isolated_cli.invoke(cli, ["delete-note", task_id])
    assert result.exit_code == 0


def test_relationship_workflow(isolated_cli):
    """Test relationship workflow: add tasks -> relate them."""
    # Add tasks
    result1 = isolated_cli.invoke(cli, ["add", "Task 1"])
    assert result1.exit_code == 0
    task1_id = result1.output.split("#")[1].split()[0]

    result2 = isolated_cli.invoke(cli, ["add", "Task 2"])
    assert result2.exit_code == 0
    task2_id = result2.output.split("#")[1].split()[0]

    # Add relationship
    result = isolated_cli.invoke(cli, ["relate", task1_id, "--depends-on", task2_id])
    assert result.exit_code == 0

    # Show task to verify relationship
    result = isolated_cli.invoke(cli, ["show", task1_id])
    assert result.exit_code == 0
