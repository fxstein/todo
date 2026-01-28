# Prune Command Examples

The `prune` command removes old archived tasks from TODO.md to keep your task list manageable. All pruned tasks are automatically backed up with complete metadata for restoration if needed.

## CLI Examples

### Basic Usage (30-day default)

```bash
# Prune tasks archived more than 30 days ago
ai-todo prune

# Preview first (dry-run)
ai-todo prune --dry-run

# Skip confirmation prompt
ai-todo prune --force
```

### Custom Retention Periods

```bash
# Keep tasks for 60 days before pruning
ai-todo prune --days 60

# Prune tasks archived before specific date
ai-todo prune --older-than 2025-10-01

# Aggressive pruning (14 days)
ai-todo prune --days 14
```

### Task ID Range Pruning

```bash
# Remove tasks #1 through #100
ai-todo prune --from-task 100

# Remove very old tasks #1-#50
ai-todo prune --from-task 50

# Preview what would be removed
ai-todo prune --from-task 100 --dry-run
```

### Backup Options

```bash
# Prune without creating backup (not recommended)
ai-todo prune --days 30 --no-backup

# Default behavior: Creates backup in .ai-todo/archives/
ai-todo prune --days 30
```

## MCP Examples

### For AI Agents (via Cursor/Claude)

**Natural Language:**

- *"Prune archived tasks older than 60 days"*
- *"Remove archived tasks from #1 to #50"*
- *"Show me what would be pruned with a dry run"*
- *"Clean up old tasks but keep the last 90 days"*

**Tool Calls:**

```python
# Default 30-day prune
prune_tasks()

# Custom retention period
prune_tasks(days=60)

# Date-based pruning
prune_tasks(older_than="2025-10-01")

# Range-based pruning
prune_tasks(from_task="100")

# Dry-run preview
prune_tasks(days=30, dry_run=True)

# Prune without backup (not recommended)
prune_tasks(days=30, backup=False)
```

## Backup and Restoration

### Backup Files

Pruned tasks are saved to `.ai-todo/archives/TODO_ARCHIVE_YYYY-MM-DD.md` with:

- Complete task descriptions, tags, notes, and dates
- TASK_METADATA with created_at/updated_at timestamps
- Full restoration capability
- Sequential numbering if multiple prunes happen same day (`_1.md`, `_2.md`)

### Backup Format

```markdown
# Archived Tasks - Pruned on 2026-01-28

**Prune Statistics:**
- Tasks Pruned: 37 root tasks
- Subtasks Pruned: 182 subtasks
- Total: 219 items
- Retention Period: 60 days

## Pruned Tasks

- [x] **#10** Old task `#feature` (2025-10-15)
  > Task notes preserved
  - [x] **#10.1** Subtask (2025-10-15)

## Task Metadata

<!-- TASK_METADATA
# Format: task_id:created_at[:updated_at]
10:2025-10-01T10:00:00:2025-10-15T11:00:00
10.1:2025-10-01T10:00:00:2025-10-15T11:00:00
-->
```

### Restoring From Backup

Backups are in standard TODO.md format. To restore:

1. Open the backup file (`.ai-todo/archives/TODO_ARCHIVE_YYYY-MM-DD.md`)
2. Copy the tasks you want to restore
3. Paste into the appropriate section of `TODO.md` (Tasks, Archived, etc.)
4. The TASK_METADATA section can be copied as-is if you want to preserve timestamps

## Common Use Cases

### Quarterly Cleanup

```bash
# End of quarter: prune tasks older than 90 days
ai-todo prune --days 90 --dry-run   # Preview first
ai-todo prune --days 90             # Execute
```

### Initial Repository Cleanup

```bash
# Remove very old tasks from legacy history
ai-todo prune --from-task 50       # Remove #1-#50
ai-todo prune --older-than 2024-01-01  # Remove all 2023 tasks
```

### Regular Maintenance

```bash
# Weekly automation (add to cron/scheduled task)
ai-todo prune --days 30 --force    # Automatic, no prompts
```

## Safety Features

### What Gets Pruned

- ✅ **Archived tasks only** (tasks in "## Archived" section)
- ❌ **Never touches active tasks** (in "## Tasks" section)
- ❌ **Never touches recently completed** (in "## Recently Completed")
- ❌ **Never touches deleted tasks** (in "## Deleted Tasks")

### Backup Safety

- **Automatic backups** created before every prune (unless `--no-backup`)
- **Complete metadata** preserved (timestamps, relationships)
- **Conflict handling** - multiple prunes same day create separate files
- **Restoration capability** - backups are in standard TODO.md format

### Dry-Run Mode

Always preview with `--dry-run` before pruning:

```bash
# Preview what will be removed
ai-todo prune --days 30 --dry-run

# If it looks good, run without --dry-run
ai-todo prune --days 30
```

## Best Practices

1. **Preview first:** Always use `--dry-run` before your first prune
2. **Keep backups:** Don't use `--no-backup` unless you're certain
3. **Regular schedule:** Run monthly or quarterly to keep TODO.md manageable
4. **Conservative retention:** Start with longer periods (60-90 days)
5. **Check git history:** Backups are in `.ai-todo/archives/` and can be committed

## Troubleshooting

### No tasks found

**Problem:** "No archived tasks match the prune criteria"

**Solution:**
- Check if you have archived tasks: `ai-todo list --archived`
- Verify retention period: Try longer period with `--days 90`
- Ensure tasks are actually archived (not just completed)

### Backup location

**Problem:** Where are my backups?

**Answer:** `.ai-todo/archives/TODO_ARCHIVE_YYYY-MM-DD.md`

Check with: `ls -l .ai-todo/archives/`

### Restore from backup

**Problem:** Need to restore pruned tasks

**Answer:**
1. Open backup: `.ai-todo/archives/TODO_ARCHIVE_YYYY-MM-DD.md`
2. Copy tasks to restore
3. Paste into `TODO.md` in the appropriate section
4. Copy TASK_METADATA entries if preserving timestamps

## Related Documentation

- [Getting Started](../guides/GETTING_STARTED.md) - Basic setup and usage
- [Usage Patterns](../guides/USAGE_PATTERNS.md) - Real-world workflows
- [FAQ](../FAQ.md) - Common questions answered
