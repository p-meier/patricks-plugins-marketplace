#!/bin/bash
# Validates the deep-researcher environment: venv, dependencies, API keys, tools.
# Run this before any research operation. Exits 0 if ready, 1 if critical issues found.

PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
ERRORS=0
WARNINGS=0

# --- Step 1: Run setup (venv + deps + .env) ---
bash "$PLUGIN_DIR/scripts/setup.sh" 2>&1
if [ $? -ne 0 ]; then
    echo "FAIL: Setup script failed. Check Python 3.9+ is installed."
    exit 1
fi

# --- Step 2: Check API keys ---
# Load .env if not already loaded
ENV_FILE="$PLUGIN_DIR/.env"
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
fi

if [ -z "$PERPLEXITY_API_KEY" ]; then
    echo "FAIL: PERPLEXITY_API_KEY not set. Add it to $PLUGIN_DIR/.env or export it."
    ERRORS=$((ERRORS + 1))
else
    echo "OK: PERPLEXITY_API_KEY is set."
fi

if [ -z "$FIRECRAWL_API_KEY" ]; then
    echo "WARN: FIRECRAWL_API_KEY not set. Firecrawl scraping will not work."
    WARNINGS=$((WARNINGS + 1))
else
    echo "OK: FIRECRAWL_API_KEY is set."
fi

if [ -z "$APIFY_API_KEY" ]; then
    echo "WARN: APIFY_API_KEY not set. YouTube transcripts and LinkedIn scraping will not work."
    WARNINGS=$((WARNINGS + 1))
else
    echo "OK: APIFY_API_KEY is set."
fi

# --- Step 3: Check ppxl works (import test) ---
PPXL_TEST=$("$PLUGIN_DIR/.venv/bin/python" -c "from perplexity import Perplexity; print('OK')" 2>&1)
if [ "$PPXL_TEST" = "OK" ]; then
    echo "OK: Perplexity SDK loaded."
else
    echo "FAIL: Perplexity SDK import failed: $PPXL_TEST"
    ERRORS=$((ERRORS + 1))
fi

# --- Step 4: Live Perplexity test (small search) ---
if [ -n "$PERPLEXITY_API_KEY" ] && [ "$PPXL_TEST" = "OK" ]; then
    PPXL_LIVE=$("$PLUGIN_DIR/scripts/ppxl" search "test" --max-results 1 2>&1)
    if echo "$PPXL_LIVE" | grep -qi "error\|traceback\|exception\|failed"; then
        echo "FAIL: Perplexity live test failed: $(echo "$PPXL_LIVE" | head -3)"
        ERRORS=$((ERRORS + 1))
    else
        echo "OK: Perplexity live test passed."
    fi
fi

# --- Step 5: Check firecrawl CLI ---
if command -v firecrawl &>/dev/null; then
    echo "OK: firecrawl CLI available."
else
    echo "WARN: firecrawl CLI not found. Install with: npm install -g firecrawl"
    WARNINGS=$((WARNINGS + 1))
fi

# --- Step 6: Check apify CLI ---
if command -v apify &>/dev/null; then
    echo "OK: apify CLI available."
else
    echo "WARN: apify CLI not found. Install with: npm install -g apify-cli"
    WARNINGS=$((WARNINGS + 1))
fi

# --- Summary ---
echo ""
if [ $ERRORS -gt 0 ]; then
    echo "RESULT: $ERRORS error(s), $WARNINGS warning(s). Fix errors before starting research."
    exit 1
else
    echo "RESULT: Ready. $WARNINGS warning(s)."
    exit 0
fi
