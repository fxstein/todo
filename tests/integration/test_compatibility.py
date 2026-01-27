from ai_todo.core.file_ops import FileOps
from ai_todo.core.task import Task


def test_preserve_file_structure(tmp_path):
    """Test that FileOps preserves header content and regenerates standard footer.

    Note: Custom footer content is NOT preserved (GitHub Issue #47 fix).
    Footer is always regenerated with standard ai-todo timestamp format.
    """
    todo_path = tmp_path / "TODO.md"

    original_content = """# Custom Header
> Some warning

## Tasks
- [ ] **#1** Task 1

## Recently Completed
- [x] **#2** Task 2

## Deleted Tasks

------------------
**Last Updated:** Thu Oct 30 21:17:25 CET 2025
**Repository:** https://github.com/fxstein/ai-todo
**Maintenance:** Use `ai-todo` CLI/MCP
"""
    todo_path.write_text(original_content, encoding="utf-8")

    # 1. Read tasks
    ops = FileOps(str(todo_path))
    tasks = ops.read_tasks()

    assert len(tasks) == 2
    assert tasks[0].id == "1"
    assert tasks[1].id == "2"

    # 2. Add a new task (simulated by appending to list)
    new_task = Task(id="3", description="Task 3")
    tasks.append(new_task)

    # 3. Write tasks back
    ops.write_tasks(tasks)

    # 4. Verify content
    new_content = todo_path.read_text(encoding="utf-8")

    # Check that header is preserved
    assert "# Custom Header" in new_content
    assert "> Some warning" in new_content

    # Check that tasks are present
    assert "**#1** Task 1" in new_content
    assert "**#3** Task 3" in new_content

    # Check that footer is regenerated with standard format
    # (Custom footer content is NOT preserved - GitHub Issue #47 fix)
    assert "---" in new_content
    assert "Last Updated:" in new_content
