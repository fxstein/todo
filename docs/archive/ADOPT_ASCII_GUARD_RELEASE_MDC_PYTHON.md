# Adopting ascii-guard release.mdc for todo.ai (Python Project)

## ✅ **REASSESSMENT: todo.ai IS a Python Project**

### Current Python Infrastructure

1. ✅ **Python Package Structure**
   - `pyproject.toml` with full project configuration
   - `todo_ai/` package directory with modules
   - Entry points: `todo-ai` and `todo-ai-mcp`

2. ✅ **uv Dependency Management**
   - `uv.lock` file exists
   - CI/CD uses `uv sync --all-extras`
   - Development dependencies configured

3. ✅ **CI/CD Workflows**
   - `.github/workflows/ci.yml` - Testing, linting, type checking
   - `.github/workflows/release.yml` - PyPI publishing on tags
   - Uses uv, pytest, ruff, mypy

4. ✅ **Release Workflow**
   - Builds Python package (`uv run python -m build`)
   - Publishes to PyPI (via GitHub Actions)
   - Creates GitHub releases with dist artifacts

5. ⚠️ **Version Management**
   - Currently: `pyproject.toml` + `todo.ai` (shell script)
   - Missing: `todo_ai/__init__.py` with `__version__`
   - **Recommendation:** Add `__version__` to `todo_ai/__init__.py`

---

## What Can We Adopt from ascii-guard?

### ✅ **CAN ADOPT (with minor adaptations)**

1. **✅ Python Environment Management** (lines 26-93)
   - ✅ **FULLY APPLICABLE** - todo.ai uses uv
   - ⚠️ Adapt: Check if `.venv` exists (todo.ai may use different setup)
   - ⚠️ Adapt: Setup script path (`./setup.sh` vs actual setup)

2. **✅ Step 0: CI/CD Check** (lines 96-135)
   - ✅ **FULLY APPLICABLE** - todo.ai has CI/CD
   - ⚠️ Adapt: Create `./scripts/wait-for-ci.sh` OR use `gh run list` directly
   - ✅ Same principle: Don't release if CI/CD is failing

3. **✅ Error Handling** (lines 139-229)
   - ✅ **FULLY APPLICABLE** - Generic error handling
   - ✅ Keep Python-specific errors (build module, pyenv)
   - ✅ Keep all error examples

4. **✅ Step 1-4 Workflow** (lines 233-380)
   - ✅ **FULLY APPLICABLE** - Same workflow
   - ⚠️ Adapt: File names (see below)
   - ⚠️ Adapt: Version files (see below)

5. **✅ GitHub Actions Integration** (lines 413-435)
   - ✅ **FULLY APPLICABLE** - todo.ai has release.yml
   - ⚠️ Adapt: Project name references
   - ⚠️ Note: todo.ai uses PyPI token (not trusted publishing yet)

6. **✅ Safeguards** (lines 439-458)
   - ✅ **FULLY APPLICABLE** - All safeguards apply
   - ✅ Keep: "uv run python -m build" check
   - ✅ Keep: All other safeguards

7. **✅ Files and Tracking** (lines 524-552)
   - ✅ **FULLY APPLICABLE** - Python package structure
   - ⚠️ Adapt: Version file locations (see below)

8. **✅ AI Agent Workflow** (lines 556-633)
   - ✅ **FULLY APPLICABLE** - Same workflow
   - ⚠️ Adapt: File names and project references

---

## Adaptations Needed

### 1. **File Names**

| ascii-guard | todo.ai | Decision |
|-------------|---------|----------|
| `release/AI_RELEASE_SUMMARY.md` | `release/RELEASE_SUMMARY.md` | **Option A:** Keep todo.ai's convention (single file) OR **Option B:** Adopt ascii-guard's two-file system |
| `release/RELEASE_NOTES.md` | `release/RELEASE_NOTES.md` | Only if adopting two-file system |
| `src/ascii_guard/__init__.py` | `todo_ai/__init__.py` | ✅ Add `__version__` to match ascii-guard pattern |

### 2. **Version Files**

**Current todo.ai:**
- `pyproject.toml` ✅ (already updated)
- `todo.ai` (shell script) ✅ (already updated)

**ascii-guard pattern:**
- `pyproject.toml` ✅
- `src/ascii_guard/__init__.py` with `__version__`

**Recommendation:**
- ✅ Keep updating `pyproject.toml` and `todo.ai`
- ✅ **ADD:** `todo_ai/__init__.py` with `__version__ = "X.Y.Z"`
- Update `release.sh` to also update `__init__.py`

### 3. **CI/CD Check Script**

**ascii-guard:** Uses `./scripts/wait-for-ci.sh`

**todo.ai options:**
- **Option A:** Create `./scripts/wait-for-ci.sh` (match ascii-guard exactly)
- **Option B:** Use `gh run list` and `gh run watch` directly in rule
- **Option C:** Make it conditional (if script exists, use it; else use gh commands)

