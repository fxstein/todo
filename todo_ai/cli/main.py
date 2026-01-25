import click

from todo_ai.cli.commands import (
    add_command,
    add_subtask_command,
    archive_command,
    backups_command,
    complete_command,
    config_command,
    delete_command,
    delete_note_command,
    detect_coordination_tool_command,
    edit_command,
    lint_command,
    list_command,
    list_mode_backups_tool_command,
    log_command,
    modify_command,
    note_command,
    reformat_command,
    relate_command,
    reorder_command,
    report_bug_tool_command,
    resolve_conflicts_command,
    restore_command,
    rollback_mode_tool_command,
    rollback_tool_command,
    setup_coordination_tool_command,
    setup_wizard_tool_command,
    show_command,
    show_root_command,
    switch_mode_tool_command,
    undo_command,
    uninstall_tool_command,
    update_note_command,
    update_tool_command,
    version_tool_command,
)
from todo_ai.core.exceptions import TamperError


@click.group()
@click.option("--todo-file", envvar="TODO_FILE", default="TODO.md", help="Path to TODO.md file")
@click.option("--root", envvar="TODO_AI_ROOT", help="Root directory for the project")
@click.pass_context
def cli(ctx, todo_file, root):
    """todo.ai - AI-Agent First TODO List Tracker"""
    from pathlib import Path

    ctx.ensure_object(dict)
    # Resolve todo_file relative to root if root is provided
    if root and not Path(todo_file).is_absolute():
        ctx.obj["todo_file"] = str(Path(root) / todo_file)
    else:
        ctx.obj["todo_file"] = todo_file
    ctx.obj["root"] = root


def main():
    """Entry point for the CLI with error handling."""
    try:
        cli()
    except TamperError as e:
        print("")
        print("⛔ TAMPER DETECTED: TODO.md has been modified externally.")
        print(f"Expected hash: {e.expected_hash[:8]}...")
        print(f"Actual hash:   {e.actual_hash[:8]}...")
        print("")
        print("Use 'todo-ai tamper diff' to see changes.")
        print("Use 'todo-ai tamper accept \"reason\"' to accept external changes.")
        print("")
        import sys

        sys.exit(1)
    except Exception as e:
        # Let other exceptions bubble up or handle them if needed
        raise e


@cli.command()
@click.argument("description")
@click.argument("tags", nargs=-1)
@click.pass_context
def add(ctx, description, tags):
    """Add a new task."""
    add_command(description, list(tags), todo_path=ctx.obj["todo_file"])


