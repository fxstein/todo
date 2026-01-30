# Release Please Migration Analysis - AIT-8

**Date:** 2026-01-30
**Linear Issue:** [AIT-8](https://linear.app/fxstein/issue/AIT-8/release-please)
**GitHub Issue:** [#59](https://github.com/fxstein/ai-todo/issues/59)
**Task:** #269

## Executive Summary

Analyze the current custom `release.sh` workflow and assess migration path to Google's [Release Please](https://github.com/googleapis/release-please) automation tool. Release Please automates CHANGELOG generation, version bumping, and release PR management based on conventional commits.

**Key Question:** Can Release Please accommodate our custom AI-generated release summaries (using Gemini) while maintaining our current release quality and beta workflow?

---

## Current Release Infrastructure

### 1. Release Scripts

**Primary: `release/release.sh` (2,330 lines)**
- Intelligent version analysis from commit messages
- Two-phase workflow: `--prepare` (preview) → `--execute` (publish)
- Beta release support (`--beta` flag)
- AI summary integration (`--summary` flag)
- Version override (`--set-version`)
- Automatic cleanup of failed releases (`--abort`)
- Commit categorization (breaking/features/fixes)
- Git tag management
- GitHub release creation (delegated to CI/CD)

**Supporting Scripts:**
- `release/publish_pypi.sh` - Manual PyPI publishing helper (35 lines, rarely used)
- `release/convert_zsh_to_bash.sh` - Legacy bash compatibility converter

### 2. Cursor Rules

**`release-workflow.mdc` (37 lines, alwaysApply: true)**
- Simple prepare → review → execute workflow
- Agent instructions for manual release flow
- AI summary generation requirement (2-3 paragraphs)
- Beta vs stable commit analysis rules
- Error handling: STOP on failures

**`linear-release-workflow.mdc` (50 lines, alwaysApply: false, DISABLED)**
- Automated release workflow with Linear tracking
- ai-todo task structure creation
- Approval gate via Linear comments
- CI monitoring and status updates
- Currently disabled for testing

### 3. Version Management

**Version Sources:**
- `pyproject.toml` - PRIMARY (Python package version)
- `ai_todo/__init__.py` - Python module version
- `legacy/todo.ai` - Legacy script version (for validation)

**Version Format:**
- Stable: `4.0.0`
- Beta: `4.0.0b2`
- Follows semantic versioning strictly

### 4. Release Types & Decision Logic

**Automatic Bump Type Detection:**

| Priority | Criteria | Bump Type | Example |
|----------|----------|-----------|---------|
| 1 | Explicit prefixes | PATCH | `backend:`, `infra:`, `release:`, `internal:` |
| 1 | Explicit prefixes | MINOR | `feat:`, `feature:` |
| 1 | Explicit prefixes | PATCH | `fix:`, `docs:`, `chore:` |
| 1 | Breaking indicators | MAJOR | `breaking`, `!:`, `feat!:` |
| 2 | File analysis | PATCH | Only backend files changed |
| 3 | Keyword analysis | MINOR | `add`, `new`, `implement`, `create` |
| 3 | Keyword analysis | PATCH | `fix`, `bug`, `correct` |

**Backend Files** (trigger PATCH only):
- `.cursor/rules/`
- `.ai-todo/`
- `tests/`
- `release/*` (release infrastructure)
- `docs/TEST_PLAN.md`, design docs

**Frontend Files** (trigger MINOR):
- `README.md`
- User-facing documentation
- `ai_todo/` Python source (functional changes)

### 5. Beta Release Workflow

**Beta Cycle:**
1. When current version is beta (e.g., `4.0.0b2`), all subsequent betas use same base version
2. Beta numbering is auto-incremented: `4.0.0b1` → `4.0.0b2` → `4.0.0b3`
3. Beta → Stable graduation: Release summary covers ALL commits since last stable

**Major Release Enforcement:**
- Major releases (e.g., 3.0.0 → 4.0.0) **MUST** have at least one beta
- Script blocks major stable releases if no beta exists
- Recommended beta testing period: 7+ days for major, 2+ days for minor

**Beta Maturity Validation:**
- Warning-only (never blocks)
- Checks days since beta published
- Recommends 7-day minimum for major, 2-day for minor

### 6. CI/CD Integration (`.github/workflows/ci-cd.yml`)

**Release Job Flow:**
```
changes → quality → tests → all-tests-pass → validate-release → release
```

**Validate Release Job:**
- Triggered only on `refs/tags/v*` pushes
- Validates CI passed on the tagged commit
- Extracts version from tag
- Detects pre-release (beta) status
- Blocks release if CI failed

**Release Job (`release`):**
- Runs only on tag pushes (`refs/tags/v*`)
- Depends on `validate-release` (blocks if validation fails)
- Uses GitHub Actions trusted publishing for PyPI (no token needed)
- Steps:
  1. Build Python package (`python -m build`)
  2. Check package (`twine check dist/*`)
  3. Publish to PyPI (auto-publish via trusted publisher)
  4. Create GitHub release with:
     - Python dist files (`dist/*`)
     - Legacy scripts (`legacy/todo.ai`, `legacy/todo.bash`)
     - Release notes from `release/RELEASE_NOTES.md`

**Key Safety Features:**
- Release CANNOT proceed unless ALL tests pass
- Tag-triggered releases always run full test suite
- PyPI publishing MUST succeed before GitHub release is created
- Release notes committed to repo (single source of truth)

### 7. AI Summary Integration

**Current Approach:**
- AI agent (Claude) generates 2-3 paragraph summary
- Saved to `release/AI_RELEASE_SUMMARY.md`
- Committed before running `--prepare`
- Script validates summary is recent (committed in last 2 commits)
- Script validates summary is newer than last release tag
- Copied into `release/RELEASE_SUMMARY.md` during prepare
- Included at top of `release/RELEASE_NOTES.md` (above commit list)

**Summary Requirements:**
- Focus on user-facing benefits
- Plain language (avoid jargon)
- Highlight most important changes first
- Optional: include commit links for key changes

### 8. Version History Analysis

**Current State:**
- **Latest stable:** v3.0.2
- **Latest beta:** v4.0.0b2
- **Status:** In v4.0.0 beta cycle

**Version Timeline:**
```
v3.0.0 (stable)
├─ v3.0.0b1 → b18 (18 beta iterations)
├─ Released: v3.0.0
├─ Patches: v3.0.1, v3.0.2
v4.0.0 (beta cycle - CURRENT)
├─ v4.0.0b1, v4.0.0b2
└─ → Next: v4.0.0b3 or v4.0.0 stable
```

**Release Cadence:**
- Beta cycles: 1-18 iterations (v3.0.0 had 18 betas)
- Stable releases: After beta testing period
- Patch releases: As needed for bug fixes

### 9. Release Artifacts

**Generated During Release:**
- `release/RELEASE_NOTES.md` - Full release notes (summary + commits)
- `release/RELEASE_SUMMARY.md` - AI-generated summary (copy of AI_RELEASE_SUMMARY.md)
- `release/RELEASE_LOG.log` - Detailed operation log (newest entries on top)
- `release/.prepare_state` - Prepare phase state (for execute phase)
- `todo.bash` - Bash-converted version of `legacy/todo.ai`

**PyPI Distribution:**
- `dist/*.whl` - Python wheel
- `dist/*.tar.gz` - Source distribution

**GitHub Release Assets:**
- Python distributions (`dist/*`)
- Legacy scripts (`legacy/todo.ai`, `legacy/todo.bash`)

### 10. Error Handling & Rollback

**Abort Mechanism (`--abort`):**
- Detects failed releases automatically
- Deletes tag (local + remote)
- Deletes GitHub release (if created)
- Reverts version files to previous version
- Cleans up release artifacts
- Creates abort commit
- Ready for immediate retry

**Safety Checks:**
- Pre-flight validation before execute
- CI must pass before tag push
- CI must pass before GitHub release
- Tag verification (ensures version files match)
- Prevents duplicate tags

---

## Current Workflow Analysis

### Strengths

1. **Two-Phase Safety:** Prepare → Review → Execute prevents accidents
2. **AI Summary Integration:** Claude generates human-readable summaries
3. **Beta Enforcement:** Major releases require beta testing
4. **Comprehensive Logging:** `RELEASE_LOG.log` tracks all operations
5. **Intelligent Version Analysis:** Automatic bump detection from commits
6. **Backend-Only Detection:** Infrastructure changes → PATCH only
7. **Beta Graduation:** Stable releases cover entire beta cycle
8. **Rollback Support:** `--abort` quickly cleans up failed releases
9. **CI Integration:** Waits for CI before publishing
10. **Version Consistency:** Validates GitHub ↔ file version sync

### Weaknesses

1. **Custom Maintenance:** 2,330-line shell script requires ongoing updates
2. **No Automated PRs:** Manual prepare → execute workflow
3. **Manual CHANGELOG:** No automatic CHANGELOG.md generation
4. **Bespoke Logic:** Version analysis, beta detection all custom
5. **Shell Script Fragility:** Complex shell logic prone to edge cases
6. **No Draft Release:** Must execute immediately after prepare
7. **Linear Integration:** Currently disabled, not fully automated

---

## Release Please Overview

### What is Release Please?

Release Please is a GitHub Action that automates release workflows by:
- Parsing conventional commits
- Generating CHANGELOG.md automatically
- Creating release PRs with version bumps
- Publishing GitHub releases when PR is merged
- Supporting multiple release strategies

### Core Features

1. **Automated Release PRs:**
   - Creates/updates PR with version bump and CHANGELOG
   - PR title: `chore(main): release 4.0.0`
   - Single PR per release (continuously updated)

2. **CHANGELOG Generation:**
   - Follows Keep a Changelog format
   - Categorizes commits by conventional commit type
   - Tracks unreleased changes

3. **Version Bumping:**
   - Automatic based on conventional commits
   - Supports multiple files (`pyproject.toml`, `__init__.py`, etc.)
   - Custom version strings via config

4. **Release Strategies:**
   - `python`: Python package with `pyproject.toml`
   - `simple`: Generic versioning
   - Supports custom strategies

### Conventional Commits

Release Please requires conventional commit format:
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat:` → MINOR bump
- `fix:` → PATCH bump
- `feat!:` or `BREAKING CHANGE:` footer → MAJOR bump
- `docs:`, `chore:`, `refactor:`, etc. → No bump (included in CHANGELOG)

---

## Gap Analysis: Current vs Release Please

| Feature | Current (release.sh) | Release Please | Gap? |
|---------|---------------------|----------------|------|
| **Version Bump** | Automatic (custom logic) | Automatic (conventional commits) | ⚠️ Different logic |
| **Beta Support** | Yes (`--beta` flag) | Yes (prerelease config) | ✅ Compatible |
| **AI Summaries** | Yes (Gemini/Claude) | No (CHANGELOG only) | ❌ **CRITICAL GAP** |
| **CHANGELOG** | Manual (uncommitted) | Automatic (CHANGELOG.md) | ⚠️ Different approach |
| **Release PR** | No (direct to main) | Yes (automated PR) | ⚠️ Workflow change |
| **Two-Phase Safety** | Prepare → Execute | PR review → Merge | ✅ Similar |
| **Backend Detection** | Yes (file analysis) | No | ❌ Missing |
| **Beta Enforcement** | Major requires beta | No | ❌ Missing |
| **Beta Graduation** | Covers full cycle | Incremental | ⚠️ Different |
| **Rollback** | `--abort` command | Delete PR | ⚠️ Different |
| **CI Integration** | Built-in | Via GitHub Actions | ✅ Compatible |
| **Linear Tracking** | Planned (disabled) | No | ❌ Missing |

---

## Critical Gaps

### 1. AI-Generated Summaries

**Current:**
- Claude/Gemini generates 2-3 paragraph summary
- Focuses on user-facing benefits
- Included at top of release notes
- Validated for recency

**Release Please:**
- No built-in AI summary support
- CHANGELOG is auto-generated from commits
- Cannot inject custom content into CHANGELOG header

**Impact:** **HIGH** - AI summaries are a key differentiator for our releases

### 2. Backend-Only Release Detection

**Current:**
- Infrastructure changes (tests, .cursor/, .ai-todo/) → PATCH
- Prevents version inflation for internal improvements

**Release Please:**
- All `feat:` → MINOR (regardless of file changes)
- No file-based analysis

**Impact:** **MEDIUM** - Version numbers may inflate for backend work

### 3. Beta Enforcement for Major Releases

**Current:**
- Major releases MUST have at least one beta
- Script blocks major stable releases without beta
- Maturity validation (recommended testing period)

**Release Please:**
- No beta requirement enforcement
- Pre-release is opt-in via config

**Impact:** **MEDIUM** - Requires manual process to enforce beta policy

### 4. Linear Integration

**Current:**
- `linear-release-workflow.mdc` defines automated workflow
- ai-todo task tracking
- Approval gates via Linear comments
- Status updates at each step

**Release Please:**
- No Linear integration
- No approval gate system

**Impact:** **LOW** - Can be added as separate workflow layer

---

## Migration Challenges

### Challenge 1: AI Summary Injection

**Problem:** Release Please auto-generates CHANGELOG.md. How do we inject AI summaries?

**Options:**
1. **Pre-commit hook:** Inject AI summary into CHANGELOG before Release Please PR is created
2. **Post-generation script:** Modify CHANGELOG.md after Release Please generates it
3. **Custom release-please plugin:** Extend Release Please (requires Node.js)
4. **Separate workflow:** Generate AI summary, create PR comment, let human merge manually
5. **Hybrid approach:** Keep AI summary generation separate, append to GitHub release body

### Challenge 2: Backend-Only Detection

**Problem:** Release Please uses conventional commits only, ignores file changes.

**Options:**
1. **Accept inflation:** Allow `feat:` commits for backend to trigger MINOR
2. **Strict commit discipline:** Use `infra:` for backend, but this requires training
3. **Custom workflow:** Pre-process commits before Release Please runs
4. **Abandon backend detection:** Rely solely on conventional commit types

### Challenge 3: Beta Enforcement

**Problem:** Release Please doesn't enforce beta policy for major releases.

**Options:**
1. **Manual process:** Developer creates beta PR first, then stable
2. **Custom GitHub Action:** Block major release PRs if no beta exists
3. **Branch protection:** Require specific reviewers for major releases
4. **Accept risk:** Rely on team discipline

### Challenge 4: Existing Custom Logic

**Problem:** 2,330 lines of battle-tested shell logic may have edge cases.

**Options:**
1. **Gradual migration:** Keep `release.sh` alongside Release Please
2. **Feature parity testing:** Extensive testing before cutover
3. **Hybrid mode:** Use Release Please for CHANGELOG, keep `release.sh` for execution

---

## Compatibility Assessment

### ✅ Compatible Features

- **Beta releases:** Release Please supports pre-release versions
- **CI/CD integration:** Works with existing GitHub Actions
- **PyPI publishing:** No impact (still uses trusted publisher)
- **Version bumping:** Can update multiple files (`pyproject.toml`, `__init__.py`)
- **Conventional commits:** We already use commit prefixes

### ⚠️ Requires Adaptation

- **AI summaries:** Need custom injection mechanism
- **Commit analysis:** More strict than current logic
- **Release workflow:** PR-based instead of direct to main
- **CHANGELOG format:** Keep a Changelog vs our current approach

### ❌ Incompatible Features

- **Backend-only detection:** Release Please doesn't analyze files
- **Beta enforcement:** No built-in major → beta requirement
- **Two-phase with state:** Release Please uses PR draft instead
- **Custom abort logic:** Different cleanup approach

---

## Conventional Commits Audit

Let me analyze our recent commits to assess conventional commit compliance:

**Recent Commits (v4.0.0b2..HEAD):**
- ✅ `docs:` - Conventional
- ✅ `chore:` - Conventional
- ✅ `feat:` - Conventional
- ✅ `fix:` - Conventional
- ✅ `refactor:` - Conventional
- ✅ `test:` - Conventional

**Compliance:** **HIGH** (90%+) - We already follow conventional commits closely

**Non-conventional examples:**
- `Merge pull request #XX` - Merge commits (ignored by most tools)

---

## Release Please Configuration

### Basic Setup

**`.github/workflows/release-please.yml`:**
```yaml
name: Release Please
on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        with:
          release-type: python
```

**`release-please-config.json`:**
```json
{
  "packages": {
    ".": {
      "release-type": "python",
      "package-name": "todo-ai",
      "include-component-in-tag": false,
      "bump-minor-pre-major": true,
      "bump-patch-for-minor-pre-major": true,
      "extra-files": [
        {
          "type": "python",
          "path": "ai_todo/__init__.py",
          "glob": false
        }
      ]
    }
  }
}
```

---

## Migration Paths

### Option A: Full Migration (Replace release.sh)

**Approach:**
- Remove `release.sh` entirely
- Use Release Please for all release automation
- Implement custom AI summary injection
- Adapt workflow to PR-based releases

**Pros:**
- Industry-standard tool (maintained by Google)
- Automatic CHANGELOG generation
- Less custom code to maintain
- PR-based workflow (more visibility)

**Cons:**
- **CRITICAL:** AI summary injection is complex
- Lose backend-only detection
- Lose beta enforcement
- Lose two-phase prepare/execute safety
- Significant workflow change

### Option B: Hybrid Approach (Keep release.sh, Add Release Please)

**Approach:**
- Use Release Please for CHANGELOG generation only
- Keep `release.sh` for execution
- Release Please PR → triggers `release.sh --prepare --beta`
- Merge PR after review

**Pros:**
- Preserve existing safety mechanisms
- Get automatic CHANGELOG
- Gradual migration path
- Keep AI summary integration

**Cons:**
- Maintain both systems
- More complex workflow
- Potential for confusion

### Option C: Enhanced release.sh (No Release Please)

**Approach:**
- Keep current `release.sh` workflow
- Add automatic CHANGELOG.md generation to `release.sh`
- Implement PR-based workflow manually
- Enhance Linear integration

**Pros:**
- No migration risk
- Keep all custom logic
- Full control over workflow

**Cons:**
- Continue maintaining custom solution
- Miss out on Release Please ecosystem

---

## Recommendations

### Recommended Path: Option A with Custom Enhancements

**Phase 1: Foundation**
1. Set up Release Please with basic Python configuration
2. Test CHANGELOG generation against recent releases
3. Verify version bumping works correctly
4. Validate pre-release (beta) support

**Phase 2: AI Summary Integration**
1. Create custom GitHub Action: `generate-ai-summary`
   - Runs before Release Please
   - Generates summary using Gemini API
   - Injects into CHANGELOG.md header
   - Commits update to release PR
2. Configure GitHub secret for Gemini API key
3. Test end-to-end: commit → AI summary → release PR

**Phase 3: Policy Enforcement**
1. Create custom GitHub Action: `enforce-beta-policy`
   - Blocks major release PRs if no beta tag exists
   - Checks PR title for version
   - Queries GitHub releases for betas
2. Add to Release Please PR checks

**Phase 4: Migration**
1. Archive `release.sh` (keep for reference)
2. Update Cursor rules for new workflow
3. Document new release process
4. Create migration guide for contributors

### Open Questions

1. **Gemini API Access:**
   - Do we have Gemini API credentials for GitHub Actions?
   - Cost implications for API usage?
   - Fallback if API fails?

2. **Backend-Only Detection:**
   - Accept version inflation for backend work?
   - Or enforce strict `infra:` prefix discipline?

3. **Beta Enforcement:**
   - Hard block (prevent PR merge)?
   - Or soft warning (require override approval)?

4. **CHANGELOG Format:**
   - Keep a Changelog format (Release Please default)
   - Or custom format?

5. **Linear Integration:**
   - Keep automated workflow?
   - Or manual Linear updates?

---

## Success Criteria

1. ✅ Release Please generates accurate CHANGELOG.md
2. ✅ Version bumping works for all files (`pyproject.toml`, `__init__.py`)
3. ✅ Beta releases work correctly (prerelease flag)
4. ✅ AI summaries appear in release notes
5. ✅ Major releases require beta (enforced)
6. ✅ CI/CD integration works (PyPI → GitHub release)
7. ✅ Existing release quality maintained or improved
8. ✅ Migration path documented for contributors

---

## Next Steps

1. **Review this analysis** with stakeholders
2. **Answer open questions** about Gemini API, enforcement policies
3. **Create design document** with detailed implementation plan
4. **Prototype AI summary injection** to validate feasibility
5. **Test Release Please** on a branch to verify behavior

---

**Status:** Analysis complete, ready for design phase
**Author:** AI Assistant
**Date:** 2026-01-30
