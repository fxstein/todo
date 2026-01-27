"""Test that MCP tools produce identical output to CLI commands.

This test suite verifies that every MCP tool produces exactly the same
results as its corresponding CLI command. This is critical for ensuring
consistent behavior across both interfaces.
"""

import io
import sys
from pathlib import Path

import pytest

import ai_todo.mcp.server as mcp_server_module
from ai_todo.cli.commands import (
    add_command,
    archive_command,
    complete_command,
    delete_command,
    lint_command,
    list_command,
    modify_command,
    note_command,
    show_command,
)
from ai_todo.mcp.server import mcp


@pytest.fixture
def test_todo_file(tmp_path):
    """Create a test TODO.md file."""
    todo_file = tmp_path / "TODO.md"
    todo_file.write_text(
        """# TODO

## Tasks

- [ ] **#1** First task `#test`
  > This is a note
- [ ] **#2** Second task `#feature`
  - [ ] **#2.1** Subtask one
  - [ ] **#2.2** Subtask two

## Recently Completed

## Deleted Tasks

**Repository:** https://github.com/fxstein/ai-todo
""",
        encoding="utf-8",
    )

    # Create .ai-todo directory
    todo_ai_dir = tmp_path / ".ai-todo"
    todo_ai_dir.mkdir(exist_ok=True)
    (todo_ai_dir / "serial").write_text("2", encoding="utf-8")
    (todo_ai_dir / "config.yaml").write_text(
        """mode: single-user
coordination: none
""",
        encoding="utf-8",
    )

    return str(todo_file)


def capture_cli_output(func, *args, **kwargs) -> str:
    """Capture CLI command output."""
    old_stdout = sys.stdout
    sys.stdout = captured = io.StringIO()
    try:
        func(*args, **kwargs)
        return captured.getvalue()
    finally:
        sys.stdout = old_stdout


async def capture_mcp_output(tool_name: str, arguments: dict, todo_path: str) -> str:
    """Capture MCP tool output by calling the tool directly."""
    # Set the global TODO path in the server module
    mcp_server_module.CURRENT_TODO_PATH = todo_path

    # Find the tool function
    # FastMCP stores tools in _tool_manager._tools dictionary
    try:
        tool = mcp._tool_manager._tools.get(tool_name)
        if tool:
            tool_func = tool.fn
        else:
            tool_func = None
    except AttributeError:
        # Fallback if internal structure changes, try public API if available
        # But for now we rely on internal structure for testing
        return "Error: Could not access tool manager"

    if not tool_func:
        return f"Unknown tool: {tool_name}"

    # Call the tool function with arguments
    # We use the underlying function 'fn' to bypass FastMCP runtime overhead for unit testing
    try:
        result = tool.fn(**arguments)
        return result
    except Exception as e:
        return f"Error calling tool {tool_name}: {e}"


