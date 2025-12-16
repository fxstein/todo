# Comparison: todo.ai vs ascii-guard

## Release Script Comparison

### Scope and Functionality

#### ✅ **Matching Features**

Both scripts share these core capabilities:

1. **Two-phase release process** (prepare → execute)
   - ✅ Prepare mode: Analyze commits, determine version bump, generate release notes
   - ✅ Execute mode: Update versions, commit, tag, push, create GitHub release

2. **Version management**
   - ✅ Get current version from GitHub releases (source of truth)
   - ✅ Automatic version bump detection (major/minor/patch)
   - ✅ Version override capability (`--set-version`)
   - ✅ Update version in project files

3. **Release notes generation**
   - ✅ AI summary integration
   - ✅ Categorized commits (breaking, features, fixes, other)
   - ✅ Commit links with repository URLs
   - ✅ Preview before execution

4. **Release logging**
   - ✅ Release log file with timestamps
   - ✅ User tracking
   - ✅ Step-by-step logging

5. **State management**
   - ✅ Prepare state file (`.prepare_state`)
   - ✅ Prevents execution without prepare
   - ✅ Validates state consistency

6. **Git operations**
   - ✅ Tag creation and pushing
   - ✅ Branch pushing
   - ✅ Commit message formatting

#### 🔄 **Key Differences**

| Feature | todo.ai | ascii-guard |
|---------|---------|-------------|
| **Shell** | zsh (converts to bash) | bash |
| **Environment Validation** | ❌ None | ✅ Comprehensive (uv, venv, Python version, gh CLI) |
| **CI/CD Check** | ❌ None | ✅ Mandatory (`./scripts/wait-for-ci.sh`) |
| **Package Building** | ❌ N/A (single file) | ✅ Python package (wheel/sdist) |
| **PyPI Publishing** | ❌ N/A | ✅ Via GitHub Actions (trusted publishing) |
| **Bash Conversion** | ✅ Converts zsh → bash | ❌ N/A |
| **GitHub Release Assets** | ✅ todo.ai, todo.bash, install.sh | ✅ Wheel and sdist (via GitHub Actions) |
| **Summary File Location** | `release/RELEASE_SUMMARY.md` | `release/AI_RELEASE_SUMMARY.md` |
| **Release Notes File** | Generated in temp file | `release/RELEASE_NOTES.md` (persistent) |
| **Version Files** | `todo.ai`, `pyproject.toml` | `pyproject.toml`, `src/ascii_guard/__init__.py` |
| **Auto-commit Changes** | ✅ Yes (uncommitted changes) | ❌ No (fails on uncommitted) |
| **Stale Summary Detection** | ✅ Yes (checks file age vs last release) | ✅ Yes (checks file age < 60 seconds) |

#### 📊 **Functional Parity Assessment**

**Core Release Functionality: ✅ MATCHING**
- Both handle the complete release lifecycle
- Both support prepare/execute workflow
- Both generate release notes from commits
- Both create GitHub releases

**Project-Specific Features: ⚠️ DIFFERENT (Expected)**
- todo.ai: Bash conversion, single-file releases
- ascii-guard: Python package building, PyPI publishing, CI/CD integration

**Missing in todo.ai (Potential Improvements):**
1. ❌ Environment validation before release
2. ❌ CI/CD status check requirement
3. ❌ Stricter uncommitted changes handling (ascii-guard fails, todo.ai auto-commits)

