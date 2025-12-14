#!/bin/zsh
# Setup script for installing linting tools required for git hooks
# This script detects available package managers and installs the recommended linters

set -e

echo "🔍 Setting up linting tools for git hooks..."
echo ""

# Track installation results
installed_tools=()
skipped_tools=()
failed_tools=()

# Check and install markdownlint-cli2 or mdl
install_markdown_linter() {
    echo "📝 Checking Markdown linter..."

    # Check if already installed
    if command -v markdownlint-cli2 >/dev/null 2>&1; then
        echo "   ✅ markdownlint-cli2 already installed"
        installed_tools+=("markdownlint-cli2")
        return 0
    elif command -v mdl >/dev/null 2>&1; then
        echo "   ✅ mdl already installed"
        installed_tools+=("mdl")
        return 0
    fi

    # Try to install markdownlint-cli2 (preferred)
    if command -v npm >/dev/null 2>&1; then
        echo "   📦 Installing markdownlint-cli2 via npm..."
        if npm install -g markdownlint-cli2 2>/dev/null; then
            echo "   ✅ markdownlint-cli2 installed successfully"
            installed_tools+=("markdownlint-cli2")
            return 0
        fi
    fi

    # Fallback to mdl
    if command -v gem >/dev/null 2>&1; then
        echo "   📦 Installing mdl via gem..."
        if gem install mdl 2>/dev/null; then
            echo "   ✅ mdl installed successfully"
            installed_tools+=("mdl")
            return 0
        fi
    fi

    echo "   ⚠️  No package manager found (npm or gem)"
    skipped_tools+=("Markdown linter (markdownlint-cli2 or mdl)")
    return 1
}

# Check and install yamllint or yq
install_yaml_linter() {
    echo "📄 Checking YAML linter..."

    # Check if already installed
    if command -v yamllint >/dev/null 2>&1; then
        echo "   ✅ yamllint already installed"
        installed_tools+=("yamllint")
        return 0
    elif command -v yq >/dev/null 2>&1; then
        echo "   ✅ yq already installed"
        installed_tools+=("yq")
        return 0
    fi

    # Try to install yamllint (preferred)
    if command -v pip3 >/dev/null 2>&1; then
        echo "   📦 Installing yamllint via pip3..."
        if pip3 install yamllint 2>/dev/null; then
            echo "   ✅ yamllint installed successfully"
            installed_tools+=("yamllint")
            return 0
        fi
    elif command -v pip >/dev/null 2>&1; then
        echo "   📦 Installing yamllint via pip..."
        if pip install yamllint 2>/dev/null; then
            echo "   ✅ yamllint installed successfully"
            installed_tools+=("yamllint")
            return 0
        fi
    fi

    # Fallback to yq (brew)
    if command -v brew >/dev/null 2>&1; then
        echo "   📦 Installing yq via brew..."
        if brew install yq 2>/dev/null; then
            echo "   ✅ yq installed successfully"
            installed_tools+=("yq")
            return 0
        fi
    fi

    # Fallback to yq (apt-get) - requires sudo, so we'll just warn
    if command -v apt-get >/dev/null 2>&1; then
        echo "   ⚠️  yq available via apt-get but requires sudo"
        echo "   Run manually: sudo apt-get install -y yq"
    fi

    echo "   ⚠️  No package manager found (pip3, pip, or brew)"
    skipped_tools+=("YAML linter (yamllint or yq)")
    return 1
}

