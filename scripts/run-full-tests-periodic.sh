#!/bin/bash
# Run full test suite every 10th commit
# Used by pre-commit hook to periodically catch integration test failures

COUNTER_FILE=".ai-todo/.commit-count"
INTERVAL=10

# Ensure directory exists
mkdir -p .ai-todo

# Read current count (default to 0)
COUNT=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)
COUNT=$((COUNT + 1))
echo "$COUNT" > "$COUNTER_FILE"

# Check if it's time for full tests
if [ $((COUNT % INTERVAL)) -eq 0 ]; then
    echo "🧪 Running full test suite (commit #$COUNT)..."
    uv run pytest
    exit $?
else
    NEXT_FULL=$((((COUNT / INTERVAL) + 1) * INTERVAL))
    echo "⏭️  Skipping full tests (commit #$COUNT, next full run at #$NEXT_FULL)"
    exit 0
fi
