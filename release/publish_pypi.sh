#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}📦 Preparing PyPI Package...${NC}"

# 1. Install build tools
echo -e "${YELLOW}Installing build tools...${NC}"
pip install --upgrade build twine

# 2. Clean previous builds
echo -e "${YELLOW}Cleaning previous builds...${NC}"
rm -rf dist/ build/ *.egg-info

# 3. Build
echo -e "${YELLOW}Building package...${NC}"
python3 -m build

# 4. Check
echo -e "${YELLOW}Verifying package metadata...${NC}"
python3 -m twine check dist/*

echo -e "${GREEN}✅ Build successful!${NC}"
echo ""
echo -e "${YELLOW}To publish to PyPI, run:${NC}"
echo "python3 -m twine upload dist/*"
echo ""
echo -e "${YELLOW}To publish to TestPyPI (recommended first), run:${NC}"
echo "python3 -m twine upload --repository testpypi dist/*"
