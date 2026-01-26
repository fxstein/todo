# Beta Testing Guide for todo.ai

Thank you for helping test beta releases of todo.ai! This guide will help you install, test, and provide feedback on pre-release versions.

## What is Beta Testing?

Beta releases are feature-complete pre-releases that need real-world testing before stable release. They help us:

- Catch bugs before they reach stable users
- Gather feedback on new features
- Test cross-platform compatibility
- Validate migrations and upgrades

## Installing Beta Releases

### Using uv (Recommended)

```bash
# Install latest beta
uv tool install --prerelease=allow ai-todo

# Upgrade to latest beta
uv tool upgrade ai-todo

# Switch back to stable
uv tool uninstall ai-todo
uv tool install ai-todo
```

### Using pipx

```bash
# Install latest beta
pipx install --pre ai-todo

# Upgrade to latest beta
pipx upgrade ai-todo

# Switch back to stable
pipx uninstall ai-todo
pipx install ai-todo
```

### Check Your Version

```bash
todo-ai version
```

Beta versions look like: `v1.0.0b1`, `v1.0.0b2`, etc.

## What to Test

### 1. Core Functionality

Test the basic commands you use most:

```bash
# Task management
ai-todo add "Test task" "#test"
ai-todo list
ai-todo complete 1
todo-ai archive 1

# Subtasks
ai-todo add-subtask 1 "Test subtask" "#test"
ai-todo complete 1.1
```

### 2. Your Platform

We need testing on:

- **macOS** 13+ (Apple Silicon and Intel)
- **Linux** (Ubuntu 20.04+, other distros)
- **Windows** (WSL2)

Help us by testing on your specific platform and reporting any issues.

### 3. Upgrades/Migrations

If you're upgrading from a previous version:

1. **Backup first:** Your TODO.md should be in Git, but make sure it's committed
2. **Test the upgrade:** Install beta and verify your tasks still work
3. **Report migration issues:** If anything breaks during upgrade, let us know

### 4. MCP Server (If Using Cursor)

If you use the MCP server integration:

```bash
# Verify MCP server works
todo-ai-mcp

# Test in Cursor with your normal workflow
```

## What to Look For

### Common Issues to Report

- **Crashes or errors:** Any command that fails or produces errors
- **Data corruption:** Tasks disappearing, IDs changing, formatting broken
- **Performance:** Commands taking >1 second (they should be instant)
- **Cross-platform issues:** Features that work on macOS but not Linux, etc.
- **Documentation errors:** Instructions that don't work or are unclear

### What NOT to Report

- **Known limitations:** Check the README first
- **Feature requests:** Beta testing is for bugs, not new features
- **"It's different":** Beta may have intentional changes - focus on things that are broken

## How to Report Issues

### Using the Bug Reporter

```bash
todo-ai report-bug "Error when completing task #5"
```

This automatically collects context and creates a GitHub Issue.

### Manual Reporting

If you prefer, create a GitHub Issue manually:

1. Go to: https://github.com/fxstein/todo.ai/issues
2. Click "New Issue"
3. Title: `[Beta v1.0.0b1] Bug description`
4. Include:
   - Beta version number
   - Platform (macOS 14.2, Ubuntu 22.04, etc.)
   - Shell (zsh, bash)
   - Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages (if any)

### Example Bug Report

```markdown
**Version:** v1.0.0b1
**Platform:** macOS 14.2 (Apple Silicon)
**Shell:** zsh 5.9
**Python:** 3.12.0

**Steps to reproduce:**
1. Run: ai-todo add "Test task"
2. Run: ai-todo complete 1
3. Error occurs

**Expected:** Task marked as completed
**Actual:** Error: "Task ID not found"

**Error message:**
```
Traceback (most recent call last):
  ...
```
```

## Providing Feedback

### What's Helpful

- **Specific:** "The `list` command is slow with 100+ tasks" vs "It's slow"
- **Reproducible:** Include steps so we can reproduce the issue
- **Context:** What were you trying to do? What workflow were you using?

### Where to Share Feedback

- **Bugs:** Use GitHub Issues or `todo-ai report-bug`
- **General feedback:** GitHub Discussions
- **Questions:** GitHub Discussions

## Testing Timeline

### Major Releases (e.g., 1.0.0 → 2.0.0)

- **Beta period:** 7+ days recommended
- **Multiple betas:** b1, b2, b3... as needed
- **Your help:** Test as soon as beta is available

### Minor Releases (e.g., 1.0.0 → 1.1.0)

- **Beta period:** 2-3 days recommended
- **Fewer betas:** Usually just b1 or b2
- **Your help:** Quick sanity check on your platform

## Switching Back to Stable

If you encounter issues and need to switch back:

```bash
# Using uv
uv tool uninstall ai-todo
uv tool install ai-todo

# Using pipx
pipx uninstall ai-todo
pipx install ai-todo
```

Your TODO.md is safe - it's just a text file. The tool never modifies data in a destructive way.

## Testing Checklist

Before reporting "all good":

- [ ] Installed beta successfully
- [ ] Ran `todo-ai version` to confirm beta version
- [ ] Tested basic commands (add, list, complete)
- [ ] Tested subtasks (if you use them)
- [ ] Tested MCP server (if you use Cursor)
- [ ] Tested on your specific platform
- [ ] No errors, crashes, or unexpected behavior

If all checks pass, let us know in GitHub Discussions! Positive feedback is just as helpful as bug reports.

## Thank You!

Beta testing is critical to maintaining quality. Your feedback helps ensure stable releases are solid for all users.

**Questions?** Ask in [GitHub Discussions](https://github.com/fxstein/todo.ai/discussions)

**Found a bug?** Use `todo-ai report-bug` or create an [issue](https://github.com/fxstein/todo.ai/issues)
