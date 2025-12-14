"""MCP server for todo.ai."""

import asyncio
import io
import sys
from pathlib import Path

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

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
    lint_command,
    list_command,
    log_command,
    modify_command,
    note_command,
    reformat_command,
    relate_command,
    report_bug_tool_command,
    resolve_conflicts_command,
    restore_command,
    rollback_tool_command,
    setup_coordination_tool_command,
    show_command,
    switch_mode_tool_command,
    undo_command,
    uninstall_tool_command,
    update_note_command,
    update_tool_command,
)


class MCPServer:
    """MCP server for todo.ai."""

    def __init__(self, todo_path: str = "TODO.md"):
        self.app = Server("todo-ai")
        self.todo_path = todo_path
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup MCP request handlers."""

        @self.app.list_tools()
        async def list_tools() -> list[types.Tool]:
            """List all available MCP tools."""
            return [
                # Basic task operations
                types.Tool(
                    name="add_task",
                    description="Add a new task to TODO.md",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "description": {"type": "string"},
                            "tags": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": ["description"],
                    },
                ),
                types.Tool(
                    name="add_subtask",
                    description="Add a subtask to an existing task",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "parent_id": {"type": "string"},
                            "description": {"type": "string"},
                            "tags": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": ["parent_id", "description"],
                    },
                ),
                types.Tool(
                    name="complete_task",
                    description="Mark a task as complete",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"},
                            "with_subtasks": {"type": "boolean"},
                        },
                        "required": ["task_id"],
                    },
                ),
                types.Tool(
                    name="list_tasks",
                    description="List tasks from TODO.md",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["pending", "completed", "archived"],
                            },
                            "tag": {"type": "string"},
                        },
                    },
                ),
                # Phase 1: Task Management
                types.Tool(
                    name="modify_task",
                    description="Modify a task's description and/or tags",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"},
                            "description": {"type": "string"},
                            "tags": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": ["task_id", "description"],
                    },
                ),
                types.Tool(
                    name="delete_task",
                    description="Delete a task (move to Deleted section)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"},
                            "with_subtasks": {"type": "boolean"},
                        },
                        "required": ["task_id"],
                    },
                ),
                types.Tool(
                    name="archive_task",
                    description="Archive a task (move to Recently Completed section)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"},
                            "reason": {"type": "string"},
                            "with_subtasks": {"type": "boolean"},
                        },
                        "required": ["task_id"],
                    },
                ),
                types.Tool(
                    name="restore_task",
                    description="Restore a task from Deleted or Recently Completed back to Tasks section",
                    inputSchema={
                        "type": "object",
                        "properties": {"task_id": {"type": "string"}},
                        "required": ["task_id"],
                    },
                ),
                types.Tool(
                    name="undo_task",
                    description="Reopen (undo) a completed task",
                    inputSchema={
                        "type": "object",
                        "properties": {"task_id": {"type": "string"}},
                        "required": ["task_id"],
                    },
                ),
                # Phase 2: Note Management
                types.Tool(
                    name="add_note",
                    description="Add a note to a task",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"},
                            "note_text": {"type": "string"},
                        },
                        "required": ["task_id", "note_text"],
                    },
                ),
                types.Tool(
                    name="delete_note",
                    description="Delete all notes from a task",
                    inputSchema={
                        "type": "object",
                        "properties": {"task_id": {"type": "string"}},
                        "required": ["task_id"],
                    },
                ),
                types.Tool(
                    name="update_note",
                    description="Replace existing notes with new text",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"},
                            "new_note_text": {"type": "string"},
                        },
                        "required": ["task_id", "new_note_text"],
                    },
                ),
                # Phase 3: Task Display and Relationships
                types.Tool(
                    name="show_task",
                    description="Display task with subtasks, relationships, and notes",
                    inputSchema={
                        "type": "object",
                        "properties": {"task_id": {"type": "string"}},
                        "required": ["task_id"],
                    },
                ),
                types.Tool(
                    name="relate_task",
                    description="Add task relationship (completed-by, depends-on, blocks, related-to, duplicate-of)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"},
                            "rel_type": {
                                "type": "string",
                                "enum": [
                                    "completed-by",
                                    "depends-on",
                                    "blocks",
                                    "related-to",
                                    "duplicate-of",
                                ],
                            },
                            "target_ids": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": ["task_id", "rel_type", "target_ids"],
                    },
                ),
                # Phase 4: File Operations
                types.Tool(
                    name="lint_todo",
                    description="Identify formatting issues (indentation, checkboxes)",
                    inputSchema={"type": "object", "properties": {}},
                ),
                types.Tool(
                    name="reformat_todo",
                    description="Apply formatting fixes",
                    inputSchema={
                        "type": "object",
                        "properties": {"dry_run": {"type": "boolean"}},
                    },
                ),
                types.Tool(
                    name="resolve_conflicts",
                    description="Detect and resolve duplicate task IDs",
                    inputSchema={
                        "type": "object",
                        "properties": {"dry_run": {"type": "boolean"}},
                    },
                ),
                # Phase 5: System Operations
                types.Tool(
                    name="view_log",
                    description="View TODO operation log",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filter": {"type": "string"},
                            "lines": {"type": "integer"},
                        },
                    },
                ),
                types.Tool(
                    name="update_tool",
                    description="Update todo.ai to latest version",
                    inputSchema={"type": "object", "properties": {}},
                ),
                types.Tool(
                    name="list_backups",
                    description="List available backup versions",
                    inputSchema={"type": "object", "properties": {}},
                ),
                types.Tool(
                    name="rollback",
                    description="Rollback to previous version (by index or timestamp)",
                    inputSchema={
                        "type": "object",
                        "properties": {"target": {"type": "string"}},
                    },
                ),
                # Phase 6: Configuration and Setup
                types.Tool(
                    name="show_config",
                    description="Show current configuration",
                    inputSchema={"type": "object", "properties": {}},
                ),
                types.Tool(
                    name="detect_coordination",
                    description="Detect available coordination options based on system",
                    inputSchema={"type": "object", "properties": {}},
                ),
                types.Tool(
                    name="setup_coordination",
                    description="Set up coordination service (github-issues, counterapi)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "coord_type": {
                                "type": "string",
                                "enum": ["github-issues", "counterapi"],
                            },
                        },
                        "required": ["coord_type"],
                    },
                ),
                types.Tool(
                    name="switch_mode",
                    description="Switch numbering mode (single-user, multi-user, branch, enhanced)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "mode": {
                                "type": "string",
                                "enum": ["single-user", "multi-user", "branch", "enhanced"],
                            },
                            "force": {"type": "boolean"},
                            "renumber": {"type": "boolean"},
                        },
                        "required": ["mode"],
                    },
                ),
                # Phase 7: Utility Commands
                types.Tool(
                    name="report_bug",
                    description="Report bugs to GitHub Issues (with duplicate detection)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "error_description": {"type": "string"},
                            "error_context": {"type": "string"},
                            "command": {"type": "string"},
                        },
                        "required": ["error_description"],
                    },
                ),
                types.Tool(
                    name="uninstall_tool",
                    description="Uninstall todo.ai",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "remove_data": {"type": "boolean"},
                            "remove_rules": {"type": "boolean"},
                            "force": {"type": "boolean"},
                        },
                    },
                ),
            ]

        @self.app.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
            """Handle MCP tool calls by routing to CLI command functions."""
            # Capture stdout to return as text content
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()

            try:
                # Basic task operations
                if name == "add_task":
                    tags = arguments.get("tags", [])
                    if not isinstance(tags, list):
                        tags = []
                    add_command(arguments["description"], tags, todo_path=self.todo_path)

                elif name == "add_subtask":
                    tags = arguments.get("tags", [])
                    if not isinstance(tags, list):
                        tags = []
                    add_subtask_command(
                        arguments["parent_id"],
                        arguments["description"],
                        tags,
                        todo_path=self.todo_path,
                    )

                elif name == "complete_task":
                    task_ids = [arguments["task_id"]]
                    with_subtasks = arguments.get("with_subtasks", False)
                    complete_command(task_ids, with_subtasks, todo_path=self.todo_path)

                elif name == "list_tasks":
                    tag = arguments.get("tag")
                    # list_command signature: (tag, incomplete_only, parents_only, has_subtasks, todo_path)
                    # Note: status filter not directly supported, would need to filter results
                    list_command(tag=tag, todo_path=self.todo_path)

                # Phase 1: Task Management
                elif name == "modify_task":
                    tags = arguments.get("tags", [])
                    if not isinstance(tags, list):
                        tags = []
                    modify_command(
                        arguments["task_id"],
                        arguments["description"],
                        tags,
                        todo_path=self.todo_path,
                    )

                elif name == "delete_task":
                    task_ids = [arguments["task_id"]]
                    with_subtasks = arguments.get("with_subtasks", False)
                    delete_command(task_ids, with_subtasks, todo_path=self.todo_path)

                elif name == "archive_task":
                    task_ids = [arguments["task_id"]]
                    reason = arguments.get("reason")
                    # archive_command signature: (task_ids, reason, todo_path) - no with_subtasks parameter
                    archive_command(task_ids, reason, todo_path=self.todo_path)

                elif name == "restore_task":
                    restore_command(arguments["task_id"], todo_path=self.todo_path)

                elif name == "undo_task":
                    undo_command(arguments["task_id"], todo_path=self.todo_path)

                # Phase 2: Note Management
                elif name == "add_note":
                    note_command(
                        arguments["task_id"],
                        arguments["note_text"],
                        todo_path=self.todo_path,
                    )

                elif name == "delete_note":
                    delete_note_command(arguments["task_id"], todo_path=self.todo_path)

                elif name == "update_note":
                    update_note_command(
                        arguments["task_id"],
                        arguments["new_note_text"],
                        todo_path=self.todo_path,
                    )

                # Phase 3: Task Display and Relationships
                elif name == "show_task":
                    show_command(arguments["task_id"], todo_path=self.todo_path)

                elif name == "relate_task":
                    relate_command(
                        arguments["task_id"],
                        arguments["rel_type"],
                        arguments["target_ids"],
                        todo_path=self.todo_path,
                    )

                # Phase 4: File Operations
                elif name == "lint_todo":
                    lint_command(todo_path=self.todo_path)

                elif name == "reformat_todo":
                    dry_run = arguments.get("dry_run", False)
                    reformat_command(dry_run, todo_path=self.todo_path)

                elif name == "resolve_conflicts":
                    dry_run = arguments.get("dry_run", False)
                    resolve_conflicts_command(dry_run, todo_path=self.todo_path)

                # Phase 5: System Operations
                elif name == "view_log":
                    filter_text = arguments.get("filter")
                    lines = arguments.get("lines")
                    log_command(filter_text=filter_text, lines=lines, todo_path=self.todo_path)

                elif name == "update_tool":
                    update_tool_command()

                elif name == "list_backups":
                    backups_command(todo_path=self.todo_path)

                elif name == "rollback":
                    target = arguments.get("target")
                    rollback_tool_command(target=target, todo_path=self.todo_path)

                # Phase 6: Configuration and Setup
                elif name == "show_config":
                    config_command(todo_path=self.todo_path)

                elif name == "detect_coordination":
                    detect_coordination_tool_command(todo_path=self.todo_path)

                elif name == "setup_coordination":
                    setup_coordination_tool_command(
                        arguments["coord_type"],
                        interactive=False,
                        todo_path=self.todo_path,
                    )

                elif name == "switch_mode":
                    switch_mode_tool_command(
                        arguments["mode"],
                        force=arguments.get("force", False),
                        renumber=arguments.get("renumber", False),
                        todo_path=self.todo_path,
                    )

                # Phase 7: Utility Commands
                elif name == "report_bug":
                    report_bug_tool_command(
                        arguments["error_description"],
                        error_context=arguments.get("error_context"),
                        command=arguments.get("command"),
                    )

                elif name == "uninstall_tool":
                    uninstall_tool_command(
                        remove_data=arguments.get("remove_data", False),
                        remove_rules=arguments.get("remove_rules", False),
                        force=arguments.get("force", False),
                    )

                else:
                    raise ValueError(f"Unknown tool: {name}")

                # Get captured output
                output = captured_output.getvalue()
                return [types.TextContent(type="text", text=output or "Success")]

            except Exception as e:
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]
            finally:
                sys.stdout = old_stdout

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.app.run(read_stream, write_stream, self.app.create_initialization_options())


async def main():
    """Main entry point for MCP server."""
    todo_path = Path.cwd() / "TODO.md"
    server = MCPServer(str(todo_path))
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
