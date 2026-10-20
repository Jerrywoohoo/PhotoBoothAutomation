#!/usr/bin/env bash
# Quick launcher for Photo Booth Print Automation
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="/Applications/miniconda3/bin/python3"

if [ ! -f "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

"$PYTHON_BIN" "$DIR/photobooth.py" "$@"

