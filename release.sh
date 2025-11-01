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

