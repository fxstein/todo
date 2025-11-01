This release introduces the new bug reporting feature, enabling todo.ai to self-report bugs to GitHub Issues with intelligent duplicate detection and user-controlled reporting.

**New Feature: Bug Reporting System**
- Self-reporting to GitHub Issues: When errors occur, todo.ai can suggest creating a bug report on GitHub Issues
- Manual confirmation required: Always requires explicit user confirmation before any GitHub API calls - never automatic
- Duplicate detection: Intelligently searches for similar issues before creating new ones
- "Me Too" replies: If similar issues exist, users can add "me too" comments with their context
- Context collection: Automatically gathers error details, system information, and recent logs (50 lines)
- Privacy protection: For private repositories, hides repository identifiers to protect privacy
- Log history: Includes collapsed log sections with the 50 most recent entries (newest first)
- GitHub CLI integration: Uses GitHub CLI for seamless issue creation and commenting

**Technical Details:**
- Similarity threshold: 75% for duplicate detection (word-based comparison)
- Log collection: Automatically collects and sanitizes logs (passwords, tokens filtered)
- Template-based reports: Structured bug reports with version, OS, shell, error context, and logs
- Cursor rules integration: Automatically adds rules to .cursorrules for AI agent behavior

**User Experience:**
- Error suggestion: When errors occur, todo.ai suggests reporting (never forces it)
- Preview before submit: Shows preview of bug report before asking for confirmation
- Interactive flow: Guides users through duplicate detection and "me too" reply process
- Graceful fallbacks: Works even if GitHub CLI is unavailable (just suggests reporting)

**Usage:**

For AI Agents:
```
./todo.ai report-bug "Error description" "Error context" "command"
```

For Humans:
```
Report this bug to GitHub Issues
```

This feature significantly improves the feedback loop between users and developers while maintaining full user control and privacy protection.
