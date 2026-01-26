"""Tests for Cursor rules auto-installation."""

from ai_todo.mcp.server import _init_cursor_rules


class TestCursorRulesAutoInstall:
    """Test MCP server auto-installs Cursor rules."""

    def test_creates_rule_file_when_missing(self, tmp_path):
        """Test that rule file is created when it doesn't exist."""
        _init_cursor_rules(tmp_path)

        rule_file = tmp_path / ".cursor" / "rules" / "ai-todo-task-management.mdc"
        assert rule_file.exists()
        assert "ai-todo" in rule_file.read_text()
        assert "MCP SERVER" in rule_file.read_text()

    def test_creates_rules_directory(self, tmp_path):
        """Test that .cursor/rules directory is created."""
        assert not (tmp_path / ".cursor").exists()

        _init_cursor_rules(tmp_path)

        assert (tmp_path / ".cursor" / "rules").is_dir()

    def test_does_not_overwrite_existing_rule(self, tmp_path):
        """Test that existing rule file is not overwritten."""
        rules_dir = tmp_path / ".cursor" / "rules"
        rules_dir.mkdir(parents=True)
        rule_file = rules_dir / "ai-todo-task-management.mdc"
        custom_content = "# Custom user rules\nDo not overwrite me!"
        rule_file.write_text(custom_content)

        _init_cursor_rules(tmp_path)

        # File should still have custom content
        assert rule_file.read_text() == custom_content

    def test_rule_content_matches_expected(self, tmp_path):
        """Test that created rule has expected content."""
        _init_cursor_rules(tmp_path)

        rule_file = tmp_path / ".cursor" / "rules" / "ai-todo-task-management.mdc"
        content = rule_file.read_text()

        # Check frontmatter
        assert 'description: "Task management via ai-todo MCP server"' in content
        assert "alwaysApply: true" in content

        # Check key instructions
        assert "USE THE MCP SERVER" in content
        assert "NEVER" in content
        assert "built-in TODO tools" in content

    def test_handles_permission_error_gracefully(self, tmp_path):
        """Test that permission errors don't raise exceptions."""
        # Create a read-only directory
        rules_dir = tmp_path / ".cursor" / "rules"
        rules_dir.mkdir(parents=True)

        # Make directory read-only (skip on Windows)
        import sys

        if sys.platform != "win32":
            rules_dir.chmod(0o444)
            try:
                # Should not raise - silently fails
                _init_cursor_rules(tmp_path)
            finally:
                # Restore permissions for cleanup
                rules_dir.chmod(0o755)
