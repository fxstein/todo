#!/bin/zsh
# Pre-commit hook for todo.ai repository
# Validates Markdown, YAML, JSON, and TODO.md files before commit

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track if any errors occurred
errors=0

echo "🔍 Running pre-commit validations..."

# Check for suspicious files with quotes or spaces in the name
# This usually indicates a shell quoting issue in a script or command
suspicious_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E "(todo\.ai[[:space:]]|'|\")")

if [[ -n "$suspicious_files" ]]; then
    echo -e "${RED}❌ Pre-commit check failed!${NC}"
    echo ""
    echo -e "${YELLOW}Found suspicious file(s) with quotes or spaces in the name:${NC}"
    echo "$suspicious_files"
    echo ""
    echo "This usually indicates a shell quoting issue in a script or command."
    echo ""
    echo -e "${YELLOW}Action required:${NC}"
    echo "  1. Remove the suspicious file(s): rm -f \"filename\""
    echo "  2. Investigate the root cause (check recent commands, scripts, release process)"
    echo "  3. Fix any unquoted variables or command substitutions"
    echo "  4. Try committing again"
    echo ""
    exit 1
fi

# Check for actual files in working directory (not just staged)
actual_suspicious=$(ls -1 | grep -E "^todo\.ai[[:space:]]" 2>/dev/null)

if [[ -n "$actual_suspicious" ]]; then
    echo -e "${RED}❌ Pre-commit check failed!${NC}"
    echo ""
    echo -e "${YELLOW}Found suspicious file(s) in working directory:${NC}"
    echo "$actual_suspicious"
    echo ""
    echo "File exists but is not staged. This indicates a quoting/escaping issue."
    echo ""
    echo -e "${YELLOW}Action required:${NC}"
    echo "  1. Delete the file: rm -f \"$actual_suspicious\""
    echo "  2. Investigate which command created it (check:"
    echo "     - Release script (release/release.sh)"
    echo "     - Any cp/mv commands with unquoted variables)"
    echo "     - Command history for 'todo.ai' operations)"
    echo "  3. Fix the root cause before committing"
    echo ""
    exit 1
fi

# Get staged files
staged_files=$(git diff --cached --name-only --diff-filter=ACM)

if [[ -z "$staged_files" ]]; then
    echo "✅ No staged files to validate"
    exit 0
fi

# Validate Markdown files
validate_markdown() {
    local files="$1"
    local file_errors=0
    
    # Check if markdownlint-cli2 is available
    if command -v markdownlint-cli2 >/dev/null 2>&1; then
        for file in $files; do
            if ! markdownlint-cli2 "$file" 2>/dev/null; then
                echo -e "${RED}❌ Markdown linting failed: $file${NC}"
                file_errors=$((file_errors + 1))
            fi
        done
    elif command -v mdl >/dev/null 2>&1; then
        # Fallback to mdl
        for file in $files; do
            if ! mdl "$file" 2>/dev/null; then
                echo -e "${RED}❌ Markdown linting failed: $file${NC}"
                file_errors=$((file_errors + 1))
            fi
        done
    else
        echo -e "${YELLOW}⚠️  No Markdown linter found, skipping Markdown validation${NC}"
        echo "   Install 'markdownlint-cli2' or 'mdl' for Markdown linting"
    fi
    
    return $file_errors
}

# Validate YAML files
validate_yaml() {
    local files="$1"
    local file_errors=0
    
    # Check if yamllint is available
    if command -v yamllint >/dev/null 2>&1; then
        for file in $files; do
            if ! yamllint -d relaxed "$file" 2>/dev/null; then
                echo -e "${RED}❌ YAML linting failed: $file${NC}"
                file_errors=$((file_errors + 1))
            fi
        done
    elif command -v yq >/dev/null 2>&1; then
        # Fallback to yq validation
        for file in $files; do
            if ! yq eval '.' "$file" >/dev/null 2>&1; then
                echo -e "${RED}❌ Invalid YAML: $file${NC}"
                file_errors=$((file_errors + 1))
            fi
        done
    else
        echo -e "${YELLOW}⚠️  No YAML linter found, skipping YAML validation${NC}"
        echo "   Install 'yamllint' or 'yq' for YAML linting"
    fi
    
    return $file_errors
}

# Validate JSON files
validate_json() {
    local files="$1"
    local file_errors=0
    
    # Check if jq is available
    if command -v jq >/dev/null 2>&1; then
        for file in $files; do
            if ! jq empty "$file" 2>/dev/null; then
                echo -e "${RED}❌ Invalid JSON: $file${NC}"
                file_errors=$((file_errors + 1))
            fi
        done
    elif command -v jsonlint >/dev/null 2>&1; then
        # Fallback to jsonlint
        for file in $files; do
            if ! jsonlint "$file" 2>/dev/null; then
                echo -e "${RED}❌ Invalid JSON: $file${NC}"
                file_errors=$((file_errors + 1))
            fi
        done
    else
        # Basic validation: check syntax with Python
        if command -v python3 >/dev/null 2>&1; then
            for file in $files; do
                if ! python3 -m json.tool "$file" >/dev/null 2>&1; then
                    echo -e "${RED}❌ Invalid JSON: $file${NC}"
                    file_errors=$((file_errors + 1))
                fi
            done
        else
            echo -e "${YELLOW}⚠️  No JSON linter found, skipping JSON validation${NC}"
            echo "   Install 'jq', 'jsonlint', or ensure 'python3' is available for JSON linting"
        fi
    fi
    
    return $file_errors
}

