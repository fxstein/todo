import click
from todo_ai.cli.commands import add_command, complete_command, list_command, add_subtask_command

@click.group()
@click.option('--todo-file', envvar='TODO_FILE', default='TODO.md', help='Path to TODO.md file')
@click.pass_context
def cli(ctx, todo_file):
    """todo.ai - AI-Agent First TODO List Tracker"""
    ctx.ensure_object(dict)
    ctx.obj['todo_file'] = todo_file

@cli.command()
@click.argument('description')
@click.argument('tags', nargs=-1)
@click.pass_context
def add(ctx, description, tags):
    """Add a new task."""
    add_command(description, list(tags), todo_path=ctx.obj['todo_file'])

@cli.command("add-subtask")
@click.argument('parent_id')
@click.argument('description')
@click.argument('tags', nargs=-1)
@click.pass_context
def add_subtask(ctx, parent_id, description, tags):
    """Add a subtask."""
    add_subtask_command(parent_id, description, list(tags), todo_path=ctx.obj['todo_file'])

@cli.command()
@click.argument('task_id')
@click.pass_context
def complete(ctx, task_id):
    """Mark a task as complete."""
    complete_command(task_id, todo_path=ctx.obj['todo_file'])

@cli.command("list")
@click.option('--status', help='Filter by status')
@click.option('--tag', help='Filter by tag')
@click.pass_context
def list_tasks(ctx, status, tag):
    """List tasks."""
    list_command(status, tag, todo_path=ctx.obj['todo_file'])

if __name__ == '__main__':
    cli()
