# Release Numbering Analysis & Recommendations

**Created:** 2025-11-01  
**Task:** #36.5 - Review and finetune release numbering logic

## Release History Analysis

### Release 1.1.0 (Initial Release)

**Files Changed:**
- `.cursor/rules/` (backend - agent config)
- `.todo.ai/.todo.ai.log` (backend - internal state)
- `.todo.ai/.todo.ai.serial` (backend - internal state)
- `.todo.ai/backups/` (backend - backup files)
- `README.md` (frontend - user documentation)
- `TODO.md` (frontend - task list, but also used by script)
- `docs/RELEASE_PROCESS.md` (frontend - user documentation)
- `release.sh` (backend - release automation)
- `tests/TEST_PLAN.md` (backend - test infrastructure)
- `todo.ai` (frontend - user-facing CLI tool)

**Commit Analysis:**
- Mostly fixes and backend improvements
- Fixes to modify function (backend)
- macOS compatibility fixes (backend)
- Git tracking setup (backend)
- Initial release setup (mixed)

**Classification:** **Mixed** - Had both frontend and backend changes, but mostly backend fixes

---

### Release 1.2.0

**Files Changed:**
- `.cursor/rules/` (backend - agent config)
- `RELEASE_SUMMARY.md` (frontend - release notes)
- `docs/RELEASE_PROCESS.md` (frontend - user documentation)
- `release.sh` (backend - release automation)
- `todo.ai` (frontend - user-facing CLI tool, but changes were internal)

**Commits:**
- `Add support for AI-generated human-readable release summaries` - Backend (release process)
- `Fix version update to only replace VERSION assignments` - Backend (release script fix)
- Documentation updates - Frontend

**Classification:** **Backend** - Release automation improvements, no user-facing CLI changes

---

### Release 1.3.0

**Files Changed:**
- `.cursor/rules/` (backend - agent config)
- `RELEASE_SUMMARY.md` (frontend - release notes)
- `docs/RELEASE_PROCESS.md` (frontend - user documentation)
- `release.sh` (backend - release automation)
- `todo.ai` (frontend - user-facing CLI tool, but no functional changes)

**Commits:**
- `Add GitHub commit links to release notes and summaries` - Backend (release process)
- `Fix uncommitted changes check and add comprehensive release logging` - Backend (release script)
- Documentation updates - Frontend

**Classification:** **Backend** - Release automation improvements, no user-facing CLI changes

---

## Frontend vs Backend Classification

### Frontend (User-Facing Changes)
Files that directly affect end users or AI agents using the tool:

- `todo.ai` - **Functional changes** to CLI commands/behavior
- `README.md` - User documentation
- `TODO.md` - Task list (but changes here are usually data, not features)
- `docs/*.md` - User-facing documentation
- User-visible features in `todo.ai` script

### Backend (Infrastructure Changes)
Files that don't directly affect end users:

- `release.sh` - Release automation
- `.cursor/rules/` - Agent configuration (affects agents but not tool users)
- `.todo.ai/` - Internal state/logs
- `tests/` - Test infrastructure
- `docs/RELEASE_PROCESS.md` - Developer documentation
- Bug fixes in `todo.ai` script (fixes existing behavior)
- Internal improvements to `todo.ai` script (performance, code quality)

### Ambiguous Cases
- `.cursor/rules/` - Affects AI agents but not end users
- Documentation updates - Could be frontend (user-facing) or backend (dev docs)
- `RELEASE_SUMMARY.md` - Part of release process, not tool functionality

---

## Current Problem

**Backend-only releases** (like 1.2.0 and 1.3.0) are being released as **minor versions**, but:
- They don't add new user-facing features
- They don't change CLI behavior
- Users don't benefit directly from them
- They're internal infrastructure improvements

**Semantic Versioning Standard:**
- **MAJOR**: Breaking changes to API/behavior
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes and small improvements

**Our Current Logic:**
- Looks for keywords like "add", "new", "implement" → **MINOR**
- Looks for "fix", "bug" → **PATCH**
- Problem: Backend infrastructure changes get tagged as "add"/"implement" → **MINOR** when they should be **PATCH**

---

## Recommendations

### Option 1: Use Patch for Backend-Only Releases

**Approach:** Detect backend-only changes and force them to be patch releases.

**Detection Logic:**
1. Check which files changed in commits
2. If **only** backend files changed → **PATCH**
3. If frontend files changed → use current logic

**Backend File Patterns:**
- `release.sh`
- `.cursor/rules/` (maybe - it affects agents)
- `.todo.ai/*`
- `tests/*`
- `docs/RELEASE_PROCESS.md`
- `docs/TEST_PLAN.md`
- `RELEASE_SUMMARY.md`
- `RELEASE_LOG.md`

**Frontend File Patterns:**
- `todo.ai` (only if functional changes)
- `README.md`
- `docs/*.md` (excluding RELEASE_PROCESS.md and TEST_PLAN.md)

**Implementation:**
```bash
# In analyze_commits():
# 1. Get list of changed files
# 2. Classify as frontend/backend
# 3. If only backend → force patch
# 4. If frontend → use keyword analysis
```

**Pros:**
- Aligns with semantic versioning
- Clear distinction between user-facing features and infrastructure
- Prevents version number inflation from backend work

