# todo.ai Task Numbering Modes - User Guide

## Overview

> **Related Documentation:**
> - [Hybrid Task Numbering Design](HYBRID_TASK_NUMBERING_DESIGN.md) - Technical design details
> - [Usage Patterns](USAGE_PATTERNS.md) - Practical setup examples for different scenarios

`todo.ai` supports multiple task numbering modes to accommodate different development scenarios, from single developers to large teams. This guide explains how to choose, configure, and switch between numbering modes.

---

## Available Modes

### Mode 1: Single-User (Default)

**Best for:** Individual developers working alone

**Characteristics:**
- Simple sequential numbering: `#1`, `#2`, `#3`
- No coordination needed
- No prefixes required
- Fastest and simplest mode

**Example:**
```markdown
- [ ] **#50** Implement feature X
- [ ] **#51** Fix bug Y
  - [ ] **#51.1** Investigate root cause
  - [ ] **#51.2** Apply fix
```

**Configuration:**
```yaml
# .todo.ai/config.yaml
mode: single-user
```

---

### Mode 2: Multi-User (Simple)

**Best for:** Small teams (2-5 developers) working on same branch

**Characteristics:**
- Prefixed task IDs: `fxstein-50`, `alice-51`
- Prefix = first 7 characters of GitHub username
- No coordination service needed
- Automatic task reference resolution

**Example:**
```markdown
- [ ] **#fxstein-50** Implement feature X
- [ ] **#alice-51** Fix bug Y
  - [ ] **#alice-51.1** Investigate root cause
  - [ ] **#alice-51.2** Apply fix
```

**Usage:**
```bash
# User can reference tasks by number only (tool adds prefix)
./todo.ai complete 50      # Auto-resolves to fxstein-50
./todo.ai show alice-51    # Must use full ID for other users' tasks
```

**Configuration:**
```yaml
# .todo.ai/config.yaml
mode: multi-user
coordination:
  type: none
```

---

### Mode 3: Branch Mode

**Best for:** Feature branches, experimental work, branch-specific task tracking

**Characteristics:**
- Prefixed task IDs: `feature-50`, `fix-bug-51`
- Prefix = first 7 characters of Git branch name
- Tasks isolated per branch
- Useful for branch-specific work

**Example:**
```markdown
- [ ] **#feature-50** Implement feature X
- [ ] **#feature-51** Add tests
  - [ ] **#feature-51.1** Unit tests
  - [ ] **#feature-51.2** Integration tests
```

**Configuration:**
```yaml
# .todo.ai/config.yaml
mode: branch
coordination:
  type: none
```

---

### Mode 4: Enhanced Multi-User

**Best for:** Large teams needing atomic coordination, preventing numbering conflicts

**Characteristics:**
- Uses GitHub Issues API or CounterAPI for atomic ID assignment
- Prefixed task IDs with coordinated numbering
- Automatic fallback to Multi-User mode if coordination fails
- Requires GitHub CLI (`gh`) or CounterAPI configuration

**Example:**
```markdown
- [ ] **#fxstein-50** Implement feature X (assigned atomically via GitHub Issues)
- [ ] **#alice-51** Fix bug Y (assigned atomically via GitHub Issues)
```

**Configuration (GitHub Issues):**
```yaml
# .todo.ai/config.yaml
mode: enhanced
coordination:
  type: github-issues
  issue_number: 123  # GitHub issue used for coordination
  fallback: multi-user
```

**Configuration (CounterAPI):**
```yaml
# .todo.ai/config.yaml
mode: enhanced
coordination:
  type: counterapi
  namespace: my-project-team
  fallback: multi-user
```

---

## Choosing the Right Mode

### Decision Tree

```
┌─────────────────────────────────┐
│  How many developers?           │
└─────────────────────────────────┘
          │
          ├─→ 1 developer
          │   └─→ **Single-User** (default)
          │
          ├─→ 2-5 developers
          │   └─→ **Multi-User** (simple)
          │
          └─→ 6+ developers
              │
              ├─→ Need atomic coordination?
              │   ├─→ Yes → **Enhanced Multi-User**
              │   └─→ No  → **Multi-User** (simple)
              │
              └─→ Working on branches?
                  └─→ **Branch Mode** (per branch)
```

### Quick Comparison

| Feature | Single-User | Multi-User | Branch | Enhanced |
|---------|------------|------------|--------|----------|
| **Max Developers** | 1 | Unlimited | 1 per branch | Unlimited |
| **Coordination** | None | None | None | GitHub Issues / CounterAPI |
| **Task ID Format** | `#50` | `#fxstein-50` | `#feature-50` | `#fxstein-50` |
| **Setup Complexity** | None | Low | Low | Medium |
| **Conflict Risk** | None | Low | None | None (atomic) |
| **GitHub CLI Required** | No | No | No | Yes (for GitHub Issues) |

---

## Switching Between Modes

### Using the Switch Command

```bash
# Switch to multi-user mode
./todo.ai switch-mode multi-user

# Switch to branch mode
./todo.ai switch-mode branch

# Switch to enhanced mode (requires configuration)
./todo.ai switch-mode enhanced

# Switch back to single-user mode
./todo.ai switch-mode single-user
```

