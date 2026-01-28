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

    def test_overwrites_existing_rule_when_content_differs(self, tmp_path):
        """Test that existing rule file is overwritten when content differs from shipped content."""
        from ai_todo.mcp.server import AI_TODO_CURSOR_RULE

        rules_dir = tmp_path / ".cursor" / "rules"
        rules_dir.mkdir(parents=True)
        rule_file = rules_dir / "ai-todo-task-management.mdc"
        custom_content = "# Custom user rules\nDo not overwrite me!"
        rule_file.write_text(custom_content)

        _init_cursor_rules(tmp_path)

        canonical = AI_TODO_CURSOR_RULE.strip() + "\n"
        assert rule_file.read_text() == canonical

    def test_does_not_overwrite_when_content_matches(self, tmp_path):
        """Test that existing rule file is left unchanged when content matches shipped content."""
        from ai_todo.mcp.server import AI_TODO_CURSOR_RULE

        _init_cursor_rules(tmp_path)
        rule_file = tmp_path / ".cursor" / "rules" / "ai-todo-task-management.mdc"
        canonical = AI_TODO_CURSOR_RULE.strip() + "\n"
        assert rule_file.read_text() == canonical

        _init_cursor_rules(tmp_path)
        assert rule_file.read_text() == canonical

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

        # Managed-file header (task #265)
        assert "managed by ai-todo" in content
        assert "may override" in content

        # Commit guideline (task #265)
        assert "When committing" in content
        assert "TODO.md" in content
        assert ".ai-todo/" in content
        assert "stage and commit them together" in content

        # Task-tracking rules (task #265)
        assert "TodoWrite" in content
        assert "task tracking" in content
        assert "use ai-todo for task tracking" in content

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
