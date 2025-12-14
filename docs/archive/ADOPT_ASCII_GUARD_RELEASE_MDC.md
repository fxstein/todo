# Adopting ascii-guard release.mdc for todo.ai

## Analysis: What's Generic vs ascii-guard-Specific

### ✅ **GENERIC (Can Adopt As-Is)**

1. **Two-Phase Process with Human Gate** (lines 3-21)
   - ✅ Completely generic - applies to any project
   - ✅ Strong emphasis on stopping after prepare

2. **Error Handling During Releases** (lines 139-229)
   - ✅ Generic error handling principles
   - ⚠️ Need to remove Python-specific error examples (pyenv, build module)
   - ✅ Keep: git push failures, gh CLI, general errors

3. **Step 1: Generate AI Release Summary** (lines 233-261)
   - ⚠️ Change file name: `AI_RELEASE_SUMMARY.md` → `RELEASE_SUMMARY.md`
   - ⚠️ Change header note: "ascii-guard vX.Y.Z" → "todo.ai vX.Y.Z"
   - ✅ Rest is generic

4. **Step 2: Prepare Release** (lines 263-291)
   - ⚠️ Change file references: `AI_RELEASE_SUMMARY.md` → `RELEASE_SUMMARY.md`
   - ⚠️ Change command: `--prepare` → `--prepare --summary release/RELEASE_SUMMARY.md`
   - ✅ Rest is generic

5. **Step 3: Review & Edit Release Notes** (lines 293-359)
   - ⚠️ Change file references: `AI_RELEASE_SUMMARY.md` → `RELEASE_SUMMARY.md`
   - ✅ Rest is generic

6. **Safeguards Section** (lines 439-458)
   - ⚠️ Remove: "uv run python -m build" check
   - ⚠️ Change file: `AI_RELEASE_SUMMARY.md` → `RELEASE_SUMMARY.md`
   - ✅ Rest is generic

7. **Version Numbering** (lines 489-520)
   - ✅ Completely generic

8. **AI Agent Workflow** (lines 556-633)
   - ⚠️ Remove: PyPI publishing references
   - ⚠️ Change file names
   - ⚠️ Adapt CI/CD check (todo.ai may not have wait-for-ci.sh)
   - ✅ Rest is generic

### ❌ **ASCII-GUARD SPECIFIC (Must Remove/Adapt)**

1. **Python Environment Management** (lines 26-93)
   - ❌ **ENTIRE SECTION** - Remove completely
   - Contains: uv, venv, Python-specific rules
   - Not applicable to todo.ai (shell script project)

2. **Step 0: CI/CD Check** (lines 96-135)
   - ⚠️ **ADAPT** - todo.ai has CI/CD but may not have `wait-for-ci.sh`
   - Options:
     - Option A: Create `wait-for-ci.sh` script for todo.ai
     - Option B: Use `gh run list` and `gh run watch` directly
     - Option C: Make it optional/conditional

3. **Step 4: Execute Release** (lines 361-380)
   - ❌ Remove: "Builds Python package (`uv run python -m build`)"
   - ❌ Remove: "Updates version in `pyproject.toml` and `src/ascii_guard/__init__.py`"
   - ❌ Remove: "GitHub Actions takes over: PyPI publishing"
   - ✅ Keep: "Updates version in todo.ai"
   - ✅ Keep: "Commits, tags, pushes, creates GitHub release"
   - ✅ Keep: "Creates GitHub release with assets"

4. **Key GitHub Actions Integration** (lines 413-435)
   - ❌ **ENTIRE SECTION** - Remove completely
   - Contains: PyPI publishing, trusted publishing, wheel/sdist
   - todo.ai creates GitHub releases directly, doesn't publish to PyPI

5. **Files and Tracking** (lines 524-552)
   - ⚠️ **ADAPT** - Change file references:
     - `pyproject.toml` → `todo.ai`, `pyproject.toml`
     - `src/ascii_guard/__init__.py` → Remove (not applicable)
     - `dist/`, `build/`, `*.egg-info/` → Remove (not applicable)
   - ✅ Keep: Release log, summary files

6. **Error Handling Examples** (lines 160-161, 479-482)
   - ❌ Remove: "pyenv: version 'X.Y' is not installed"
   - ❌ Remove: "No module named 'build'"
   - ❌ Remove: "Package build failed"
   - ✅ Keep: "gh: command not found", "git push failed", general errors

