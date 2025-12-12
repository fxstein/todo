import click
from todo_ai.cli.commands import add_command, complete_command, list_command

@click.group()
def cli():
    """todo.ai - AI-Agent First TODO List Tracker"""
    pass

@cli.command()
@click.argument('description')
@click.argument('tags', nargs=-1)
def add(description, tags):
    """Add a new task."""
    add_command(description, list(tags))

@cli.command()
@click.argument('task_id')
def complete(task_id):
    """Mark a task as complete."""
    complete_command(task_id)

@cli.command("list")
@click.option('--status', help='Filter by status')
@click.option('--tag', help='Filter by tag')
def list_tasks(status, tag):
    """List tasks."""
    list_command(status, tag)

if __name__ == '__main__':
    cli()

