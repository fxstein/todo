# Release Process for todo.ai

This document outlines the **automated** process for creating releases of `todo.ai` on GitHub using GitHub CLI.

## Prerequisites

### Install GitHub CLI

```bash
# macOS
brew install gh

# Linux
# See https://cli.github.com/manual/installation

# Verify installation
gh --version
```

### Authenticate GitHub CLI

```bash
gh auth login
```

Follow the prompts to authenticate. You'll need:
- GitHub account with write access to the repository
- Authentication via web browser or token

### Verify Access

```bash
gh repo view fxstein/todo.ai
```

## Version Numbering

`todo.ai` uses [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes, backward compatible

Current version format in `todo.ai`:
```zsh
VERSION="1.0.0"
```

## Beta and Stable Releases

`todo.ai` uses a **2-tier release strategy** for managing risk and gathering feedback:

### Release Channels

- **Beta (Pre-Release):** Testing channel for new features (format: `v1.0.0b1`, `v1.0.0b2`, etc.)
- **Stable (Production):** Production-ready releases (format: `v1.0.0`)

### When to Use Beta Releases

**REQUIRED:**
- **Major releases** (e.g., 2.0.0 → 3.0.0) MUST have at least one beta first
  - The release script automatically enforces this requirement
  - Recommended testing period: 7+ days

**RECOMMENDED:**
- Significant new features or refactoring
- Changes that could impact existing workflows
- Recommended testing period: 2-3 days for minor releases

**NOT NEEDED:**
- Patch releases (bug fixes)
- Documentation-only changes

### Beta Release Commands

```bash
# Prepare beta release
./release/release.sh --prepare --beta

# Review release notes, then execute
./release/release.sh --execute

# Result: v1.0.0b1, v1.0.0b2, etc.
```

### Override Proposed Version (Optional)

If you need to override the proposed version (e.g., force `3.0.0b3`), use
`--set-version` during prepare:

```bash
# Force a specific beta version
./release/release.sh --prepare --beta --set-version 3.0.0b3

# Force a specific stable version
./release/release.sh --prepare --set-version 3.0.0
```

**Constraints:**
- Version must be greater than the current GitHub release
- Beta overrides must keep the same base version during an active beta cycle

### Stable Release Commands

```bash
# Prepare stable release (default)
./release/release.sh --prepare

# Review release notes, then execute
./release/release.sh --execute

# Result: v1.0.0
```

### Beta Testing

Users can install beta releases to help test:

```bash
# Using uv (recommended)
uv tool install --prerelease=allow todo-ai

# Using pipx
pipx install --pre todo-ai
```

After beta testing period, create stable release with the same commands (without `--beta` flag).

## Intelligent Automated Release Process

### Using AI Agents (Cursor)

Simply tell your AI agent:

```
Release todo.ai
```

The agent will automatically:
1. **Check CI/CD status** - Ensures all tests pass before proceeding
2. **Determine release type:**
   - **Major bump:** Agent will check if beta exists, create beta if needed
   - **Minor bump:** Agent will ask if you want beta or stable
   - **Patch bump:** Agent will proceed directly to stable
3. **Generate a human-readable release summary** by analyzing commits since the last release
   - Review commit messages to understand changes
   - Write a 2-3 paragraph summary highlighting key improvements and user-facing benefits
   - Save the summary to `release/AI_RELEASE_SUMMARY.md`
4. **Run the intelligent release script** with the summary: `./release/release.sh --prepare [--beta] --summary release/AI_RELEASE_SUMMARY.md`
   - The script copies the AI summary into `release/RELEASE_SUMMARY.md`
   - Automatically analyzes commits and determines version bump
   - Generates detailed release notes in `release/RELEASE_NOTES.md` (summary + categorized commits)
5. **Show you the generated release notes** (including the summary and release type)
6. **STOP and wait for approval** before executing
7. **Execute the release** only after you say "execute release"

**Cursor rules** are configured so agents follow the beta release decision tree automatically when you request a release.

### Quick Release (Manual)

**Without AI-generated summary:**
```bash
./release/release.sh --prepare
./release/release.sh --execute
```

**With AI-generated summary:**
```bash
./release/release.sh --prepare --summary release/AI_RELEASE_SUMMARY.md
./release/release.sh --execute
```

The intelligent release script will:
1. **Include AI-generated summary** (if provided via `--summary` flag)
2. **Analyze commits** since the last release
3. **Determine version bump** (major/minor/patch) based on commit messages
4. **Generate release notes** automatically from commits
5. **Request human review** for major releases or releases with >10 commits
6. **Wait for explicit execute** after prepare

### How It Works

The script uses a **hybrid approach** with three priority levels:

**Priority 1: Explicit Prefixes** (fastest, explicit)
- `backend:`, `infra:`, `release:`, `internal:` → **PATCH** (backend-only work)
- `feat:`, `feature:` → **MINOR** (new user-facing features)
- `fix:`, `bugfix:` → **PATCH** (bug fixes)
- `breaking:`, `!:` → **MAJOR** (breaking changes)

**Priority 2: File Analysis** (catches forgotten prefixes)
- If **only backend files** changed → **PATCH** (infrastructure only)
- Backend files: `release/release.sh`, `.cursor/rules/`, `.todo.ai/`, `tests/`, `release/RELEASE_*.md`, `docs/TEST_PLAN.md`
- Frontend files: `README.md`, `todo.ai` (functional changes), user-facing docs

**Priority 3: Keyword Analysis** (fallback for mixed/frontend)
- **Major release** (X.0.0): Breaking changes detected
  - Keywords: `breaking`, `break`, `major`, `!:` in commit messages
  - Commits with `!` suffix (e.g., `feat!:`, `fix!:`)

- **Minor release** (0.X.0): New features added
  - Keywords: `feat:`, `feature:`, `add`, `new`, `implement`, `create`, `support`

- **Patch release** (0.0.X): Bug fixes and other changes
  - Keywords: `fix:`, `bugfix:`, `patch:`, `bug`, `hotfix`, `correct`
  - All other commits default to patch

**Why This Approach?**
- Backend-only releases (infrastructure improvements) should be **PATCH**, not **MINOR**
- Version numbers reflect actual user impact
- Automatic detection catches forgotten prefixes
- Aligns with semantic versioning principles

### Release Notes Generation

The script generates release notes in two parts:

1. **AI-Generated Summary** (optional, recommended)
   - Human-readable 2-3 paragraph summary highlighting key improvements
   - Focuses on user-facing benefits and notable changes
   - Generated by the AI agent and saved to `release/AI_RELEASE_SUMMARY.md`
   - Copied into `release/RELEASE_SUMMARY.md` during prepare
   - Included at the top of release notes when provided via `--summary` flag

2. **Detailed Commit List** (automatic)
   - Automatically categorizes commits into:
     - **Breaking Changes**: Commits indicating breaking changes
     - **Added**: New features and additions
     - **Changed**: Updates, refactors, improvements
     - **Fixed**: Bug fixes and corrections
     - **Other**: Unclassified commits

**Example usage with summary:**
```bash
./release/release.sh --prepare --summary release/AI_RELEASE_SUMMARY.md
```

**Example release notes format:**

When using the `--summary` flag, the release notes will have this structure:

For beta releases, the generated notes append the previous beta's
`RELEASE_NOTES.md` under a "Previous Beta Release Notes" header.

```markdown
## Release 1.2.0

This release enhances the automated release process with AI-generated
human-readable summaries and fixes a critical bug in the version update
mechanism.

The most significant improvement is the introduction of AI-generated
release summaries. When using AI agents like Cursor, agents can now
automatically generate a 2-3 paragraph human-readable summary that
highlights key improvements and user-facing benefits...

Additionally, a critical bug fix ([f6965b6](https://github.com/fxstein/todo.ai/commit/f6965b6...))
ensures that version updates only replace actual `VERSION=` variable
assignments...

---

### Added
- Add support for AI-generated human-readable release summaries ([dcbcb66](https://github.com/fxstein/todo.ai/commit/dcbcb66...))
- Add release summary for testing AI-generated summary feature ([99475d2](https://github.com/fxstein/todo.ai/commit/99475d2...))

### Changed
- Update version to 1.1.0 to match release ([f3eaeac](https://github.com/fxstein/todo.ai/commit/f3eaeac...))

### Fixed
- Fix version update to only replace VERSION assignments ([f6965b6](https://github.com/fxstein/todo.ai/commit/f6965b6...))

### Other
- Document AI-generated release summary feature ([9429c14](https://github.com/fxstein/todo.ai/commit/9429c14...))

*Total commits: 5*
```

**Note:** All commits in the release notes automatically include GitHub commit links with short hash for readability.

**Creating an AI-generated summary:**

When generating a summary, save it to `release/AI_RELEASE_SUMMARY.md` with this format.
Do not include markdown headers.

```markdown
This release enhances the automated release process with AI-generated
human-readable summaries and fixes a critical bug in the version update
mechanism.

The most significant improvement is the introduction of AI-generated
release summaries ([dcbcb66](https://github.com/fxstein/todo.ai/commit/dcbcb66...)).
When using AI agents like Cursor, agents can now automatically generate
a 2-3 paragraph human-readable summary that highlights key improvements
and user-facing benefits. This summary appears at the top of release notes,
making them much more accessible and informative than raw commit lists alone.

Additionally, a critical bug fix ([f6965b6](https://github.com/fxstein/todo.ai/commit/f6965b6...))
ensures that version updates only replace actual `VERSION=` variable
assignments, not all occurrences throughout the codebase. This prevents
accidental corruption of grep patterns and other code that might contain
version-like strings.
```

**Including commit links in summaries:**

When referencing specific commits in summaries, use this format:
- `([short-hash](https://github.com/user/repo/commit/full-hash))`
- Get the repo URL with: `git remote get-url origin` (convert SSH to HTTPS if needed)
- Get full commit hash: `git rev-parse <short-hash>`
- Example: `The fix ([f6965b6](https://github.com/fxstein/todo.ai/commit/f6965b6a1c2...)) resolves...`

**Guidelines for summary writing:**
- Focus on user-facing benefits and improvements
- Explain what's new and why it matters
- Use 2-3 paragraphs (not too short, not too long)
- Write in plain language (avoid overly technical jargon)
- Highlight the most important changes first
- Optionally include commit links for key changes: `([hash](https://github.com/user/repo/commit/fullhash))`

### Human Review Safeguards

The script automatically requests human review if:
- **Major release**: Breaking changes detected
- **Large release**: More than 10 commits since last release

When review is needed, the script will:
1. Display generated release notes
2. Ask for confirmation before proceeding
3. Allow you to cancel if needed

### Manual Release Steps (Optional)

For manual control, you can still use the process below.

### Manual Release Steps

#### 1. Update Version Number

Update version in `todo.ai`:

```bash
# Set new version (e.g., 1.0.1)
NEW_VERSION="1.0.1"

# Update version in script (both locations)
sed -i '' "s/VERSION=\"[^\"]*\"/VERSION=\"$NEW_VERSION\"/" todo.ai
sed -i '' "s/# Version: [0-9.]*/# Version: $NEW_VERSION/" todo.ai

# Verify changes
grep "VERSION=" todo.ai
```

**Note:** On Linux, use `sed -i` instead of `sed -i ''`

#### 2. Commit Version Changes

```bash
git add todo.ai
git commit -m "Bump version to $NEW_VERSION"
```

#### 3. Create and Push Tag

```bash
git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"
git push origin main
git push origin "v$NEW_VERSION"
```

#### 4. Create GitHub Release with GitHub CLI

```bash
# Create release from notes file
gh release create "v$NEW_VERSION" \
  --title "$NEW_VERSION" \
  --notes-file RELEASE_NOTES.md

# Or create with inline notes
gh release create "v$NEW_VERSION" \
  --title "$NEW_VERSION" \
  --notes "Release notes here"
```

**GitHub CLI automatically:**
- Creates the release on GitHub
- Associates it with the tag
- Publishes it immediately

## Release Notes

### Creating Release Notes

Create a `RELEASE_NOTES.md` file (or use your preferred name):

```markdown
## Release X.Y.Z

### Added
- New feature description

### Changed
- Changed behavior description

### Fixed
- Bug fix description

### Breaking Changes
- Breaking change description (only for major releases)

### Migration Notes
- Instructions for users upgrading (if needed)
```

### Release Notes Template

Use this template for consistent formatting:

```markdown
## Release X.Y.Z

### Added
-

### Changed
-

### Fixed
-

### Breaking Changes
-

### Migration Notes
-
```

## Release Script Details

The `release/release.sh` script is an intelligent, fully automated release tool that:

1. **Automatically determines version** by analyzing commit history
2. **Includes AI-generated summary** (if provided via `--summary` flag)
3. **Generates release notes** from commit messages
4. **Requests human review** when needed (major releases, >10 commits)
5. **Waits for explicit execute** after prepare

**Usage:**
```bash
# Without AI summary
./release/release.sh --prepare
./release/release.sh --execute

# With AI-generated summary
./release/release.sh --prepare --summary release/AI_RELEASE_SUMMARY.md
./release/release.sh --execute
```

**Options:**
- `--prepare`: Analyze commits and generate release preview (default)
- `--execute`: Execute prepared release (no prompts)
- `--abort [version]`: Abort/clean release state (optional version context)
- `--beta`: Create beta/pre-release (e.g., `v1.0.0b1`)
- `--summary <file>` or `-s <file>`: Include AI-generated summary from the specified file (auto-detects `release/AI_RELEASE_SUMMARY.md` if omitted)
- `--set-version <version>`: Override proposed version during prepare (e.g., `3.0.0b3`)
- `--dry-run`: Generate preview without committing or writing prepare state
- `--help` or `-h`: Show usage and exit

**Release Logging:**

All release operations are automatically logged to `release/RELEASE_LOG.log`. The log uses a pipe-delimited format:
- Format: `TIMESTAMP | USER | STEP | MESSAGE`
- Newest entries appear at the top of the file
- Includes timestamp, GitHub user ID, step name, and message for each operation
- Success or failure status for each operation
- Error messages if any step fails
- Release details (version, tag, URL)

This helps debug issues when releases get stuck or fail. Check `release/RELEASE_LOG.log` to see exactly where and why a release might have failed.

**Uncommitted Files Handling:**

The script now properly handles:
- `release/AI_RELEASE_SUMMARY.md` - should be committed before prepare when using AI summaries
- `release/RELEASE_SUMMARY.md` - generated during prepare and **committed** with the version bump
- Other uncommitted files - will block the release (must commit or stash before releasing)

**IMPORTANT:** Release notes and summaries are never allowed as uncommitted changes. Commit `release/AI_RELEASE_SUMMARY.md` before prepare when used, and the script will commit `release/RELEASE_SUMMARY.md` along with the version bump to keep release materials tracked in git.

## Pre-Release Checklist

Before creating a release, ensure:

- [ ] All tests pass (if applicable)
- [ ] README.md is up to date
- [ ] Documentation is current
- [ ] All planned features for this release are complete
- [ ] TODO.md is updated with completed tasks
- [ ] GitHub CLI authenticated (`gh auth status`)
- [ ] **Migrations reviewed** (if any migrations are included in this release)

**Notes:**
- Release notes are automatically generated from commits - no manual preparation needed!
- AI-generated summaries (recommended) should be created by the agent and saved to `release/AI_RELEASE_SUMMARY.md`
- The summary file (`release/RELEASE_SUMMARY.md`) **will be automatically committed** as part of the release process
- **NEVER** allow release notes or summaries to remain uncommitted - they must be committed as part of the release
- All release operations are automatically logged to `release/RELEASE_LOG.log` with detailed timestamps for debugging and auditing

## Migrations in Releases

### Overview

`todo.ai` includes an automatic migration system that runs one-time fixes and cleanups on existing installations when they update. Migrations are registered in the script and execute automatically based on version.

### Adding Migrations to a Release

1. **During Development:**
   - Identify migration needs (e.g., structural fixes, format changes)
   - Write migration function following the pattern in `docs/development/MIGRATION_GUIDE.md`
   - Add migration to the `MIGRATIONS` registry with target version
   - Test migration locally

2. **Before Release:**
   - Review migrations for this release
   - Ensure migrations are idempotent (safe to run multiple times)
   - Verify migration version matches release version
   - Test migration with wrong state (problem exists)
   - Test migration with correct state (problem doesn't exist)
   - Test idempotency (runs twice without issues)

3. **During Release:**
   - Migrations are included automatically in the new version
   - No additional release steps needed
   - Migration will run automatically on user update

4. **Release Notes:**
   - Document migrations in release notes if user-visible
   - Include in "Migration Notes" section
   - Example:
     ```markdown
     ### Migration Notes

     This release includes automatic migrations that will run once on update:

     - **Section Order Fix (v1.3.5):** Automatically reorders TODO.md sections to correct order
     - **Backup Cleanup (v1.4.0):** Removes obsolete .bak files from previous versions
     ```

### Migration Registry

Migrations are registered in `todo.ai` in the `MIGRATIONS` array:

```zsh
declare -a MIGRATIONS=(
    "1.3.5|section_order_fix|Fix TODO.md section order|migrate_section_order"
    "1.4.0|cleanup_old_backups|Remove old .bak files|cleanup_old_backup_files"
)
```

**Format:** `"VERSION|MIGRATION_ID|DESCRIPTION|FUNCTION_NAME"`

### Migration Execution

Migrations run automatically:
- On every script execution (fast check via `.migrated` file)
- After initialization, before main logic
- Only if version >= target version
- Only if not already executed (checked via `.migrated` file)
- Locked to prevent concurrent execution

### Migration Testing

Before including migrations in a release:

1. **Test with wrong state:**
   - Create TODO.md with problem state
   - Run migration
   - Verify it fixes the issue

2. **Test with correct state:**
   - Create TODO.md without problem
   - Run migration
   - Verify it doesn't break anything

3. **Test idempotency:**
   - Run migration
   - Run again
   - Verify second run is skipped (already migrated)

4. **Test version check:**
   - Verify migration runs when version >= target
   - Verify migration doesn't run when version < target

### Documentation

For detailed migration creation instructions, see:
- **Migration Guide:** `docs/development/MIGRATION_GUIDE.md`
- **Design Document:** `docs/design/MIGRATION_SYSTEM_DESIGN.md`

### Example Migration Workflow

1. **Identify need:** Existing installations have wrong section order
2. **Write migration:** Create `migrate_section_order()` function
3. **Test migration:** Verify it fixes the problem
4. **Add to registry:** `"1.3.5|section_order_fix|Fix TODO.md section order|migrate_section_order"`
5. **Test idempotency:** Run twice, verify second run is skipped
6. **Release:** Migration runs automatically when users update to 1.3.5+

## Post-Release Tasks

After creating the release:

- [ ] Verify the release appears on GitHub
- [ ] Test that `./todo.ai update` works and fetches the new version
- [ ] Test that users can install from the raw GitHub URL
- [ ] Update TODO.md with completed release task
- [ ] Mark release task as complete: `./todo.ai complete <task-id>`

### Automated Verification

```bash
# Verify release exists
gh release view "v$NEW_VERSION"

# Verify version in script
curl -s https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai | grep "VERSION="

# Test update (if you have a test installation)
./todo.ai update
./todo.ai version  # Should show new version
```

## Testing the Release

### Test Installation from Raw URL

```bash
# Test that the raw GitHub URL returns the correct version
curl -s https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai | grep "VERSION="
```

### Test Update Command

```bash
# Test update functionality
./todo.ai update
./todo.ai version  # Should show new version
```

## Rollback Process

If a release has critical issues:

1. Create a hotfix commit
2. Bump patch version (e.g., 1.0.1 → 1.0.2)
3. Follow the release steps above
4. Document the issue in the release notes
5. Optionally delete the problematic release:

```bash
gh release delete "v$PROBLEMATIC_VERSION" --yes
```

## Automatic Updates

Users can update `todo.ai` using:

```bash
./todo.ai update
```

This command:
1. Checks the current version
2. Fetches the latest version from GitHub
3. Creates a backup before updating
4. Replaces the script with the new version

The update command uses `SCRIPT_URL` which points to:
```
https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai
```

## Release Frequency

- **Major releases:** As needed for breaking changes
- **Minor releases:** For new features
- **Patch releases:** For bug fixes and urgent issues

Release when ready—no fixed schedule.

## Additional Notes

- The script is a single file (`todo.ai`) distributed via raw GitHub URL
- No build process required—just version bump and tag
- Users install directly from GitHub raw URL
- Version must be updated in both the header comment and VERSION variable
- Always test the update mechanism after releasing
- GitHub CLI automates the entire release workflow
- All releases are created via command-line—no manual GitHub UI steps needed
