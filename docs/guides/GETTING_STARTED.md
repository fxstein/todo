# Getting Started with todo.ai

This guide will help you install and configure `todo.ai` for your development workflow. Choose the setup that matches your needs.

> **Related Documentation:**
> - [Numbering Modes Guide](NUMBERING_MODES_GUIDE.md) - Complete guide to all modes
> - [Usage Patterns](USAGE_PATTERNS.md) - Real-world usage scenarios  
> - [Coordination Setup Instructions](COORDINATION_SETUP.md) - Detailed setup guides

---

## Quick Start

### Installation

```bash
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh
```

This smart installer auto-detects your system and installs the optimal version (zsh or bash 4+).

### Initialize

```bash
./todo.ai init
```

### Use Interactive Setup Wizard

The easiest way to configure todo.ai:

```bash
./todo.ai setup
```

The wizard will:
1. Detect your system capabilities
2. Guide you through mode selection
3. Set up coordination (if needed)
4. Apply configuration automatically

---

## Understanding Modes

todo.ai supports four numbering modes to match your workflow:

### Mode 1: Single-User (Default)

**Format:** `#1`, `#2`, `#3`, ...

**Best for:** Individual developers working alone or small teams with plain numeric IDs

**Setup:**
```bash
./todo.ai switch-mode single-user
```

**Optional:** Add coordination for atomic numbering across multiple developers:
```bash
./todo.ai setup-coordination github-issues
# or
./todo.ai setup-coordination counterapi
```

### Mode 2: Multi-User

**Format:** `fxstein-50`, `alice-50`

**Best for:** Multiple developers working in the same repository without coordination

**Setup:**
```bash
./todo.ai switch-mode multi-user
```

### Mode 3: Branch

**Format:** `feature-50`, `main-50`

**Best for:** Feature branch development or branch-specific task tracking

**Setup:**
```bash
./todo.ai switch-mode branch
```

### Mode 4: Enhanced Multi-User

**Format:** `fxstein-50`, `alice-51` (atomically assigned)

**Best for:** Large teams or high-concurrency environments needing atomic coordination

**Setup:**
```bash
./todo.ai switch-mode enhanced
./todo.ai setup-coordination github-issues
# or
./todo.ai setup-coordination counterapi
```

---

## Coordination Services

Coordination ensures atomic task numbering across multiple developers or branches.

### GitHub Issues Coordination

**Prerequisites:**
- GitHub CLI installed (`brew install gh`)
- GitHub CLI authenticated (`gh auth login`)
- Git repository connected to GitHub

**Setup:**
```bash
./todo.ai setup-coordination github-issues
```

The tool will:
- Search for existing coordination issue
- Create new issue if none exists
- Initialize with next available number
- Configure automatically

### CounterAPI Coordination

**Prerequisites:**
- `curl` installed
- `jq` or `python3` installed
- Internet connectivity

**Setup:**
```bash
./todo.ai setup-coordination counterapi
```

The tool will:
- Prompt for a namespace
- Test connection to CounterAPI
- Configure automatically

### No Coordination (Fallback)

If coordination is unavailable or not needed, enhanced mode falls back to multi-user mode.

---

## Common Setup Scenarios

### Scenario 1: Individual Developer

**Goal:** Track personal tasks with simple numbering

**Setup:**
```bash
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh
./todo.ai init
```

Default mode: Single-user (no configuration needed)

**Usage:**
```bash
./todo.ai add "Fix authentication bug" "#bug"
./todo.ai complete 1
./todo.ai list
```

### Scenario 2: Small Team (2-10 developers)

**Goal:** Collaborate on shared tasks

**Setup:**
```bash
# Install todo.ai in repository
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh
./todo.ai init

# Configure multi-user mode
./todo.ai switch-mode multi-user

# Commit configuration
git add .todo.ai/config.yaml TODO.md
git commit -m "Initialize todo.ai multi-user mode"
```

**Usage:**
Each team member gets their own prefix:
```bash
./todo.ai add "Implement user profiles" "#feature"
# Creates: #fxstein-50

./todo.ai add "Add database indexes" "#performance"
# Creates: #alice-50
```

### Scenario 3: Large Team with Atomic Coordination

**Goal:** Prevent numbering conflicts across multiple developers

**Setup:**
```bash
# Install and initialize
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh
./todo.ai init

# Use interactive wizard (recommended)
./todo.ai setup
# Select: 4) enhanced
# Select: 1) GitHub Issues (or 2) CounterAPI)
```

**Alternative manual setup:**
```bash
./todo.ai switch-mode enhanced
./todo.ai setup-coordination github-issues
# Follow prompts to configure issue
```

