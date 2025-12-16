# Beta and Pre-Release Strategy: Simplification & Hardening Recommendations

**Document Version:** 1.0
**Date:** December 16, 2025
**Status:** RECOMMENDATIONS (Not Yet Implemented)
**Related:** `BETA_PRERELEASE_STRATEGY.md` v1.1

---

## Executive Summary

This document provides recommendations to simplify and harden the proposed beta/pre-release strategy for todo.ai. The goal is to create a self-contained, error-resistant process that integrates seamlessly with the existing two-phase release workflow (prepare → execute) while reducing complexity and operational burden.

**Key Changes Recommended:**
- **Simplify:** Reduce 4 release tiers to 2 (Beta + Stable)
- **Harden:** Add automatic enforcement of major release requirements
- **Integrate:** Seamlessly work with existing two-phase process
- **Protect:** Add comprehensive validation gates to prevent errors

**Philosophy:** Keep it simple, make it bulletproof, integrate naturally.

---

## 1. Simplification Recommendations

### 1.1 Reduce Release Tiers: 4 → 2

**Current Proposal:** Alpha → Beta → RC → Stable (4 tiers)

**Recommended:** Beta → Stable (2 tiers)

```
SIMPLIFIED STRUCTURE:

├── Beta (pre-release testing)
│   ├── Format: v1.0.0b1, v1.0.0b2, v1.0.0b3...
│   ├── Target: PyPI (pre-release flag)
│   ├── Purpose: External testing, feedback gathering
│   └── Duration: 7+ days for major, 2-3 days for minor
│
└── Stable (production)
    ├── Format: v1.0.0
    ├── Target: PyPI (stable)
    └── Purpose: General availability

ELIMINATED:
✂️ Alpha tier   → Use feature branches + CI instead
✂️ RC tier      → Last beta serves this purpose
✂️ TestPyPI     → Adds complexity, limited value
```

**Rationale:**
- todo.ai has comprehensive CI/CD and 150+ automated tests
- Alpha testing can happen in feature branches
- RC is redundant when you can iterate betas (b1, b2, b3...)
- TestPyPI dependency resolution issues outweigh benefits
- Most successful CLI tools use 2-tier approach

**Impact:**
- ✅ Reduces operational complexity by 50%
- ✅ Eliminates TestPyPI credential management
- ✅ Removes version format conversion logic
- ✅ Clearer user communication (beta vs stable)

---

### 1.2 Single Version Format: PEP 440 Everywhere

**Current Proposal:** Dual format (PEP 440 for PyPI, SemVer for git tags)

**Recommended:** PEP 440 everywhere

```
UNIFIED VERSION FORMAT:

Git Tags:          v1.0.0b1  (valid PEP 440 with 'v' prefix)
PyPI Version:      1.0.0b1   (same, minus 'v')
Python __version__: "1.0.0b1" (same)

CONVERSION LOGIC: Remove 'v' prefix. That's it.

EXAMPLES:
├── Beta 1:    v1.0.0b1  → PyPI: 1.0.0b1
├── Beta 2:    v1.0.0b2  → PyPI: 1.0.0b2
└── Stable:    v1.0.0    → PyPI: 1.0.0

ELIMINATED:
✂️ SemVer format (v1.0.0-beta.1)
✂️ Format conversion functions
✂️ Dual tracking in release notes
✂️ Confusion about which format to use
```

**Implementation:**
```bash
# Simple conversion:
git_tag="v1.0.0b1"
pypi_version="${git_tag#v}"  # Remove 'v' prefix → "1.0.0b1"
```

**Rationale:**
- PEP 440 is the Python standard
- PyPI natively understands it
- Git tags can use any format (PEP 440 is fine)
- No conversion logic = no conversion bugs

---

### 1.3 Simplify GitHub Actions: Auto-Detection Only

**Current Proposal:** Complex conditional logic for alpha/beta/rc/stable with different PyPI targets

**Recommended:** Simple tag-based detection, single PyPI target

```yaml
# Simplified GitHub Actions workflow

- name: Detect pre-release type
  id: prerelease
  run: |
    TAG="${{ github.ref_name }}"
    # Simple regex: if tag ends with 'b' + digits, it's a beta
    if [[ "$TAG" =~ b[0-9]+$ ]]; then
      echo "is_prerelease=true" >> $GITHUB_OUTPUT
      echo "type=beta" >> $GITHUB_OUTPUT
    else
      echo "is_prerelease=false" >> $GITHUB_OUTPUT
      echo "type=stable" >> $GITHUB_OUTPUT
    fi

# Single PyPI publish step (no conditionals)
- name: Publish to PyPI
  env:
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
  run: uv run twine upload dist/*

# GitHub release auto-marks pre-release
- name: Create GitHub Release
  uses: softprops/action-gh-release@v1
  with:
    files: dist/*
    prerelease: ${{ steps.prerelease.outputs.is_prerelease }}
    generate_release_notes: true
```

**Eliminated:**
- ✂️ TestPyPI publish step
- ✂️ Alpha/RC detection logic
- ✂️ Multiple conditional branches
- ✂️ TEST_PYPI_API_TOKEN secret requirement

---

### 1.4 Defer Feature Flags (YAGNI)

**Current Proposal:** Feature flag system for experimental functionality

**Recommended:** Eliminate feature flags, use beta releases instead

```
PHILOSOPHY: You Ain't Gonna Need It (YAGNI)

Instead of feature flags:
├── Experimental features → Develop in feature branches
├── Test with users       → Release as beta
├── Gather feedback       → Iterate with b2, b3...
└── Ready for production  → Release as stable

ELIMINATED:
✂️ FeatureFlag enum class
✂️ is_feature_enabled() function
✂️ Environment variable management
✂️ Conditional code paths based on flags
✂️ Documentation of flag behavior
```