@pytest.mark.asyncio
class TestMCPCLIParity:
    """Test parity between MCP tools and CLI commands."""

    async def test_add_task_parity(self, test_todo_file):
        """Test add_task MCP tool matches add CLI command."""
        # CLI output (add_command takes title as first arg)
        cli_output = capture_cli_output(
            add_command, "Test task", ["test", "feature"], todo_path=test_todo_file
        )

        # Reset file
        Path(test_todo_file).write_text(
            """# TODO

## Tasks

- [ ] **#1** First task `#test`
  > This is a note
- [ ] **#2** Second task `#feature`
  - [ ] **#2.1** Subtask one
  - [ ] **#2.2** Subtask two

## Recently Completed

## Deleted Tasks

**Repository:** https://github.com/fxstein/ai-todo
""",
            encoding="utf-8",
        )

        # MCP output (add_task takes title as first param)
        mcp_output = await capture_mcp_output(
            "add_task", {"title": "Test task", "tags": ["test", "feature"]}, test_todo_file
        )

        # Compare (both should show "Added: #N Test task `#feature` `#test`")
        # Task ID might differ (3 vs 4) due to serial file state, but format should match
        import re

        cli_match = re.search(r"Added: #(\d+) Test task `#feature` `#test`", cli_output)
        mcp_match = re.search(r"Added: #(\d+) Test task `#feature` `#test`", mcp_output)

        assert cli_match is not None, f"CLI output format incorrect: {cli_output}"
        assert mcp_match is not None, f"MCP output format incorrect: {mcp_output}"

        # Both should have same format, task IDs should be sequential (within 1-2 of each other)
        cli_id = int(cli_match.group(1))
        mcp_id = int(mcp_match.group(1))
        assert abs(cli_id - mcp_id) <= 2, f"Task IDs too different: CLI={cli_id}, MCP={mcp_id}"

    async def test_complete_task_parity(self, test_todo_file):
        """Test complete_task MCP tool matches complete CLI command."""
        # CLI output
        cli_output = capture_cli_output(
            complete_command, ["1"], with_subtasks=False, todo_path=test_todo_file
        )

        # Reset file
        Path(test_todo_file).write_text(
            """# TODO

## Tasks

- [ ] **#1** First task `#test`
  > This is a note
- [ ] **#2** Second task `#feature`
  - [ ] **#2.1** Subtask one
  - [ ] **#2.2** Subtask two

## Recently Completed

## Deleted Tasks

**Repository:** https://github.com/fxstein/ai-todo
""",
            encoding="utf-8",
        )

        # MCP output
        mcp_output = await capture_mcp_output(
            "complete_task", {"task_ids": ["1"], "with_subtasks": False}, test_todo_file
        )

        # Compare
        assert cli_output.strip() == mcp_output.strip()

    async def test_modify_task_parity(self, test_todo_file):
        """Test modify_task MCP tool matches modify CLI command."""
        # CLI output (modify_command takes title as second arg)
        cli_output = capture_cli_output(
            modify_command, "1", "Modified task", ["test", "modified"], todo_path=test_todo_file
        )

        # Reset file
        Path(test_todo_file).write_text(
            """# TODO

## Tasks

- [ ] **#1** First task `#test`
  > This is a note
- [ ] **#2** Second task `#feature`
  - [ ] **#2.1** Subtask one
  - [ ] **#2.2** Subtask two

## Recently Completed

## Deleted Tasks

**Repository:** https://github.com/fxstein/ai-todo
""",
            encoding="utf-8",
        )

        # MCP output (modify_task takes title as param)
        mcp_output = await capture_mcp_output(
            "modify_task",
            {"task_id": "1", "title": "Modified task", "tags": ["test", "modified"]},
            test_todo_file,
        )

        # Compare
        assert cli_output.strip() == mcp_output.strip()

    async def test_delete_task_parity(self, test_todo_file):
        """Test delete_task MCP tool matches delete CLI command."""
        # CLI output
        cli_output = capture_cli_output(
            delete_command, ["1"], with_subtasks=False, todo_path=test_todo_file
        )

        # Reset file
        Path(test_todo_file).write_text(
            """# TODO

## Tasks

- [ ] **#1** First task `#test`
  > This is a note
- [ ] **#2** Second task `#feature`
  - [ ] **#2.1** Subtask one
  - [ ] **#2.2** Subtask two

## Recently Completed

## Deleted Tasks

**Repository:** https://github.com/fxstein/ai-todo
""",
            encoding="utf-8",
        )

        # MCP output
        mcp_output = await capture_mcp_output(
            "delete_task", {"task_ids": ["1"], "with_subtasks": False}, test_todo_file
        )

        # Compare
        assert cli_output.strip() == mcp_output.strip()

    async def test_archive_task_parity(self, test_todo_file):
        """Test archive_task MCP tool matches archive CLI command."""
        # Clear session completions to avoid cooldown from previous tests
        mcp_server_module.SESSION_COMPLETIONS.clear()

        # Start with a pre-completed task (not completed in this session)
        # This avoids the MCP session-based archive cooldown
        Path(test_todo_file).write_text(
            """# TODO

## Tasks

- [x] **#1** First task `#test` (2026-01-01)
  > This is a note
- [ ] **#2** Second task `#feature`
  - [ ] **#2.1** Subtask one
  - [ ] **#2.2** Subtask two

## Recently Completed

## Deleted Tasks

**Repository:** https://github.com/fxstein/ai-todo
""",
            encoding="utf-8",
        )

        # CLI output
        cli_output = capture_cli_output(archive_command, ["1"], None, todo_path=test_todo_file)

        # Reset file with pre-completed task
        Path(test_todo_file).write_text(
            """# TODO

## Tasks

- [x] **#1** First task `#test` (2026-01-01)
  > This is a note
- [ ] **#2** Second task `#feature`
  - [ ] **#2.1** Subtask one
  - [ ] **#2.2** Subtask two

## Recently Completed

## Deleted Tasks

**Repository:** https://github.com/fxstein/ai-todo
""",
            encoding="utf-8",
        )

        # MCP output (no cooldown since task wasn't completed in this session)
        mcp_output = await capture_mcp_output("archive_task", {"task_ids": ["1"]}, test_todo_file)

        # Compare
        assert cli_output.strip() == mcp_output.strip()

    async def test_description_operations_parity(self, test_todo_file):
        """Test set_description MCP tool matches note CLI command."""
        # Use task #2 which has no notes
        # Add note - CLI (note_command adds a note/description)
        cli_add_output = capture_cli_output(
            note_command, "2", "Test note", todo_path=test_todo_file
        )

        # Reset file (task #2 has no notes)
        Path(test_todo_file).write_text(
            """# TODO

## Tasks

- [ ] **#1** First task `#test`
  > This is a note
- [ ] **#2** Second task `#feature`
  - [ ] **#2.1** Subtask one
  - [ ] **#2.2** Subtask two

## Recently Completed

## Deleted Tasks

**Repository:** https://github.com/fxstein/ai-todo
""",
            encoding="utf-8",
        )

        # set_description on task without notes matches note_command output
        mcp_add_output = await capture_mcp_output(
            "set_description", {"task_id": "2", "description": "Test note"}, test_todo_file
        )

        assert cli_add_output.strip() == mcp_add_output.strip()

    async def test_show_task_parity(self, test_todo_file):
        """Test show_task MCP tool matches show CLI command."""
        # CLI output
        cli_output = capture_cli_output(show_command, "2", todo_path=test_todo_file)

        # MCP output
        mcp_output = await capture_mcp_output("show_task", {"task_id": "2"}, test_todo_file)

        # Compare
        assert cli_output.strip() == mcp_output.strip()

    async def test_lint_parity(self, test_todo_file):
        """Test lint MCP tool matches lint CLI command."""
        # CLI output
        cli_output = capture_cli_output(lint_command, todo_path=test_todo_file)

        # MCP output
        mcp_output = await capture_mcp_output("lint", {}, test_todo_file)

        # Compare (lint output should be identical)
        assert cli_output.strip() == mcp_output.strip()

    async def test_list_tasks_output_format(self, test_todo_file):
        """Test list_tasks MCP tool produces correct format."""
        mcp_output = await capture_mcp_output("list_tasks", {}, test_todo_file)

        # Should contain task markers
        assert "**#1**" in mcp_output
        assert "**#2**" in mcp_output
        assert "[ ]" in mcp_output  # Checkbox

        # Compare with CLI
        cli_output = capture_cli_output(list_command, None, False, False, False, test_todo_file)
        assert cli_output.strip() == mcp_output.strip()


