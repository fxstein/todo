# Release Please Phase 1 Summary - AIT-8

**Date:** 2026-01-30
**Task:** #269.3
**Phase:** 1 of 6 - Configure Release Please Baseline

---

## ✅ Completed

### Configuration Files Created

1. **`.github/workflows/release-please.yml`**
   - Main Release Please workflow
   - Triggers on push to `main` branch
   - Permissions: `contents: write`, `pull-requests: write`
   - Outputs: PR number, release status, tag name

2. **`.github/release-please-config.json`**
   - Release type: `python`
   - Package name: `todo-ai`
   - Tag format: `v4.0.0` (no component prefix)
   - Version bumping: Pre-major (allows minor bumps before 1.0.0)
   - Extra files: `ai_todo/__init__.py` (in addition to `pyproject.toml`)
   - Custom changelog sections (13 types):
     - ✨ Features (`feat:`)
     - 🐛 Bug Fixes (`fix:`)
     - 📚 Documentation (`docs:`)
     - ⚙️ Backend (`backend:`)
     - 🏗️ Infrastructure (`infra:`)
     - 🔧 Maintenance (`chore:`)
     - 🧪 Tests (`test:`)
     - 👷 CI/CD (`ci:`)
     - 📦 Release (`release:`)
     - 🔒 Internal (`internal:`)
     - ⚡ Performance (`perf:`)
     - ♻️ Refactoring (`refactor:`)
     - 🏗️ Build (`build:`)

3. **`.github/release-please-manifest.json`**
   - Bootstrapped with current version: `4.0.0b2`
   - Will be automatically maintained by Release Please

---

## 🎯 How It Works

### Workflow Trigger

**On Push to Main:**
1. Release Please analyzes commits since last release
2. Categorizes commits by conventional commit type
3. Determines version bump (major/minor/patch) based on commit types
4. Creates or updates a Release PR with:
   - Updated `CHANGELOG.md`
   - Version bump in `pyproject.toml`
   - Version bump in `ai_todo/__init__.py`
   - Updated manifest file

**Release PR Format:**
- **Title:** `chore(main): release 4.0.1`
- **Body:** Generated CHANGELOG with categorized commits
- **Files:** All version files + CHANGELOG.md

### Release PR Lifecycle

**Continuous Updates:**
- Each new push to `main` updates the same Release PR
- CHANGELOG grows with new commits
- Version recalculated if breaking changes added

**Merge Triggers Release:**
- When Release PR is merged → Release Please creates tag
- Tag push triggers existing CI/CD pipeline
- Existing `release` job publishes to PyPI + GitHub

---

## 🧪 Testing Required (Phase 1)

### Test 1: CHANGELOG Generation

**Goal:** Verify Release Please generates correct CHANGELOG from commits

**Steps:**
1. Merge this PR to `main` branch
2. Wait for Release Please workflow to run
3. Check for Release PR creation (title: `chore(main): release X.Y.Z`)
4. Review CHANGELOG.md in PR:
   - Are commits categorized correctly?
   - Are custom sections (backend, infra) working?
   - Is version number correct?

**Expected Result:**
- Release PR created with categorized commits
- All conventional commit types recognized
- Custom sections (backend, infra, etc.) populated

### Test 2: Version Bumping

**Goal:** Verify version updates in all required files

**Steps:**
1. Review Release PR files changed
2. Check `pyproject.toml` - version updated?
3. Check `ai_todo/__init__.py` - version updated?
4. Check `.github/release-please-manifest.json` - version updated?

**Expected Result:**
- All three files have consistent version numbers
- Version increment follows semantic versioning rules

### Test 3: Pre-release (Beta) Support

**Goal:** Validate beta release workflow

**Steps:**
1. Update `.github/release-please-config.json`:
   ```json
   {
     "packages": {
       ".": {
         "prerelease": true,
         "prerelease-type": "b"
       }
     }
   }
   ```
2. Commit and push to `main`
3. Verify Release PR creates beta version (e.g., `4.0.1b1`)
4. Merge and verify tag format includes beta suffix

**Expected Result:**
- Beta version format: `4.0.1b1`
- Tag format: `v4.0.1b1`
- PyPI release marked as pre-release

### Test 4: Conventional Commit Types

**Goal:** Verify all commit types trigger correct version bumps

**Test Matrix:**

