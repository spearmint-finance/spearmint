#!/bin/bash
# Periodic work history logger for Notion
# Usage: ./scripts/log_work.sh

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📝 Work History Logger${NC}\n"

# Prompt for work details
read -p "What did you work on? " TITLE
read -p "Description (optional): " DESCRIPTION
read -p "Hours spent (optional): " DURATION
read -p "Tags (comma-separated, optional): " TAGS
read -p "Status [Completed]: " STATUS
STATUS=${STATUS:-Completed}

# Build command
CMD="python -m spearmint_cli.main notion add \"$TITLE\""

if [ -n "$DESCRIPTION" ]; then
    CMD="$CMD --desc \"$DESCRIPTION\""
fi

if [ -n "$DURATION" ]; then
    CMD="$CMD --duration $DURATION"
fi

if [ -n "$TAGS" ]; then
    CMD="$CMD --tags \"$TAGS\""
fi

CMD="$CMD --status \"$STATUS\""

# Execute
cd "$(dirname "$0")/../cli"
eval $CMD

echo -e "\n${GREEN}✓ Work logged to Notion!${NC}"
