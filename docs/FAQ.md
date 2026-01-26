# Frequently Asked Questions

## Why not use GitHub Issues?

AI agents need a **fast, local, Markdown-native** way to manage tasks. GitHub Issues adds complexity and overhead that slows down task management.

**Key differences:**

| Feature | todo.ai | GitHub Issues |
|---------|---------|---------------|
| **Speed** | Instant, local operations | API calls, network latency |
| **Authentication** | None required | OAuth/PAT tokens needed |
| **Rate Limits** | None | API rate limits apply |
| **Offline Support** | Full functionality | Requires network |
| **Format** | Plain Markdown | Proprietary API format |
| **Version Control** | Native Git integration | Separate from codebase |

**When to use each:**

- **todo.ai**: Day-to-day task tracking during development, AI agent workflows, quick task management
- **GitHub Issues**: Bug reports from users, feature requests, cross-repository coordination, public discussion

**Integration**: You can reference GitHub Issues in todo.ai tasks:

```
Create a task for fixing #123
Add subtask: Address PR #456 feedback
```

This keeps todo.ai fast and simple while maintaining links to your GitHub workflow.

## How do I migrate from the shell script to Python?

See the [Python Migration Guide](user/PYTHON_MIGRATION_GUIDE.md) for step-by-step instructions. The short version:

1. Install: `uv tool install ai-todo`
2. Replace `./todo.ai` with `todo-ai` in your workflow
3. No data migration needed - same file formats

## Can I use todo.ai without Python?

Yes. The legacy shell script (v2.x) is still available:

```bash
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai
```

Note: The shell script lacks MCP integration for AI agents. We recommend Python v3.0+ when possible.

## How do I set up Cursor integration?

Add this to your project's `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "todo-ai": {
      "command": "uvx",
      "args": ["--from", "ai-todo", "todo-ai", "serve", "--root", "${workspaceFolder}"]
    }
  }
}
```

See the [MCP Setup Guide](user/MCP_SETUP.md) for detailed instructions.

## Where is my data stored?

- **Tasks**: `TODO.md` in your project root
- **Configuration**: `.todo.ai/config.yaml`
- **State**: `.todo.ai/` directory (serial numbers, checksums, logs)

All files are plain text and safe to commit to Git.

## Can multiple people work on the same TODO.md?

Yes. Since TODO.md is a plain text file tracked in Git, standard Git workflows apply:

- Each developer works on their branch
- Merge conflicts are resolved like any other file
- Task IDs are unique within the file

For real-time collaboration, consider using GitHub Issues for shared tasks and todo.ai for personal/branch-specific work.