**Recommendation:** Option A - Create the script for consistency

### 4. **Project Name References**

Replace throughout:
- "ascii-guard" → "todo.ai"
- "ascii_guard" → "todo_ai"
- "src/ascii_guard" → "todo_ai"

### 5. **Setup Script**

**ascii-guard:** Uses `./setup.sh`

**todo.ai:** Check what setup script exists
- If `./setup.sh` exists → Keep reference
- If different → Adapt to actual script name
- If none → Remove or make optional

### 6. **PyPI Publishing**

**ascii-guard:** Uses trusted publishing (OIDC)

**todo.ai:** Currently uses PyPI token (`TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}`)

**Adaptation:**
- Keep the workflow description
- Note that todo.ai uses token-based auth (can upgrade to trusted publishing later)

---

## Sections to Remove/Modify

### ❌ **Remove (Not Applicable)**

1. **Nothing major!** - Most content is applicable

### ⚠️ **Modify (Adaptations)**

1. **File name references** - Change to todo.ai conventions
2. **Project name** - Replace "ascii-guard" with "todo.ai"
3. **Version file paths** - `src/ascii_guard/__init__.py` → `todo_ai/__init__.py`
4. **CI/CD script path** - Create or adapt `wait-for-ci.sh`
5. **Setup script** - Verify actual script name
6. **PyPI auth** - Note token-based (can mention trusted publishing as future)

---

## Recommended Adoption Plan

### Phase 1: Core Adoption (Immediate)

1. ✅ **Adopt entire structure** - 95% applicable
2. ✅ **Adapt file names** - Change to todo.ai conventions
3. ✅ **Adapt project references** - Replace "ascii-guard" with "todo.ai"
4. ✅ **Add `__version__` to `todo_ai/__init__.py`**
5. ✅ **Update `release.sh`** to also update `__init__.py`

### Phase 2: Infrastructure (Short-term)

1. ✅ **Create `./scripts/wait-for-ci.sh`** - Match ascii-guard pattern
2. ✅ **Verify setup script** - Ensure `./setup.sh` exists or adapt
3. ⚠️ **Consider trusted publishing** - Upgrade PyPI auth (optional)

### Phase 3: File Workflow Decision

**Decision needed:** Single file vs two-file system

- **Option A:** Keep `RELEASE_SUMMARY.md` (todo.ai's current approach)
  - Simpler, single source of truth
  - Already working

- **Option B:** Adopt `AI_RELEASE_SUMMARY.md` → `RELEASE_NOTES.md` (ascii-guard's approach)
  - More structured, separates AI summary from full notes
  - Requires updating release.sh

**Recommendation:** Option B - Adopt ascii-guard's two-file system for consistency and better structure

---

## File Name Decision Matrix

### Current todo.ai Workflow:
```
1. AI writes → release/RELEASE_SUMMARY.md
2. Prepare reads → release/RELEASE_SUMMARY.md
3. Execute regenerates from → release/RELEASE_SUMMARY.md
```

### ascii-guard Workflow:
```
1. AI writes → release/AI_RELEASE_SUMMARY.md
2. AI commits immediately
3. Prepare reads → release/AI_RELEASE_SUMMARY.md
4. Prepare writes → release/RELEASE_NOTES.md (summary + commits)
5. Human edits → release/RELEASE_NOTES.md
6. Execute uses → release/RELEASE_NOTES.md
```

### Recommendation:
**Adopt ascii-guard's two-file system** because:
- ✅ Better separation of concerns (AI summary vs full notes)
- ✅ Matches ascii-guard pattern (consistency)
- ✅ Allows editing full notes without touching AI summary
- ✅ More structured workflow

**Required changes:**
- Update `release.sh` to use two-file system
- Update rule to reference both files
- Add timing constraint (commit summary within 60 seconds)

---

## Summary

### ✅ **YES - We can adopt ~95% of ascii-guard's release.mdc!**

**Why:**
- todo.ai IS a Python project ✅
- Uses uv ✅
- Has CI/CD ✅
- Publishes to PyPI ✅
- Has GitHub Actions workflows ✅

**Main adaptations:**
1. File names (RELEASE_SUMMARY.md vs AI_RELEASE_SUMMARY.md)
2. Project name references
3. Version file paths (add `__init__.py`)
4. CI/CD script (create wait-for-ci.sh)
5. Setup script verification

**Estimated effort:**
- Core adoption: ~2-3 hours (file name changes, project references)
- Infrastructure: ~1 hour (create wait-for-ci.sh, add **version**)
- Testing: ~1 hour (verify workflow)

**Result:** Comprehensive release.mdc matching ascii-guard's quality and safeguards, adapted for todo.ai's Python project structure.
