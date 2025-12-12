import asyncio
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from todo_ai.core.task import TaskManager
from todo_ai.core.file_ops import FileOps

class MCPServer:
    """MCP server for todo.ai."""
    
    def __init__(self):
        self.app = Server("todo-ai")
        self.file_ops = FileOps()
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup MCP request handlers."""
        
        @self.app.list_tools()
        async def list_tools() -> list[types.Tool]:
            return [
                types.Tool(
                    name="add_task",
                    description="Add a new task to TODO.md",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "description": {"type": "string"},
                            "tags": {
                                "type": "array", 
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["description"]
                    }
                ),
                types.Tool(
                    name="complete_task",
                    description="Mark a task as complete",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"}
                        },
                        "required": ["task_id"]
                    }
                ),
                types.Tool(
                    name="list_tasks",
                    description="List tasks from TODO.md",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "enum": ["pending", "completed", "archived"]},
                            "tag": {"type": "string"}
                        }
                    }
                )
            ]

        @self.app.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
            tasks = self.file_ops.read_tasks()
            manager = TaskManager(tasks)
            
            try:
                if name == "add_task":
                    task = manager.add_task(
                        description=arguments["description"],
                        tags=arguments.get("tags")
                    )
                    self.file_ops.write_tasks(manager.list_tasks())
                    return [types.TextContent(type="text", text=f"Added: #{task.id} {task.description}")]
                    
                elif name == "complete_task":
                    task = manager.complete_task(arguments["task_id"])
                    self.file_ops.write_tasks(manager.list_tasks())
                    return [types.TextContent(type="text", text=f"Completed: #{task.id} {task.description}")]
                    
                elif name == "list_tasks":
                    # filters = {}
                    if arguments.get("status"):
                        # Convert string to enum if needed, or update TaskManager to handle strings
                        # For now, simplistic filtering:
                        pass # Filter logic handled in manager usually but simpler here for now
                        
                    results = manager.list_tasks()
                    output = ""
                    for task in results:
                        # Simple format
                        if arguments.get("status") and task.status.value != arguments["status"]:
                            continue
                        if arguments.get("tag") and arguments["tag"] not in task.tags:
                            continue
                            
                        checkbox = "[x]" if task.status.value != "pending" else "[ ]"
                        output += f"{checkbox} #{task.id} {task.description}\n"
                        
                    return [types.TextContent(type="text", text=output or "No tasks found.")]
                    
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.app.run(
                read_stream,
                write_stream,
                self.app.create_initialization_options()
            )

async def main():
    server = MCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())

