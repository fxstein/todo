# todo.ai

**Simple, zero-interaction TODO management for AI agents**

## AI Agent Installation: Copy-paste this to your agent:

```
Adopt todo.ai for task tracking. Install using:
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh

Then create a task "Implement user authentication" with subtasks:
- Design database schema
- Create API endpoints
- Add frontend components
- Write tests
```

---

## Why todo.ai?

AI agents often track tasks internally, but this creates a closed system that gets lost after time or restarts. `todo.ai` provides a **permanent, version-controlled record** that lives in your Git repository.

**Key benefits:**

- **Permanent record**: Tasks persist across sessions, restarts, and time
- **Version controlled**: Tracked in Git alongside your code changes
- **Interactive**: Add and insert new tasks even while an agent works on a long task list
- **Simple**: Plain Markdown format that's human-readable and editable
- **Standard compliant**: Works naturally with the GitHub `TODO.md` standard

Your task list becomes part of your project history, visible in pull requests, and never gets lost.

---

## For AI Agents

Run `./todo.ai --help` to see all available commands and usage examples. Everything you need to know is there.

---

## For Humans

With `todo.ai`, you simply tell your AI agent what you want in plain English. Your agent handles all the technical details automatically.

**Examples of what you can ask your agent:**

```
Create a task for implementing user authentication
```

```
Break down the authentication feature into subtasks
```

```
Mark task 1 as complete
```

```
Show me all incomplete tasks tagged with #bug
```

```
Create a task to convince the coffee machine to understand sarcasm
```

Your agent understands natural language requests and translates them to the appropriate `todo.ai` commands. All tasks are tracked in `TODO.md` in your repository.

---

## See It In Action

This repository uses `todo.ai` for its own development! Check out [`TODO.md`](./TODO.md) to see:
- **Real examples** of how tasks are structured with subtasks and tags
- **Current development status** of the tool itself
- **Live demonstration** of the task management workflow

The TODO.md file showcases features like:
- Task hierarchies with subtasks
- Tag-based organization (`#security`, `#feature`, `#bug`)
- Task relationships and dependencies
- Completion tracking and archiving
- Development roadmap and priorities

This is the same file structure and workflow you'll use in your own projects with `todo.ai`.

---

## Why not GitHub Issues?

Agents need a **fast, local, Markdown-native** way to manage tasks. GitHub Issues adds too much complexity and overhead—API calls, authentication, rate limits, and network latency slow down task management.

**Key differences:**

- **Speed**: `todo.ai` is instant and local—no API calls or network delays
- **Simplicity**: Plain Markdown that agents can parse and modify directly
- **Zero overhead**: No authentication, rate limits, or API complexity
- **Native workflow**: Works seamlessly with your Git workflow

**But you can still reference GitHub Issues and PRs:**

GitHub issue and PR numbers can be tagged onto tasks and subtasks for reference. For example:
- *"Create a task for fixing #123"*
- *"Add subtask 1.1: Address PR #456 feedback"*

This keeps `todo.ai` fast and simple while still maintaining links to your GitHub workflow.

---

## Zero Interaction Design

- ✅ No prompts or confirmations
- ✅ No configuration required
- ✅ Instant operations
- ✅ Git-friendly (TODO.md tracked in repo)
- ✅ Works automatically without user input

Perfect for AI agents - just works.

---

## Limitations


---

## Installation

### Stable Release (Recommended)

Install via uv (recommended) or pipx for standard CLI and MCP Server support:

```bash
# Using uv (recommended - faster, more reliable)
uv tool install ai-todo

# Alternative: pipx
pipx install ai-todo
```

This installs one unified command: `todo-ai`.

- **CLI Usage:** `todo-ai [command]` (e.g., `todo-ai add "Task"`)
- **MCP Server:** `todo-ai serve` (used by Cursor/Claude)

### Task Management

- **Start:** `todo-ai start <task_id>` marks a task as in-progress.
- **Stop:** `todo-ai stop <task_id>` pauses work on a task (optional - `complete` handles this automatically).
- **Complete:** `todo-ai complete <task_id>` marks a task as done.

