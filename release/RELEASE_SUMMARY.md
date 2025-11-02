# Release Summary: Fix Update Command for System-Wide Installations

This release addresses a critical bug where the `update` command failed when `todo.ai` was installed to a system directory in PATH (e.g., `/usr/local/bin` or `/usr/bin`). The issue was reported in GitHub issue #17 and affected users who installed `todo.ai` system-wide for global access.

## Key Improvements

**Fixed Update Command for System-Wide Installations:**
- Enhanced the `get_script_path()` function to properly detect the script location when installed system-wide
- Added support for locating the script via `command -v` and `which` when executed from PATH
- Implemented robust path validation and absolute path conversion with fallback to `realpath`
- The update command now works correctly regardless of installation method (local project directory or system-wide PATH installation)

## Technical Details

The fix implements a multi-strategy approach to locate the script:
1. First tries zsh-specific absolute path expansion (for direct execution)
2. Uses `command -v`/`which` to find the script in PATH (for system-wide installations)
3. Falls back to current directory and relative path detection

This ensures compatibility with all installation scenarios while maintaining backward compatibility with existing local installations.

## Usage

For AI Agents:
```bash
Fix update command for system-wide installations
```

For Humans:
```bash
Tell todo.ai to update itself: todo.ai update
```

---

**Fixes:** GitHub issue #17  
**Task:** #55
