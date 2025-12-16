#!/bin/bash
# Check for forbidden flags in shell scripts and workflows
# This prevents dangerous shortcuts from entering the codebase

set -e

# Build the forbidden flag using string concatenation to avoid self-detection
FORBIDDEN="--no-""verify"

# Color codes
RED='\033[0;31m'
NC='\033[0m' # No Color

# Files to check (passed as arguments by pre-commit, or default to all)
FILES="${@}"
if [[ -z "$FILES" ]]; then
    FILES=$(find release/ .github/ scripts/ -type f \( -name "*.sh" -o -name "*.yml" -o -name "*.yaml" \))
fi

# Search for the forbidden flag
FOUND=0
for file in $FILES; do
    if [[ -f "$file" ]] && grep -q "$FORBIDDEN" "$file" 2>/dev/null; then
        echo -e "${RED}ERROR: Found forbidden flag '$FORBIDDEN' in: $file${NC}"
        FOUND=1
    fi
done

if [[ $FOUND -eq 1 ]]; then
    echo ""
    echo -e "${RED}CRITICAL: The flag '$FORBIDDEN' is ETERNALLY FORBIDDEN.${NC}"
    echo -e "${RED}It bypasses all pre-commit hooks and safety checks.${NC}"
    echo -e "${RED}No automated process may use it without explicit human approval.${NC}"
    exit 1
fi

exit 0