**Usage:**
Tasks get atomically assigned numbers:
```bash
./todo.ai add "Refactor API layer" "#refactor"
# Atomically assigns: #fxstein-50

./todo.ai add "Update documentation" "#docs"
# Atomically assigns: #alice-51
```

### Scenario 4: Feature Branch Development

**Goal:** Track tasks per branch

**Setup:**
```bash
./todo.ai switch-mode branch
```

**Usage:**
Tasks automatically use branch prefix:
```bash
# On branch: feature/auth
./todo.ai add "Add login page" "#frontend"
# Creates: #feature-50

# Switch to branch: main
./todo.ai add "Update dependencies" "#maintenance"
# Creates: #main-50
```

### Scenario 5: Plain Numeric IDs with Coordination

**Goal:** Use simple #1, #2 format but prevent conflicts across developers

**Setup:**
```bash
# Switch to single-user mode
./todo.ai switch-mode single-user

# Add coordination
./todo.ai setup-coordination github-issues
# or
./todo.ai setup-coordination counterapi
```

**Usage:**
Tasks use plain numbers but are atomically assigned:
```bash
./todo.ai add "Deploy to staging" "#deploy"
# Atomically assigns: #50

./todo.ai add "Run performance tests" "#test"
# Atomically assigns: #51
```

---

## Verification

After setup, verify your configuration:

### Check Configuration
```bash
./todo.ai config
```

Example output:
```yaml
Current Configuration:
======================
mode: enhanced
coordination:
  type: github-issues
  issue_number: 123
  fallback: multi-user
```

### Detect Available Options
```bash
./todo.ai detect-coordination
```

Example output:
```
System Capabilities:
✅ GitHub CLI installed and authenticated
✅ CounterAPI support available (curl + jq)
✅ Git repository with GitHub remote
```

### Test Task Creation
```bash
./todo.ai add "Test task"
./todo.ai list
```

---

## Troubleshooting

### "GitHub CLI not installed"
```bash
# macOS
brew install gh

# Linux
# See: https://cli.github.com/manual/installation
```

### "GitHub CLI not authenticated"
```bash
gh auth login
```

### "Not in a GitHub repository"
Ensure you're in a git repository with a GitHub remote:
```bash
git remote -v
# Should show GitHub URL
```

### "CounterAPI connection failed"
Check internet connectivity:
```bash
curl https://api.counterapi.dev
# Should return JSON
```

### Configuration file errors
View current config:
```bash
./todo.ai config
```

Re-run setup:
```bash
./todo.ai setup
```

---

## Next Steps

1. **Read the documentation:**
   - [Numbering Modes Guide](NUMBERING_MODES_GUIDE.md) - Complete mode reference
   - [Usage Patterns](USAGE_PATTERNS.md) - Real-world examples
   - [Coordination Setup](COORDINATION_SETUP.md) - Detailed coordination guides

2. **Try common commands:**
   ```bash
   ./todo.ai add "Implement feature X"
   ./todo.ai add-subtask 1 "Break into smaller tasks"
   ./todo.ai complete 1
   ./todo.ai list --tag "#feature"
   ```

3. **Configure team workflow:**
   - Share `.todo.ai/config.yaml` via Git
   - Ensure all team members run `./todo.ai setup`
   - Document your numbering mode choice

4. **Get help:**
   ```bash
   ./todo.ai --help
   ./todo.ai show 1
   ./todo.ai log --lines 20
   ```

---

## Quick Reference

### Setup Commands
```bash
./todo.ai setup                      # Interactive setup wizard
./todo.ai switch-mode <mode>         # Switch numbering mode
./todo.ai setup-coordination <type>  # Configure coordination
./todo.ai config                     # View current configuration
./todo.ai detect-coordination        # Check available options
```

### Task Management
```bash
./todo.ai add "Task description" "#tags"
./todo.ai add-subtask 1 "Subtask description"
./todo.ai complete 1
./todo.ai list --tag "#tag"
./todo.ai show 1
./todo.ai modify 1 "Updated description"
./todo.ai note 1 "Add implementation notes"
./todo.ai update-note 1 "Replace existing notes"
./todo.ai delete-note 1
./todo.ai delete 1
./todo.ai archive 1
```

### Information Commands
```bash
./todo.ai --help                      # Show help
./todo.ai config                      # Show configuration
./todo.ai log                         # View operation log
./todo.ai version                     # Show version
```

---

## Need Help?

- **Documentation:** See `docs/` directory for detailed guides
- **Report bugs:** `./todo.ai report-bug "description" "context" "command"`
- **GitHub:** https://github.com/fxstein/todo.ai
- **Issues:** https://github.com/fxstein/todo.ai/issues