**Cons:**
- Requires file change analysis (more complex)
- Need to maintain list of backend vs frontend files

---

### Option 2: Use Commit Message Prefixes

**Approach:** Require explicit prefixes for backend-only changes:
- `backend:` prefix → always PATCH
- `infra:` prefix → always PATCH
- `docs:` prefix → always PATCH (unless user-facing docs)
- `release:` prefix → always PATCH

**Examples:**
- `backend: Fix release script version update logic` → PATCH
- `infra: Add release logging` → PATCH
- `docs: Update release process documentation` → PATCH
- `feat: Add new task filtering command` → MINOR

**Pros:**
- Simple to implement
- Explicit and clear
- No file analysis needed

**Cons:**
- Requires discipline in commit messages
- Easy to forget prefix
- Doesn't work retroactively

---

### Option 3: Hybrid Approach ⭐ SELECTED

**Approach:** Combine file analysis with commit message prefixes.

**Detection:**
1. **If commit message has explicit prefix** → use prefix logic
   - `backend:` → PATCH
   - `infra:` → PATCH
   - `release:` → PATCH
   - `docs:` (dev docs) → PATCH
   - `docs:` (user docs) → check keywords

2. **If no prefix, analyze file changes:**
   - Only backend files → PATCH
   - Frontend files present → use keyword analysis

3. **Fallback to keyword analysis** if file analysis fails

**Backend Keywords:**
- `backend`, `infra`, `release`, `internal`, `refactor`
- Explicitly mark backend-only work

**Implementation Priority:**
1. Check for prefixes first (fastest, explicit)
2. Check file changes (slower, but catches forgotten prefixes)
3. Fall back to keyword analysis (current behavior)

**Pros:**
- Best of both worlds
- Handles cases where prefixes are forgotten
- Flexible and explicit
- Backward compatible

**Cons:**
- More complex implementation
- Need to maintain file classification

---

## Recommended Implementation

### Phase 1: Add File Analysis

Add function to detect backend-only releases:

```bash
is_backend_only_release() {
    local commit_range="$1"
    local changed_files=$(git diff --name-only "$commit_range" 2>/dev/null || \
                          git diff --name-only HEAD -- "$commit_range" 2>/dev/null || echo "")
    
    if [[ -z "$changed_files" ]]; then
        return 1  # Can't determine, use normal logic
    fi
    
    # Backend file patterns
    local backend_patterns=(
        "release.sh"
        ".cursor/rules/"
        ".todo.ai/"
        "tests/"
        "RELEASE_SUMMARY.md"
        "RELEASE_LOG.md"
        "docs/RELEASE_PROCESS.md"
        "docs/TEST_PLAN.md"
    )
    
    # Frontend file patterns
    local frontend_patterns=(
        "README.md"
        "todo.ai"  # Only count if functional changes
    )
    
    local has_frontend=false
    local has_backend=false
    
    while IFS= read -r file; do
        [[ -z "$file" ]] && continue
        
        # Check if frontend
        for pattern in "${frontend_patterns[@]}"; do
            if [[ "$file" == "$pattern" ]] || [[ "$file" =~ ^$pattern ]]; then
                has_frontend=true
                break
            fi
        done
        
        # Check if backend
        for pattern in "${backend_patterns[@]}"; do
            if [[ "$file" == "$pattern" ]] || [[ "$file" =~ ^$pattern ]]; then
                has_backend=true
                break
            fi
        done
    done <<< "$changed_files"
    
    # If only backend files changed, it's a backend-only release
    if [[ "$has_backend" == true ]] && [[ "$has_frontend" == false ]]; then
        return 0  # Backend only
    fi
    
    return 1  # Has frontend or mixed
}
```

### Phase 2: Update analyze_commits()

```bash
analyze_commits() {
    local last_tag="$1"
    # ... existing code ...
    
    # Check for backend-only release
    if is_backend_only_release "$commit_range"; then
        echo "patch"
        return
    fi
    
    # Check for explicit prefixes
    if echo "$commits" | grep -qiE "^(backend|infra|release|internal):"; then
        echo "patch"
        return
    fi
    
    # Continue with existing keyword analysis...
}
```

### Phase 3: Handle `todo.ai` Script Carefully

The `todo.ai` file is tricky:
- **Functional changes** (new commands, changed behavior) → MINOR/MAJOR
- **Bug fixes** → PATCH
- **Backend refactoring** (no behavior change) → PATCH

**Solution:** Use commit message to distinguish:
- `fix:` or `bug:` in commit message → PATCH
- `feat:` or `add:` with functional description → MINOR
- `refactor:` or `internal:` → PATCH

---

## Summary

**✅ SELECTED: Hybrid Approach (Option 3)**

This approach has been selected and will be implemented.

1. **Explicit prefixes** for backend work (enforce via cursor rules)
2. **File analysis** as fallback to catch forgotten prefixes
3. **Force PATCH** for backend-only releases

**Expected Results:**
- Releases 1.2.0 and 1.3.0 would have been **1.1.1** and **1.1.2** (patch releases)
- Clear distinction between user-facing features and infrastructure
- Aligns with semantic versioning principles
- Version numbers reflect actual user impact

**Implementation Status:**
- ✅ Analysis document created
- ✅ Option 3 selected
- 🔄 Implementation in progress