# Check and install jq or jsonlint
install_json_linter() {
    echo "📊 Checking JSON linter..."

    # Check if already installed
    if command -v jq >/dev/null 2>&1; then
        echo "   ✅ jq already installed"
        installed_tools+=("jq")
        return 0
    elif command -v jsonlint >/dev/null 2>&1; then
        echo "   ✅ jsonlint already installed"
        installed_tools+=("jsonlint")
        return 0
    elif command -v python3 >/dev/null 2>&1; then
        echo "   ✅ python3 available (can use json.tool as fallback)"
        installed_tools+=("python3 (json.tool)")
        return 0
    fi

    # Try to install jq (preferred)
    if command -v brew >/dev/null 2>&1; then
        echo "   📦 Installing jq via brew..."
        if brew install jq 2>/dev/null; then
            echo "   ✅ jq installed successfully"
            installed_tools+=("jq")
            return 0
        fi
    elif command -v apt-get >/dev/null 2>&1; then
        echo "   ⚠️  jq available via apt-get but requires sudo"
        echo "   Run manually: sudo apt-get install -y jq"
    elif command -v dnf >/dev/null 2>&1; then
        echo "   ⚠️  jq available via dnf but requires sudo"
        echo "   Run manually: sudo dnf install -y jq"
    elif command -v pacman >/dev/null 2>&1; then
        echo "   ⚠️  jq available via pacman but requires sudo"
        echo "   Run manually: sudo pacman -S jq"
    fi

    # Fallback to jsonlint
    if command -v npm >/dev/null 2>&1; then
        echo "   📦 Installing jsonlint via npm..."
        if npm install -g jsonlint 2>/dev/null; then
            echo "   ✅ jsonlint installed successfully"
            installed_tools+=("jsonlint")
            return 0
        fi
    fi

    # Final fallback: python3 json.tool
    if command -v python3 >/dev/null 2>&1; then
        echo "   ✅ python3 available (can use json.tool as fallback)"
        installed_tools+=("python3 (json.tool)")
        return 0
    fi

    echo "   ⚠️  No package manager found and python3 not available"
    skipped_tools+=("JSON linter (jq, jsonlint, or python3)")
    return 1
}

# Check and install ascii-guard
install_ascii_guard() {
    echo "📐 Checking ASCII chart linter (ascii-guard)..."

    # Check if already installed
    if command -v ascii-guard >/dev/null 2>&1; then
        echo "   ✅ ascii-guard already installed"
        installed_tools+=("ascii-guard")
        return 0
    fi

    # Try to install via pipx (preferred - isolated environment)
    if command -v pipx >/dev/null 2>&1; then
        echo "   📦 Installing ascii-guard via pipx (isolated environment)..."
        if pipx install ascii-guard 2>/dev/null; then
            echo "   ✅ ascii-guard installed successfully"
            installed_tools+=("ascii-guard")
            return 0
        fi
    fi

    # Check if pipx needs to be installed first
    if command -v pip3 >/dev/null 2>&1; then
        echo "   ⚠️  pipx not found, but pip3 is available"
        echo "   Install pipx first: pip3 install --user pipx && pipx ensurepath"
        echo "   Then install ascii-guard: pipx install ascii-guard"
    elif command -v pip >/dev/null 2>&1; then
        echo "   ⚠️  pipx not found, but pip is available"
        echo "   Install pipx first: pip install --user pipx && pipx ensurepath"
        echo "   Then install ascii-guard: pipx install ascii-guard"
    else
        echo "   ⚠️  No Python package manager found"
    fi

    skipped_tools+=("ASCII chart linter (ascii-guard)")
    return 1
}

# Run installations
install_markdown_linter
echo ""
install_yaml_linter
echo ""
install_json_linter
echo ""
install_ascii_guard
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Installation Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [[ ${#installed_tools[@]} -gt 0 ]]; then
    echo "✅ Installed/Available tools:"
    for tool in "${installed_tools[@]}"; do
        echo "   - $tool"
    done
    echo ""
fi

if [[ ${#skipped_tools[@]} -gt 0 ]]; then
    echo "⚠️  Tools that could not be installed (no package manager):"
    for tool in "${skipped_tools[@]}"; do
        echo "   - $tool"
    done
    echo ""
    echo "💡 Manual installation required - see docs/GIT_HOOKS_DESIGN.md for instructions"
    echo ""
fi

# Install git hooks
echo "🔧 Installing git hooks..."
if [[ -f "scripts/setup-git-hooks.sh" ]]; then
    ./scripts/setup-git-hooks.sh
else
    echo "   ⚠️  scripts/setup-git-hooks.sh not found"
    echo "   Run manually: ./scripts/setup-git-hooks.sh"
fi

echo ""
echo "✅ Setup complete!"
