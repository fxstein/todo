# todo.ai Usage Patterns

## Overview

This document describes various usage patterns and setups for `todo.ai` in different development scenarios. Each pattern addresses specific needs and constraints, from individual developer workflows to team collaboration.

---

## Pattern 1: Individual Developer (Project Not Using todo.ai)

### Scenario
- Individual developer wants to use `todo.ai` for personal task management
- Main project repository does NOT use `todo.ai`
- Developer works on forks and branches
- Tasks should NOT be committed to main/upstream repository
- Developer wants to use single-user mode without coordination

### Solution: Separate Developer Repository

**Approach:** Create a separate Git repository for developer tooling, use Git submodule or nested repository to link it to the code repository.

### Setup

**1. Create Developer Repository:**
```bash
# In a separate directory from your code repo
mkdir my-project-tasks
cd my-project-tasks
git init
git remote add origin https://github.com/your-username/my-project-tasks.git

# Install todo.ai
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai
chmod +x todo.ai

# Initialize todo.ai
./todo.ai init

# Create initial TODO.md
./todo.ai add "Set up developer task management"
```

**2. Link to Code Repository via Git Submodule:**
```bash
# In your main code repository
cd my-project
git submodule add https://github.com/your-username/my-project-tasks.git .dev-tasks
git commit -m "Add developer tasks submodule"

# Or create a nested repository (no submodule overhead):
cd my-project
git clone https://github.com/your-username/my-project-tasks.git .dev-tasks
# Add .dev-tasks/ to .gitignore
```

**3. Configure .gitignore:**
```bash
# In main code repository .gitignore
.dev-tasks/
.dev-tasks/**
```

**4. Workflow:**
```bash
# Navigate to tasks directory
cd .dev-tasks

# Add task
./todo.ai add "Implement feature X"

# Work on code in parent directory
cd ..

# Your tasks are in .dev-tasks/TODO.md
# Code repository has no todo.ai artifacts
```

### Benefits
- ✅ **Clean code repository:** No todo.ai artifacts in main/upstream repo
- ✅ **Single-user mode:** Simple sequential numbering, no coordination needed
- ✅ **Personal task management:** Developer controls their own tasks
- ✅ **Fork-friendly:** Tasks stay in developer's repository, not in forks
- ✅ **Merge-safe:** No conflicts when merging code (tasks are separate)
- ✅ **Branch-safe:** Tasks work on any branch without affecting code repo

### Directory Structure
```
my-project/                    # Main code repository
├── src/
├── README.md
├── .gitignore                 # Excludes .dev-tasks/
└── .dev-tasks/                # Separate Git repository (submodule or nested)
    ├── todo.ai
    ├── TODO.md
    └── .todo.ai/
        ├── .todo.ai.serial
        └── .todo.ai.log
```

### Configuration
```yaml
# .todo.ai/config.yaml
mode: single-user
```

**No coordination needed - personal tasks only.**

---

## Pattern 2: Team Repository (Embedded todo.ai)

### Scenario
- Team wants to use `todo.ai` for shared task management
- Tasks should be committed to main repository
- Team collaborates on same repository
- Need multi-user coordination

### Solution: Embedded in Main Repository

**Approach:** Install `todo.ai` directly in the main code repository, configure for multi-user mode.

### Setup

**1. Install in Main Repository:**
```bash
cd my-project
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai
chmod +x todo.ai
git add todo.ai
git commit -m "Add todo.ai task management tool"
```

**2. Initialize and Configure:**
```bash
# Initialize
./todo.ai init

# Setup multi-user mode
./todo.ai setup-mode multi-user

# Commit configuration
git add .todo.ai/config TODO.md
git commit -m "Initialize todo.ai multi-user mode"
```

**3. Team Workflow:**
```bash
# Each team member adds tasks
./todo.ai add "Implement feature X"

# Tasks committed to main repo
git add TODO.md .todo.ai/
git commit -m "feat: Add feature X task (fxstein-50)"
```

### Benefits
- ✅ **Shared tasks:** Team can see all tasks in one place
- ✅ **Repository-integrated:** Tasks are part of code repository
- ✅ **Multi-user coordination:** Prefix-based numbering prevents conflicts
- ✅ **Version-controlled:** Task history in Git
- ✅ **Visible in repository:** Tasks visible in GitHub/GitLab

### Limitations
- ⚠️ **Tasks in code repo:** Todo.ai artifacts committed to main repository
- ⚠️ **Fork pollution:** Fork contributors see tasks (unless configured)
- ⚠️ **Merge conflicts:** Task conflicts possible (handled by conflict resolution)

