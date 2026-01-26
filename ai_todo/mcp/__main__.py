import asyncio

from ai_todo.mcp.server import main as async_main


def main():
    """Entry point for ai-todo MCP server."""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