### With Automatic Renumbering

By default, existing tasks keep their current IDs when switching modes. To renumber existing tasks to match the new mode:

```bash
# Switch and renumber existing tasks
./todo.ai switch-mode multi-user --renumber

# Preview what would change (dry-run not supported yet)
./todo.ai switch-mode multi-user --renumber
```

**What Happens:**
1. Backup created automatically (`.todo.ai/backups/mode-switch-TIMESTAMP/`)
2. Existing tasks are renumbered to match new mode
3. All task references updated (relationships, notes, subtasks)
4. Configuration file updated

**Example:**
```bash
# Before switch (single-user mode):
- [ ] **#50** Implement feature X
- [ ] **#51** Fix bug Y

# After switch to multi-user with --renumber:
- [ ] **#fxstein-50** Implement feature X
- [ ] **#fxstein-51** Fix bug Y
```

### Rollback from Mode Switch

If something goes wrong, you can rollback:

```bash
# List available backups
./todo.ai list-mode-backups

# Rollback to a specific backup
./todo.ai rollback-mode mode-switch-20250102120000
```

---

## Migration Paths

### From Single-User to Multi-User

**Scenario:** Team is growing, need to support multiple developers

**Steps:**
1. **Repository owner configures mode:**
   ```bash
   ./todo.ai switch-mode multi-user
   ```

2. **Optionally renumber existing tasks:**
   ```bash
   ./todo.ai switch-mode multi-user --renumber
   ```

3. **Share configuration:**
   ```bash
   # Commit config file
   git add .todo.ai/config.yaml
   git commit -m "Configure multi-user numbering mode"
   git push
   ```

4. **Team members update:**
   ```bash
   git pull
   # Next task assignment uses new mode
   ```

**During Transition:**
- Old format (`#50`) and new format (`fxstein-50`) both work
- Tool automatically resolves number-only references (`50` → `fxstein-50`)
- Gradually migrate old tasks if desired, or leave them as-is

---

### From Single-User to Branch Mode

**Scenario:** Starting feature branch work, want branch-specific task tracking

**Steps:**
1. **Switch to branch mode:**
   ```bash
   ./todo.ai switch-mode branch
   ```

2. **Create feature branch:**
   ```bash
   git checkout -b feature/new-feature
   ```

3. **Tasks automatically use branch prefix:**
   ```bash
   ./todo.ai add "Implement new feature"
   # Assigned: #feature-50 (based on branch name "feature/new-feature")
   ```

---

### From Multi-User to Enhanced

**Scenario:** Team is growing, experiencing numbering conflicts, need atomic coordination

**Prerequisites:**
- GitHub CLI installed and authenticated (`gh auth login`)
- Create a GitHub Issue for coordination (or use CounterAPI)

**Steps:**
1. **Create coordination GitHub Issue:**
   ```bash
   gh issue create --title "todo.ai Task Number Coordination" --body "This issue is used for atomic task number coordination"
   # Note the issue number (e.g., #123)
   ```

2. **Switch to enhanced mode:**
   ```bash
   # You'll need to manually create config.yaml with coordination settings
   cat > .todo.ai/config.yaml <<EOF
   mode: enhanced
   coordination:
     type: github-issues
     issue_number: 123
     fallback: multi-user
   EOF

   ./todo.ai switch-mode enhanced
   ```

3. **Test coordination:**
   ```bash
   ./todo.ai add "Test atomic coordination"
   # Task assigned atomically via GitHub Issues API
   ```

---

## Best Practices

### 1. Choose Mode at Repository Setup

**Best Practice:** Decide on numbering mode when setting up the repository, before creating many tasks.

**Why:** Switching modes later requires renumbering, which can be disruptive.

### 2. Commit Configuration File

**Best Practice:** Always commit `.todo.ai/config.yaml` to the repository.

**Why:** Ensures all team members use the same numbering mode.

```bash
git add .todo.ai/config.yaml
git commit -m "Configure todo.ai numbering mode"
```

### 3. Use Backups Before Mode Switches

**Best Practice:** The tool automatically creates backups, but you can also create manual backups.

```bash
# Manual backup before major mode switch
cp TODO.md TODO.md.backup
cp .todo.ai/config.yaml .todo.ai/config.yaml.backup
```

### 4. Test in a Branch First

**Best Practice:** When switching modes, test in a feature branch first.

**Why:** Allows verification before affecting main branch.

```bash
git checkout -b test/multi-user-mode
./todo.ai switch-mode multi-user --renumber
# Test tasks, verify everything works
git checkout main
git merge test/multi-user-mode
```

### 5. Resolve Conflicts Before Switching

**Best Practice:** Run conflict resolution before switching modes.

```bash
# Check for duplicate task IDs
./todo.ai --lint

# Resolve any conflicts
./todo.ai resolve-conflicts

# Then switch modes
./todo.ai switch-mode multi-user
```

---

## Troubleshooting

### Issue: "Invalid mode in config"

**Cause:** Configuration file has invalid mode value.

