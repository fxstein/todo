# Coordination Service Setup Instructions

This guide provides step-by-step instructions for setting up coordination services for `todo.ai`.

**Coordination is supported in:**
- **Enhanced mode** (with user prefixes: `fxstein-50`)
- **Single-user mode** (with plain numbers: `#50`)

> **Related Documentation:**
> - [Numbering Modes Guide](NUMBERING_MODES_GUIDE.md) - Overview of all modes and coordination options
> - [Hybrid Task Numbering Design](HYBRID_TASK_NUMBERING_DESIGN.md) - Technical details

---

## Table of Contents

1. [GitHub Issues Coordination](#github-issues-coordination)
2. [CounterAPI Coordination](#counterapi-coordination)
3. [Verification](#verification)
4. [Troubleshooting](#troubleshooting)

---

## GitHub Issues Coordination

### Prerequisites

Before setting up GitHub Issues coordination, ensure you have:

1. **GitHub CLI installed**
   - macOS: `brew install gh`
   - Linux: See [GitHub CLI installation](https://cli.github.com/manual/installation)
   - Windows: See [GitHub CLI installation](https://cli.github.com/manual/installation)

2. **GitHub CLI authenticated**
   ```bash
   gh auth login
   ```
   Follow the prompts to authenticate. You'll need:
   - GitHub account with write access to the repository
   - Authentication method (browser or token)

3. **Git repository with GitHub remote**
   ```bash
   git remote -v
   ```
   Should show a GitHub remote URL (e.g., `https://github.com/owner/repo.git`)

4. **Write access to repository**
   - You need permissions to create and comment on issues

### Setup Method 1: Interactive Setup

**Step 1: Run the setup command**
```bash
./todo.ai setup-coordination github-issues
```

**Step 2: Automatic setup**
The tool will automatically:
1. Search for an existing coordination issue (titled "todo.ai Task Number Coordination")
2. Use the existing issue if found
3. Create a new issue if none exists
4. Initialize with max(highest_task_number, current_coordinator_value) + 1
5. Save configuration automatically

**Note:** The tool is smart about initialization - it will check both TODO.md and the current coordinator value and use the maximum to ensure no duplicates.

**Step 3: Verify setup**
```bash
./todo.ai config
```

You should see:
```yaml
mode: enhanced  # or single-user
coordination:
  type: github-issues
  issue_number: 123
  fallback: multi-user  # Only used in enhanced mode
```

### Setup Method 2: Setup Wizard

**Run the interactive wizard:**
```bash
./todo.ai setup
```

The wizard will:
1. Detect available coordination options
2. Guide you through mode selection
3. Set up coordination if enhanced mode is selected

### Setup Method 3: Manual Setup

**Step 1: Create or select a GitHub issue**

**Option A: Create a new issue**
```bash
gh issue create --title "todo.ai Task Number Coordination" \
  --body "This issue is used by todo.ai for atomic task number coordination.

Do not manually comment on this issue - it is managed automatically by todo.ai."
```

Note the issue number from the output.

**Option B: Use an existing issue**
1. Find an existing issue number: `gh issue list`
2. Use that issue number in the configuration

**Step 2: Update configuration file**

Edit `.todo.ai/config.yaml`:
```yaml
mode: enhanced
coordination:
  type: github-issues
  issue_number: 123  # Replace with your issue number
  fallback: multi-user
```

**Step 3: Verify setup**
```bash
./todo.ai config
```

### Verification

**Test the setup:**
1. Check the issue exists:
   ```bash
   gh issue view <issue-number>
   ```

2. Create a test task:
   ```bash
   ./todo.ai add "Test task for coordination"
   ```

3. Check the issue comments:
   ```bash
   gh issue view <issue-number> --comments
   ```
   Should show a comment with "Next task number: X"

---

## CounterAPI Coordination

### Prerequisites

Before setting up CounterAPI coordination, ensure you have:

1. **curl installed**
   - macOS: Usually pre-installed
   - Linux: `sudo apt-get install curl` or `sudo yum install curl`
   - Windows: Download from [curl website](https://curl.se/download.html)

2. **JSON parser (one of):**
   - `jq`: `brew install jq` (macOS) or `sudo apt-get install jq` (Linux)
   - `python3`: Usually pre-installed (macOS/Linux)

3. **Internet connectivity**
   - CounterAPI is a cloud service requiring internet access

### Setup Method 1: Interactive Setup

**Step 1: Run the setup command**
```bash
./todo.ai setup-coordination counterapi
```

**Step 2: Enter namespace**
The tool will prompt:
```
Enter CounterAPI namespace [repo-name]:
```

- **Default:** Repository name (if in a git repo)
- **Custom:** Any lowercase alphanumeric string with hyphens/underscores
- **Example:** `my-project-tasks`, `todo-ai-repo-2025`

**Step 3: Verify setup**
```bash
./todo.ai config
```

You should see:
```yaml
mode: enhanced  # or single-user
coordination:
  type: counterapi
  namespace: your-namespace
  fallback: multi-user  # Only used in enhanced mode
```

### Setup Method 2: Setup Wizard

**Run the interactive wizard:**
```bash
./todo.ai setup
```

The wizard will:
1. Detect available coordination options
2. Guide you through mode selection
3. Set up coordination if enhanced mode is selected

### Setup Method 3: Manual Setup

**Step 1: Choose a namespace**
Choose a unique namespace for your project:
- Use repository name (e.g., `my-project`)
- Use project name (e.g., `todo-ai-production`)
- Use timestamp for uniqueness (e.g., `todo-ai-20251102`)

**Step 2: Update configuration file**

Edit `.todo.ai/config.yaml`:
```yaml
mode: enhanced
coordination:
  type: counterapi
  namespace: your-namespace  # Replace with your namespace
  fallback: multi-user
```

**Step 3: Verify setup**
```bash
./todo.ai config
```

### Namespace Guidelines

**Good namespaces:**
- `my-project-tasks`
- `todo-ai-production`
- `myrepo-tasks`
- `project-2025`

**Avoid:**
- Namespaces with spaces or special characters
- Namespaces with uppercase letters (CounterAPI is case-sensitive)
- Very short names (may conflict with others)
- Names that expose sensitive information

### Verification

**Test the setup:**
1. Test CounterAPI connection:
   ```bash
   curl -X POST "https://api.counterapi.dev/v1/your-namespace/test-counter/up"
   ```
   Should return JSON with a counter value.

2. Create a test task:
   ```bash
   ./todo.ai add "Test task for coordination"
   ```

3. Verify task was created with correct number:
   ```bash
   ./todo.ai list
   ```

---

## Verification

### Check Current Configuration

**View configuration:**
```bash
./todo.ai config
```

**Check available coordination options:**
```bash
./todo.ai detect-coordination
```

### Test Coordination

**GitHub Issues:**
```bash
# View the coordination issue
gh issue view <issue-number>

# Check for new comments (after creating a task)
gh issue view <issue-number> --comments | tail -5
```

**CounterAPI:**
```bash
# Test connection
curl -X POST "https://api.counterapi.dev/v1/<namespace>/test-counter/up"

# Should return: {"status":"success","value":<number>}
```

### Create Test Tasks

After setup, create a few test tasks to verify coordination:

```bash
./todo.ai add "Test task 1"
./todo.ai add "Test task 2"
./todo.ai add "Test task 3"
```

Check that:
- Tasks are numbered sequentially
- Task numbers are correct for your mode
- No duplicate numbers are created

---

## Troubleshooting

### GitHub Issues Setup Issues

**Problem: "GitHub CLI (gh) is not installed"**
- **Solution:** Install GitHub CLI
  - macOS: `brew install gh`
  - Linux: See [GitHub CLI installation](https://cli.github.com/manual/installation)

**Problem: "GitHub CLI is not authenticated"**
- **Solution:** Authenticate GitHub CLI
  ```bash
  gh auth login
  ```

**Problem: "Not in a GitHub repository"**
- **Solution:** Ensure you're in a git repository with a GitHub remote
  ```bash
  git remote add origin https://github.com/owner/repo.git
  ```

**Problem: "Issue #123 not found or not accessible"**
- **Solution:**
  - Verify the issue number is correct
  - Check you have access to the repository
  - Ensure the issue exists: `gh issue list`

**Problem: "Failed to create GitHub issue"**
- **Solution:**
  - Check GitHub CLI authentication: `gh auth status`
  - Verify repository access: `gh repo view`
  - Check repository permissions (need write access)

### CounterAPI Setup Issues

**Problem: "curl is not installed"**
- **Solution:** Install curl
  - macOS: Usually pre-installed
  - Linux: `sudo apt-get install curl`
  - Windows: Download from [curl website](https://curl.se/download.html)

**Problem: "jq or python3 required for JSON parsing"**
- **Solution:** Install one of:
  - `jq`: `brew install jq` (macOS) or `sudo apt-get install jq` (Linux)
  - `python3`: Usually pre-installed

**Problem: "Could not reach CounterAPI"**
- **Solution:**
  - Check internet connectivity
  - Verify CounterAPI service is accessible: `curl https://api.counterapi.dev`
  - Check firewall/proxy settings

**Problem: "Namespace must contain only lowercase letters..."**
- **Solution:** Use only:
  - Lowercase letters (a-z)
  - Numbers (0-9)
  - Hyphens (-)
  - Underscores (_)

### General Issues

**Problem: Coordination not working (falling back to multi-user)**
- **Check:**
  1. Run `./todo.ai detect-coordination` to verify prerequisites
  2. Run `./todo.ai config` to verify configuration
  3. Check error messages when creating tasks
  4. Verify network connectivity (for CounterAPI)

**Problem: Configuration file errors**
- **Solution:**
  1. View config: `./todo.ai config`
  2. Check YAML syntax
  3. Ensure required fields are present
  4. Re-run setup: `./todo.ai setup-coordination <type>`

**Problem: Tasks not getting unique numbers**
- **Check:**
  1. Verify coordination is working (see Test Coordination section)
  2. Check if fallback mode is being used
  3. Ensure coordination service is accessible
  4. Review error logs: `./todo.ai log`

### Getting Help

If you encounter issues not covered here:

1. **Check documentation:**
   - [Numbering Modes Guide](NUMBERING_MODES_GUIDE.md)
   - [Hybrid Task Numbering Design](HYBRID_TASK_NUMBERING_DESIGN.md)

2. **Run diagnostics:**
   ```bash
   ./todo.ai detect-coordination
   ./todo.ai config
   ./todo.ai log --lines 20
   ```

3. **Report bugs:**
   ```bash
   ./todo.ai report-bug "Issue description" "Context" "Command that failed"
   ```

---

## Quick Reference

### GitHub Issues Setup
```bash
# Quick setup
./todo.ai setup-coordination github-issues

# Or use wizard
./todo.ai setup
```

### CounterAPI Setup
```bash
# Quick setup
./todo.ai setup-coordination counterapi

# Or use wizard
./todo.ai setup
```

### Verify Setup
```bash
# Check configuration
./todo.ai config

# Detect available options
./todo.ai detect-coordination

# Test by creating a task
./todo.ai add "Test coordination"
```

---

## Further Reading

- [Numbering Modes Guide](NUMBERING_MODES_GUIDE.md) - Complete guide to all modes
- [Hybrid Task Numbering Design](HYBRID_TASK_NUMBERING_DESIGN.md) - Technical implementation
- [Usage Patterns](USAGE_PATTERNS.md) - Real-world usage examples
