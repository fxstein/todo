# README.md Redesign for v3.0

**Task:** #203.1 - Design new README structure
**Status:** In Progress
**Date:** 2026-01-26

## Current State Assessment

### Problems with Current README

1. **Inconsistent Interface Hierarchy**
   - The "AI Agent Installation" section still uses curl/shell script
   - MCP is mentioned but not as the primary interface
   - Installation section lists Python first but doesn't emphasize MCP

2. **Confusing Installation Options**
   - Too many options presented at once (uv, pipx, pip, curl, zsh, bash)
   - No clear recommendation for the average user
   - Legacy shell script given equal weight to modern Python/MCP

3. **Missing Zero-Install Option**
   - `uvx` allows running without installation but isn't prominently featured
   - This is the easiest path for new users but is buried in docs

4. **Outdated "For AI Agents" Section**
   - Still references `./todo.ai --help` (shell script)
   - Doesn't mention MCP tools at all

5. **Verbose and Repetitive**
   - Same information repeated in multiple sections
   - Installation instructions scattered across document

### Current Structure

```
1. Title + Tagline
2. AI Agent Installation (shell script - OUTDATED)
3. Why todo.ai?
4. For AI Agents (shell script reference - OUTDATED)
5. For Humans
6. See It In Action
7. Why not GitHub Issues?
8. Zero Interaction Design
9. Limitations (empty)
10. Installation (long, confusing)
11. Documentation
12. License
```

## Proposed New Structure

### Design Principles

1. **MCP First** - The primary interface for AI agents
2. **Progressive Disclosure** - Simple first, details later
3. **Clear Hierarchy** - uvx → uv → legacy shell
4. **Minimal Friction** - Zero-install option front and center

### New Structure

```
1. Title + Tagline
2. Quick Start (MCP with uvx - ZERO INSTALL)
3. Why todo.ai?
4. Installation Options
   a. Zero-Install MCP (uvx) - PRIMARY
   b. System Install (uv/pipx) - SECONDARY
   c. Legacy Shell Script - FALLBACK
5. For Humans (natural language examples)
6. See It In Action
7. Documentation Links
8. License
```

## Proposed Content

### Section 1: Title + Tagline

```markdown
# todo.ai

**AI-native task management for coding agents**

Simple, persistent, version-controlled TODO tracking that works naturally with AI agents like Cursor, Claude, and Copilot.
```

### Section 2: Quick Start (MCP - Zero Install)

```markdown
## Quick Start

Add this to your project's `.cursor/mcp.json`:

\`\`\`json
{
  "mcpServers": {
    "todo-ai": {
      "command": "uvx",
      "args": ["ai-todo", "serve", "--root", "${workspaceFolder}"]
    }
  }
}
\`\`\`

That's it! Your AI agent can now manage tasks directly. No installation required.

**Try it:** Ask your agent to "create a task for implementing user authentication"
```

### Section 3: Why todo.ai?

```markdown
## Why todo.ai?

AI agents track tasks internally, but this creates a closed system that gets lost after sessions end. todo.ai provides a **permanent, version-controlled record** in your Git repository.

- **Persistent**: Tasks survive across sessions, restarts, and time
- **Version Controlled**: Tracked in Git alongside your code
- **AI-Native**: MCP integration for direct agent interaction
- **Human Readable**: Plain Markdown in standard TODO.md format
- **Zero Config**: Works immediately, no setup required
```

### Section 4: Installation Options

