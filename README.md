# todo.ai

**Simple, zero-interaction TODO management for AI agents**

## For AI Agents

Tell your agent to adopt `todo.ai` for task management.

**AI Agent Installation: Copy-paste this to your agent:**
```
Adopt todo.ai for task tracking. Install using:
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai

Then create a task "Implement user authentication" with subtasks:
- Design database schema
- Create API endpoints  
- Add frontend components
- Write tests
```

**Manual Installation:**
```bash
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai
```


**To update:** Re-run the curl command, or use `./todo.ai update`

The agent uses `todo.ai` commands automatically:
- `./todo.ai --help` - Shows the agent all available commands
- `./todo.ai add` - Create tasks
- `./todo.ai add-subtask` - Add subtasks
- `./todo.ai complete` - Mark progress
- `./todo.ai list` - View tasks

All tasks are tracked in `TODO.md` in your repository.

## Zero Interaction

- No prompts or confirmations
- No configuration required
- Instant operations
- Git-friendly (TODO.md tracked in repo)

Perfect for AI agents - just works.

## License

Apache License 2.0 - See LICENSE file