| Commit Type | Expected Bump | Test Commit |
|-------------|---------------|-------------|
| `feat:` | MINOR | `feat: Add new feature` |
| `fix:` | PATCH | `fix: Resolve bug` |
| `docs:` | PATCH | `docs: Update README` |
| `backend:` | PATCH | `backend: Refactor core` |
| `infra:` | PATCH | `infra: Update CI` |
| `feat!:` | MAJOR | `feat!: Breaking change` |
| `BREAKING CHANGE:` | MAJOR | Footer: `BREAKING CHANGE: API changed` |

**Steps:**
1. Make test commits with each type
2. Push to `main`
3. Verify Release PR shows correct version bump
4. Verify commit appears in correct CHANGELOG section

**Expected Result:**
- Version bump matches commit type
- Commit categorized in correct CHANGELOG section

---

## 📋 Open Questions (Phase 1)

### Q1: First Release PR Behavior

**Question:** Will Release Please create a PR for the entire commit history since `v4.0.0b2`?

**Impact:** CHANGELOG could be very long if many commits exist

**Resolution:**
- Review first Release PR carefully
- Consider squashing/cleaning CHANGELOG if needed
- Document expected behavior for future releases

### Q2: Beta → Stable Transition

**Question:** How does Release Please handle graduation from `4.0.0b2` → `4.0.0` stable?

**Approach:**
- Set `prerelease: false` in config
- Release Please should create `4.0.0` (stable)
- Verify CHANGELOG covers full beta cycle

**Testing:** Required before Phase 6 (first production release)

### Q3: Manifest File Management

**Question:** Should `.github/release-please-manifest.json` be committed?

**Answer:** Yes
- Release Please updates this file automatically
- Must be committed to track version state
- Should be included in Release PR

---

## 🚀 Next Steps

### Immediate (Testing Phase 1)

1. **Review and approve** this implementation
2. **Merge PR** to `main` branch
3. **Monitor** Release Please workflow execution
4. **Review** generated Release PR
5. **Validate** CHANGELOG and version bumping
6. **Test** beta release workflow
7. **Document** any issues or unexpected behavior

### Phase 2: AI Summary Integration (Next)

1. **Create Gemini API service account**
   - Generate API key
   - Configure GitHub secret: `GEMINI_API_KEY` # pragma: allowlist secret

2. **Implement AI summary workflow**
   - `.github/workflows/ai-release-summary.yml`
   - `.github/scripts/generate_ai_summary.py`
   - `.github/scripts/inject_summary.py`

3. **Test end-to-end**
   - Trigger Release PR creation
   - Verify AI summary generated
   - Verify summary injected into CHANGELOG
   - Verify PR updated with summary

### Subsequent Phases

- **Phase 3:** Beta policy enforcement (hard block)
- **Phase 4:** Integration testing (5 scenarios)
- **Phase 5:** Migration cutover (archive release.sh)
- **Phase 6:** First production release

---

## 📊 Success Criteria (Phase 1)

- [x] Configuration files created
- [x] Files committed and pushed
- [ ] Release PR created on merge to main
- [ ] CHANGELOG generated correctly
- [ ] Version bumping works (all files)
- [ ] Custom sections appear in CHANGELOG
- [ ] Beta release workflow validated
- [ ] No errors in Release Please workflow

**Status:** Configuration complete, ready for merge to main and testing

---

## 📝 Notes

### Configuration Decisions

1. **`include-component-in-tag: false`**
   - Tags: `v4.0.0` (not `todo-ai-v4.0.0`)
   - Matches current tag format

2. **`bump-minor-pre-major: true`**
   - Allows minor bumps before 1.0.0
   - Current: `4.0.0` (already > 1.0.0, but future-proof)

3. **`bump-patch-for-minor-pre-major: false`**
   - Allows minor bumps for `feat:` commits
   - Prevents forcing PATCH bumps pre-1.0.0

4. **Custom changelog sections**
   - Includes project-specific types: `backend`, `infra`, `release`, `internal`
   - Supports existing commit conventions

### Known Limitations (Phase 1)

1. **No AI summary** (Phase 2)
2. **No beta policy enforcement** (Phase 3)
3. **Manual beta config** (requires config update for beta releases)
4. **No Linear integration** (manual updates only)

---

**Prepared By:** AI Assistant
**Date:** 2026-01-30
**Task:** #269.3 (Phase 1)
**Design:** docs/design/release_please_design.md
