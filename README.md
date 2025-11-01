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
Link task 2 as depending on task 1
```

```
Add a note to task 1 that testing revealed an edge case
```

```
Complete task 1 with all its subtasks
```

```
Archive completed tasks
```

```
Show me details of task 1
```

```
Filter tasks by tag #api
```

```
Undo completion of task 1
```

```
Delete task 1
```

```
Restore deleted task 1
```

Your agent understands natural language requests and translates them to the appropriate `todo.ai` commands. All tasks are tracked in `TODO.md` in your repository.

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

At the moment, `todo.ai` is focused on a **single developer-AI agent relationship**. The tool does not yet sync issue numbers across teams, branches, or PRs. This functionality is planned but has not been implemented yet.

---

## Manual Installation

```bash
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai
```

**To update:** Re-run the curl command, or use `./todo.ai update`

---

## License

Apache License 2.0 - See LICENSE file