### Configuration
```yaml
# .todo.ai/config.yaml
mode: multi-user
coordination:
  type: none
```

---

## Pattern 3: Hybrid - Developer Repo + Team Repo

### Scenario
- Team wants shared coordination for major tasks
- Individual developers want personal task management
- Need to separate team tasks from individual tasks
- Developers work on forks and branches

### Solution: Dual Repository Setup

**Approach:** 
- **Team repository:** Embedded todo.ai for team coordination
- **Developer repository:** Separate todo.ai for personal tasks

### Setup

**1. Team Repository (Embedded):**
```bash
cd my-project
# Setup as Pattern 2 (multi-user mode)
./todo.ai setup-mode enhanced
# Configure GitHub Issues or CounterAPI coordination
```

**2. Developer Repository (Separate):**
```bash
cd ~/my-project-tasks
# Setup as Pattern 1 (single-user mode)
./todo.ai setup-mode single-user
```

**3. Workflow:**
```bash
# Team tasks (in code repo)
cd my-project
./todo.ai add "Team task: Implement authentication"  # Gets fxstein-50

# Personal tasks (separate repo)
cd ~/my-project-tasks
./todo.ai add "Personal: Research auth libraries"   # Gets #50
```

### Benefits
- ✅ **Separation of concerns:** Team tasks vs. personal tasks
- ✅ **Team coordination:** Shared tasks use enhanced mode
- ✅ **Personal flexibility:** Individual tasks use simple mode
- ✅ **Clean forks:** Personal tasks don't pollute forks

### Directory Structure
```
my-project/                    # Main code repository (team tasks)
├── src/
├── todo.ai                    # Team todo.ai
├── TODO.md                    # Team tasks (fxstein-50, alice-51, etc.)
└── .todo.ai/
    ├── config                 # Enhanced mode config
    └── ...

~/my-project-tasks/            # Developer personal repo
├── todo.ai
├── TODO.md                    # Personal tasks (#1, #2, etc.)
└── .todo.ai/
    ├── config                 # Single-user mode config
    └── ...
```

---

## Pattern 4: Git Submodule for Tooling (Recommended for Individual Developers)

### Scenario
- Individual developer wants to use todo.ai
- Main project does NOT use todo.ai
- Want to keep tooling and tasks separate
- Need version control for task management
- Want to sync tasks across multiple machines

### Solution: Git Submodule for Developer Tooling

**Approach:** Create a "developer tooling" repository, add as Git submodule to code repository.

### Setup

**1. Create Tooling Repository:**
```bash
# Create separate repository for developer tooling
mkdir my-project-dev-tools
cd my-project-dev-tools
git init
git remote add origin https://github.com/your-username/my-project-dev-tools.git

# Install todo.ai
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai
chmod +x todo.ai

# Initialize todo.ai
./todo.ai init

# Initial commit
git add .
git commit -m "Initial commit: Developer tooling with todo.ai"
git push -u origin main
```

**2. Add as Submodule to Code Repository:**
```bash
cd my-project
git submodule add https://github.com/your-username/my-project-dev-tools.git .dev-tools
git commit -m "Add developer tooling submodule"

# Optionally add to .gitignore if you don't want to track submodule updates in main repo
# Or keep it tracked to sync tooling across team
```

**3. Configure .gitignore (Optional):**
```bash
# If you want tooling to be personal (not committed to main repo):
# Add to my-project/.gitignore:
.dev-tools/
```

**4. Workflow:**
```bash
# Navigate to tooling directory
cd .dev-tools

# Use todo.ai
./todo.ai add "Implement feature X"
./todo.ai show

# Tasks in .dev-tools/TODO.md (separate from code)
# Code repository remains clean
```

**5. Sync Across Machines:**
```bash
# On machine 1: commit tasks
cd my-project/.dev-tools
git add TODO.md .todo.ai/
git commit -m "Update tasks"
git push

# On machine 2: pull tasks
cd my-project
git submodule update --remote .dev-tools
```

### Benefits
- ✅ **Version-controlled tasks:** Tasks in Git (can sync across machines)
- ✅ **Clean code repo:** Main repository has no todo.ai artifacts
- ✅ **Submodule management:** Can be shared with team or personal only
- ✅ **Easy sync:** Git handles synchronization
- ✅ **Branch support:** Tasks work on any branch without conflicts

### Directory Structure
```
my-project/                    # Main code repository
├── src/
├── .gitmodules               # Submodule reference
└── .dev-tools/               # Git submodule (separate repo)
    ├── todo.ai
    ├── TODO.md
    ├── .todo.ai/
    └── .git/                 # Submodule's own Git
```

