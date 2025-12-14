#!/bin/sh
# todo.ai Smart Installer
# Detects your environment and installs the best version for your system
#
# Usage: curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh

set -e

# GitHub repository information
REPO_OWNER="fxstein"
REPO_NAME="todo.ai"
GITHUB_API="https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}"

# Colors for output (if terminal supports it)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0;m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

# Get latest release tag from GitHub API
get_latest_release() {
    # Try to get latest release from GitHub API
    if command -v curl >/dev/null 2>&1; then
        local release_info=$(curl -fsSL "${GITHUB_API}/releases/latest" 2>/dev/null || echo "")
        if [ -n "$release_info" ]; then
            # Extract tag_name from JSON (simple grep/sed, no jq required)
            echo "$release_info" | grep '"tag_name"' | sed -E 's/.*"tag_name": "([^"]+)".*/\1/' | head -1
            return 0
        fi
    elif command -v wget >/dev/null 2>&1; then
        local release_info=$(wget -qO- "${GITHUB_API}/releases/latest" 2>/dev/null || echo "")
        if [ -n "$release_info" ]; then
            echo "$release_info" | grep '"tag_name"' | sed -E 's/.*"tag_name": "([^"]+)".*/\1/' | head -1
            return 0
        fi
    fi

    # No release found
    echo ""
    return 1
}

# Construct download URL for release asset
get_release_asset_url() {
    local tag="$1"
    local filename="$2"
    echo "https://github.com/${REPO_OWNER}/${REPO_NAME}/releases/download/${tag}/${filename}"
}

# Fallback to main branch (for development or if no releases exist)
get_main_branch_url() {
    local filename="$1"
    echo "https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/main/${filename}"
}

echo "${BLUE}todo.ai Smart Installer${NC}"
echo "========================"
echo ""

# Function to get bash version
get_bash_version() {
    if command -v bash >/dev/null 2>&1; then
        bash -c 'echo ${BASH_VERSION%%.*}' 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

# Function to check if zsh is available
has_zsh() {
    command -v zsh >/dev/null 2>&1
}

# Detect operating system
OS="$(uname -s)"
case "$OS" in
    Darwin)
        OS_NAME="macOS"
        ;;
    Linux)
        OS_NAME="Linux"
        ;;
    MINGW*|MSYS*|CYGWIN*)
        OS_NAME="Windows"
        ;;
    *)
        OS_NAME="Unix"
        ;;
esac

echo "🔍 Detected: ${GREEN}${OS_NAME}${NC}"

# Determine which version to install
INSTALL_VERSION=""
INSTALL_URL=""
INSTALL_REASON=""

if [ "$OS" = "Darwin" ]; then
    # macOS - prefer zsh (default on 10.15+)
    if has_zsh; then
        INSTALL_VERSION="zsh"
        INSTALL_URL="$ZSH_URL"
        INSTALL_REASON="zsh is default on modern macOS"
    else
        # Check bash version
        BASH_VER=$(get_bash_version)
        if [ "$BASH_VER" -ge 4 ]; then
            INSTALL_VERSION="bash"
            INSTALL_URL="$BASH_URL"
            INSTALL_REASON="bash ${BASH_VER} detected (requires 4+)"
        else
            echo "${RED}✗ Error: No compatible shell found${NC}"
            echo ""
            echo "todo.ai requires either:"
            echo "  • zsh (recommended for macOS)"
            echo "  • bash 4.0+ (macOS ships with bash 3.2)"
            echo ""
            echo "Install zsh: Already available on macOS 10.15+"
            echo "Or upgrade bash: brew install bash"
            exit 1
        fi
    fi
else
    # Linux/Windows/Unix - prefer bash if 4+, fallback to zsh
    BASH_VER=$(get_bash_version)
    if [ "$BASH_VER" -ge 4 ]; then
        INSTALL_VERSION="bash"
        INSTALL_URL="$BASH_URL"
        INSTALL_REASON="bash ${BASH_VER} detected (requires 4+)"
    elif has_zsh; then
        INSTALL_VERSION="zsh"
        INSTALL_URL="$ZSH_URL"
        INSTALL_REASON="bash 4+ not found, using zsh"
    else
        echo "${RED}✗ Error: No compatible shell found${NC}"
        echo ""
        echo "todo.ai requires either:"
        echo "  • bash 4.0+ (you have bash ${BASH_VER:-0})"
        echo "  • zsh"
        echo ""
        echo "Install options:"
        echo "  Ubuntu/Debian: sudo apt install zsh"
        echo "  RHEL/CentOS: sudo yum install zsh"
        echo "  Or upgrade bash to 4.0+"
        exit 1
    fi
fi

# Determine which file to download based on version
if [ "$INSTALL_VERSION" = "zsh" ]; then
    INSTALL_FILENAME="todo.ai"
else
    INSTALL_FILENAME="todo.bash"
fi

echo "📦 Installing: ${GREEN}${INSTALL_VERSION} version${NC} (${INSTALL_FILENAME})"
echo "   Reason: ${INSTALL_REASON}"
echo ""

# Get latest release tag
echo "🔍 Checking for latest release..."
LATEST_TAG=$(get_latest_release)

if [ -n "$LATEST_TAG" ]; then
    INSTALL_URL=$(get_release_asset_url "$LATEST_TAG" "$INSTALL_FILENAME")
    echo "${GREEN}✓${NC} Latest release: ${LATEST_TAG}"
    echo "📥 Downloading from release..."
else
    echo "${YELLOW}⚠${NC}  No releases found, using main branch (development version)"
    INSTALL_URL=$(get_main_branch_url "$INSTALL_FILENAME")
    echo "📥 Downloading from main branch..."
fi

# Download the appropriate version
if command -v curl >/dev/null 2>&1; then
    if curl -fsSL -o todo.ai "$INSTALL_URL"; then
        echo "${GREEN}✓${NC} Downloaded successfully"
    else
        echo "${RED}✗ Download failed${NC}"
        echo "   URL: $INSTALL_URL"
        exit 1
    fi
elif command -v wget >/dev/null 2>&1; then
    if wget -q -O todo.ai "$INSTALL_URL"; then
        echo "${GREEN}✓${NC} Downloaded successfully"
    else
        echo "${RED}✗ Download failed${NC}"
        echo "   URL: $INSTALL_URL"
        exit 1
    fi
else
    echo "${RED}✗ Error: Neither curl nor wget found${NC}"
    echo "Please install curl or wget and try again"
    exit 1
fi

# Make executable
chmod +x todo.ai
echo "${GREEN}✓${NC} Made executable"

echo ""
echo "${GREEN}✅ Installation complete!${NC}"
echo ""
echo "Get started:"
echo "  ${BLUE}./todo.ai --help${NC}     Show all commands"
echo "  ${BLUE}./todo.ai add \"Fix bug\" '#bug'${NC}     Create a task"
echo ""
echo "📚 Repository: https://github.com/fxstein/todo.ai"
echo ""

# Show version info if installed successfully
if [ -f "./todo.ai" ]; then
    ./todo.ai version 2>/dev/null || true
fi
