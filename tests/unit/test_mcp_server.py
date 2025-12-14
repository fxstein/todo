import pytest

from todo_ai.mcp.server import MCPServer


@pytest.mark.asyncio
async def test_server_initialization():
    server = MCPServer()
    assert server.app.name == "todo-ai"


# Note: Testing MCP server comprehensively usually requires an MCP client client mock
# For unit testing, we can check if tools are registered conceptually,
# but testing `run()` involves stdio streams which is complex in unit tests.
# We'll stick to basic instantiation test for now.