---

## Pattern 5: Embedded Repository (Nested Git)

### Scenario
- Individual developer wants todo.ai
- Don't want submodule overhead
- Want tasks version-controlled
- Don't want to pollute main repository

### Solution: Nested Git Repository (not submodule)

**Approach:** Create a separate Git repository inside code repository, ignore it in main repo's `.gitignore`.

### Setup

**1. Create Nested Repository:**
```bash
cd my-project
mkdir .dev-tasks
cd .dev-tasks
git init
git remote add origin https://github.com/your-username/my-project-dev-tasks.git

# Install todo.ai
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai
chmod +x todo.ai
./todo.ai init

# Commit to nested repo
git add .
git commit -m "Initial commit"
git push -u origin main
```

**2. Ignore in Main Repository:**
```bash
# In my-project/.gitignore
.dev-tasks/
```

**3. Workflow:**
```bash
# Navigate to nested repo
cd .dev-tasks

# Use todo.ai (separate Git)
./todo.ai add "Task"

# Tasks committed to nested repo only
git add TODO.md
git commit -m "Add task"
git push
```

### Benefits
- ✅ **No submodule overhead:** Simpler than Git submodule
- ✅ **Separate version control:** Tasks have their own Git history
- ✅ **Clean main repo:** Ignored by main repository's Git
- ✅ **Full control:** Can manage tasks independently

### Limitations
- ⚠️ **No automatic sync:** Must manually manage nested repo
- ⚠️ **Team confusion:** Team members need to know about nested repo

---

## Pattern 6: Fork-Safe Development

### Scenario
- Developer forks upstream repository
- Upstream does NOT use todo.ai
- Developer wants task management for fork work
- Need to merge fork to upstream without todo.ai artifacts

### Solution: Separate Developer Repository

**Approach:** Keep todo.ai completely separate from fork, use Pattern 1 or 4.

### Setup

**1. Create Separate Tasks Repository:**
```bash
# Outside of fork directory
mkdir upstream-project-tasks
cd upstream-project-tasks
git init
git remote add origin https://github.com/your-username/upstream-project-tasks.git

# Install and setup todo.ai (single-user mode)
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai
chmod +x todo.ai
./todo.ai init
```

**2. Work on Fork:**
```bash
# Fork upstream repository
git clone https://github.com/upstream/my-project.git
cd my-project

# Work on code (no todo.ai here)
# ... make changes ...

# Manage tasks in separate repository
cd ../upstream-project-tasks
./todo.ai add "Fix bug in authentication"
./todo.ai show
```

**3. Merge Fork to Upstream:**
```bash
# Tasks repository is separate - no conflicts!
cd my-project
git checkout -b fix/authentication-bug
# ... work ...
git push origin fix/authentication-bug
# Create PR to upstream - no todo.ai artifacts in fork
```

### Benefits
- ✅ **Fork stays clean:** No todo.ai artifacts in fork
- ✅ **Merge-safe:** Upstream receives clean code, no task files
- ✅ **Task persistence:** Tasks remain in personal repository
- ✅ **Single-user mode:** Simple sequential numbering

---

## Pattern Comparison

| Pattern | Code Repo Has Tasks | Tasks Version Controlled | Fork-Safe | Team Coordination | Complexity |
|---------|-------------------|-------------------------|-----------|-------------------|------------|
| **Pattern 1: Separate Dev Repo** | ❌ No | ✅ Yes | ✅ Yes | ❌ No | ⭐ Simple |
| **Pattern 2: Embedded in Main** | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | ⭐⭐ Medium |
| **Pattern 3: Hybrid** | ✅ Partial | ✅ Yes | ✅ Yes | ✅ Yes | ⭐⭐⭐ Complex |
| **Pattern 4: Git Submodule** | ❌ No | ✅ Yes | ✅ Yes | ⚠️ Optional | ⭐⭐ Medium |
| **Pattern 5: Nested Repo** | ❌ No | ✅ Yes | ✅ Yes | ❌ No | ⭐ Simple |
| **Pattern 6: Fork-Safe** | ❌ No | ✅ Yes | ✅ Yes | ❌ No | ⭐ Simple |

---

## Configuration Examples

### Pattern 1, 4, 5, 6: Single-User Mode
```json
{
  "mode": "single-user"
}
```

### Pattern 2: Multi-User Mode
```json
{
  "mode": "multi-user",
  "coordination": {
    "type": "none"
  }
}
```

