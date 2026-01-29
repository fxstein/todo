import click

from ai_todo.cli.commands import (
    add_command,
    add_subtask_command,
    archive_command,
    complete_command,
    config_command,
    delete_command,
    delete_note_command,
    detect_coordination_tool_command,
    empty_trash_command,
    lint_command,
    list_command,
    modify_command,
    note_command,
    prune_command,
    reformat_command,
    relate_command,
    reorder_command,
    resolve_conflicts_command,
    restore_command,
    setup_coordination_tool_command,
    setup_wizard_tool_command,
    show_command,
    show_root_command,
    switch_mode_tool_command,
    undo_command,
    update_note_command,
    version_tool_command,
)
from ai_todo.core.exceptions import TamperError


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
        print("Use 'ai-todo tamper diff' to see changes.")
        print("Use 'ai-todo tamper accept \"reason\"' to accept external changes.")
        print("")
        import sys

        sys.exit(1)
    except Exception as e:
        # Let other exceptions bubble up or handle them if needed
        raise e


@cli.command("add-task")
@click.argument("title")
@click.option("--description", "-d", help="Optional detailed notes for the task")
@click.argument("tags", nargs=-1)
@click.pass_context
def add_task(ctx, title, description, tags):
    """Add a new task."""
    add_command(title, list(tags), todo_path=ctx.obj["todo_file"])
    # If description provided, add notes
    if description:
        import re

        from ai_todo.cli.commands import get_manager

        manager = get_manager(ctx.obj["todo_file"])
        # Find the task we just added (newest task)
        tasks = manager.list_tasks()
        if tasks:
            # Get task IDs and find highest
            task_ids = [t.id for t in tasks if "." not in t.id]
            if task_ids:
                # Find newest task (highest ID)
                newest_id = max(task_ids, key=lambda x: int(re.sub(r"[^0-9]", "", x) or "0"))
                note_command(newest_id, description, todo_path=ctx.obj["todo_file"])


@cli.command("add-subtask")
@click.argument("parent_id")
@click.argument("title")
@click.option("--description", "-d", help="Optional detailed notes for the subtask")
@click.argument("tags", nargs=-1)
@click.pass_context
def add_subtask(ctx, parent_id, title, description, tags):
    """Add a subtask."""
    add_subtask_command(parent_id, title, list(tags), todo_path=ctx.obj["todo_file"])
    # If description provided, add notes
    if description:
        from ai_todo.cli.commands import get_manager

        manager = get_manager(ctx.obj["todo_file"])
        # Find subtasks of this parent and get the newest one
        subtasks = manager.get_subtasks(parent_id)
        if subtasks:
            # Get newest subtask (highest ID)
            newest_subtask = max(subtasks, key=lambda t: [int(x) for x in t.id.split(".")])
            note_command(newest_subtask.id, description, todo_path=ctx.obj["todo_file"])


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


