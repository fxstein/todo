# todo.ai

**Simple, zero-interaction TODO management for AI agents**

## AI Agent Installation: Copy-paste this to your agent:

```
Adopt todo.ai for task tracking. Install using:
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai

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

## Manual Installation

```bash
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai
```

**To update:** Re-run the curl command, or use `./todo.ai update`

**To uninstall:** Run `./todo.ai uninstall` (removes script only) or `./todo.ai uninstall --all` (removes script, data, and rules)

---

## Documentation

**Getting Started:** [GETTING_STARTED.md](docs/GETTING_STARTED.md) - Quick start guide with setup instructions

**Additional Guides:**
- [Numbering Modes](docs/NUMBERING_MODES_GUIDE.md) - Complete guide to all numbering modes
- [Usage Patterns](docs/USAGE_PATTERNS.md) - Real-world usage scenarios
- [Coordination Setup](docs/COORDINATION_SETUP.md) - Setup guides for coordination services

---

## License

Apache License 2.0 - See LICENSE file