### Pattern 2: Enhanced Multi-User Mode
```yaml
# .todo.ai/config.yaml
mode: enhanced
coordination:
  type: github-issues
  issue_number: 123
  fallback: multi-user
```

### Pattern 3: Team Repo (Enhanced)
```json
{
  "mode": "enhanced",
  "coordination": {
    "type": "counterapi",
    "namespace": "my-project-team",
    "fallback": "multi-user"
  }
}
```

### Pattern 3: Developer Repo (Single-User)
```yaml
# .todo.ai/config.yaml
mode: single-user
```

---

## Recommended Patterns by Scenario

### Individual Developer, Upstream Doesn't Use todo.ai
- **Recommended:** Pattern 1 (Separate Dev Repo) or Pattern 4 (Git Submodule)
- **Mode:** Single-user
- **Why:** Clean separation, no pollution of upstream, simple setup

### Team Wants Shared Task Management
- **Recommended:** Pattern 2 (Embedded in Main)
- **Mode:** Multi-user or Enhanced
- **Why:** Shared tasks, visible to team, integrated with code

### Individual + Team Coordination
- **Recommended:** Pattern 3 (Hybrid)
- **Mode:** Enhanced for team, Single-user for personal
- **Why:** Best of both worlds - shared and personal tasks

### Fork-Based Contributions
- **Recommended:** Pattern 1 or Pattern 6 (Separate Repo)
- **Mode:** Single-user
- **Why:** Fork stays clean, easy to merge upstream

---

## Implementation Notes

### Creating a Separate Developer Repository

**Quick Setup Script:**
```bash
#!/bin/zsh
# setup-dev-tasks.sh

REPO_NAME="${1:-dev-tasks}"
REPO_DIR="${2:-.dev-tasks}"

# Create directory
mkdir -p "$REPO_DIR"
cd "$REPO_DIR"

# Initialize Git
git init
git remote add origin "https://github.com/$(gh api user --jq '.login')/${REPO_NAME}.git" || true

# Install todo.ai
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai
chmod +x todo.ai

# Initialize todo.ai
./todo.ai init

# Configure single-user mode
cat > .todo.ai/config <<EOF
MODE=single-user
EOF

# Initial commit
git add .
git commit -m "Initial commit: Developer task management"
git push -u origin main || echo "Note: Create GitHub repository ${REPO_NAME} first"

echo "✅ Developer tasks repository setup complete!"
echo "📁 Location: $REPO_DIR"
echo "💡 Use: cd $REPO_DIR && ./todo.ai add 'Your task'"
```

### Adding Submodule for Tooling

**Quick Setup:**
```bash
# In main code repository
git submodule add https://github.com/your-username/my-project-dev-tools.git .dev-tools
git commit -m "Add developer tooling submodule"

# Clone repository with submodule
git clone --recurse-submodules https://github.com/org/repo.git
```

---

## Migration Between Patterns

### From Pattern 1 to Pattern 2
- Tasks are in separate repo → Need to move to main repo
- **Steps:**
  1. Copy `.dev-tasks/TODO.md` to main repo
  2. Setup multi-user mode in main repo
  3. Renumber tasks (or keep old format during transition)
  4. Remove separate dev-tasks repo

### From Pattern 2 to Pattern 1
- Tasks in main repo → Move to separate repo
- **Steps:**
  1. Create separate dev-tasks repository
  2. Copy `TODO.md` and `.todo.ai/` to separate repo
  3. Setup single-user mode
  4. Remove from main repo (optional - can keep for history)

---

## Best Practices

1. **Document Your Pattern:** Add README in `.dev-tasks/` explaining setup
2. **Team Agreement:** If using Pattern 2 or 3, get team buy-in
3. **Configuration Sharing:** Commit `.todo.ai/config` for team patterns
4. **Ignore Patterns:** Add appropriate `.gitignore` entries
5. **Regular Commits:** Commit tasks regularly (they're part of workflow)
6. **Backup Tasks:** If separate repo, push regularly for backup

---

## Conclusion

These usage patterns provide flexibility for different development scenarios:

- **Individual developers** can use todo.ai without affecting upstream
- **Teams** can coordinate tasks in shared repositories
- **Hybrid approaches** support both team and individual workflows
- **Fork-based work** remains clean and merge-safe

Choose the pattern that best fits your workflow and collaboration needs.

---

## Next Steps

1. **Choose a pattern** based on your scenario
2. **Follow setup instructions** for your chosen pattern
3. **Configure todo.ai** for appropriate mode
4. **Document your setup** for team members (if applicable)
5. **Start managing tasks** with your chosen pattern

