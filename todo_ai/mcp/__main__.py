import asyncio

from todo_ai.mcp.server import main as async_main


def main():
    """Entry point for todo-ai-mcp."""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