7. **Safeguards - Build Dependencies** (line 456)
   - ❌ Remove: "uv run python -m build" check
   - ✅ Keep: "gh auth status" check

8. **AI Agent Workflow - Success Report** (lines 620-633)
   - ❌ Remove: PyPI publishing references
   - ❌ Remove: "Publishing to PyPI (trusted publishing)"
   - ✅ Keep: GitHub release creation
   - ✅ Keep: GitHub Actions monitoring (if applicable)

---

## Recommended Adoption Strategy

### Phase 1: Core Adoption (High Priority)

1. ✅ **Adopt Two-Phase Process with Human Gate**
   - Strong emphasis on stopping after prepare
   - Multiple warnings about never auto-executing

2. ✅ **Adopt Error Handling Section**
   - Remove Python-specific errors
   - Keep generic error handling principles

3. ✅ **Adopt Step 1-3 Workflow**
   - Adapt file names to todo.ai conventions
   - Keep the detailed guidance

4. ✅ **Adopt Safeguards Section**
   - Remove Python-specific items
   - Keep generic safeguards

### Phase 2: CI/CD Integration (Medium Priority)

1. ⚠️ **CI/CD Check Requirement**
   - Decision needed: Create `wait-for-ci.sh` or use `gh` commands directly?
   - todo.ai has `.github/workflows/ci.yml` and `release.yml`
   - Can use: `gh run list --limit 1 --json status --jq '.[0].status'`

2. ⚠️ **GitHub Actions Monitoring**
   - todo.ai's release.sh creates GitHub releases directly
   - May not need GitHub Actions workflow monitoring
   - But could add it for consistency

### Phase 3: File Workflow (Low Priority)

1. ⚠️ **File Naming Decision**
   - ascii-guard: `AI_RELEASE_SUMMARY.md` → `RELEASE_NOTES.md`
   - todo.ai: `RELEASE_SUMMARY.md` (single source of truth)
   - **Decision:** Keep todo.ai's simpler workflow OR adopt ascii-guard's two-file system?

2. ⚠️ **Timing Constraints**
   - ascii-guard: Must commit summary within 60 seconds
   - todo.ai: No timing constraints currently
   - **Decision:** Add timing validation to prevent stale summaries?

---

## File Name Mapping

| ascii-guard | todo.ai | Action |
|-------------|---------|--------|
| `release/AI_RELEASE_SUMMARY.md` | `release/RELEASE_SUMMARY.md` | Change all references |
| `release/RELEASE_NOTES.md` | `release/RELEASE_NOTES.md` | Keep (if adopting two-file system) OR remove (if keeping single file) |
| `pyproject.toml` | `todo.ai`, `pyproject.toml` | Change version file references |
| `src/ascii_guard/__init__.py` | N/A | Remove all references |

---

## Sections to Remove Completely

1. ❌ **Python Environment Management** (lines 26-93) - 68 lines
2. ❌ **Key GitHub Actions Integration** (lines 413-435) - 23 lines
3. ❌ Python-specific error examples
4. ❌ PyPI publishing references throughout

**Total to remove:** ~100 lines of ascii-guard-specific content

---

## Sections to Adapt

1. ⚠️ **Step 0: CI/CD Check** - Adapt script path or use gh commands
2. ⚠️ **Step 4: Execute Release** - Remove Python package building, keep GitHub release
3. ⚠️ **Files and Tracking** - Change file references
4. ⚠️ **All file name references** - Change to todo.ai conventions
5. ⚠️ **AI Agent Workflow** - Remove PyPI, adapt file names

---

## Recommendation

**YES, we can adopt most of ascii-guard's release.mdc**, but need to:

1. ✅ **Remove** ~100 lines of Python/PyPI-specific content
2. ✅ **Adapt** file names and version file references
3. ⚠️ **Decide** on CI/CD check implementation
4. ⚠️ **Decide** on file workflow (single vs two-file system)
5. ⚠️ **Decide** on timing constraints

**Estimated effort:**
- Core adoption: ~80% of content is generic and adoptable
- Adaptations needed: File names, version files, remove Python-specific
- Decisions needed: CI/CD check method, file workflow, timing

**Result:** A comprehensive release.mdc with strong safeguards, error handling, and human gate enforcement, adapted for todo.ai's shell script project.
