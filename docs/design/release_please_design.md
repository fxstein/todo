# Release Please Integration Design - AIT-8

**Date:** 2026-01-30
**Linear Issue:** [AIT-8](https://linear.app/fxstein/issue/AIT-8/release-please)
**GitHub Issue:** [#59](https://github.com/fxstein/ai-todo/issues/59)
**Task:** #269
**Analysis:** [release_please_analysis.md](./release_please_analysis.md)

## Executive Summary

Design a migration from custom `release.sh` to Google's Release Please with custom enhancements for:
- AI-generated release summaries (Gemini API)
- Beta policy enforcement for major releases
- Existing CI/CD integration (PyPI trusted publishing, GitHub releases)

**Migration Strategy:** Full replacement with custom GitHub Actions to preserve current release quality.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Release Please Configuration](#release-please-configuration)
3. [AI Summary Injection System](#ai-summary-injection-system)
4. [Beta Policy Enforcement](#beta-policy-enforcement)
5. [CI/CD Integration](#cicd-integration)
6. [Migration Plan](#migration-plan)
7. [Rollback Strategy](#rollback-strategy)
8. [Testing Approach](#testing-approach)
9. [Approved Decisions](#approved-decisions)

---

## Architecture Overview

### High-Level Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Developer Push                              │
│                    (Conventional Commits)                            │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Release Please Workflow                           │
│  - Analyze commits (major/minor/patch)                              │
│  - Generate/update CHANGELOG.md                                     │
│  - Bump version in pyproject.toml, __init__.py                      │
│  - Create/update Release PR                                         │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  AI Summary Generation (Custom)                      │
│  - Triggered on Release PR creation/update                          │
│  - Call Gemini API with commit history                              │
│  - Generate 2-3 paragraph summary                                   │
│  - Inject into CHANGELOG.md header                                  │
│  - Commit update to Release PR                                      │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│             Beta Policy Enforcement (Custom, if Major)               │
│  - Detect major release from PR title                               │
│  - Query GitHub releases for existing betas                         │
│  - Block PR merge if no beta exists                                 │
│  - Post comment with instructions                                   │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Human Review & Approval                        │
│  - Review CHANGELOG.md + AI summary                                 │
│  - Verify version bump is correct                                   │
│  - Check beta policy (if major)                                     │
│  - Approve and merge PR                                             │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Existing CI/CD Pipeline                           │
│  - Tag created automatically by Release Please                      │
│  - CI runs full test suite (existing)                               │
│  - PyPI publish (trusted publisher, existing)                       │
│  - GitHub release created (existing)                                │
│  - Assets attached (dist/, legacy scripts, existing)                │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Release Please** (upstream)
   - Commit analysis
   - CHANGELOG generation
   - Version bumping
   - Release PR management
   - Tag creation

2. **AI Summary Generator** (custom)
   - GitHub Action
   - Gemini API integration
   - CHANGELOG injection

3. **Beta Policy Enforcer** (custom)
   - GitHub Action
   - Major release detection
   - Beta verification
   - PR blocking

4. **Existing CI/CD** (keep as-is)
   - Test suite
   - PyPI publishing
   - GitHub release
   - Asset management

---

## Review and Approval Workflow

### How Release Preparation Works

**CRITICAL:** Release Please creates a **Release PR** that serves as the review gate. This PR is where all review and approval happens BEFORE any release is executed.

### Step-by-Step Review Process

1. **Developer pushes to main:**
   - Commits accumulate on main branch
   - Each commit follows conventional commit format

2. **Release Please creates/updates Release PR:**
   - **Automated:** Runs on every push to main
   - **PR Title:** `chore(main): release 4.0.1` (example)
   - **PR Body:** Complete CHANGELOG preview
   - **PR Contents:** Version bumps in all files
   - **Single PR:** Same PR updated for all commits until merged

3. **AI Summary Injection (custom):**
   - **Triggered:** When Release PR is created/updated
   - **Action:** Gemini API generates 2-3 paragraph summary
   - **Injection:** Summary added to CHANGELOG.md header
   - **Commit:** Updated CHANGELOG committed to Release PR

4. **Beta Policy Check (custom, if major):**
   - **Triggered:** When Release PR is opened
   - **Check:** Validates beta exists if major release
   - **Block:** Prevents merge if policy violated
   - **Comment:** Posts instructions if blocked

5. **Human Review (APPROVAL GATE):**
   - **Review CHANGELOG:** Check AI summary quality and commit categorization
   - **Verify version:** Ensure correct version bump (major/minor/patch)
   - **Check beta policy:** If major, confirm beta was tested
   - **Test locally:** Optional - install from PR branch
   - **Approve PR:** Required status checks must pass
   - **Merge PR:** This triggers the release execution

6. **Release Execution (automated after merge):**
   - **Tag creation:** Release Please creates git tag (e.g., `v4.0.1`)
   - **CI/CD triggered:** Existing pipeline runs on tag push
   - **Tests run:** Full test suite must pass
   - **PyPI publish:** Trusted publisher uploads to PyPI
   - **GitHub release:** Created with CHANGELOG and assets

### Key Safety Features

- **PR = Review Gate:** ALL changes visible before execution
- **Required Checks:** CI, beta policy must pass before merge allowed
- **Branch Protection:** Enforce reviewers, status checks
- **No Direct Commits:** Main branch protected, only PR merges
- **Audit Trail:** PR shows who approved, when, and why

### Comparison to Current Process

| Feature | Current (release.sh) | New (Release Please) |
|---------|---------------------|---------------------|
| **Prepare** | Manual `--prepare` command | Automatic Release PR creation |
| **Review** | Preview in terminal | Review PR on GitHub |
| **Approval** | User runs `--execute` | User merges PR |
| **Safety** | Two-phase (prepare/execute) | PR merge = execution trigger |
| **Visibility** | Local only | Public PR (team can review) |

### Example Release PR

**Title:** `chore(main): release 4.0.1`

**Body Preview:**
```markdown
## 4.0.1 (2026-01-30)

[AI-GENERATED SUMMARY INSERTED HERE]
This release enhances the Release Please workflow with improved
AI summary generation and fixes several edge cases in version bumping...

---

### ✨ Features

* Add Release Please integration (#59) ([abc123](link))

### 🐛 Bug Fixes

* Fix version bumping for beta releases ([def456](link))

### 📚 Documentation

* Update RELEASE_PROCESS.md ([ghi789](link))
```

**Files Changed:**
- `CHANGELOG.md` (AI summary + commit list)
- `pyproject.toml` (version: 4.0.1)
- `ai_todo/__init__.py` (version: 4.0.1)
- `.github/release-please-manifest.json` (version: 4.0.1)

**Checks:**
- ✅ CI/CD (all tests pass)
- ✅ Beta Policy (not major, no check needed)
- ✅ Linters (markdown, python)

**Human Decision:** Approve and merge when ready → Release executes automatically

---

## Release Please Configuration

### 1. Workflow File

**File:** `.github/workflows/release-please.yml`

```yaml
name: Release Please

on:
  push:
    branches:
      - main

permissions:
  contents: write
  pull-requests: write

jobs:
  release-please:
    name: 📦 Release Please
    runs-on: ubuntu-latest
    outputs:
      pr_number: ${{ steps.release.outputs.pr }}
      releases_created: ${{ steps.release.outputs.releases_created }}
      tag_name: ${{ steps.release.outputs.tag_name }}

    steps:
      - name: Run Release Please
        id: release
        uses: googleapis/release-please-action@v4
        with:
          # Config file path
          config-file: .github/release-please-config.json
          manifest-file: .github/release-please-manifest.json
```

### 2. Configuration File

**File:** `.github/release-please-config.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
  "packages": {
    ".": {
      "release-type": "python",
      "package-name": "todo-ai",
      "include-component-in-tag": false,
      "bump-minor-pre-major": true,
      "bump-patch-for-minor-pre-major": false,
      "changelog-sections": [
        {"type": "feat", "section": "✨ Features", "hidden": false},
        {"type": "fix", "section": "🐛 Bug Fixes", "hidden": false},
        {"type": "perf", "section": "⚡ Performance", "hidden": false},
        {"type": "refactor", "section": "♻️ Refactoring", "hidden": false},
        {"type": "docs", "section": "📚 Documentation", "hidden": false},
        {"type": "chore", "section": "🔧 Maintenance", "hidden": false},
        {"type": "test", "section": "🧪 Tests", "hidden": false},
        {"type": "build", "section": "🏗️ Build", "hidden": false},
        {"type": "ci", "section": "👷 CI/CD", "hidden": false},
        {"type": "backend", "section": "⚙️ Backend", "hidden": false},
        {"type": "infra", "section": "🏗️ Infrastructure", "hidden": false},
        {"type": "release", "section": "📦 Release", "hidden": false},
        {"type": "internal", "section": "🔒 Internal", "hidden": false}
      ],
      "extra-files": [
        {
          "type": "python",
          "path": "ai_todo/__init__.py",
          "glob": false
        }
      ],
      "prerelease": false
    }
  }
}
```

**Configuration Notes:**
- `bump-patch-for-minor-pre-major: false` - Allows minor bumps before 1.0.0
- Custom changelog sections for our commit types
- Extra files: Updates `ai_todo/__init__.py` in addition to `pyproject.toml`

### 3. Manifest File

**File:** `.github/release-please-manifest.json`

```json
{
  ".": "4.0.0b2"
}
```

**Bootstrap:**
- Initialize with current version from `pyproject.toml`
- Release Please will maintain this file automatically

### 4. Pre-release Configuration

**For Beta Releases:**

To create a beta release, temporarily update the config:

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

**Approach:**
- **Option A:** Manual config update (commit to trigger beta PR)
- **Option B:** Separate workflow with `--prerelease` flag
- **Recommendation:** Option A for simplicity

---

## AI Summary Injection System

### 1. GitHub Action Workflow

**File:** `.github/workflows/ai-release-summary.yml`

```yaml
name: AI Release Summary

on:
  pull_request:
    types: [opened, synchronize]
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  generate-summary:
    name: 🤖 Generate AI Summary
    # Only run on Release Please PRs
    if: |
      startsWith(github.event.pull_request.title, 'chore(main): release') ||
      startsWith(github.event.pull_request.title, 'chore: release')
    runs-on: ubuntu-latest

    steps:
      - name: Checkout PR branch
        uses: actions/checkout@v6
        with:
          ref: ${{ github.event.pull_request.head.ref }}
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.14"
          allow-prereleases: true

      - name: Install dependencies
        run: |
          pip install google-generativeai requests

      - name: Generate AI Summary
        id: generate
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
          REPO: ${{ github.repository }}
        run: |
          python .github/scripts/generate_ai_summary.py

      - name: Inject into CHANGELOG
        run: |
          python .github/scripts/inject_summary.py

      - name: Commit updated CHANGELOG
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add CHANGELOG.md
          git diff --staged --quiet || git commit -m "docs: Add AI-generated release summary"
          git push
```

### 2. AI Summary Generator Script

**File:** `.github/scripts/generate_ai_summary.py`

```python
#!/usr/bin/env python3
"""
Generate AI release summary using Gemini API.
"""
import os
import sys
import re
import subprocess
import google.generativeai as genai
import requests

def get_commits_since_last_release():
    """Get commits since last release tag."""
    # Get last tag
    result = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        # No previous tags, get all commits
        last_tag = None
    else:
        last_tag = result.stdout.strip()

    # Get commits
    if last_tag:
        range_spec = f"{last_tag}..HEAD"
    else:
        range_spec = "HEAD"

    result = subprocess.run(
        ["git", "log", range_spec, "--pretty=format:%H|%s|%b"],
        capture_output=True,
        text=True
    )

    commits = []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        parts = line.split('|', 2)
        if len(parts) >= 2:
            commits.append({
                'hash': parts[0][:7],
                'subject': parts[1],
                'body': parts[2] if len(parts) > 2 else ''
            })

    return commits

def categorize_commits(commits):
    """Categorize commits by type."""
    categories = {
        'breaking': [],
        'features': [],
        'fixes': [],
        'docs': [],
        'other': []
    }

    for commit in commits:
        subject = commit['subject']
        body = commit['body']

        # Check for breaking changes
        if ('BREAKING CHANGE' in body or
            '!' in subject.split(':')[0] or
            'breaking' in subject.lower()):
            categories['breaking'].append(commit)
        # Features
        elif subject.startswith(('feat:', 'feature:')):
            categories['features'].append(commit)
        # Fixes
        elif subject.startswith('fix:'):
            categories['fixes'].append(commit)
        # Docs
        elif subject.startswith('docs:'):
            categories['docs'].append(commit)
        # Other
        else:
            categories['other'].append(commit)

    return categories

def generate_summary_with_gemini(commits, categories, api_key):
    """Generate summary using Gemini API."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    # Prepare context
    commit_summary = f"Total commits: {len(commits)}\n\n"

    if categories['breaking']:
        commit_summary += f"Breaking changes ({len(categories['breaking'])}):\n"
        for c in categories['breaking'][:5]:
            commit_summary += f"  - {c['subject']}\n"
        commit_summary += "\n"

    if categories['features']:
        commit_summary += f"Features ({len(categories['features'])}):\n"
        for c in categories['features'][:10]:
            commit_summary += f"  - {c['subject']}\n"
        commit_summary += "\n"

    if categories['fixes']:
        commit_summary += f"Fixes ({len(categories['fixes'])}):\n"
        for c in categories['fixes'][:10]:
            commit_summary += f"  - {c['subject']}\n"
        commit_summary += "\n"

    # Prompt
    prompt = f"""You are a technical writer creating release notes for an open-source Python project called "ai-todo" - a command-line task manager with AI integration.

Analyze these commits and write a concise, user-focused release summary:

{commit_summary}

Guidelines:
1. Write 2-3 paragraphs (150-250 words total)
2. Focus on user-facing benefits and improvements
3. Use plain language (avoid technical jargon)
4. Highlight the most important changes first
5. Explain what's new and why it matters
6. Do NOT include markdown headers or formatting
7. Do NOT list individual commits
8. Do NOT start with "This release..."

Write the summary:"""

    response = model.generate_content(prompt)
    return response.text.strip()

def save_summary(summary):
    """Save summary to file."""
    with open('ai_summary.txt', 'w') as f:
        f.write(summary)
    print(f"Summary saved to ai_summary.txt")

def main():
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY not set")
        sys.exit(1)

    print("Fetching commits...")
    commits = get_commits_since_last_release()

    if not commits:
        print("No commits found")
        sys.exit(0)

    print(f"Found {len(commits)} commits")

    print("Categorizing commits...")
    categories = categorize_commits(commits)

    print("Generating AI summary...")
    summary = generate_summary_with_gemini(commits, categories, api_key)

    print("\nGenerated Summary:")
    print("=" * 80)
    print(summary)
    print("=" * 80)

    save_summary(summary)

if __name__ == '__main__':
    main()
```

### 3. CHANGELOG Injection Script

**File:** `.github/scripts/inject_summary.py`

```python
#!/usr/bin/env python3
"""
Inject AI summary into CHANGELOG.md.
"""
import re
import sys

def inject_summary_into_changelog():
    """Inject AI summary into CHANGELOG.md header."""
    # Read summary
    try:
        with open('ai_summary.txt', 'r') as f:
            summary = f.read().strip()
    except FileNotFoundError:
        print("No summary file found, skipping injection")
        return

    if not summary:
        print("Empty summary, skipping injection")
        return

    # Read CHANGELOG
    try:
        with open('CHANGELOG.md', 'r') as f:
            changelog = f.read()
    except FileNotFoundError:
        print("Error: CHANGELOG.md not found")
        sys.exit(1)

    # Find the first version header (e.g., "## [4.0.0]" or "## 4.0.0")
    # Insert summary immediately after it
    pattern = r'(## \[?\d+\.\d+\.\d+.*?\]?.*?\n)'

    match = re.search(pattern, changelog)
    if not match:
        print("Warning: Could not find version header in CHANGELOG.md")
        print("Adding summary at the beginning")
        # Fallback: add at beginning after title
        parts = changelog.split('\n\n', 1)
        if len(parts) == 2:
            changelog = f"{parts[0]}\n\n{summary}\n\n{parts[1]}"
        else:
            changelog = f"{summary}\n\n{changelog}"
    else:
        # Insert after version header
        header_end = match.end()
        changelog = (
            changelog[:header_end] +
            '\n' + summary + '\n\n' +
            '---\n\n' +
            changelog[header_end:]
        )

    # Write updated CHANGELOG
    with open('CHANGELOG.md', 'w') as f:
        f.write(changelog)

    print("Summary injected into CHANGELOG.md")

if __name__ == '__main__':
    inject_summary_into_changelog()
```

### 4. GitHub Secrets Configuration

**Required Secrets:**
- `GEMINI_API_KEY` - Gemini API key for AI summary generation

**Setup:**
```bash
# In repository settings > Secrets > Actions
gh secret set GEMINI_API_KEY
```

### 5. Fallback Behavior

**If Gemini API fails:**
- Log error to workflow
- Skip summary injection
- Allow release to proceed
- CHANGELOG will have commit list only (still useful)

**Error Handling:**
```python
try:
    summary = generate_summary_with_gemini(...)
except Exception as e:
    print(f"Warning: AI summary generation failed: {e}")
    print("Continuing without AI summary")
    sys.exit(0)  # Success exit, allow workflow to continue
```

---

## Beta Policy Enforcement

### 1. GitHub Action Workflow

**File:** `.github/workflows/enforce-beta-policy.yml`

```yaml
name: Enforce Beta Policy

on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches: [main]

permissions:
  contents: read
  pull-requests: write

jobs:
  enforce-beta:
    name: 🛡️ Enforce Beta Policy
    # Only run on Release Please PRs
    if: |
      startsWith(github.event.pull_request.title, 'chore(main): release') ||
      startsWith(github.event.pull_request.title, 'chore: release')
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
        with:
          fetch-depth: 0  # Need full history for version analysis

      - name: Extract version from PR title
        id: version
        run: |
          PR_TITLE="${{ github.event.pull_request.title }}"
          VERSION=$(echo "$PR_TITLE" | grep -oP '(?<=release )\d+\.\d+\.\d+' || echo "")

          if [ -z "$VERSION" ]; then
            echo "Could not extract version from PR title"
            exit 1
          fi

          echo "version=$VERSION" >> $GITHUB_OUTPUT
          echo "Detected version: $VERSION"

      - name: Check if major release
        id: check_major
        run: |
          VERSION="${{ steps.version.outputs.version }}"
          NEW_MAJOR=$(echo "$VERSION" | cut -d'.' -f1)

          # Get current version from latest tag
          CURRENT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null | sed 's/^v//' || echo "0.0.0")
          CURRENT_MAJOR=$(echo "$CURRENT_VERSION" | cut -d'.' -f1 | cut -d'b' -f1)

          echo "Current major: $CURRENT_MAJOR"
          echo "New major: $NEW_MAJOR"

          if [ "$NEW_MAJOR" -gt "$CURRENT_MAJOR" ]; then
            echo "is_major=true" >> $GITHUB_OUTPUT
            echo "This is a MAJOR release"
          else
            echo "is_major=false" >> $GITHUB_OUTPUT
            echo "This is NOT a major release"
          fi

      - name: Check for existing beta
        id: check_beta
        if: steps.check_major.outputs.is_major == 'true'
        run: |
          VERSION="${{ steps.version.outputs.version }}"

          # Query for beta tags matching this version
          BETA_TAGS=$(git tag -l "v${VERSION}b*" || echo "")

          if [ -z "$BETA_TAGS" ]; then
            echo "has_beta=false" >> $GITHUB_OUTPUT
            echo "No beta found for $VERSION"
          else
            echo "has_beta=true" >> $GITHUB_OUTPUT
            echo "Found beta tags: $BETA_TAGS"
          fi

      - name: Block major release without beta
        if: |
          steps.check_major.outputs.is_major == 'true' &&
          steps.check_beta.outputs.has_beta == 'false'
        uses: actions/github-script@v7
        with:
          script: |
            const version = '${{ steps.version.outputs.version }}';

            // Post blocking comment
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `## ❌ Major Release Requires Beta Testing

            This is a major release (\`${version}\`), which requires at least one beta release for testing.

            **Next Steps:**

            1. **Close this PR** (do not merge)
            2. **Create a beta release** by updating \`.github/release-please-config.json\`:
               \`\`\`json
               {
                 "packages": {
                   ".": {
                     "prerelease": true,
                     "prerelease-type": "b"
                   }
                 }
               }
               \`\`\`
            3. **Commit and push** to trigger a beta release PR
            4. **Merge the beta PR** to publish beta version (e.g., \`v${version}b1\`)
            5. **Test the beta** for at least 7 days
            6. **Remove prerelease config** and push to trigger stable release PR

            **Policy:** Major releases MUST have beta testing to reduce risk of breaking changes.

            ---
            *This check enforces the beta policy for major releases.*`
            });

            // Fail the check to block merge
            core.setFailed('Major release requires beta testing first');

      - name: Approve non-major or beta-tested major
        if: |
          steps.check_major.outputs.is_major == 'false' ||
          steps.check_beta.outputs.has_beta == 'true'
        run: |
          echo "✅ Beta policy check passed"
          if [ "${{ steps.check_major.outputs.is_major }}" == "true" ]; then
            echo "Major release with existing beta - OK to proceed"
          else
            echo "Non-major release - no beta required"
          fi
```

### 2. Branch Protection Rule

**Recommendation:** Add this workflow as a required status check.

**Settings > Branches > main > Branch protection rules:**
- ✅ Require status checks to pass before merging
  - ✅ `enforce-beta / 🛡️ Enforce Beta Policy`

This prevents merging if the check fails.

---

## CI/CD Integration

### 1. Existing Pipeline Compatibility

Release Please creates tags automatically when the release PR is merged. Our existing `.github/workflows/ci-cd.yml` workflow already handles tag pushes:

```yaml
# Existing workflow (no changes needed)
on:
  push:
    tags:
      - 'v*'
```

**Trigger Flow:**
```
Release PR merged → Release Please creates tag → Existing CI/CD triggered
```

**No changes needed** to existing CI/CD workflow.

### 2. CHANGELOG in GitHub Release

Our existing `ci-cd.yml` uses `release/RELEASE_NOTES.md` for release body. With Release Please, we'll use `CHANGELOG.md` instead.

**Change in `.github/workflows/ci-cd.yml`:**

```yaml
- name: Create GitHub Release with all assets
  uses: softprops/action-gh-release@v1
  with:
    files: |
      dist/*
    # OLD: body_path: release/RELEASE_NOTES.md
    # NEW: Extract relevant section from CHANGELOG.md
    body_path: .github/scripts/extract_changelog_section.sh
```

**Script:** `.github/scripts/extract_changelog_section.sh`

```bash
#!/bin/bash
# Extract version-specific section from CHANGELOG.md

VERSION=${GITHUB_REF_NAME#v}  # Remove 'v' prefix

# Extract section between this version and next version header
awk "/^## \[?${VERSION}\]?/,/^## \[?[0-9]/" CHANGELOG.md | head -n -1 > release_notes.txt

cat release_notes.txt
```

### 3. Asset Management

**Changes needed:**
- Remove `legacy/*` scripts from assets (retired in v3.0.0)
- Keep only Python distributions: `dist/*`

---

## Migration Plan

### Phase 1: Setup

**Goal:** Configure Release Please without affecting current process

**Tasks:**
1. Create Release Please configuration files
   - `.github/release-please-config.json`
   - `.github/release-please-manifest.json`
   - `.github/workflows/release-please.yml`
2. Test on a branch (no PR to main)
3. Verify CHANGELOG generation
4. Verify version bumping
5. Document configuration

**Validation:**
- ✅ CHANGELOG.md generated correctly
- ✅ Version bumped in `pyproject.toml` and `ai_todo/__init__.py`
- ✅ Release PR created
- ✅ PR has correct title and body

**Branch:** `feat/release-please-setup`
**PR:** Draft PR for review only, DO NOT MERGE

### Phase 2: AI Summary Integration

**Goal:** Add AI summary generation workflow

**Tasks:**
1. Create AI summary generation scripts
   - `.github/scripts/generate_ai_summary.py`
   - `.github/scripts/inject_summary.py`
2. Create AI summary workflow
   - `.github/workflows/ai-release-summary.yml`
3. Configure GitHub secret (`GEMINI_API_KEY`)
4. Test on Release Please PR
5. Verify summary injection

**Validation:**
- ✅ AI summary generated successfully
- ✅ Summary injected into CHANGELOG.md
- ✅ Summary quality matches current standards
- ✅ Fallback works if API fails

**Branch:** `feat/ai-summary-integration`
**PR:** Draft PR for review only, DO NOT MERGE

### Phase 3: Beta Policy Enforcement

**Goal:** Add beta policy enforcement

**Tasks:**
1. Create beta policy enforcement workflow
   - `.github/workflows/enforce-beta-policy.yml`
2. Test with mock major release PR
3. Verify blocking behavior
4. Verify approval for non-major releases
5. Update branch protection rules

**Validation:**
- ✅ Major releases without beta are blocked
- ✅ Major releases with beta are allowed
- ✅ Non-major releases are allowed
- ✅ Comment posted with clear instructions

**Branch:** `feat/beta-policy-enforcement`
**PR:** Draft PR for review only, DO NOT MERGE

### Phase 4: Integration Testing

**Goal:** Test complete workflow end-to-end

**Tasks:**
1. Merge all feature branches into integration branch
2. Create test release (patch bump)
3. Verify complete workflow:
   - Release Please PR creation
   - AI summary generation
   - Beta policy check (non-major)
   - PR merge
   - Tag creation
   - CI/CD execution
   - PyPI publish
   - GitHub release
4. Test beta release workflow:
   - Enable prerelease config
   - Verify beta PR creation
   - Verify beta numbering
5. Document any issues

**Validation:**
- ✅ Complete workflow executes successfully
- ✅ AI summary appears in CHANGELOG
- ✅ GitHub release created with correct assets
- ✅ PyPI package published
- ✅ Beta releases work correctly

**Branch:** `feat/release-please-integration`
**Test Tag:** `v4.0.0-test1` (deleted after test)

### Phase 5: Migration Cutover

**Goal:** Replace `release.sh` with Release Please

**Tasks:**
1. Archive `release.sh` and related scripts
   - Move to `release/archive/`
   - Update documentation references
2. Update Cursor rules
   - Remove `release-workflow.mdc` (old workflow)
   - Create `release-please-workflow.mdc` (new workflow)
3. Update documentation
   - `RELEASE_PROCESS.md` - new workflow
   - `CONTRIBUTING.md` - conventional commits
   - Add migration guide
4. Communicate changes
   - Linear comment on AIT-8
   - GitHub discussion post
   - Update README if needed
5. Create final PR
6. Merge to main

**Validation:**
- ✅ Documentation updated
- ✅ Cursor rules updated
- ✅ Contributors notified
- ✅ Old scripts archived (not deleted)

**Branch:** `feat/release-please-cutover`
**PR:** Regular PR for review and merge

### Phase 6: First Production Release

**Goal:** Create first production release with new system

**Tasks:**
1. Accumulate commits on main
2. Wait for Release Please to create PR
3. Review PR (AI summary, CHANGELOG, version)
4. Approve and merge
5. Monitor CI/CD execution
6. Verify release quality
7. Document lessons learned

**Validation:**
- ✅ Release PR created automatically
- ✅ AI summary quality is good
- ✅ Release succeeds without issues
- ✅ No functionality regressions

**Release:** `v4.0.0` or `v4.0.1` (depending on current state)

---

## Rollback Strategy

### Scenario 1: Release Please PR Issues

**Problem:** Release Please PR has incorrect version or CHANGELOG

**Rollback:**
1. Close the Release Please PR (do not merge)
2. Release Please will recreate it on next push
3. No impact on main branch

**Recovery Time:** Immediate (no changes to main)

### Scenario 2: AI Summary Generation Failure

**Problem:** AI summary workflow fails consistently

**Rollback:**
1. Disable AI summary workflow
   ```yaml
   # In .github/workflows/ai-release-summary.yml
   on: []  # Disable all triggers
   ```
2. Release Please PR will still have commit-based CHANGELOG
3. Manual summary can be added if needed

**Recovery Time:** < 1 hour (disable workflow)

### Scenario 3: Beta Policy False Positive

**Problem:** Beta policy blocks a valid release

**Rollback:**
1. Temporarily disable beta policy workflow
   ```yaml
   # In .github/workflows/enforce-beta-policy.yml
   on: []  # Disable all triggers
   ```
2. Remove from required status checks
3. Merge Release Please PR
4. Fix policy logic
5. Re-enable workflow

**Recovery Time:** < 1 hour (disable workflow, manual merge)

### Scenario 4: Complete System Failure

**Problem:** Release Please system is broken, need release ASAP

**Rollback:**
1. Restore `release.sh` from archive
   ```bash
   cp release/archive/release.sh release/release.sh
   chmod +x release/release.sh
   ```
2. Use old workflow to create release
3. Tag and push manually
4. Existing CI/CD will handle the rest

**Recovery Time:** < 30 minutes (restore script, manual release)

### Scenario 5: Permanent Rollback

**Problem:** Release Please doesn't meet requirements, revert permanently

**Rollback:**
1. Restore `release.sh` from archive
2. Disable all Release Please workflows
3. Revert Cursor rules to old workflow
4. Update documentation
5. Close Release Please PRs
6. Continue with old system

**Recovery Time:** < 1 day (full revert and documentation)

---

## Testing Approach

### Unit Tests

**What:** Test individual components in isolation

**Components:**
1. AI summary generator
   - Mock Gemini API responses
   - Test commit categorization
   - Test summary formatting
2. CHANGELOG injector
   - Test header detection
   - Test summary insertion
   - Test malformed CHANGELOG handling
3. Beta policy enforcer
   - Test version parsing
   - Test major detection
   - Test beta existence check

**Framework:** pytest

**Location:** `tests/unit/test_release_please.py`

### Integration Tests

**What:** Test complete workflows end-to-end

**Scenarios:**
1. **Patch Release:**
   - Commits: Fix commits only
   - Expected: Patch bump, no beta policy check
2. **Minor Release:**
   - Commits: Feature commits
   - Expected: Minor bump, no beta policy check
3. **Major Release without Beta:**
   - Commits: Breaking change commits
   - Expected: Major bump, blocked by beta policy
4. **Major Release with Beta:**
   - Prior: Beta tag exists (v4.0.0b1)
   - Commits: Breaking change commits
   - Expected: Major bump, beta policy passes
5. **Beta Release:**
   - Config: prerelease: true
   - Expected: Beta version (v4.0.0b1), no policy check

**Framework:** GitHub Actions workflow dispatch (manual trigger)

**Location:** `.github/workflows/test-release-please.yml`

### Smoke Tests

**What:** Quick validation after deployment

**Steps:**
1. Create test commit (feat: add test feature)
2. Wait for Release Please PR
3. Verify PR created correctly
4. Check AI summary generated
5. Verify beta policy check ran
6. Close PR (do not merge)

**Frequency:** After each deployment to main

### Beta Testing

**What:** Real-world validation before stable release

**Process:**
1. Create beta release (v4.0.1b1) using new system
2. Test complete workflow:
   - PR creation
   - AI summary
   - Merge
   - CI/CD
   - PyPI publish
   - GitHub release
3. Install beta locally:
   ```bash
   uv tool install --prerelease=allow todo-ai
   ```
4. Use for 3-7 days
5. Verify no regressions
6. Graduate to stable if successful

**Timeline:** 1 week minimum

---

## Approved Decisions

All design questions have been reviewed and approved. Implementation will proceed with the following decisions:

### 1. Gemini API Configuration ✅

**Decision:** **Option B** - Create new service account

**Implementation:**
- Create dedicated Gemini API service account for release automation
- Configure `GEMINI_API_KEY` GitHub secret
- Ensure API key has appropriate rate limits and quotas

**Action Items:**
- [ ] Create Gemini API service account
- [ ] Generate API key
- [ ] Configure GitHub repository secret: `GEMINI_API_KEY` # pragma: allowlist secret

### 2. Backend-Only Detection ✅

**Decision:** **Option B** - Enforce strict `infra:` prefix discipline

**Implementation:**
- Require `infra:`, `backend:`, `internal:` prefixes for infrastructure work
- Document commit prefix guidelines in CONTRIBUTING.md
- Add pre-commit linter to validate commit prefixes (optional)
- Accept that Release Please will use conventional commit types only

**Action Items:**
- [ ] Update CONTRIBUTING.md with commit prefix guidelines
- [ ] Add examples: `infra:` vs `feat:` usage
- [ ] Consider pre-commit hook for prefix validation

### 3. Beta Enforcement Strictness ✅

**Decision:** **Option A** - Hard block (prevent merge)

**Implementation:**
- Major release PRs without beta will be blocked (cannot merge)
- GitHub Action will fail required status check
- Clear error message with instructions posted to PR
- Requires workflow disable to bypass (intentional friction)

**Action Items:**
- [ ] Implement as designed in `.github/workflows/enforce-beta-policy.yml`
- [ ] Add to branch protection required checks
- [ ] Monitor for false positives after deployment

### 4. CHANGELOG Format ✅

**Decision:** **Option A** - Keep a Changelog (industry standard)

**Implementation:**
- Use Release Please default format
- Enhance with AI-generated summary at top of each release section
- Standard sections: Features, Bug Fixes, Documentation, etc.
- Links to commits maintained

**Action Items:**
- [ ] Accept Release Please default CHANGELOG format
- [ ] Ensure AI summary injection preserves format
- [ ] Validate markdown linting passes

### 5. Linear Integration ✅

**Decision:** **Option A** - Manual updates initially

**Implementation:**
- Manual Linear comments on release PRs
- Manual status updates after releases
- Automation can be added later if workflow becomes repetitive

**Action Items:**
- [ ] Update Linear manually after each release
- [ ] Document Linear update process
- [ ] Revisit automation after 3-5 releases

### 6. API Cost Management ✅

**Decision:** **Confirmed** - Costs acceptable

**Analysis:**
- Cost per release: ~$0.0004
- Annual cost (50 releases): ~$0.02
- Negligible impact on budget

**Action Items:**
- [ ] Monitor actual API usage after deployment
- [ ] Set up billing alerts if needed (optional)

### 7. Legacy Scripts Retirement ✅

**Decision:** Remove ALL `legacy/` scripts from releases

**Implementation:**
- Remove `legacy/todo.ai` from GitHub release assets
- Remove `legacy/todo.bash` (already removed)
- Exclude entire `legacy/` folder from release artifacts
- Focus exclusively on Python package distribution

**Rationale:** Legacy scripts retired in v3.0.0, no longer maintained

**Action Items:**
- [x] Remove `legacy/todo.ai` from CI/CD workflow
- [x] Update asset management documentation
- [ ] Verify no other legacy references remain

---

## Success Criteria

### Functional Requirements

1. ✅ Release Please generates accurate CHANGELOG.md
2. ✅ Version bumping works for all files (`pyproject.toml`, `__init__.py`)
3. ✅ Beta releases work correctly (prerelease flag)
4. ✅ AI summaries appear in CHANGELOG (2-3 paragraphs, user-focused)
5. ✅ Major releases require beta (enforced, blocks merge)
6. ✅ CI/CD integration works (PyPI → GitHub release)
7. ✅ Existing release quality maintained or improved
8. ✅ Migration documented for contributors

### Non-Functional Requirements

1. ✅ Release process takes ≤ 10 minutes (commit → tag → release)
2. ✅ AI summary generation ≤ 30 seconds
3. ✅ Beta policy check ≤ 10 seconds
4. ✅ System is maintainable (less custom code than release.sh)
5. ✅ Rollback possible in < 30 minutes
6. ✅ Documentation complete and clear
7. ✅ Contributors understand new workflow

### Validation Methods

1. **Unit tests:** All scripts have 80%+ coverage
2. **Integration tests:** 5 scenarios pass consistently
3. **Smoke tests:** Manual validation after each phase
4. **Beta testing:** 1 week real-world usage
5. **User acceptance:** Contributors approve workflow
6. **Performance:** Release timing meets requirements

---

## Next Steps

1. ✅ **Design approved** - All decisions confirmed
2. ✅ **Open questions answered** - Implementation path clear
3. **Start Phase 1** - Setup Release Please configuration
4. **Create GitHub secrets** - GEMINI_API_KEY (service account)
5. **Update CONTRIBUTING.md** - Commit prefix guidelines
6. **Write unit tests** - Custom scripts (AI summary, beta policy)

---

**Status:** Design approved, ready for implementation
**Approver:** Oliver Ratzesberger
**Approval Date:** 2026-01-30
**Author:** AI Assistant
**Date:** 2026-01-30
