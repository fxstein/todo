# Cursor Rules Migration: .cursorrules to .cursor/rules/

## Verification Summary (Task #44.1)

✅ **Confirmed**: `.cursor/rules/` is the latest official Cursor implementation according to [docs.cursor.com](https://docs.cursor.com/en/context/rules).

### Current Status

- **Current Implementation**: `.cursorrules` file (legacy, deprecated)
- **Target Implementation**: `.cursor/rules/` directory with `.mdc` files (official, recommended)

### Migration Path

1. **Structure Change**:
   - From: Single `.cursorrules` file with sections
   - To: `.cursor/rules/` directory with individual `.mdc` files

2. **File Format**:
   - Each rule becomes a separate `.mdc` file
   - Each file requires front matter (YAML) with metadata:
     ```yaml
     ---
     description: "Brief overview of the rule"
     globs: ["pattern1", "pattern2"]  # Optional: file patterns
     alwaysApply: true  # Boolean: always include rule
     ---
     ```

3. **Current Rules in `.cursorrules`** (categorized):

   **Rules for End Users (shipped with tool - created by `init_cursor_rules()`):**
   - **## Task Management** section:
     - Rule 1: Track tasks using todo.ai (not built-in TODO tools)
     - Rule 2: TODO.md and .todo.ai/ must be committed together
     - Rule 3: Ask confirmation before archiving tasks
   
   - **## Installation** section:
     - Installation instructions for todo.ai
     - How to download and set up the tool using curl
     - Note: NOT cloning the repo, only downloading the single file
     - Helps agents install or update todo.ai when needed
   
   - **## Bug Reporting** section:
     - Critical requirements for bug reporting
     - Usage examples
     - Why it's required
   
   **Rules for Developer Environment (local to todo.ai repo only - NOT created by `init_cursor_rules()`, manually committed):**
   - **## Repository Context** section (NEW):
     - This is the development repository for todo.ai itself
     - We are developing the tool here, NOT installing it
     - Do NOT run installation commands (curl, download) - the tool is already present in this repo
     - The `todo.ai` file in this directory IS the tool being developed
     - Avoid circular references: don't try to install/update todo.ai when already in the todo.ai repo
   
   - **## Releases** section:
     - Release process instructions
     - How to generate release summaries
     - How to run release script
   
   - **## Commit Message Prefixes for Release Numbering** section:
     - Guidelines for backend/infrastructure commits (PATCH)
     - Guidelines for frontend/user-facing commits (MINOR/MAJOR)
     - Special cases handling

### Proposed Migration Structure

**Rules for End Users (shipped with tool - created by `init_cursor_rules()`):**
```
.cursor/
  rules/
    todo.ai-task-management.mdc
    todo.ai-installation.mdc
    todo.ai-bug-reporting.mdc
```

**Rules for Developer Environment (local to todo.ai repo only - manually committed to repo):**
```
.cursor/
  rules/
    repository-context.mdc
    releases.mdc
    commit-prefixes.mdc
```

**Naming Convention**:
- **End User Rules** (shipped with tool): Prefixed with `todo.ai-` to:
  - Clearly identify rules that come from todo.ai installation
  - Enable easy filtering and identification (users can easily see which rules are from todo.ai)
  - Avoid conflicts with user's own custom rules
  - Allow users to organize/manage todo.ai rules separately from their own rules
  
- **Developer Rules** (local to repo): NO prefix to:
  - Clearly distinguish them from tool-installed rules
  - Show they are specific to the todo.ai development environment
  - Make it obvious which rules are repo-specific vs. tool-provided
  - Allow easy identification: `todo.ai-*` = from tool, no prefix = dev environment

**Important Distinction:**
- **End User Rules**: These rules are created by `init_cursor_rules()` when users install/update todo.ai. They help AI agents use todo.ai correctly in any project. Currently: Task Management, Installation, Bug Reporting.
- **Developer Rules**: These rules are ONLY for the todo.ai repository itself. They guide AI agents working on the todo.ai codebase (repository context, release process, commit conventions). These are NOT created by `init_cursor_rules()` - they are manually committed to the repo. Currently: Repository Context, Releases, Commit Message Prefixes.

**Why This Distinction Matters:**
- End user rules need to be automatically created/updated when users install or update todo.ai
- Developer rules are specific to the todo.ai development environment and should not be auto-generated for end users
- This separation allows end users to have only the rules they need, while developers have the full set
- The Installation rule helps agents install or update todo.ai when needed (useful for both end users and developers)

### Benefits of Migration

1. **Better Organization**: Each rule in its own file
2. **Version Control**: Easier to track changes to individual rules
3. **Selective Application**: Can use `globs` to apply rules to specific file patterns
4. **Scalability**: Easy to add new rules without modifying existing ones
5. **Future-Proof**: Official implementation that will be maintained

### Migration Requirements

- **Backward Compatibility**: `.cursorrules` is still supported but deprecated
- **No Breaking Changes**: Both formats will work during transition
- **Automatic Migration**: Need to migrate existing `.cursorrules` files on update

### Next Steps

1. ✅ Verify official implementation (Task #44.1) - **COMPLETE**
2. Create design document (Task #44.2)
3. Implement migration logic (Task #44.3)
4. Update `init_cursor_rules` function (Task #44.4)
5. Create migration for existing installations (Task #44.5)
6. Test migration (Task #44.6)
7. Update documentation (Task #44.7)
8. Update release process docs (Task #44.8)

