# todo - Simple TODO Tracker

**AI-agent first TODO management - zero interaction, pure simplicity**

## Quick Start

**1. Install**
```zsh
git clone https://github.com/fxstein/todo.git
cd todo
chmod +x todo.zsh
```

**2. Add your first task**
```zsh
./todo.zsh add "First task" "#tag"
```

**3. Done!** Your `TODO.md` is automatically created and ready.

## Essential Commands

```zsh
# Add tasks
./todo.zsh add "Task description" "#tag"

# Add subtasks
./todo.zsh add-subtask 1 "Subtask description"

# Complete tasks
./todo.zsh complete 1
./todo.zsh complete 1 --with-subtasks  # Include all subtasks

# View tasks
./todo.zsh list
./todo.zsh list --incomplete-only

# Archive completed
./todo.zsh archive 1
```

That's it. No configuration. No prompts. Just works.

## Why This Tool?

- ✅ **Zero interaction** - Perfect for AI agents
- ✅ **Git-friendly** - TODO.md tracked in your repo
- ✅ **Simple IDs** - Sequential numbering (1, 2, 3...)
- ✅ **Fast** - Local files, instant operations

See `./todo.zsh --help` for complete command reference.

## License

Apache License 2.0 - See LICENSE file