```markdown
## Installation Options

### Option A: Zero-Install MCP (Recommended)

For AI agent integration via Cursor or similar IDEs:

**Project-specific** (`.cursor/mcp.json`):
\`\`\`json
{
  "mcpServers": {
    "todo-ai": {
      "command": "uvx",
      "args": ["ai-todo", "serve", "--root", "${workspaceFolder}"]
    }
  }
}
\`\`\`

This uses `uvx` to run todo-ai on-demand without permanent installation. Requires [uv](https://docs.astral.sh/uv/) to be installed.

### Option B: System Installation

For CLI usage or permanent MCP server setup:

\`\`\`bash
# Install globally (recommended)
uv tool install ai-todo

# Or with pipx
pipx install ai-todo
\`\`\`

**CLI Usage:** `ai-todo [command]` (e.g., `ai-todo add "My task"`)
**MCP Server:** `ai-todo serve` (for Cursor integration)

### Option C: Legacy Shell Script

For environments without Python 3.10+:

\`\`\`bash
# Smart installer (detects your shell)
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh

# Or manual download
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai
\`\`\`

**Usage:** `./todo.ai [command]`

> **Note:** The shell script provides core functionality but lacks MCP integration. We recommend upgrading to Python v3.0+ when possible.
```

### Section 5: For Humans

```markdown
## For Humans

With todo.ai, you simply tell your AI agent what you want in plain English:

- "Create a task for implementing user authentication"
- "Break down the auth feature into subtasks"
- "Mark task 1 as complete"
- "Show me all tasks tagged with #bug"
- "Archive completed tasks"

Your agent handles the technical details. All tasks are stored in `TODO.md` in your repository.
```

### Section 6: See It In Action

```markdown
## See It In Action

This repository uses todo.ai for its own development! Check [`TODO.md`](./TODO.md) to see:

- Task hierarchies with subtasks
- Tag-based organization (`#feature`, `#bug`, `#documentation`)
- Completion tracking and archiving
- Real development workflow in action
```

### Section 7: Documentation Links

```markdown
## Documentation

- **[MCP Setup Guide](docs/user/MCP_SETUP.md)** - Detailed Cursor integration
- **[Migration Guide](docs/user/PYTHON_MIGRATION_GUIDE.md)** - Upgrading from v2.x shell script
- **[Getting Started](docs/guides/GETTING_STARTED.md)** - Complete setup walkthrough
- **[Full Documentation](docs/README.md)** - All guides and references
```

### Section 8: License

```markdown
## License

Apache License 2.0 - See [LICENSE](LICENSE)
```

## Sections to Remove or Relocate

### Remove Entirely

1. **"AI Agent Installation" section** - Replaced by Quick Start
2. **"For AI Agents" section** - Outdated shell script reference
3. **"Why not GitHub Issues?"** - Move to FAQ or separate doc
4. **"Zero Interaction Design"** - Incorporate into "Why todo.ai?"
5. **"Limitations"** - Empty, remove or populate
6. **Detailed installation subsections** - Collapse into cleaner structure

### Relocate to Separate Docs

1. **Beta Testing instructions** → `docs/guides/BETA_TESTING_GUIDE.md`
2. **TODO.md formatting standards** → `docs/development/TODO_FORMAT.md`
3. **Quality gates (pre-commit, CI)** → `docs/development/QUALITY_GATES.md`
4. **Release channels explanation** → `docs/guides/INSTALLATION.md`

## Interface Hierarchy Summary

| Priority | Interface | Setup Method | Use Case |
|----------|-----------|--------------|----------|
| 1 (Primary) | MCP Server | `uvx` in mcp.json | AI agent integration, zero-install |
| 2 (Secondary) | CLI | `uv tool install` | Command-line users, scripts |
| 3 (Legacy) | Shell Script | `curl` download | No Python 3.10+ available |

## Migration Path

For existing users:

1. **Shell → CLI**: `uv tool install ai-todo`, replace `./todo.ai` with `ai-todo`
2. **CLI → MCP**: Add `.cursor/mcp.json` config, agents use MCP automatically
3. **Shell → MCP**: Install uv, add `.cursor/mcp.json` config

## Design Decisions

| Question | Decision |
|----------|----------|
| GitHub Issues reference | Keep brief mention in "For Humans" section (e.g., "Reference GitHub issues: 'Fix bug from #123'") |
| "Why not GitHub Issues?" section | Move to new `docs/FAQ.md` page |
| Comparison page for alternatives | Skip for now, can add later if needed |
