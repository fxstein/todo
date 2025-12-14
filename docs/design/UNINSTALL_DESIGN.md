# Uninstall Feature Design

## Overview

The uninstall feature enables users to cleanly remove `todo.ai` from their system. It safely removes the script file and optionally removes associated data directories and Cursor rules, while preserving user data by default.

## Problem Statement

Currently, to uninstall `todo.ai`, users must manually:
1. Find where the script is installed
2. Delete the script file
3. Optionally remove the `.todo.ai/` directory
4. Optionally remove Cursor rules created by `todo.ai`

This process is error-prone and may leave orphaned files or directories. Users may not know where the script was installed or which Cursor rules were created by `todo.ai`.

## Goals

1. **Simple Uninstall**: Provide a single command to uninstall the tool
2. **Safe by Default**: Preserve user data (TODO.md, .todo.ai/) unless explicitly requested
3. **Complete Cleanup**: Optionally remove all associated files and directories
4. **Clear Feedback**: Show what will be removed and require confirmation
5. **Path Detection**: Automatically detect where the tool is installed

## Architecture

### Components

1. **Installation Detection**: Detects where `todo.ai` is installed
2. **File Discovery**: Finds all associated files and directories
3. **Uninstall Handler**: Orchestrates the removal process
4. **Confirmation System**: Requires user confirmation before removal

### Workflow

```
┌─────────────────┐
│ uninstall cmd   │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Detect Installation │
│ - Script location   │
│ - .todo.ai/ dir     │
│ - Cursor rules      │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Show What Will Be   │
│ Removed              │
│ - Script file       │
│ - .todo.ai/ (opt)   │
│ - Cursor rules (opt)│
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ User Confirmation   │
│ - Required          │
│ - Options for data  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Execute Removal     │
│ - Remove script     │
│ - Remove dirs (opt) │
│ - Clean rules (opt) │
└─────────────────────┘
```

## Implementation Details

### Installation Detection

The uninstall function should use `get_script_path()` to detect where the script is installed:

```zsh
uninstall_tool() {
    local script_path
    script_path=$(get_script_path) || {
        echo "Error: Cannot locate todo.ai script"
        echo "It may already be uninstalled."
        return 1
    }

    # ... rest of uninstall logic
}
```

### Files to Remove

1. **Script File** (always removed):
   - The `todo.ai` script itself (detected via `get_script_path()`)

2. **Data Directory** (optional, default: preserve):
   - `.todo.ai/` directory containing:
     - `.todo.ai.log` (operation log)
     - `.todo.ai.serial` (task ID counter)
     - `backups/` (versioned backups)
     - `migrations/` (migration markers)

3. **Cursor Rules** (optional, default: preserve):
   - `.cursor/rules/todo.ai-*.mdc` files (end-user rules)
   - Note: Developer rules (without `todo.ai-` prefix) should NOT be removed

### Command Options

```bash
# Basic uninstall (removes script only, preserves data)
./todo.ai uninstall

# Uninstall with options
./todo.ai uninstall --remove-data      # Remove .todo.ai/ directory
./todo.ai uninstall --remove-rules    # Remove Cursor rules created by todo.ai
./todo.ai uninstall --all             # Remove everything (script + data + rules)
```

### Confirmation Flow

1. **Show what will be removed**:
   ```
   The following will be removed:
   - Script: /path/to/todo.ai
   - Data directory: /path/to/.todo.ai/ (optional)
   - Cursor rules: .cursor/rules/todo.ai-*.mdc (optional)
   ```

2. **Ask for confirmation**:
   ```
   Proceed with uninstall? (y/N)
   ```

3. **If data or rules are included, show warning**:
   ```
   ⚠️  Warning: This will remove your TODO data (.todo.ai/ directory).
   ⚠️  Your TODO.md file will remain untouched.
   ```

### Safety Features

1. **Data Preservation by Default**: Never remove `.todo.ai/` or Cursor rules unless explicitly requested
2. **TODO.md Preservation**: Never remove `TODO.md` (user data)
3. **Confirmation Required**: Always require user confirmation
4. **Read-only Check**: Check if files are writable before attempting removal
5. **Error Handling**: Gracefully handle permission errors or missing files

## User Interface

### Command Syntax

```bash
./todo.ai uninstall [OPTIONS]
```

### Options

- `--remove-data` or `--data`: Remove `.todo.ai/` directory (preserves TODO.md)
- `--remove-rules` or `--rules`: Remove Cursor rules created by `todo.ai`
- `--all`: Remove script, data directory, and Cursor rules
- `--force` or `-f`: Skip confirmation (use with caution)

### Example Output

```
$ ./todo.ai uninstall --all

🗑️  Uninstalling todo.ai

The following will be removed:
  ✗ Script: /Users/username/bin/todo.ai
  ✗ Data directory: /path/to/project/.todo.ai/
  ✗ Cursor rules:
      - .cursor/rules/todo.ai-task-management.mdc
      - .cursor/rules/todo.ai-installation.mdc
      - .cursor/rules/todo.ai-bug-reporting.mdc

⚠️  Warning: This will remove your TODO data (.todo.ai/ directory).
⚠️  Your TODO.md file will remain untouched.

Proceed with uninstall? (y/N): y

✅ Removed script: /Users/username/bin/todo.ai
✅ Removed data directory: /path/to/project/.todo.ai/
✅ Removed 3 Cursor rules

✅ Uninstall complete!
```

## Edge Cases

1. **Script not found**: Inform user it may already be uninstalled
2. **Permission denied**: Show clear error message
3. **Partial installation**: Handle missing files gracefully
4. **Symlinks**: Follow symlinks to actual script location
5. **Multiple installations**: Uninstall from current working directory's installation only

## Testing Strategy

1. **Basic uninstall**: Remove script only
2. **Uninstall with data**: Remove script + `.todo.ai/`
3. **Uninstall with rules**: Remove script + Cursor rules
4. **Full uninstall**: Remove everything
5. **Permission errors**: Test with read-only files
6. **Missing files**: Test when files don't exist
7. **Symlink handling**: Test with symlinked installations

## Security Considerations

1. **Never remove TODO.md**: User data must be preserved
2. **Confirm destructive operations**: Always require confirmation
3. **Safe defaults**: Preserve data unless explicitly requested
4. **Path validation**: Verify paths before removal to prevent accidental deletion

## Future Enhancements

1. **Uninstall from PATH**: Detect all installations if tool is in PATH
2. **Backup before uninstall**: Create backup of `.todo.ai/` before removal
3. **Reinstall prompt**: Suggest reinstall command if needed
