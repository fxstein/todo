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

## Automated Release Process

### Quick Release (All-in-One)

Run the automated release script:

```bash
./release.sh <version> <release-notes-file>
```

Or use the manual steps below for more control.

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

## Automated Release Script

Create a `release.sh` script for one-command releases:

```bash
#!/bin/zsh

set -e

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <version> [release-notes-file]"
    echo "Example: $0 1.0.1 RELEASE_NOTES.md"
    exit 1
fi

VERSION="$1"
NOTES_FILE="${2:-RELEASE_NOTES.md}"
TAG="v$VERSION"

echo "🚀 Starting release process for version $VERSION..."

# Verify we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "main" ]]; then
    echo "⚠️  Warning: Not on main branch (current: $CURRENT_BRANCH)"
    read "?Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo "❌ Error: Uncommitted changes detected"
    echo "Please commit or stash changes before releasing"
    exit 1
fi

# Update version in todo.ai
echo "📝 Updating version to $VERSION..."
if [[ "$(uname)" == "Darwin" ]]; then
    sed -i '' "s/VERSION=\"[^\"]*\"/VERSION=\"$VERSION\"/" todo.ai
    sed -i '' "s/# Version: [0-9.]*/# Version: $VERSION/" todo.ai
else
    sed -i "s/VERSION=\"[^\"]*\"/VERSION=\"$VERSION\"/" todo.ai
    sed -i "s/# Version: [0-9.]*/# Version: $VERSION/" todo.ai
fi

# Verify version update
if ! grep -q "VERSION=\"$VERSION\"" todo.ai; then
    echo "❌ Error: Version update failed"
    exit 1
fi

# Commit version change
echo "💾 Committing version change..."
git add todo.ai
git commit -m "Bump version to $VERSION"

# Create and push tag
echo "🏷️  Creating tag $TAG..."
git tag -a "$TAG" -m "Release version $VERSION"
git push origin main
git push origin "$TAG"

# Create GitHub release
echo "📦 Creating GitHub release..."
if [[ -f "$NOTES_FILE" ]]; then
    gh release create "$TAG" \
        --title "$VERSION" \
        --notes-file "$NOTES_FILE"
    echo "✅ Release created with notes from $NOTES_FILE"
else
    echo "⚠️  Release notes file not found: $NOTES_FILE"
    read "?Create release without notes? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        gh release create "$TAG" \
            --title "$VERSION" \
            --notes "Release version $VERSION"
    else
        echo "❌ Release cancelled. Create $NOTES_FILE and try again."
        exit 1
    fi
fi

echo "✅ Release $VERSION published successfully!"
echo "🔗 View release: https://github.com/fxstein/todo.ai/releases/tag/$TAG"
```

**Make it executable:**
```bash
chmod +x release.sh
```

**Usage:**
```bash
./release.sh 1.0.1 RELEASE_NOTES.md
```

## Pre-Release Checklist

Before creating a release, ensure:

- [ ] All tests pass (if applicable)
- [ ] README.md is up to date
- [ ] Documentation is current
- [ ] All planned features for this release are complete
- [ ] TODO.md is updated with completed tasks
- [ ] No breaking changes unless it's a major version
- [ ] Release notes prepared in `RELEASE_NOTES.md`
- [ ] GitHub CLI authenticated (`gh auth status`)

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
