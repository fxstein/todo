This release introduces a comprehensive uninstall feature that makes it easy to cleanly remove `todo.ai` from your system.

**New Feature: Uninstall Command**

The new `uninstall` command provides a safe and straightforward way to remove `todo.ai`. It automatically detects where the tool is installed and what associated files exist, then gives you clear control over what gets removed.

**Key Features:**
- **Safe by default**: User data (TODO.md and `.todo.ai/` directory) is preserved unless explicitly requested
- **Automatic detection**: Finds the script location, data directory, and Cursor rules automatically
- **Clear preview**: Shows exactly what will be removed before asking for confirmation
- **Flexible options**: Choose what to remove with `--remove-data`, `--remove-rules`, or `--all`
- **Complete cleanup**: Optionally removes the script, data directory, and Cursor rules created by `todo.ai`

**Usage:**
```bash
# Remove script only (preserves data and rules)
./todo.ai uninstall

# Remove script and data directory
./todo.ai uninstall --remove-data

# Remove script and Cursor rules
./todo.ai uninstall --remove-rules

# Remove everything (script, data, and rules)
./todo.ai uninstall --all
```

**For AI Agents:**
```bash
./todo.ai uninstall [--remove-data] [--remove-rules] [--all]
```

**For Humans:**
Tell your agent: "Uninstall todo.ai" or "Remove todo.ai from the system"

The uninstall process is interactive and will show you what will be removed before asking for confirmation. Your `TODO.md` file is always preserved as it contains your task data.