# Validate ASCII charts in Markdown files
validate_ascii_charts() {
    local files="$1"
    local file_errors=0
    
    # Check if ascii-guard is available
    if command -v ascii-guard >/dev/null 2>&1; then
        for file in $files; do
            # Only check files that might contain ASCII art (Markdown files)
            if [[ "$file" =~ \.(md|mdc|txt)$ ]]; then
                if ! ascii-guard lint "$file" 2>/dev/null; then
                    echo -e "${RED}❌ ASCII chart linting failed: $file${NC}"
                    file_errors=$((file_errors + 1))
                fi
            fi
        done
    else
        echo -e "${YELLOW}⚠️  ascii-guard not found, skipping ASCII chart validation${NC}"
        echo "   Install 'ascii-guard' for ASCII chart linting: pipx install ascii-guard"
    fi
    
    return $file_errors
}

# Run Python tests if python files are changed
validate_python_tests() {
    local files="$1"
    
    # If no Python files changed, check if pytest config changed
    if [[ -z "$files" ]] && [[ ! -f "pyproject.toml" ]]; then
        return 0
    fi
    
    echo "🧪 Running Python tests..."
    
    # Check if virtual environment exists
    if [[ ! -d ".venv" ]]; then
        echo -e "${YELLOW}⚠️  .venv not found. Skipping Python tests.${NC}"
        echo "   Run 'python3 -m venv .venv && source .venv/bin/activate && pip install pytest' to setup"
        return 0
    fi
    
    # Activate venv and run tests
    # Using a subshell to avoid changing current shell environment
    (
        source .venv/bin/activate
        if ! command -v pytest >/dev/null 2>&1; then
             echo -e "${YELLOW}⚠️  pytest not found in .venv. Skipping tests.${NC}"
             exit 0
        fi
        
        if ! pytest; then
            echo -e "${RED}❌ Python tests failed${NC}"
            exit 1
        fi
    )
    
    # Check exit code of subshell
    if [[ $? -ne 0 ]]; then
        return 1
    fi
    
    return 0
}


# Validate TODO.md
validate_todo() {
    local file_errors=0
    
    # Check if TODO.md exists
    if [[ ! -f "TODO.md" ]]; then
        echo -e "${YELLOW}⚠️  TODO.md not found, skipping validation${NC}"
        return 0
    fi
    
    # Check if todo.ai exists and is executable
    if [[ ! -x "./todo.ai" ]]; then
        echo -e "${YELLOW}⚠️  todo.ai not found or not executable, skipping TODO validation${NC}"
        return 0
    fi
    
    # Run todo.ai --lint
    if ! ./todo.ai --lint 2>/dev/null; then
        echo -e "${RED}❌ TODO.md validation failed${NC}"
        echo "   Run './todo.ai --lint' to see details"
        file_errors=$((file_errors + 1))
    fi
    
    return $file_errors
}

# Validate TODO.md if it's in staged files
if echo "$staged_files" | grep -q "TODO.md"; then
    echo "📋 Validating TODO.md..."
    if ! validate_todo; then
        errors=$((errors + 1))
    else
        echo -e "${GREEN}✅ TODO.md validation passed${NC}"
    fi
fi

# Validate Markdown files (exclude .mdc files - they have YAML front matter)
md_files=$(echo "$staged_files" | grep -E '\.md$' || true)
if [[ -n "$md_files" ]]; then
    echo "📝 Validating Markdown files..."
    if ! validate_markdown "$md_files"; then
        errors=$((errors + 1))
    else
        echo -e "${GREEN}✅ Markdown validation passed${NC}"
    fi
fi

# Validate YAML files (exclude backup files)
yaml_files=$(echo "$staged_files" | grep -E '\.(yml|yaml)$' | grep -v '/backups/' || true)
if [[ -n "$yaml_files" ]]; then
    echo "📄 Validating YAML files..."
    if ! validate_yaml "$yaml_files"; then
        errors=$((errors + 1))
    else
        echo -e "${GREEN}✅ YAML validation passed${NC}"
    fi
fi

# Validate JSON files
json_files=$(echo "$staged_files" | grep -E '\.json$' || true)
if [[ -n "$json_files" ]]; then
    echo "📊 Validating JSON files..."
    if ! validate_json "$json_files"; then
        errors=$((errors + 1))
    else
        echo -e "${GREEN}✅ JSON validation passed${NC}"
    fi
fi

# Validate ASCII charts in Markdown files
md_files_for_ascii=$(echo "$staged_files" | grep -E '\.(md|mdc|txt)$' || true)
if [[ -n "$md_files_for_ascii" ]]; then
    echo "📐 Validating ASCII charts..."
    if ! validate_ascii_charts "$md_files_for_ascii"; then
        errors=$((errors + 1))
    else
        echo -e "${GREEN}✅ ASCII chart validation passed${NC}"
    fi
fi

# Run Python tests if Python files or config changed
py_files=$(echo "$staged_files" | grep -E '\.(py|toml)$' || true)
if [[ -n "$py_files" ]]; then
    if ! validate_python_tests "$py_files"; then
        errors=$((errors + 1))
    else
        echo -e "${GREEN}✅ Python tests passed${NC}"
    fi
fi

# Exit with error if any validations failed
if [[ $errors -gt 0 ]]; then
    echo ""
    echo -e "${RED}❌ Pre-commit validation failed${NC}"
    echo "   Fix errors above and try again"
    echo "   Use 'git commit --no-verify' to bypass (not recommended)"
    exit 1
fi

echo -e "${GREEN}✅ All validations passed${NC}"
exit 0