**Missing in ascii-guard:**
1. ❌ Bash conversion (not needed for Python project)
2. ❌ Auto-commit of uncommitted changes (todo.ai's approach may be more convenient)

---

## Cursor Rules Comparison

### Shared Rules (todo.ai-*)

These rules should be **identical** across both repositories since they're installed by todo.ai:

#### ✅ **todo.ai-installation.mdc**

**todo.ai version:**
```markdown
When installing todo.ai from https://github.com/fxstein/todo.ai, use curl to download the single file: `curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai`. Do NOT clone the repository with git clone - only the single todo.ai file is needed.
```

**ascii-guard version:**
```markdown
When installing todo.ai from https://github.com/fxstein/todo.ai, use curl to download the single file: `curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai`. Do NOT clone the repository with git clone - only the single todo.ai file is needed.

To update an existing installation, run: `./todo.ai update`
```

**Difference:** ⚠️ ascii-guard has additional update instruction

#### ✅ **todo.ai-bug-reporting.mdc**

**todo.ai version:**
- Has AI Agent Workflow section (auto-submit for agents)
- Has Human Workflow section
- More concise examples

**ascii-guard version:**
- Has more detailed examples (✅/❌ format)
- Has privacy requirement (#6)
- Has explicit confirmation requirement (#4, #5)

**Difference:** ⚠️ ascii-guard has more detailed examples and explicit requirements

#### ✅ **todo.ai-task-management.mdc**

**todo.ai version:**
```markdown
It is required to track tasks and subtasks using todo.ai and not via built in TODO tools
TODO.md and .todo.ai/ must always be committed together
Always ask for user confirmation before archiving completed tasks using todo.ai
NEVER modify TODO.md directly using sed or similar - ALWAYS use todo.ai to manipulate it.
```

**ascii-guard version:**
```markdown
It is required to track tasks and subtasks using todo.ai and not via built in TODO tools
TODO.md and .todo.ai/ must always be committed together
Always ask for user confirmation before archiving completed tasks using todo.ai
```

**Difference:** ⚠️ todo.ai has additional "NEVER modify TODO.md directly" rule

#### ✅ **todo.ai-commit-format.mdc**

**Status:** ✅ **IDENTICAL** (both have same content)

#### ✅ **todo.ai-task-notes.mdc**

**Status:** ✅ **IDENTICAL** (both have same content)

#### ✅ **todo.ai-uninstall.mdc**

**Status:** ✅ **IDENTICAL** (both have same content)

### Project-Specific Rules

#### **releases.mdc (todo.ai) vs ascii-guard-releases.mdc (ascii-guard)**

These are **project-specific** and should differ:

**todo.ai/releases.mdc:**
- Focuses on todo.ai release process
- Uses `RELEASE_SUMMARY.md` as single source of truth
- Regenerates notes during execute
- No CI/CD check requirement
- No environment validation

**ascii-guard/ascii-guard-releases.mdc:**
- Focuses on ascii-guard release process
- Uses `AI_RELEASE_SUMMARY.md` → `RELEASE_NOTES.md` workflow
- Mandatory CI/CD check (`./scripts/wait-for-ci.sh`)
- Comprehensive environment validation
- Python package building and PyPI publishing
- uv package management rules
- Error handling guidelines

**Difference:** ✅ **EXPECTED** (project-specific rules)

---

## Summary

### Release Script: ✅ **SCOPE MATCHES** (with expected project differences)

**Core functionality is identical:**
- ✅ Two-phase prepare/execute workflow
- ✅ Version bump detection
- ✅ Release notes generation
- ✅ GitHub release creation
- ✅ State management

**Differences are project-appropriate:**
- todo.ai: Single-file tool → bash conversion, direct GitHub release
- ascii-guard: Python package → PyPI publishing, CI/CD integration

**Potential improvements for todo.ai:**
1. Add environment validation (check gh CLI, git status)
2. Add CI/CD check (if applicable)
3. Consider stricter uncommitted changes handling

### Cursor Rules: ⚠️ **MOSTLY IDENTICAL** (minor differences)

**Shared rules (todo.ai-*):**
- ✅ `todo.ai-commit-format.mdc`: **IDENTICAL**
- ✅ `todo.ai-task-notes.mdc`: **IDENTICAL**
- ✅ `todo.ai-uninstall.mdc`: **IDENTICAL**
- ⚠️ `todo.ai-installation.mdc`: ascii-guard has update instruction
- ⚠️ `todo.ai-bug-reporting.mdc`: ascii-guard has more detailed examples
- ⚠️ `todo.ai-task-management.mdc`: todo.ai has additional "NEVER modify" rule

**Project-specific rules:**
- ✅ Different (expected) - each project has its own release process rules

### Recommendations

1. **Synchronize shared rules:**
   - Update ascii-guard's `todo.ai-installation.mdc` to match todo.ai (or vice versa)
   - Align `todo.ai-bug-reporting.mdc` examples
   - Consider adding "NEVER modify TODO.md directly" to ascii-guard's task-management rule

2. **Release script:**
   - Consider adding environment validation to todo.ai (at minimum: gh CLI check)
   - Keep project-specific differences (they're appropriate)

3. **Documentation:**
   - Document why rules differ between projects
   - Ensure shared rules stay synchronized