@cli.command("add-subtask")
@click.argument("parent_id")
@click.argument("description")
@click.argument("tags", nargs=-1)
@click.pass_context
def add_subtask(ctx, parent_id, description, tags):
    """Add a subtask."""
    add_subtask_command(parent_id, description, list(tags), todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_ids", nargs=-1, required=True)
@click.option("--with-subtasks", is_flag=True, help="Include subtasks in operation")
@click.pass_context
def complete(ctx, task_ids, with_subtasks):
    """Mark task(s) as complete."""
    complete_command(list(task_ids), with_subtasks, todo_path=ctx.obj["todo_file"])


@cli.command("list")
@click.option("--status", help="Filter by status")
@click.option("--tag", help="Filter by tag")
@click.pass_context
def list_tasks(ctx, status, tag):
    """List tasks."""
    list_command(status, tag, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_id")
@click.argument("description")
@click.argument("tags", nargs=-1)
@click.pass_context
def modify(ctx, task_id, description, tags):
    """Modify a task's description and/or tags."""
    modify_command(task_id, description, list(tags), todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_id")
@click.pass_context
def start(ctx, task_id):
    """Mark a task as in progress."""
    from todo_ai.cli.commands import start_command

    start_command(task_id, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_id")
@click.pass_context
def stop(ctx, task_id):
    """Stop progress on a task."""
    from todo_ai.cli.commands import stop_command

    stop_command(task_id, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_ids", nargs=-1, required=True)
@click.option("--with-subtasks", is_flag=True, help="Include subtasks in operation")
@click.pass_context
def delete(ctx, task_ids, with_subtasks):
    """Delete task(s) - move to Deleted section."""
    delete_command(list(task_ids), with_subtasks, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_ids", nargs=-1, required=True)
@click.option("--reason", help="Reason for archiving incomplete tasks")
@click.pass_context
def archive(ctx, task_ids, reason):
    """Archive task(s) - move to Recently Completed section."""
    archive_command(list(task_ids), reason=reason, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_id")
@click.pass_context
def restore(ctx, task_id):
    """Restore a task from Deleted or Recently Completed back to Tasks section."""
    restore_command(task_id, todo_path=ctx.obj["todo_file"])


@cli.command("show-root")
@click.option("--root", "root_override", help="Override repo root for this invocation")
@click.pass_context
def show_root(ctx, root_override):
    """Show resolved root and source."""
    show_root_command(root_override)


@cli.command()
@click.argument("task_id")
@click.pass_context
def undo(ctx, task_id):
    """Reopen (undo) a completed task."""
    undo_command(task_id, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_id")
@click.argument("note_text")
@click.pass_context
def note(ctx, task_id, note_text):
    """Add a note to a task."""
    note_command(task_id, note_text, todo_path=ctx.obj["todo_file"])


@cli.command("delete-note")
@click.argument("task_id")
@click.pass_context
def delete_note(ctx, task_id):
    """Delete all notes from a task."""
    delete_note_command(task_id, todo_path=ctx.obj["todo_file"])


@cli.command("update-note")
@click.argument("task_id")
@click.argument("new_note_text")
@click.pass_context
def update_note(ctx, task_id, new_note_text):
    """Replace existing notes with new text."""
    update_note_command(task_id, new_note_text, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_id")
@click.pass_context
def show(ctx, task_id):
    """Display task with subtasks, relationships, and notes."""
    show_command(task_id, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_id")
@click.option("--completed-by", help="Task completed by other task(s)")
@click.option("--depends-on", help="Task depends on other task(s)")
@click.option("--blocks", help="Task blocks other task(s)")
@click.option("--related-to", help="General relationship")
@click.option("--duplicate-of", help="Task is duplicate of another")
@click.pass_context
def relate(ctx, task_id, completed_by, depends_on, blocks, related_to, duplicate_of):
    """Add task relationship."""
    # Determine relationship type and targets
    rel_type = None
    targets = None

    if completed_by:
        rel_type = "completed-by"
        targets = completed_by.split()
    elif depends_on:
        rel_type = "depends-on"
        targets = depends_on.split()
    elif blocks:
        rel_type = "blocks"
        targets = blocks.split()
    elif related_to:
        rel_type = "related-to"
        targets = related_to.split()
    elif duplicate_of:
        rel_type = "duplicate-of"
        targets = [duplicate_of]  # duplicate-of takes single target

    if not rel_type or not targets:
        print("Error: Missing required parameters")
        print("Usage: relate <id> --<relation-type> <target-ids>")
        print("")
        print("Relation types:")
        print("  --completed-by <ids>   Task completed by other task(s)")
        print("  --depends-on <ids>     Task depends on other task(s)")
        print("  --blocks <ids>         Task blocks other task(s)")
        print("  --related-to <ids>     General relationship")
        print("  --duplicate-of <id>    Task is duplicate of another")
        return

    relate_command(task_id, rel_type, targets, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.pass_context
def lint(ctx):
    """Identify formatting issues (indentation, checkboxes)."""
    lint_command(todo_path=ctx.obj["todo_file"])


@cli.command()
@click.option("--dry-run", is_flag=True, help="Preview changes without applying")
@click.pass_context
def reformat(ctx, dry_run):
    """Apply formatting fixes."""
    reformat_command(dry_run, todo_path=ctx.obj["todo_file"])


@cli.command("reorder")
@click.pass_context
def reorder(ctx):
    """Reorder subtasks to match reverse-chronological order (newest on top)."""
    reorder_command(todo_path=ctx.obj["todo_file"])


@cli.command("resolve-conflicts")
@click.option("--dry-run", is_flag=True, help="Preview changes without applying")
@click.pass_context
def resolve_conflicts(ctx, dry_run):
    """Detect and resolve duplicate task IDs."""
    resolve_conflicts_command(dry_run, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.pass_context
def edit(ctx):
    """Open TODO.md in editor."""
    edit_command(todo_path=ctx.obj["todo_file"])


# Phase 5: System Operations
@cli.command()
@click.option("--filter", help="Filter log entries by text")
@click.option("--lines", type=int, help="Number of lines to show")
@click.pass_context
def log(ctx, filter, lines):
    """View TODO operation log."""
    log_command(filter_text=filter, lines=lines, todo_path=ctx.obj["todo_file"])


@cli.command()
def update():
    """Update todo.ai to latest version."""
    update_tool_command()


@cli.command("backups")
@click.pass_context
def backups(ctx):
    """List available backup versions."""
    backups_command(todo_path=ctx.obj["todo_file"])


@cli.command("list-backups")
@click.pass_context
def list_backups(ctx):
    """List available backup versions (alias for backups)."""
    backups_command(todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("target", required=False)
@click.pass_context
def rollback(ctx, target):
    """Rollback to previous version (by index or timestamp)."""
    rollback_tool_command(target=target, todo_path=ctx.obj["todo_file"])


# Phase 6: Configuration and Setup
@cli.command("config")
@click.pass_context
def config(ctx):
    """Show current configuration."""
    config_command(todo_path=ctx.obj["todo_file"])


@cli.command("show-config")
@click.pass_context
def show_config(ctx):
    """Show current configuration (alias for config)."""
    config_command(todo_path=ctx.obj["todo_file"])


@cli.command("detect-coordination")
@click.pass_context
def detect_coordination(ctx):
    """Detect available coordination options based on system."""
    detect_coordination_tool_command(todo_path=ctx.obj["todo_file"])


@cli.command("detect-options")
@click.pass_context
def detect_options(ctx):
    """Detect available coordination options (alias for detect-coordination)."""
    detect_coordination_tool_command(todo_path=ctx.obj["todo_file"])


@cli.command("setup-coordination")
@click.argument("coord_type")
@click.pass_context
def setup_coordination(ctx, coord_type):
    """Set up coordination service (github-issues, counterapi)."""
    setup_coordination_tool_command(coord_type, interactive=True, todo_path=ctx.obj["todo_file"])


@cli.command("setup")
@click.pass_context
def setup(ctx):
    """Interactive setup wizard for mode and coordination."""
    setup_wizard_tool_command(todo_path=ctx.obj["todo_file"])


@cli.command("setup-wizard")
@click.pass_context
def setup_wizard(ctx):
    """Interactive setup wizard (alias for setup)."""
    setup_wizard_tool_command(todo_path=ctx.obj["todo_file"])


@cli.command("switch-mode")
@click.argument("mode")
@click.option("--force", "-f", is_flag=True, help="Force mode switch (skip validation)")
@click.option("--renumber", is_flag=True, help="Renumber existing tasks to match new mode")
@click.pass_context
def switch_mode(ctx, mode, force, renumber):
    """Switch numbering mode (single-user, multi-user, branch, enhanced)."""
    switch_mode_tool_command(mode, force=force, renumber=renumber, todo_path=ctx.obj["todo_file"])


@cli.command("list-mode-backups")
@click.pass_context
def list_mode_backups(ctx):
    """List mode switch backups."""
    list_mode_backups_tool_command(todo_path=ctx.obj["todo_file"])


@cli.command("rollback-mode")
@click.argument("backup_name")
@click.pass_context
def rollback_mode(ctx, backup_name):
    """Rollback from mode switch backup."""
    rollback_mode_tool_command(backup_name, todo_path=ctx.obj["todo_file"])


# Phase 7: Utility Commands
@cli.command("report-bug")
@click.argument("error_description")
@click.argument("error_context", required=False)
@click.argument("command", required=False)
def report_bug(error_description, error_context, command):
    """Report bugs to GitHub Issues (with duplicate detection)."""
    report_bug_tool_command(error_description, error_context, command)


@cli.command()
@click.option("--remove-data", "--data", is_flag=True, help="Remove .todo.ai/ data directory")
@click.option("--remove-rules", "--rules", is_flag=True, help="Remove Cursor rules")
@click.option("--all", is_flag=True, help="Remove script, data, and rules")
@click.option("--force", "-f", is_flag=True, help="Skip confirmation prompt")
def uninstall(remove_data, remove_rules, all, force):
    """Uninstall todo.ai."""
    if all:
        remove_data = True
        remove_rules = True
    uninstall_tool_command(remove_data=remove_data, remove_rules=remove_rules, force=force)


@cli.command("version")
def version():
    """Show version information."""
    version_tool_command()


@cli.command("-v")
def version_v():
    """Show version information (alias)."""
    version_tool_command()


@cli.command("--version")
def version_long():
    """Show version information (alias)."""
    version_tool_command()


@cli.command("serve")
@click.option("--root", help="Root directory for the project")
@click.pass_context
def serve(ctx, root):
    """Start the MCP server over stdio."""
    from todo_ai.mcp.server import run_server

    # Use the root from command option, global option, or default to current directory
    root_path = root or ctx.obj.get("root") or "."

    # Run the server
    run_server(root_path)


# Phase 8: Tamper Detection
@cli.group()
def tamper():
    """Manage file integrity and tamper detection."""
    pass


@tamper.command("diff")
@click.pass_context
def tamper_diff(ctx):
    """Show diff between current file and last valid state."""
    from todo_ai.cli.tamper_ops import tamper_diff_command

    tamper_diff_command(todo_path=ctx.obj["todo_file"])


@tamper.command("accept")
@click.argument("reason")
@click.pass_context
def tamper_accept(ctx, reason):
    """Accept external changes."""
    from todo_ai.cli.tamper_ops import tamper_accept_command

    tamper_accept_command(reason, todo_path=ctx.obj["todo_file"])


if __name__ == "__main__":
    main()
