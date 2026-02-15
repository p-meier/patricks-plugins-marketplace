#!/bin/bash
# Setup script for deep-researcher Python environment
# Creates a virtual environment and installs the perplexityai SDK

PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
VENV_DIR="$PLUGIN_DIR/.venv"
REQ_FILE="$PLUGIN_DIR/scripts/requirements.txt"

# Load .env file if present (exports API keys like PERPLEXITY_API_KEY, FIRECRAWL_API_KEY, APIFY_API_KEY)
ENV_FILE="$PLUGIN_DIR/.env"
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "[deep-researcher] Setting up Python environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "[deep-researcher] Error: Failed to create virtual environment. Ensure python3 is installed." >&2
        exit 1
    fi
    "$VENV_DIR/bin/pip" install -q --upgrade pip
    "$VENV_DIR/bin/pip" install -q -r "$REQ_FILE"
    if [ $? -ne 0 ]; then
        echo "[deep-researcher] Error: Failed to install dependencies." >&2
        exit 1
    fi
    echo "[deep-researcher] Python environment ready."
elif [ "$REQ_FILE" -nt "$VENV_DIR/.installed" ] 2>/dev/null; then
    # Re-install if requirements changed
    "$VENV_DIR/bin/pip" install -q -r "$REQ_FILE"
fi

# Mark install time
touch "$VENV_DIR/.installed" 2>/dev/null

# Install global Node CLI tools if missing
if ! command -v firecrawl &>/dev/null; then
    echo "[deep-researcher] Installing firecrawl CLI globally..."
    npm install -g firecrawl-cli 2>&1 || echo "[deep-researcher] Warning: Failed to install firecrawl CLI."
fi

if ! command -v apify &>/dev/null; then
    echo "[deep-researcher] Installing apify CLI globally..."
    npm install -g apify-cli 2>&1 || echo "[deep-researcher] Warning: Failed to install apify CLI."
fi

# Login apify if key is available and not yet logged in
if command -v apify &>/dev/null && [ -n "$APIFY_API_KEY" ]; then
    apify login --token "$APIFY_API_KEY" 2>/dev/null
fi