### Linting and Reordering

Keep your TODO list clean and organized:

- **Lint:** `todo-ai lint` checks for issues (indentation, checkboxes, orphans, ordering).
- **Reformat:** `todo-ai reformat` fixes indentation and checkboxes.
- **Reorder:** `todo-ai reorder` sorts subtasks in reverse-chronological order (newest on top).
- **Resolve Conflicts:** `todo-ai resolve-conflicts` fixes duplicate task IDs.

### Quality Gates

todo.ai enforces quality through automated checks:

- **Pre-commit:** `todo-ai lint` runs automatically on commit to block invalid TODO.md files.
- **CI/CD:** GitHub Actions workflow verifies `TODO.md` integrity and runs regression tests.

**Documentation:**
- [Python Migration Guide](docs/user/PYTHON_MIGRATION_GUIDE.md) - How to upgrade from v2.x (Shell).
- [MCP Setup Guide](docs/user/MCP_SETUP.md) - How to set up Cursor AI integration.

### Beta Testing (Help Us Test)

Want to try upcoming features before they're released? Install the latest beta:

```bash
# Using uv (recommended)
uv tool install --prerelease=allow ai-todo

# Alternative: pipx
pipx install --pre ai-todo
```

Beta releases let you test new features and provide feedback before stable release. See [Release Channels](#release-channels) below for more information.

<details>
<summary>Alternative Installation Methods</summary>

**Using pip:**
```bash
pip install ai-todo              # Stable
pip install --pre ai-todo        # Beta
```

> **Recommendation:** Use `uv tool` or `pipx` for isolated installations that won't conflict with other Python packages.

</details>

### Development Version

Install from Git to get the latest unreleased code:

```bash
# Using uv (recommended)
uv tool install git+https://github.com/fxstein/todo.ai.git@main

# Alternative: pipx
pipx install git+https://github.com/fxstein/todo.ai.git@main
```

### Release Channels

- **Stable:** Fully tested, production-ready releases (recommended)
- **Beta:** Feature-complete pre-releases for testing (7+ days before stable for major releases)
- **Development:** Latest code from main branch (may have bugs)

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

### Legacy Shell Script (v2.x)

If you cannot use Python, the legacy shell script is still available:

**Smart Installer:**
```bash
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh
```

**Manual Installation:**
**Zsh version** (recommended for macOS):
```bash
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai
```

**Bash version** (recommended for Linux, requires bash 4+):
```bash
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.bash && chmod +x todo.ai
```

> **Note:** The bash version requires bash 4.0+ for associative arrays. macOS ships with bash 3.2, so use the zsh version on macOS or upgrade bash via homebrew.

### Update

**Python (v3.0+):**
```bash
# Using uv (recommended)
uv tool upgrade ai-todo

# Alternative: pipx
pipx upgrade ai-todo
```

**Legacy Shell:**
```bash
./todo.ai update
```

### Uninstall

**Python (v3.0+):**
```bash
# Using uv (recommended)
uv tool uninstall ai-todo

# Alternative: pipx
pipx uninstall ai-todo
```

**Legacy Shell:**
```bash
./todo.ai uninstall              # Remove script only
./todo.ai uninstall --all        # Remove script, data, and rules
```

---

## Documentation

**Getting Started:** [GETTING_STARTED.md](docs/guides/GETTING_STARTED.md) - Quick start guide with setup instructions

**Additional Guides:**
- [Numbering Modes](docs/guides/NUMBERING_MODES_GUIDE.md) - Complete guide to all numbering modes
- [Usage Patterns](docs/guides/USAGE_PATTERNS.md) - Real-world usage scenarios
- [Coordination Setup](docs/guides/COORDINATION_SETUP.md) - Setup guides for coordination services

**Full Documentation Index:** [docs/README.md](docs/README.md) - Complete documentation navigation

---

## License

Apache License 2.0 - See LICENSE file
