from pathlib import Path

from click.testing import CliRunner

from ai_todo.cli.main import cli


def test_start_from_shell_repo():
    """Test compatibility with an existing shell-script created repository.

    Note: Custom footer content (e.g., **Repository:**) is NOT preserved.
    Footer is always regenerated with standard ai-todo timestamp format (GitHub Issue #47 fix).
    """
    runner = CliRunner()

    with runner.isolated_filesystem():
        # 1. Setup shell-like environment
        todo_path = Path("TODO.md")
        config_dir = Path(".ai-todo")
        config_dir.mkdir()

        # Existing TODO.md
        todo_path.write_text(
            """# Project Tasks

## Tasks
- [ ] **#1** Legacy Task 1

## Recently Completed
- [x] **#2** Legacy Task 2

------------------
**Repository:** https://github.com/example/repo
""",
            encoding="utf-8",
        )

        # Existing Config
        (config_dir / "config.yaml").write_text("mode: single-user\n", encoding="utf-8")

        # Existing Serial (Last Used)
        (config_dir / ".ai-todo.serial").write_text("2", encoding="utf-8")

        # Existing Log
        (config_dir / ".ai-todo.log").write_text(
            "2025-01-01 | user | ADD | 1 | Legacy Task 1\n", encoding="utf-8"
        )

        # 2. Run Python CLI commands

        # A. List tasks
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "**#1** Legacy Task 1" in result.output

        # B. Add task (should continue numbering from 2 -> 3)
        result = runner.invoke(cli, ["add", "New Python Task"])
        assert result.exit_code == 0
        assert "Added: #3 New Python Task" in result.output

        # C. Verify Serial Update
        assert (config_dir / ".ai-todo.serial").read_text(encoding="utf-8") == "3"

        # D. Verify File Structure Preservation
        content = todo_path.read_text(encoding="utf-8")
        # Header preserved
        assert "# Project Tasks" in content
        # Tasks preserved
        assert "**#1** Legacy Task 1" in content
        assert "**#3** New Python Task" in content
        # Footer regenerated with standard format (custom footer NOT preserved)
        assert "Last Updated:" in content
