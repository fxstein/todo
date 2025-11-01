# Release Process for todo.ai

This document outlines the process for creating releases of `todo.ai` on GitHub.

## Version Numbering

`todo.ai` uses [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes, backward compatible

Current version format in `todo.ai`:
```zsh
VERSION="1.0.0"
```

## Pre-Release Checklist

Before creating a release, ensure:

- [ ] All tests pass (if applicable)
- [ ] README.md is up to date
- [ ] Documentation is current
- [ ] All planned features for this release are complete
- [ ] TODO.md is updated with completed tasks
- [ ] No breaking changes unless it's a major version
- [ ] Version number updated in `todo.ai` script (line 38)
- [ ] Version comment updated in `todo.ai` script (line 21)

## Release Steps

### 1. Update Version Number

Edit `todo.ai` and update the version:

```zsh
# Line 21 (in header comment)
# Version: 1.0.1

# Line 38 (in VERSION variable)
VERSION="1.0.1"
```

### 2. Commit Version Changes

```bash
git add todo.ai
git commit -m "Bump version to X.Y.Z"
```

### 3. Create a Git Tag

Tag the release with the version number:

```bash
git tag -a v1.0.1 -m "Release version 1.0.1"
```

**Tag naming convention:** `v` prefix followed by version number (e.g., `v1.0.1`)

### 4. Push Changes and Tag

```bash
git push origin main
git push origin v1.0.1
```

### 5. Create GitHub Release

1. Go to GitHub repository: https://github.com/fxstein/todo.ai
2. Click "Releases" in the right sidebar
3. Click "Create a new release"
4. Select the tag you just created (e.g., `v1.0.1`)
5. Set release title to the version number (e.g., `1.0.1`)
6. Add release notes describing:
   - New features
   - Bug fixes
   - Breaking changes (if any)
   - Migration notes (if needed)
7. Click "Publish release"

## Release Notes Template

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

## Post-Release Tasks

After creating the release:

- [ ] Verify the release appears on GitHub
- [ ] Test that `./todo.ai update` works and fetches the new version
- [ ] Test that users can install from the raw GitHub URL
- [ ] Update TODO.md with completed release task
- [ ] Mark release task as complete: `./todo.ai complete <task-id>`

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

