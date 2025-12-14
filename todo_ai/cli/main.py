import click

from todo_ai.cli.commands import (
    add_command,
    add_subtask_command,
    archive_command,
    complete_command,
    delete_command,
    delete_note_command,
    list_command,
    modify_command,
    note_command,
    relate_command,
    restore_command,
    show_command,
    undo_command,
    update_note_command,
)


@click.group()
@click.option("--todo-file", envvar="TODO_FILE", default="TODO.md", help="Path to TODO.md file")
@click.pass_context
def cli(ctx, todo_file):
    """todo.ai - AI-Agent First TODO List Tracker"""
    ctx.ensure_object(dict)
    ctx.obj["todo_file"] = todo_file


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
@click.argument("task_ids", nargs=-1, required=True)
@click.option("--with-subtasks", is_flag=True, help="Include subtasks in operation")
@click.pass_context
def delete(ctx, task_ids, with_subtasks):
    """Delete task(s) - move to Deleted section."""
    delete_command(list(task_ids), with_subtasks, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_ids", nargs=-1, required=True)
@click.option("--reason", help="Reason for archiving incomplete tasks")
@click.option("--with-subtasks", is_flag=True, help="Include subtasks in operation")
@click.pass_context
def archive(ctx, task_ids, reason, with_subtasks):
    """Archive task(s) - move to Recently Completed section."""
    archive_command(list(task_ids), reason, with_subtasks, todo_path=ctx.obj["todo_file"])


@cli.command()
@click.argument("task_id")
@click.pass_context
def restore(ctx, task_id):
    """Restore a task from Deleted or Recently Completed back to Tasks section."""
    restore_command(task_id, todo_path=ctx.obj["todo_file"])


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


if __name__ == "__main__":
    cli()