**Solution:**
```bash
# Check current config
cat .todo.ai/config.yaml

# Fix mode value (should be: single-user, multi-user, branch, or enhanced)
./todo.ai switch-mode single-user  # Fixes config automatically
```

---

### Issue: "Duplicate task IDs detected"

**Cause:** Multiple tasks have the same ID (can happen during merges or mode switches).

**Solution:**
```bash
# Check for duplicates
./todo.ai --lint

# Preview what would be fixed
./todo.ai resolve-conflicts --dry-run

# Fix duplicates automatically
./todo.ai resolve-conflicts
```

---

### Issue: "Enhanced mode coordination failed"

**Cause:** GitHub Issues API or CounterAPI unavailable or misconfigured.

**Solution:**
1. Check GitHub CLI authentication:
   ```bash
   gh auth status
   ```

2. Verify coordination issue exists:
   ```bash
   gh issue view 123  # Replace 123 with your issue number
   ```

3. Enhanced mode automatically falls back to Multi-User mode if coordination fails.

---

### Issue: "Task reference not found after mode switch"

**Cause:** Task was renumbered during mode switch, but reference wasn't updated.

**Solution:**
```bash
# Run conflict resolution to fix any orphaned references
./todo.ai resolve-conflicts

# Or manually update the reference using the task's new ID
```

---

## Command Reference

### Mode Management

```bash
# Switch numbering mode
./todo.ai switch-mode <single-user|multi-user|branch|enhanced> [--renumber] [--force]

# List mode switch backups
./todo.ai list-mode-backups

# Rollback from mode switch
./todo.ai rollback-mode <backup-name>
```

### Conflict Resolution

```bash
# Detect duplicate task IDs
./todo.ai --lint

# Preview conflict resolution
./todo.ai resolve-conflicts --dry-run

# Resolve duplicate task IDs
./todo.ai resolve-conflicts
```

### Configuration

```bash
# View current configuration
cat .todo.ai/config.yaml

# Check current mode
./todo.ai switch-mode  # Without arguments, shows current mode (if command supports it)
```

---

## Examples

### Example 1: Small Team Adoption

**Scenario:** 3-person team wants to adopt multi-user mode

**Steps:**
```bash
# 1. Repository owner switches mode
./todo.ai switch-mode multi-user

# 2. Optionally renumber existing tasks
./todo.ai switch-mode multi-user --renumber

# 3. Commit and share
git add .todo.ai/config.yaml TODO.md
git commit -m "Switch to multi-user numbering mode"
git push

# 4. Team members pull changes
git pull

# 5. Next task assignment uses new mode
./todo.ai add "Implement feature"
# Assigned: #fxstein-50 (user's prefix added automatically)
```

---

### Example 2: Feature Branch Task Tracking

**Scenario:** Working on feature branch, want branch-specific tasks

**Steps:**
```bash
# 1. Switch to branch mode
./todo.ai switch-mode branch

# 2. Create feature branch
git checkout -b feature/user-authentication

# 3. Add tasks (automatically prefixed with branch name)
./todo.ai add "Implement login"
# Assigned: #feature-50

./todo.ai add "Add password reset"
# Assigned: #feature-51

# 4. Merge feature branch
git checkout main
git merge feature/user-authentication

# 5. Tasks remain branch-specific (feature-50, feature-51)
```

---

### Example 3: Large Team with Atomic Coordination

**Scenario:** 10-person team needs atomic task numbering

**Prerequisites:**
- GitHub CLI installed and authenticated
- Create coordination issue

**Steps:**
```bash
# 1. Create coordination issue
gh issue create --title "todo.ai Task Coordination" --body "Used for atomic task numbering"
# Issue #123 created

# 2. Create config file
cat > .todo.ai/config.yaml <<EOF
mode: enhanced
coordination:
  type: github-issues
  issue_number: 123
  fallback: multi-user
EOF

# 3. Switch to enhanced mode
./todo.ai switch-mode enhanced

# 4. Commit and share
git add .todo.ai/config.yaml
git commit -m "Configure enhanced multi-user numbering with GitHub Issues coordination"
git push

# 5. Team members update
git pull

# 6. Next task uses atomic coordination
./todo.ai add "Implement feature"
# Assigned atomically via GitHub Issues API: #fxstein-50
```

---

## Related Documentation

- **[Hybrid Task Numbering Design](HYBRID_TASK_NUMBERING_DESIGN.md)** - Technical design and implementation details
- **[Usage Patterns](USAGE_PATTERNS.md)** - Practical setup examples for different development scenarios
- **[Multi-User Conflict Analysis](MULTI_USER_CONFLICT_ANALYSIS.md)** - Detailed conflict scenario analysis

---

## Summary

`todo.ai` provides flexible task numbering modes to fit different team sizes and workflows:

- **Single-User**: Default mode, perfect for individual developers
- **Multi-User**: Simple prefix-based numbering for small teams
- **Branch**: Branch-specific task tracking for feature work
- **Enhanced**: Atomic coordination for large teams

Choose the mode that fits your team size and workflow, and switch modes as your needs evolve. The tool provides automatic backup, rollback, and conflict resolution to make mode switching safe and reliable.