@pytest.mark.asyncio
async def test_all_mcp_tools_exist():
    """Verify all expected MCP tools are registered."""

    # Get registered tools from FastMCP instance
    try:
        tool_names = set(mcp._tool_manager._tools.keys())
    except AttributeError:
        pytest.fail("Could not access tools from FastMCP instance")

    # Expected tools (all phases)
    expected_tools = {
        # Core Tasks
        "add_task",
        "add_subtask",
        "complete_task",
        "list_tasks",
        "modify_task",
        "delete_task",
        "archive_task",
        "restore_task",
        "undo_task",
        # Progress
        "start_task",
        "stop_task",
        "get_active_tasks",
        # Description & Tags
        "set_description",
        "set_tags",
        # Display & Relationships
        "show_task",
        "relate_task",
        # File Operations
        "lint",
        "reformat",
        "reorder",
        "resolve_conflicts",
        # Configuration
        "show_config",
        "detect_coordination",
        "setup_coordination",
        "switch_mode",
        # Tamper Detection
        "accept_tamper",
        # Info
        "version",
    }

    # Verify all tools exist
    missing = expected_tools - tool_names
    assert not missing, f"Missing MCP tools: {missing}"

    # Verify we have the right count
    assert len(tool_names) >= len(expected_tools), (
        f"Expected at least {len(expected_tools)} tools, got {len(tool_names)}"
    )


@pytest.mark.asyncio
async def test_mcp_archive_cooldown_blocks_immediate_archive(test_todo_file):
    """Test MCP archive cooldown blocks archiving tasks completed in the same session."""
    # Clear any previous session state
    mcp_server_module.SESSION_COMPLETIONS.clear()

    # Complete a task via MCP (this adds it to SESSION_COMPLETIONS)
    complete_output = await capture_mcp_output("complete_task", {"task_ids": ["1"]}, test_todo_file)
    assert "Completed:" in complete_output

    # Try to archive immediately via MCP - should be blocked by session cooldown
    archive_output = await capture_mcp_output("archive_task", {"task_ids": ["1"]}, test_todo_file)
    assert "requires human review" in archive_output
    assert "Archived" not in archive_output


@pytest.mark.asyncio
async def test_mcp_archive_cooldown_allows_non_session_tasks(test_todo_file):
    """Test MCP archive allows archiving tasks NOT completed in current session."""
    # Clear any previous session state
    mcp_server_module.SESSION_COMPLETIONS.clear()

    # Write a pre-completed task (simulating task completed in previous session)
    Path(test_todo_file).write_text(
        """# TODO

## Tasks

- [x] **#1** First task `#test` (2026-01-01)
- [ ] **#2** Second task `#feature`

## Recently Completed

## Deleted Tasks

**Repository:** https://github.com/fxstein/ai-todo
""",
        encoding="utf-8",
    )

    # Archive via MCP - should work (task wasn't completed in this session)
    archive_output = await capture_mcp_output("archive_task", {"task_ids": ["1"]}, test_todo_file)
    assert "Archived 1 task(s)" in archive_output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
