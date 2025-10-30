# todo - AI-Agent TODO Tracker

**Simple, zero-interaction TODO management for AI agents**

## For AI Agents

Tell your agent to adopt `todo.zsh` for task management.

**Repository:** https://github.com/fxstein/todo

**Copy-paste this to your agent:**
```
Adopt todo.zsh for task tracking from https://github.com/fxstein/todo.
Download todo.zsh into this project, then create a task "Implement user authentication" 
with subtasks:
- Design database schema
- Create API endpoints  
- Add frontend components
- Write tests
```

The agent will automatically install by downloading:
```bash
curl -o todo.zsh https://raw.githubusercontent.com/fxstein/todo/main/todo.zsh
chmod +x todo.zsh
```

**To update:** Re-run the curl command, or use `./todo.zsh update`

The agent uses `todo.zsh` commands automatically:
- `./todo.zsh add` - Create tasks
- `./todo.zsh add-subtask` - Add subtasks
- `./todo.zsh complete` - Mark progress
- `./todo.zsh list` - View tasks

All tasks are tracked in `TODO.md` in your repository.

## Zero Interaction

- No prompts or confirmations
- No configuration required
- Instant operations
- Git-friendly (TODO.md tracked in repo)

Perfect for AI agents - just works.

## License

Apache License 2.0 - See LICENSE file
