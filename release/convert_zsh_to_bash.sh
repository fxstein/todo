#!/bin/bash
# Universal Zsh to Bash Converter for todo.ai
# Handles all known compatibility differences between zsh and bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SOURCE_FILE="${1:-todo.ai}"
TARGET_FILE="${2:-todo.bash}"

if [[ ! -f "$SOURCE_FILE" ]]; then
    echo -e "${RED}Error: Source file '$SOURCE_FILE' not found${NC}"
    exit 1
fi

echo -e "${GREEN}Converting Zsh to Bash: $SOURCE_FILE → $TARGET_FILE${NC}"

# Copy source to target
cp "$SOURCE_FILE" "$TARGET_FILE"

# Conversion 1: Change shebang
echo "  1. Converting shebang..."
sed -i.bak '1s|#!/bin/zsh|#!/bin/bash|' "$TARGET_FILE"

# Conversion 2: Update description comment
echo "  2. Updating description..."
sed -i.bak 's|# TODO List Tracker (Zsh)|# TODO List Tracker (Bash Version)|' "$TARGET_FILE"

# Conversion 3: Convert zsh array key iteration to bash
# Zsh: "${(@k)array_name}" -> Bash: "${!array_name[@]}"
echo "  3. Converting array key iteration syntax..."
sed -i.bak 's|"\${(@k)\([^}]*\)}"|"${!\1[@]}"|g' "$TARGET_FILE"

# Conversion 4: Convert regex capture arrays
# Zsh uses ${match[N]}, Bash uses ${BASH_REMATCH[N]}
# Only convert lines marked with # BASH_CONVERT: BASH_REMATCH[N]
echo "  4. Converting regex capture arrays (match -> BASH_REMATCH)..."
sed -i.bak '/# BASH_CONVERT: BASH_REMATCH\[/s|\${match\[\([0-9]\)\]}|${BASH_REMATCH[\1]}|g' "$TARGET_FILE"

# Conversion 5: Remove 'local' from top-level scope (outside functions)
# Bash requires 'local' to be used only inside functions
# Target specific known locations where 'local' appears at top-level
echo "  5. Removing 'local' from top-level scope (mode display section)..."

# Remove 'local' from mode display block (lines ~6900-6930)
# These are the only places where 'local' appears outside functions
sed -i.bak '/# Display current operating mode/,/^# Main command handler/ {
    s/^    local current_mode=/    current_mode=/
    s/^    local coord_type=/    coord_type=/
    s/^                    local issue_num=/                    issue_num=/
    s/^                    local namespace=/                    namespace=/
}' "$TARGET_FILE"

# Clean up backup files
rm -f "${TARGET_FILE}.bak"

# Verify the conversion
echo ""
echo -e "${GREEN}Conversion complete!${NC}"
echo ""
echo "Verification:"
echo "  Shebang: $(head -1 "$TARGET_FILE")"
echo "  Description: $(grep -m1 "# TODO List Tracker" "$TARGET_FILE")"
echo ""
echo -e "${YELLOW}Testing syntax...${NC}"

# Test bash syntax
if bash -n "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}✅ Bash syntax check passed${NC}"
else
    echo -e "${RED}❌ Bash syntax check failed${NC}"
    echo "Run: bash -n $TARGET_FILE"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Conversion successful: $TARGET_FILE${NC}"