@cli.command("modify-task")
@click.argument("task_id")
@click.argument("title")
@click.option("--description", "-d", help="Optional new detailed notes (replaces existing)")
@click.argument("tags", nargs=-1)
@click.pass_context
def modify_task(ctx, task_id, title, description, tags):
    """Modify a task's title, description, and/or tags."""
    modify_command(task_id, title, list(tags), todo_path=ctx.obj["todo_file"])
    # If description provided, update notes
    if description is not None:
        if description == "":
            delete_note_command(task_id, todo_path=ctx.obj["todo_file"])
        else:
            update_note_command(task_id, description, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_id")
@click.pass_context
def start(ctx, task_id):
    """Mark a task as in progress."""
    from ai_todo.cli.commands import start_command

    start_command(task_id, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_id")
@click.pass_context
def stop(ctx, task_id):
    """Stop progress on a task."""
    from ai_todo.cli.commands import stop_command

    stop_command(task_id, todo_path=ctx.obj["todo_file"])


@cli.command("get-active-tasks")
@click.pass_context
def get_active_tasks(ctx):
    """Get a list of all currently active tasks (marked #inprogress)."""
    list_command(tag="inprogress", incomplete_only=True, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_ids", nargs=-1, required=True)
@click.option(
    "--no-subtasks", is_flag=True, help="Delete only the specified task(s), not their subtasks"
)
@click.pass_context
def delete(ctx, task_ids, no_subtasks):
    """Delete task(s) and their subtasks - move to Deleted section."""
    delete_command(list(task_ids), with_subtasks=not no_subtasks, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_ids", nargs=-1, required=True)
@click.option("--reason", help="Reason for archiving incomplete tasks")
@click.pass_context
def archive(ctx, task_ids, reason):
    """Archive task(s) - move to Recently Completed section."""
    archive_command(list(task_ids), reason=reason, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.option("--days", type=int, default=None, help="Prune tasks older than N days (default: 30)")
@click.option("--older-than", help="Prune tasks before YYYY-MM-DD")
@click.option("--from-task", help="Prune tasks from #1 to #ID")
@click.option("--dry-run", is_flag=True, help="Preview without making changes")
@click.option("--no-backup", is_flag=True, help="Skip archive backup creation")
@click.option("--force", "-f", is_flag=True, help="Skip confirmation prompts")
@click.pass_context
def prune(ctx, days, older_than, from_task, dry_run, no_backup, force):
    """Prune old archived tasks from TODO.md."""
    prune_command(
        days=days,
        older_than=older_than,
        from_task=from_task,
        dry_run=dry_run,
        backup=not no_backup,
        force=force,
        todo_path=ctx.obj["todo_file"],
    )


@cli.command("empty-trash")
@click.option("--dry-run", is_flag=True, help="Preview without removing")
@click.pass_context
def empty_trash(ctx, dry_run):
    """Permanently remove expired deleted tasks (30-day retention)."""
    empty_trash_command(
        dry_run=dry_run,
        todo_path=ctx.obj["todo_file"],
    )


@cli.command()
@click.argument("task_ids", nargs=-1, required=True)
@click.pass_context
def restore(ctx, task_ids):
    """Restore task(s) from Deleted or Recently Completed back to Tasks section."""
    restore_command(list(task_ids), todo_path=ctx.obj["todo_file"])


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


@cli.command("set-description")
@click.argument("task_id")
@click.argument("description")
@click.pass_context
def set_description(ctx, task_id, description):
    """Set or clear a task's description (notes).

    Use "" (empty string) to clear the description.
    """
    from ai_todo.cli.commands import get_manager

    if description == "":
        delete_note_command(task_id, todo_path=ctx.obj["todo_file"])
    else:
        # Check if task has existing notes - if so, update; otherwise add
        manager = get_manager(ctx.obj["todo_file"])
        task = manager.get_task(task_id)
        if task and task.notes:
            update_note_command(task_id, description, todo_path=ctx.obj["todo_file"])
        else:
            note_command(task_id, description, todo_path=ctx.obj["todo_file"])


@cli.command("set-tags")
@click.argument("task_id")
@click.argument("tags", nargs=-1)
@click.pass_context
def set_tags(ctx, task_id, tags):
    """Set a task's tags (replaces all existing tags).

    Use no tags to clear all tags from the task.
    """
    from ai_todo.cli.commands import get_manager, save_changes

    manager = get_manager(ctx.obj["todo_file"])
    task = manager.get_task(task_id)
    if not task:
        print(f"Error: Task {task_id} not found")
        return

    # Set tags (replaces existing)
    task.tags = set(tags)
    save_changes(manager, ctx.obj["todo_file"])

    if tags:
        tag_str = " ".join([f"`#{tag}`" for tag in sorted(tags)])
        print(f"Set tags on #{task_id}: {tag_str}")
    else:
        print(f"Cleared tags from #{task_id}")


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


# Phase 5: Configuration and Setup
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


@cli.command("switch-mode")
@click.argument("mode")
@click.option("--force", "-f", is_flag=True, help="Force mode switch (skip validation)")
@click.option("--renumber", is_flag=True, help="Renumber existing tasks to match new mode")
@click.pass_context
def switch_mode(ctx, mode, force, renumber):
    """Switch numbering mode (single-user, multi-user, branch, enhanced)."""
    switch_mode_tool_command(mode, force=force, renumber=renumber, todo_path=ctx.obj["todo_file"])


# Phase 6: Info
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


@cli.command("check-update")
def check_update_cmd():
    """Check if an ai-todo update is available."""
    from pathlib import Path

    from ai_todo.core.updater import check_for_updates

    info = check_for_updates(Path.cwd())
    print(info.message)


@cli.command("update")
@click.option("--check-only", is_flag=True, help="Only check for updates, don't install")
def update_cmd(check_only):
    """Update ai-todo to the latest version."""
    from pathlib import Path

    from ai_todo.core.updater import check_for_updates, perform_update

    project_root = Path.cwd()

    if check_only:
        info = check_for_updates(project_root)
        print(info.message)
        return

    success, message = perform_update(restart=False, project_root=project_root)
    print(message)
    if not success:
        raise SystemExit(1)


# Update configuration commands
@cli.group("update-config")
def update_config():
    """Manage global update version constraints."""
    pass


@update_config.command("show")
def update_config_show():
    """Show current update version constraint."""
    from ai_todo.core.version_constraints import GlobalConfig, get_global_config_path

    config = GlobalConfig()
    constraint = config.get("update.version_constraint")
    allow_prerelease = config.get("update.allow_prerelease", False)

    print(f"Global config: {get_global_config_path()}")
    if constraint:
        print(f"Version constraint: {constraint}")
    else:
        print("Version constraint: (none - will update to latest)")
    print(f"Allow prerelease: {allow_prerelease}")


@update_config.command("set")
@click.argument("constraint")
def update_config_set(constraint):
    """Set update version constraint (e.g., '>=3.0.0,<4.0.0' or '==3.0.2')."""
    from ai_todo.core.version_constraints import GlobalConfig, parse_constraint

    # Validate the constraint
    try:
        parsed = parse_constraint(constraint)
        print(f"Parsed constraint: {parsed.raw}")
    except Exception as e:
        print(f"Error: Invalid version constraint: {e}")
        raise SystemExit(1) from None

    config = GlobalConfig()
    config.set("update.version_constraint", constraint)
    print(f"Set version constraint: {constraint}")


@update_config.command("clear")
def update_config_clear():
    """Clear update version constraint (allow updates to latest)."""
    from ai_todo.core.version_constraints import GlobalConfig

    config = GlobalConfig()
    config.set("update.version_constraint", None)
    print("Cleared version constraint - updates will go to latest version")


@cli.command("serve")
@click.option("--root", help="Root directory for the project")
@click.pass_context
def serve(ctx, root):
    """Start the MCP server over stdio."""
    from ai_todo.mcp.server import run_server

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
    from ai_todo.cli.tamper_ops import tamper_diff_command

    tamper_diff_command(todo_path=ctx.obj["todo_file"])


@tamper.command("accept")
@click.argument("reason")
@click.pass_context
def tamper_accept(ctx, reason):
    """Accept external changes."""
    from ai_todo.cli.tamper_ops import tamper_accept_command

    tamper_accept_command(reason, todo_path=ctx.obj["todo_file"])


if __name__ == "__main__":
    main()
