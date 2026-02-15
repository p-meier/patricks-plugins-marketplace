#!/bin/bash
# PreToolUse hook: enforces max 5 concurrent external API calls.
# Reads tool input JSON from stdin, checks if it's an external API call,
# then counts running external processes.
# Exit 0 = allow, Exit 2 = block.

MAX_CONCURRENT=5

# Read the tool input from stdin
INPUT=$(cat)

# Extract the bash command from the JSON input
COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)

# Block firecrawl on YouTube URLs — use the youtube skill (Apify) instead
case "$COMMAND" in
    *firecrawl*youtube.com*|*firecrawl*youtu.be*)
        echo "BLOCKED: Do not use firecrawl for YouTube URLs. Consult the youtube skill to download transcripts via Apify CLI."
        exit 2
        ;;
esac

# Check if this is an external API call
IS_EXTERNAL=false
case "$COMMAND" in
    *ppxl*|*firecrawl*|*"apify call"*|*"apify run"*|*"api.apify.com"*|*"api.perplexity.ai"*)
        IS_EXTERNAL=true
        ;;
esac

# If not external, allow immediately
if [ "$IS_EXTERNAL" = false ]; then
    exit 0
fi

# Count currently running external API processes
COUNT=0
COUNT=$((COUNT + $(pgrep -f "ppxl.py" 2>/dev/null | wc -l)))
COUNT=$((COUNT + $(pgrep -f "firecrawl" 2>/dev/null | wc -l)))
COUNT=$((COUNT + $(pgrep -f "apify" 2>/dev/null | wc -l)))

if [ "$COUNT" -ge "$MAX_CONCURRENT" ]; then
    echo "Rate limit: $COUNT/$MAX_CONCURRENT external API calls running. Wait for current calls to complete."
    exit 2
fi

exit 0