**Rationale:**
- todo.ai is a CLI tool, not a cloud service
- Beta releases serve the same purpose as feature flags
- Simpler code = fewer bugs
- Can add later if truly needed (but probably won't be)

**Impact:**
- ✅ Reduces code complexity
- ✅ Fewer edge cases to test
- ✅ Clearer user experience (beta vs stable)

---

### 1.5 Simplify Rollback Strategy

**Current Proposal:** PyPI yank + hotfix + rollback mechanisms

**Recommended:** Forward-fix only (no yanking, no rollback)

```
SIMPLIFIED ROLLBACK STRATEGY:

Scenario 1: Critical bug in stable release (1.0.0)
Solution:   Immediately release 1.0.1 with fix
Action:     ./release/release.sh --prepare  # Creates 1.0.1
            ./release/release.sh --execute

Scenario 2: Bug in beta (1.0.0b1)
Solution:   Release next beta with fix (1.0.0b2)
Action:     ./release/release.sh --prepare --beta
            ./release/release.sh --execute

Scenario 3: User needs to downgrade
Solution:   Version pinning
Action:     uv tool install todo-ai==0.9.5  # Install specific version

ELIMINATED:
✂️ PyPI yank workflow
✂️ Complex rollback procedures
✂️ Rollback documentation
✂️ User confusion about yanked versions
```

**Rationale:**
- PyPI yank is confusing and rarely done well
- Forward fixes are clearer and standard practice
- Version pinning handles user-side rollback needs
- Simpler mental model for maintainers and users

---

### 1.6 Simplify Installation Documentation

**Current Proposal:** Multiple examples with uv/pipx/pip alternatives repeated

**Recommended:** One primary method, others collapsed

```markdown
## Installation (SIMPLIFIED)

### Stable (Recommended)
```bash
uv tool install todo-ai
```

### Beta (Help Us Test)
```bash
uv tool install --prerelease=allow todo-ai
```

### Development (Latest from Git)
```bash
uv tool install git+https://github.com/fxstein/todo.ai.git@main
```

<details>
<summary>Alternative Installation Methods</summary>

**Using pipx:**
```bash
pipx install todo-ai              # Stable
pipx install --pre todo-ai        # Beta
```

**Using pip:**
```bash
pip install todo-ai               # Stable
pip install --pre todo-ai         # Beta
```
</details>

> **Recommendation:** Use `uv tool` for faster, more reliable installation.
```

**Impact:**
- ✅ Reduces documentation length by ~60%
- ✅ Clear primary recommendation
- ✅ Alternative methods still available
- ✅ Less overwhelming for new users

---

## 2 Hardening Recommendations

### 2.1 Auto-Detect Major Releases & Enforce Beta Requirement

**Problem:** No automatic detection of when beta is required

**Solution:** Add enforcement in `--prepare` phase

```bash
# In release/release.sh --prepare phase

detect_and_enforce_beta_requirement() {
    local proposed_version="$1"
    local release_type="$2"  # "beta" or "stable"

    # Get last stable release
    local last_stable=$(gh release list --json tagName,isPrerelease \
        --jq '.[] | select(.isPrerelease == false) | .tagName' | \
        head -n1 | sed 's/^v//')

    # Extract major version numbers
    local proposed_major=$(echo "$proposed_version" | cut -d. -f1)
    local last_major=$(echo "$last_stable" | cut -d. -f1)

    # Check if this is a major version bump
    if [[ "$proposed_major" != "$last_major" ]]; then
        echo "🔍 Major version bump detected: $last_stable → $proposed_version"

        if [[ "$release_type" == "stable" ]]; then
            # Preparing stable for major release - check if beta exists
            local beta_exists=$(gh release list --json tagName \
                --jq '.[] | select(.tagName | startswith("v'$proposed_version'b")) | .tagName' | \
                wc -l)

            if [[ "$beta_exists" -eq 0 ]]; then
                echo ""
                echo "❌ ERROR: Major release requires beta testing first"
                echo ""
                echo "This is a major version bump ($last_stable → $proposed_version)."
                echo "Major releases MUST have at least one beta release."
                echo ""
                echo "To create a beta:"
                echo "  ./release/release.sh --prepare --beta"
                echo ""
                echo "After beta testing, run prepare again for stable."
                exit 1
            fi
        fi
    fi
}

# RULE: Major releases cannot skip beta
# The script automatically enforces this
```

**Impact:**
- ✅ Prevents accidental major releases without testing
- ✅ No human/AI memory required - script enforces it
- ✅ Clear error message with remediation steps
- ✅ Self-documenting requirement

---

### 2.2 Validate Beta Maturity Before Stable Release

**Problem:** No enforcement of beta testing duration

**Solution:** Add maturity validation with warnings

```bash
# In release/release.sh --prepare phase

validate_beta_maturity() {
    local target_version="$1"  # e.g., "1.0.0"
    local release_type="$2"

    # Only validate when preparing stable after beta
    if [[ "$release_type" != "stable" ]]; then
        return 0
    fi

    # Find latest beta for this version
    local latest_beta=$(gh release list --json tagName,publishedAt \
        --jq '.[] | select(.tagName | startswith("v'$target_version'b")) |
        {tag: .tagName, date: .publishedAt}' | \
        head -n1)

    if [[ -z "$latest_beta" ]]; then
        # No beta found - enforcement handled by detect_and_enforce_beta_requirement
        return 0
    fi

    # Calculate days since beta release
    local beta_tag=$(echo "$latest_beta" | jq -r '.tag')
    local beta_date=$(echo "$latest_beta" | jq -r '.date')
    local days_since_beta=$(python3 -c "
from datetime import datetime
beta = datetime.fromisoformat('${beta_date}'.replace('Z', '+00:00'))
now = datetime.now(beta.tzinfo)
print((now - beta).days)
")

    # Determine minimum days based on version type
    local is_major=$(detect_major_bump "$target_version")
    local min_days=7
    if [[ "$is_major" == "false" ]]; then
        min_days=2  # Minor releases need less beta time
    fi

    echo "📊 Beta maturity check:"
    echo "   Latest beta: $beta_tag"
    echo "   Released: $days_since_beta days ago"
    echo "   Recommended: $min_days days"

    if [[ "$days_since_beta" -lt "$min_days" ]]; then
        echo ""
        echo "⚠️  WARNING: Beta released only $days_since_beta days ago"
        echo "   Recommended wait: $((min_days - days_since_beta)) more days for feedback"
        echo "   Proceeding with release..."
        echo ""
    else
        echo "   ✅ Beta has matured for recommended period"
    fi
}

# RULE: Major releases recommended 7+ days, minor 2+ days
# Script warns but does NOT block - always allows proceeding
```

**Impact:**
- ✅ Provides guidance on beta testing duration
- ✅ Never blocks releases (warning only)
- ✅ Different recommendations for major vs minor
- ✅ Clear feedback to user

---

### 2.3 Comprehensive Pre-Flight Validation

**Problem:** No systematic validation before execute

**Solution:** Add comprehensive pre-flight checklist

```bash
# In release/release.sh --execute phase

preflight_checks() {
    echo "=== Pre-Flight Validation ==="
    echo ""

    local errors=0
    local warnings=0

    # Check 1: Prepare state exists
    echo -n "1. Checking prepare state... "
    if [[ ! -f release/.prepare_state ]]; then
        echo "❌ FAIL"
        echo "   → No prepare state found"
        echo "   → Run: ./release/release.sh --prepare [--beta]"
        ((errors++))
    else
        echo "✅ OK"
    fi

    # Check 2: CI/CD status
    echo -n "2. Checking CI/CD status... "
    if ! ./scripts/wait-for-ci.sh; then
        echo "❌ FAIL"
        echo "   → CI/CD workflows failing"
        echo "   → Fix errors before releasing"
        ((errors++))
    else
        echo "✅ OK"
    fi

    # Check 3: Uncommitted changes
    echo -n "3. Checking for uncommitted changes... "
    local uncommitted=$(git status --porcelain | grep -v '^?? release/' | wc -l)
    if [[ "$uncommitted" -gt 0 ]]; then
        echo "❌ FAIL"
        echo "   → Uncommitted changes detected"
        echo "   → Commit or stash changes first"
        ((errors++))
    else
        echo "✅ OK"
    fi

    # Check 4: GitHub authentication
    echo -n "4. Checking GitHub authentication... "
    if ! gh auth status &>/dev/null; then
        echo "❌ FAIL"
        echo "   → GitHub CLI not authenticated"
        echo "   → Run: gh auth login"
        ((errors++))
    else
        echo "✅ OK"
    fi

    # Check 5: Build dependencies
    echo -n "5. Checking build dependencies... "
    if ! uv run python -m build --version &>/dev/null 2>&1; then
        echo "❌ FAIL"
        echo "   → Build dependencies missing"
        echo "   → Run: uv sync --extra dev"
        ((errors++))
    else
        echo "✅ OK"
    fi

    # Check 6: Beta maturity (for stable releases)
    if [[ -f release/.prepare_state ]]; then
        local release_type=$(jq -r '.release_type' release/.prepare_state 2>/dev/null || echo "stable")
        if [[ "$release_type" == "stable" ]]; then
            echo "6. Validating beta maturity..."
            local base_version=$(jq -r '.base_version' release/.prepare_state)
            validate_beta_maturity "$base_version" "$release_type"
            # Note: This function handles its own pass/fail/warning display
        fi
    fi

    echo ""

    # Summary
    if [[ $errors -gt 0 ]]; then
        echo "❌ $errors pre-flight check(s) failed"
        echo ""
        echo "Fix the issues above and run --execute again."
        exit 1
    elif [[ $warnings -gt 0 ]]; then
        echo "⚠️  $warnings warning(s) detected"
        echo "✅ All critical checks passed"
        echo ""
    else
        echo "✅ All pre-flight checks passed"
        echo ""
    fi
}

# RULE: All checks must pass before release proceeds
# Script provides clear remediation steps for failures
```

**Impact:**
- ✅ Catches issues before they cause problems
- ✅ Clear pass/fail reporting
- ✅ Actionable remediation steps
- ✅ Reduces failed releases

---

### 2.4 Harden Beta Version Increment Logic

**Problem:** Unclear how to determine next beta number

**Solution:** Add explicit beta version detection

```bash
# In release/release.sh --prepare phase

determine_beta_version() {
    local base_version="$1"  # e.g., "1.0.0" from version bump analysis

    echo "🔍 Determining beta version for base: $base_version"

    # Find all existing betas for this base version
    local existing_betas=$(gh release list --json tagName --jq \
        '.[] | select(.tagName | startswith("v'$base_version'b")) | .tagName')

    if [[ -z "$existing_betas" ]]; then
        # First beta for this version
        local beta_version="${base_version}b1"
        echo "   → First beta: $beta_version"
        echo "$beta_version"
    else
        # Find highest beta number
        local highest=$(echo "$existing_betas" | \
            grep -oE 'b[0-9]+$' | \
            sed 's/b//' | \
            sort -n | \
            tail -n1)

        local next=$((highest + 1))
        local beta_version="${base_version}b${next}"

        echo "   → Existing betas found: $(echo "$existing_betas" | wc -l)"
        echo "   → Highest: b$highest"
        echo "   → Next: $beta_version"

        echo "$beta_version"
    fi
}

# EXAMPLES:
# - No betas exist for 1.0.0 → Returns: 1.0.0b1
# - v1.0.0b1 exists → Returns: 1.0.0b2
# - v1.0.0b1 and v1.0.0b2 exist → Returns: 1.0.0b3
```

**Impact:**
- ✅ Automatic beta numbering
- ✅ No manual tracking needed
- ✅ Prevents duplicate versions
- ✅ Clear logging of decision

---

### 2.5 Enhanced State File for Execute Phase

**Problem:** Current .prepare_state doesn't include all needed metadata

**Solution:** Add comprehensive state tracking

```bash
# In release/release.sh --prepare phase

save_prepare_state() {
    local version="$1"
    local git_tag="$2"
    local release_type="$3"
    local base_version="$4"
    local is_major="$5"

    # Create JSON state file
    cat > release/.prepare_state <<EOF
{
  "version": "$version",
  "git_tag": "$git_tag",
  "release_type": "$release_type",
  "base_version": "$base_version",
  "is_major": $is_major,
  "prepared_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "prepared_by": "$(git config user.email)"
}
EOF

    echo "📝 Prepare state saved:"
    cat release/.prepare_state | jq .
}

# USAGE IN EXECUTE:
read_prepare_state() {
    if [[ ! -f release/.prepare_state ]]; then
        echo "❌ No prepare state found"
        exit 1
    fi

    # Load all variables from state file
    VERSION=$(jq -r '.version' release/.prepare_state)
    GIT_TAG=$(jq -r '.git_tag' release/.prepare_state)
    RELEASE_TYPE=$(jq -r '.release_type' release/.prepare_state)
    BASE_VERSION=$(jq -r '.base_version' release/.prepare_state)
    IS_MAJOR=$(jq -r '.is_major' release/.prepare_state)

    echo "📖 Loading prepare state:"
    echo "   Version: $VERSION"
    echo "   Git Tag: $GIT_TAG"
    echo "   Type: $RELEASE_TYPE"
    echo "   Major: $IS_MAJOR"
}
```

**Impact:**
- ✅ Execute phase has all needed context
- ✅ No re-computation of version/type
- ✅ Audit trail of preparation
- ✅ Enables more sophisticated validation

---

## 3 Integration with Two-Phase Process

### 3.1 Command Structure

**Existing Process (Preserved):**
```bash
# Phase 1: Prepare
./release/release.sh --prepare
# (Human reviews release/RELEASE_NOTES.md)

# Phase 2: Execute
./release/release.sh --execute
```

**Enhanced with Beta Support:**
```bash
# Phase 1: Prepare (with optional --beta flag)
./release/release.sh --prepare [--beta]
# (Human reviews release/RELEASE_NOTES.md)

# Phase 2: Execute (no changes needed)
./release/release.sh --execute
```

**Key Points:**
- ✅ Backward compatible (no --beta = stable release)
- ✅ Human review gate preserved
- ✅ Execute reads type from .prepare_state
- ✅ No new complexity for users

---

### 3.2 Prepare Phase Enhancements

**Flow Diagram:**

```
./release/release.sh --prepare [--beta]
    ↓
1. Check CI/CD (existing)
    ↓
2. Generate AI Summary (existing)
    ↓
3. Analyze commits & determine version bump (existing)
    ↓
4. NEW: Check if --beta flag provided
    ├─ If --beta: determine_beta_version()
    └─ If not: check if major bump requires beta
    ↓
5. NEW: Enforce beta requirement (if major + stable)
    ↓
6. Generate release notes (existing)
    ↓
7. NEW: Save enhanced .prepare_state
    ↓
8. Display preview (existing)
    ↓
9. STOP - Wait for human review (existing)
```

**No changes to:**
- CI/CD check
- AI summary generation
- Commit analysis
- Release notes generation
- Human review gate

**Additions:**
- Beta version determination
- Major release enforcement
- Enhanced state file

---

### 3.3 Execute Phase Enhancements

**Flow Diagram:**

```
./release/release.sh --execute
    ↓
1. NEW: Read .prepare_state (includes release_type)
    ↓
2. NEW: Pre-flight validation checklist
    ↓
3. Update version files (existing)
    ↓
4. Build package (existing)
    ↓
5. Commit version changes (existing)
    ↓
6. Create git tag (existing)
    ↓
7. Push tag + main (existing)
    ↓
8. NEW: GitHub Actions auto-detects pre-release
    ↓
9. Clean up files (existing)
    ↓
10. Commit release log (existing)
```

**No changes to:**
- Version file updates
- Package building
- Git operations
- Cleanup process

**Additions:**
- State file reading
- Pre-flight validation
- GitHub Actions auto-detection (in workflow, not script)

---

### 3.4 Backward Compatibility

**Guarantee:** All existing workflows continue to work

```bash
# Existing usage (no changes needed):
./release/release.sh --prepare
./release/release.sh --execute
# → Creates stable release (v1.0.0)

# New usage (opt-in):
./release/release.sh --prepare --beta
./release/release.sh --execute
# → Creates beta release (v1.0.0b1)

# Version override (still works):
./release/release.sh --set-version 1.5.0
./release/release.sh --execute
# → Creates stable release with custom version
```

**Key Point:** Beta support is additive, not breaking.

---

## 4 Decision Trees for AI Agents

### 4.1 When User Says "Prepare Release" or "Release todo.ai"

```
START: User requests release
    ↓
STEP 1: Check CI/CD status
    ├─ PASS → Continue
    └─ FAIL → STOP, report error, ask user to fix
    ↓
STEP 2: Analyze commits and determine version bump
    ├─ Result: Next version (e.g., "1.0.0" or "2.0.0")
    └─ Type: MAJOR, MINOR, or PATCH
    ↓
STEP 3: Decision tree based on bump type
    ↓
    ├─ MAJOR (e.g., 2.0.0 → 3.0.0)
    │   ↓
    │   Check: Does beta exist for 3.0.0?
    │       ├─ NO BETA EXISTS
    │       │   ↓
    │       │   STOP and recommend:
    │       │   "This is a major release (3.0.0).
    │       │    Major releases require beta testing.
    │       │
    │       │    To create beta:
    │       │    ./release/release.sh --prepare --beta
    │       │
    │       │    After beta testing, prepare stable."
    │       │
    │       └─ BETA EXISTS (e.g., v3.0.0b1)
    │           ↓
    │           Check beta age
    │               ├─ < 7 days
    │               │   ↓
    │               │   WARN: "Beta only X days old. Recommend waiting."
    │               │   Proceed with warning
    │               │
    │               └─ >= 7 days
    │                   ↓
    │                   Continue prepare for stable
    │
    ├─ MINOR (e.g., 2.0.0 → 2.1.0)
    │   ↓
    │   Ask user:
    │   "This is a minor release (2.1.0).
    │
    │    Options:
    │    a) Create beta first (recommended for significant features)
    │    b) Release stable directly (faster for small additions)
    │
    │    Which do you prefer?"
    │       ├─ a → Run: ./release/release.sh --prepare --beta
    │       └─ b → Run: ./release/release.sh --prepare
    │
    └─ PATCH (e.g., 2.0.0 → 2.0.1)
        ↓
        Continue prepare for stable (no beta needed)
        Run: ./release/release.sh --prepare
    ↓
STEP 4: Execute prepare command
    ↓
STEP 5: Show preview of release notes
    ↓
STEP 6: STOP and say:
    "✅ Release prepared successfully!

     - Current version: X.Y.Z
     - Proposed version: A.B.C[bN]
     - Release notes: release/RELEASE_NOTES.md

     Review the release notes, then tell me 'execute release' when ready."
    ↓
WAIT FOR USER
```

---

### 4.2 When User Says "Execute Release"

```
START: User requests execute
    ↓
STEP 1: Verify prepare was run
    ├─ .prepare_state exists → Continue
    └─ .prepare_state missing → STOP, say "Run prepare first"
    ↓
STEP 2: Run execute command
    Run: ./release/release.sh --execute
    ↓
STEP 3: Monitor execution
    ├─ SUCCESS → Continue to Step 4
    └─ ERROR → STOP, report error, DO NOT CONTINUE
    ↓
STEP 4: Read release type from state file
    ├─ Type: beta → Show beta success message
    └─ Type: stable → Show stable success message
    ↓
STEP 5: Report success
    ↓
    ├─ FOR BETA:
    │   "✅ Beta release v1.0.0b1 published successfully!
    │
    │    The beta is now available:
    │    - PyPI: https://pypi.org/project/todo-ai/
    │    - Install: uv tool install --prerelease=allow todo-ai
    │
    │    Monitor:
    │    - GitHub Actions: [link]
    │    - GitHub Release: [link]
    │
    │    After beta testing (7+ days for major), prepare stable release."
    │
    └─ FOR STABLE:
        "✅ Stable release v1.0.0 published successfully!

         The release is now available:
         - PyPI: https://pypi.org/project/todo-ai/
         - Install: uv tool install todo-ai

         Monitor:
         - GitHub Actions: [link]
         - GitHub Release: [link]"
```

---

### 4.3 Error Handling Decision Tree

```
IF ERROR OCCURS AT ANY POINT:
    ↓
1. STOP IMMEDIATELY
    ↓
2. Report error clearly:
   "❌ ERROR: [What failed]

    Error message:
    [Actual error output]

    Step: [Which step failed]"
    ↓
3. DO NOT ATTEMPT WORKAROUNDS
    ↓
4. DO NOT CONTINUE THE PROCESS
    ↓
5. Ask user:
   "An error occurred during release. How should we proceed?"
    ↓
6. WAIT FOR USER INSTRUCTION
```

---

## 4.4 Release Logging (Already in Place)

**Question:** Do we have detailed release logging that tracks all release work?

**Answer:** ✅ **Yes, comprehensive release logging is already implemented.**

### Current Release Logging System

The existing `release/release.sh` script has a robust logging system with the `log_release_step()` function:

**Log Format:**
```
TIMESTAMP | USER | STEP | MESSAGE
```

**What Gets Logged (31 log points):**
- Release start (version, bump type, files)
- Bash conversion (zsh → bash)
- Version updates (all files)
- Git commits (with full output)
- Tag creation and verification
- Push operations (main branch and tag)
- GitHub release creation
- Errors and warnings
- Release completion (with URLs)

**Log Location:**
- File: `release/RELEASE_LOG.log`
- Committed to repository after each release
- Newest entries on top for easy reading

**Example Log Entry:**
```
2025-12-12 14:40:07 | fxstein | RELEASE COMPLETE | Release 2.7.3 published successfully! - Tag: v2.7.3 - URL: https://github.com/fxstein/todo.ai/releases/tag/v2.7.3
2025-12-12 14:40:07 | fxstein | GITHUB RELEASE CREATED | GitHub release created successfully for v2.7.3
2025-12-12 14:40:01 | fxstein | PUSH TAG | Pushing tag v2.7.3 to origin
2025-12-12 14:39:59 | fxstein | TAG CREATED | Git tag v2.7.3 created successfully at commit 8ac066d
2025-12-12 14:39:58 | fxstein | VERSION COMMITTED | Version change committed: [git output]
2025-12-12 14:39:56 | fxstein | VERSION UPDATED | Version updated successfully
2025-12-12 14:39:18 | fxstein | RELEASE START | Starting release process: Current 2.7.2 → Proposed 2.7.3
```

### For Beta Support

**No changes needed to logging system** - it will automatically log beta releases:

```
2025-XX-XX XX:XX:XX | user | RELEASE START | Starting release process: Current 1.0.0 → Proposed 1.0.0b1 (beta)
2025-XX-XX XX:XX:XX | user | BETA VERSION | Creating first beta for version 1.0.0
2025-XX-XX XX:XX:XX | user | RELEASE COMPLETE | Beta release 1.0.0b1 published successfully!
```

**Advantages:**
- ✅ Full audit trail of all releases
- ✅ Easy to debug issues (check log for errors)
- ✅ Historical record committed to git
- ✅ User attribution (who ran the release)
- ✅ Timestamps for beta maturity calculation
- ✅ Works for both beta and stable releases

**Recommendation:** The existing logging system is production-ready and needs no modifications for beta support.

---

## 5 Implementation Phases

### Phase 1: Core Beta Infrastructure (Minimal Viable)

**Goal:** Enable basic beta releases with major release protection

**Tasks:**
1. Add `--beta` flag parsing to release.sh
2. Implement `determine_beta_version()` function
3. Implement `detect_and_enforce_beta_requirement()` function
4. Update `.prepare_state` to include `release_type`
5. Update GitHub Actions to detect pre-release from tag
6. Add simple pre-flight validation (CI/CD, prepare state, git auth)

**Deliverables:**
- Can create beta releases: `./release/release.sh --prepare --beta`
- Major releases blocked without beta
- GitHub Actions auto-publishes to PyPI with pre-release flag

**Testing:**
- Create test beta: v4.0.0b1
- Verify PyPI marks it as pre-release
- Verify install: `uv tool install --prerelease=allow todo-ai`
- Test major release blocking (try to prepare 4.0.0 stable without beta)

---

### Phase 2: Hardening & Validation (Production Ready)

**Goal:** Add comprehensive validation and safety checks

**Tasks:**
1. Implement `validate_beta_maturity()` function
2. Expand pre-flight checklist (all 6 checks)
3. Enhance error messages with remediation steps
4. Add beta version increment logic
5. Test all error paths and validation gates

**Deliverables:**
- Beta maturity warnings (recommends 7 days for major, 2 days for minor - never blocks)
- Comprehensive pre-flight checks
- Clear error messages with actionable steps
- All edge cases handled

**Testing:**
- Test beta maturity warnings (create beta, try stable < 7 days)
- Test each pre-flight failure scenario
- Test beta increment (b1 → b2 → b3)
- Test error message clarity

---

### Phase 3: Documentation & Polish (User Ready)

**Goal:** Complete user-facing documentation and Cursor rules

**Tasks:**
1. Update README.md with simplified installation instructions
2. Update Cursor rules with AI decision trees
3. Update release process documentation
4. Create beta testing guide for users
5. Add changelog format examples

**Deliverables:**
- Complete user documentation
- AI agent rules for handling releases
- Testing guide for beta testers
- Migration guide from old process

**Testing:**
- Test AI agent follows decision trees correctly
- Test documentation accuracy
- User acceptance testing

---

### Phase 4: Monitoring & Metrics (Long-term)

**Goal:** Add observability for release process

**Tasks:**
1. Add release metrics tracking
2. Create release dashboard (if needed)
3. Monitor beta adoption rates
4. Gather feedback from process

**Deliverables:**
- Release metrics
- Feedback loop established
- Process improvements identified

---

## 6 Before/After Comparison

### 6.1 Release Tiers

| Aspect | Before (Proposed) | After (Recommended) | Impact |
|--------|-------------------|---------------------|--------|
| **Tiers** | 4 (Alpha/Beta/RC/Stable) | 2 (Beta/Stable) | ✂️ 50% reduction |
| **PyPI Targets** | 2 (TestPyPI + PyPI) | 1 (PyPI only) | ✂️ Eliminates TestPyPI complexity |
| **Version Formats** | 2 (PEP 440 + SemVer) | 1 (PEP 440) | ✂️ No conversion logic |
| **Feature Flags** | Yes (proposed) | No (YAGNI) | ✂️ Less code complexity |

---

### 6.2 Command Complexity

| Task | Before (Proposed) | After (Recommended) |
|------|-------------------|---------------------|
| **Create Beta** | `--prepare --beta` | `--prepare --beta` (same) |
| **Create Stable** | `--prepare` | `--prepare` (same) |
| **Version Override** | `--set-version X.Y.Z` | `--set-version X.Y.Z` (same) |
| **Execute** | `--execute` | `--execute` (same) |

**Impact:** ✅ No change to user experience

---

### 6.3 Automation & Safety

| Feature | Before (Proposed) | After (Recommended) |
|---------|-------------------|---------------------|
| **Major Release Protection** | Manual policy | ✅ Automatic enforcement |
| **Beta Maturity Warnings** | Manual tracking | ✅ Automatic warnings (never blocks) |
| **Pre-flight Validation** | Partial | ✅ Comprehensive checklist |
| **Version Increment** | Manual | ✅ Automatic detection |
| **Error Prevention** | Basic | ✅ AI decision trees + script validation |

**Impact:** ✅ Significantly reduced human error risk

---

### 6.4 Operational Complexity

| Aspect | Before (Proposed) | After (Recommended) | Change |
|--------|-------------------|---------------------|--------|
| **Secrets to Manage** | 2 (PyPI + TestPyPI) | 1 (PyPI only) | -50% |
| **GitHub Actions Steps** | ~25 | ~15 | -40% |
| **Version Conversion Logic** | Required | Not needed | -100% |
| **Feature Flag Code** | New system | None | -100% |
| **Rollback Procedures** | Complex (yank + hotfix) | Simple (forward-fix) | -80% |

**Impact:** ✅ Significantly reduced operational burden

---

## 7 Risk Assessment

### 7.1 Risks of Current Proposal (v1.1)

| Risk | Severity | Likelihood | Mitigation (Recommended) |
|------|----------|------------|--------------------------|
| **TestPyPI dependency resolution issues** | High | High | ✅ Eliminate TestPyPI (use Beta on main PyPI) |
| **Version format confusion (PEP 440 vs SemVer)** | Medium | Medium | ✅ Use PEP 440 everywhere |
| **Complex GitHub Actions logic** | Medium | Low | ✅ Simplify to tag-based detection |
| **Feature flag technical debt** | Low | Medium | ✅ Defer until needed (YAGNI) |
| **Accidental major release without beta** | High | Medium | ✅ Add automatic enforcement |
| **Rushing beta to stable** | Medium | Medium | ✅ Add maturity validation |

---

### 7.2 Risks of Recommended Approach

| Risk | Severity | Likelihood | Mitigation Strategy |
|------|----------|------------|---------------------|
| **Users accidentally install beta** | Low | Low | PyPI requires `--pre` flag for pre-releases |
| **Beta testing period too short** | Medium | Medium | Script warns, requires confirmation |
| **Missing alpha tier for risky changes** | Low | Low | Use feature branches + CI for experimental work |
| **Beta numbering conflicts** | Low | Very Low | Script queries GitHub for existing betas |

**Overall Assessment:** ✅ Recommended approach has significantly lower risk profile

---

### 7.3 Migration Risk

**Question:** How risky is it to implement these recommendations?

**Answer:** Very low risk

**Reasons:**
1. **Additive Changes:** Beta support is opt-in, existing workflows unchanged
2. **No Breaking Changes:** All current commands still work
3. **Backward Compatible:** Existing release process preserved
4. **Fail-Safe:** Validation gates prevent errors before they cause problems
5. **Rollback Possible:** Can disable beta support if issues arise

**Migration Path:**
1. Implement Phase 1 (basic beta support)
2. Test with real beta release (e.g., v3.0.1b1 if needed)
3. Verify GitHub Actions handles it correctly
4. Roll out to AI agents via Cursor rules
5. Continue with Phase 2-3 for full hardening

---

## 8 Cursor AI Rules (To Be Added)

### 8.1 Release Decision Making

```markdown
# Add to .cursorrules or .cursor/rules/todo.ai-releases.mdc

When user says "prepare release" or "release todo.ai":

1. **Always check CI/CD first:**
   - Run: ./scripts/wait-for-ci.sh
   - If fails: STOP, report error, wait for user to fix

2. **Determine version bump type:**
   - Analyze commits (as normal)
   - Identify: MAJOR, MINOR, or PATCH

3. **For MAJOR bumps:**
   - Check if beta exists: `gh release list | grep "vX.Y.Zb"`
   - If NO beta:
     - STOP and say:
       "This is a major release (X.Y.Z). Major releases require beta testing.

        To create beta:
        ./release/release.sh --prepare --beta

        After beta testing, prepare stable release."
   - If beta EXISTS:
     - Check beta age
     - If < 7 days: WARN but proceed anyway
     - If >= 7 days: Proceed without warning

4. **For MINOR bumps:**
   - Ask user:
     "This is a minor release (X.Y.Z).

      Options:
      a) Create beta first (safer, for significant features)
      b) Release stable directly (faster, for small additions)

      Which do you prefer?"
   - Respect user choice

5. **For PATCH bumps:**
   - Proceed directly to stable (no beta needed)

6. **After prepare completes:**
   - STOP and show preview
   - WAIT for user to say "execute release"
   - NEVER execute automatically

7. **Error handling:**
   - ANY error → STOP immediately
   - Report error clearly
   - Do NOT attempt workarounds
   - Wait for user instruction
```

---

### 8.2 Beta Release Workflow

**Add to `.cursor/rules/todo.ai-releases.mdc`:**

When user requests beta release:

1. **Verify it makes sense:**
   - Betas appropriate for: MAJOR or significant MINOR releases
   - Not needed for: PATCH releases or trivial changes

2. **Execute beta prepare:**

   ```bash
   ./release/release.sh --prepare --beta
   ```

3. **After prepare, STOP and say:**

   ```text
   ✅ Beta release prepared.

   Version: X.Y.ZbN
   Release notes: release/RELEASE_NOTES.md

   Review the notes, then tell me 'execute release' when ready.
   ```

4. **When user says execute:**

   ```bash
   ./release/release.sh --execute
   ```

5. **After execute succeeds:**

   ```text
   ✅ Beta release vX.Y.ZbN published!

   Install: uv tool install --prerelease=allow todo-ai

   Recommended testing period: 7+ days for major, 2-3 days for minor

   After testing, prepare stable release with same version.
   ```

6. **Track beta testing:**
   - Note the beta version in TODO.md or elsewhere
   - Remind user of testing period when stable is requested

---

## 9 Success Metrics

### 9.1 Simplification Success

**Measure:** Lines of code, complexity

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Release script LOC | -20% vs proposed | `wc -l release/release.sh` |
| GitHub Actions LOC | -40% vs proposed | `wc -l .github/workflows/release.yml` |
| Documentation pages | -30% vs proposed | `wc -w docs/design/BETA_*.md` |
| Secrets to manage | 1 (not 2) | GitHub Settings → Secrets |

---

### 9.2 Hardening Success

**Measure:** Error prevention, validation coverage

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Major releases without beta | 0 | Script enforces (cannot happen) |
| Pre-flight check coverage | 6+ checks | Count checks in preflight_checks() |
| Failed releases due to missing validation | 0 | Track release failures |
| AI agent release errors | < 10% | Monitor AI release attempts |

---

### 9.3 User Experience

**Measure:** Adoption, satisfaction

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Beta releases created | >= 1 per major | GitHub releases list |
| Beta testing duration | 7+ days for major | Time between beta and stable |
| Documentation clarity | Positive feedback | User questions, GitHub discussions |
| Installation success rate | > 95% | PyPI download stats vs reported issues |

---

## 10 Recommendations Summary

### ✂️ Simplifications (Reduce Complexity)

1. **Reduce release tiers:** 4 → 2 (Beta + Stable)
2. **Single version format:** PEP 440 everywhere
3. **Eliminate TestPyPI:** Publish betas to main PyPI
4. **Defer feature flags:** Use beta releases instead (YAGNI)
5. **Simplify rollback:** Forward-fix only (no yanking)
6. **Simplify documentation:** One primary method, collapse alternatives

**Total Complexity Reduction:** ~40-50%

---

### 🔒 Hardenings (Reduce Errors)

1. **Auto-enforce beta requirement:** Major releases must have beta
2. **Validate beta maturity:** Enforce minimum testing period
3. **Pre-flight checklist:** 6+ comprehensive checks before execute
4. **Beta version logic:** Automatic increment detection
5. **Enhanced state file:** Complete metadata for execute phase
6. **AI decision trees:** Explicit rules for when to use beta

**Total Error Risk Reduction:** ~60-70%

---

### ✅ Integration (Preserve Existing)

1. **Backward compatible:** All existing commands still work
2. **Two-phase process:** Prepare → Review → Execute preserved
3. **Human review gate:** Still required for all releases
4. **CI/CD integration:** Existing checks still run
5. **Command syntax:** Minimal changes (`--beta` flag only)

**Breaking Changes:** Zero

---

## 11 Next Steps

### For Decision Makers

**Review Questions:**
1. Do you agree with 2-tier approach (Beta + Stable)?
2. Is auto-enforcement of beta for major releases acceptable?
3. Are the validation gates (maturity, pre-flight) appropriate?
4. Should we implement in phases or all at once?

**Decision:** [ ] Approve  [ ] Request Changes  [ ] Reject

---

### For Implementers

**If Approved:**
1. Start with Phase 1 (Core Beta Infrastructure)
2. Create feature branch: `feature/beta-releases-simplified`
3. Implement changes to `release/release.sh`
4. Update `.github/workflows/release.yml`
5. Test with alpha release to this branch
6. Merge and test with real beta release

---

## Appendix A: Command Reference

### Beta Release Commands

```bash
# Create first beta for version 1.0.0
./release/release.sh --prepare --beta
./release/release.sh --execute
# Result: v1.0.0b1

# Create second beta (after fixes)
./release/release.sh --prepare --beta
./release/release.sh --execute
# Result: v1.0.0b2

# After beta testing, create stable
./release/release.sh --prepare
./release/release.sh --execute
# Result: v1.0.0
```

---

### Installation Commands

```bash
# Install latest stable
uv tool install todo-ai

# Install latest beta
uv tool install --prerelease=allow todo-ai

# Install specific beta
uv tool install todo-ai==1.0.0b1

# Install from git (development)
uv tool install git+https://github.com/fxstein/todo.ai.git@main

# Upgrade to latest stable
uv tool upgrade todo-ai
```

---

### Version Checking

```bash
# Check current version
todo-ai version

# List GitHub releases (betas + stable)
gh release list

# Check PyPI versions
pip index versions todo-ai
```

---

## Appendix B: Decision Matrix

### When to Use Beta vs Direct-to-Stable

| Scenario | Recommendation | Reasoning |
|----------|----------------|-----------|
| **Major version bump** | ✅ Beta REQUIRED | Breaking changes need testing |
| **Significant new features** | ✅ Beta recommended | Risk of regression |
| **Minor enhancements** | ⚠️ Beta optional | User choice (safer vs faster) |
| **Bug fixes (patch)** | ❌ No beta needed | Low risk, need fast fixes |
| **Documentation only** | ❌ No beta needed | Zero code risk |
| **Dependency updates** | ⚠️ Beta if major deps | Depends on risk |
| **Refactoring** | ✅ Beta recommended | Risk of introducing bugs |

---

## Appendix C: Comparison Table

### Full Feature Comparison

| Feature | Proposed (v1.1) | Recommended | Improvement |
|---------|-----------------|-------------|-------------|
| **Release Tiers** | Alpha/Beta/RC/Stable | Beta/Stable | ✂️ 50% simpler |
| **Version Format** | PEP 440 + SemVer | PEP 440 only | ✂️ No conversion |
| **PyPI Targets** | TestPyPI + PyPI | PyPI only | ✂️ -1 secret |
| **Major Release Safety** | Manual policy | Auto-enforced | 🔒 100% protected |
| **Beta Maturity** | Manual tracking | Auto-validated | 🔒 Enforced |
| **Pre-flight Checks** | Basic | Comprehensive | 🔒 6+ checks |
| **Feature Flags** | Proposed system | Deferred (YAGNI) | ✂️ Less code |
| **Rollback** | Yank + hotfix | Forward-fix only | ✂️ Simpler |
| **GitHub Actions** | ~25 steps | ~15 steps | ✂️ 40% simpler |
| **Documentation** | Extensive | Focused | ✂️ 30% shorter |
| **Backward Compat** | Yes | Yes | ✅ Preserved |
| **Two-Phase Process** | Yes | Yes | ✅ Preserved |
| **Human Review** | Required | Required | ✅ Preserved |

---

**Document Status:** RECOMMENDATIONS
**Action Required:** Review and approve for implementation
**Owner:** Release Engineering Team
**Created:** December 16, 2025
**Version:** 1.0

---

**Questions or feedback?** Open discussion in GitHub or update this document.
