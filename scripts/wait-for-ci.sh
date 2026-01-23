#!/bin/zsh
# wait-for-ci.sh - Wait for all CI/CD workflows to complete
# Usage: ./scripts/wait-for-ci.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Checking CI/CD status...${NC}"
echo ""

# Get all running or queued workflows
WORKFLOWS=$(gh run list --limit 10 --json name,status,conclusion,event \
    --jq '.[] | select(.status != "completed") | .name' | sort -u)

if [ -z "$WORKFLOWS" ]; then
    # Check latest completed run only
    LATEST=$(gh run list --limit 1 --json name,status,conclusion \
        --jq '.[] | select(.status == "completed")')

    # FIX: Check if LATEST is empty (no completed workflows to verify)
    if [ -z "$LATEST" ]; then
        echo -e "${YELLOW}⚠️  No completed workflows found to verify${NC}"
        echo ""
        echo -e "${YELLOW}This could mean:${NC}"
        echo -e "${YELLOW}  - No workflows have run yet${NC}"
        echo -e "${YELLOW}  - Workflows are disabled${NC}"
        echo -e "${YELLOW}  - Repository is new and hasn't triggered CI/CD${NC}"
        echo ""
        echo -e "${RED}❌ Cannot verify CI/CD status - aborting for safety${NC}"
        echo ""
        echo -e "${YELLOW}To proceed, you must:${NC}"
        echo -e "${YELLOW}  1. Ensure CI/CD workflows are enabled${NC}"
        echo -e "${YELLOW}  2. Trigger a workflow (push a commit or create a PR)${NC}"
        echo -e "${YELLOW}  3. Wait for at least one workflow to complete${NC}"
        echo -e "${YELLOW}  4. Run this script again${NC}"
        exit 1
    fi

    CONCLUSION=$(echo "$LATEST" | grep -o '"conclusion":"[^"]*"' | cut -d'"' -f4)
    if [ "$CONCLUSION" = "success" ]; then
        echo -e "${GREEN}✅ All workflows completed successfully!${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️  Some workflows completed with failures${NC}"
        echo ""
        gh run list --limit 1 --json name,status,conclusion \
            --jq '.[] | "\(.name): \(.conclusion)"'
        exit 1
    fi
fi

# Monitor each workflow
echo -e "${YELLOW}Active workflows:${NC}"
echo "$WORKFLOWS" | sed 's/^/  - /'
echo ""

# Wait for all workflows to complete
TIMEOUT=600  # 10 minutes total
POLL_INTERVAL=10
ELAPSED=0

while [ $ELAPSED -lt $TIMEOUT ]; do
    RUNNING=$(gh run list --limit 10 --json name,status \
        --jq '.[] | select(.status != "completed") | .name' | wc -l | tr -d ' ')

    if [ "$RUNNING" -eq 0 ]; then
        # All workflows completed, check conclusions
        echo ""
        FAILURES=$(gh run list --limit 5 --json name,status,conclusion \
            --jq '.[] | select(.conclusion != "success") | .name' | wc -l | tr -d ' ')

        if [ "$FAILURES" -eq 0 ]; then
            echo -e "${GREEN}✅ All workflows completed successfully!${NC}"
            exit 0
        else
            echo -e "${RED}❌ Some workflows failed!${NC}"
            echo ""
            gh run list --limit 5 --json name,status,conclusion \
                --jq '.[] | select(.conclusion != "success") | "\(.name): \(.conclusion)"'
            exit 1
        fi
    fi

    # Show progress
    ELAPSED_MIN=$((ELAPSED / 60))
    ELAPSED_SEC=$((ELAPSED % 60))
    printf "\r${BLUE}⏳ Waiting for ${RUNNING} workflow(s)${NC} [%02d:%02d]" $ELAPSED_MIN $ELAPSED_SEC

    sleep $POLL_INTERVAL
    ELAPSED=$((ELAPSED + POLL_INTERVAL))
done

# Timeout
echo ""
echo -e "${RED}❌ Timeout waiting for workflows${NC}"
exit 4
