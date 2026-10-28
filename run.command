#!/usr/bin/env bash
# ==============================================================================
#  📸 Photo Booth Station - One-Click Launcher (macOS)
#  Double-click this file in Finder to run. No Terminal or Python setup needed!
# ==============================================================================

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo " 📸 Photo Booth Station (Canon SELPHY CP1500)"
echo "=========================================================="
echo ""

VENV_DIR="$DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python3"

# 1. Fast Path: If local virtual environment already exists and works, launch immediately!
if [ -f "$VENV_PYTHON" ]; then
    exec "$VENV_PYTHON" "$DIR/photobooth.py" "$@"
fi

# 2. First-Time Setup Path
echo "✨ First-time launch detected! Setting up environment automatically..."
echo "⏳ This only takes a few seconds and happens once..."
echo ""

# Find a viable system Python 3
SYSTEM_PY=""
for candidate in python3 /usr/bin/python3 /usr/local/bin/python3 /opt/homebrew/bin/python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
        if "$candidate" -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)" 2>/dev/null; then
            SYSTEM_PY="$(command -v "$candidate")"
            break
        fi
    fi
done

SETUP_SUCCESS=0

# Try creating venv with system Python
if [ -n "$SYSTEM_PY" ]; then
    echo "📦 Creating isolated local environment with $SYSTEM_PY..."
    "$SYSTEM_PY" -m venv "$VENV_DIR" >/dev/null 2>&1
    if [ -f "$VENV_PYTHON" ]; then
        echo "📥 Installing required image processing library (Pillow)..."
        "$VENV_PYTHON" -m pip install --quiet --upgrade pip >/dev/null 2>&1
        "$VENV_PYTHON" -m pip install --quiet Pillow
        if "$VENV_PYTHON" -c "import PIL, tkinter" >/dev/null 2>&1; then
            SETUP_SUCCESS=1
        fi
    fi
fi

# Fallback: If system Python or venv failed / missing pip, use standalone uv runner
if [ $SETUP_SUCCESS -ne 1 ]; then
    echo "⚡ Using standalone portable runner (uv)..."
    if ! command -v uv >/dev/null 2>&1; then
        echo "📥 Downloading standalone runtime (takes ~5-10s)..."
        curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1
        export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
    fi

    if command -v uv >/dev/null 2>&1; then
        uv venv "$VENV_DIR" --quiet >/dev/null 2>&1
        uv pip install --quiet --python "$VENV_PYTHON" Pillow >/dev/null 2>&1
        if [ -f "$VENV_PYTHON" ]; then
            SETUP_SUCCESS=1
        fi
    fi
fi

if [ -f "$VENV_PYTHON" ]; then
    echo "✅ Setup complete! Launching Photo Booth..."
    echo ""
    exec "$VENV_PYTHON" "$DIR/photobooth.py" "$@"
else
    echo "❌ Could not initialize Python environment automatically."
    echo "Please ensure you have an active internet connection on first launch,"
    echo "or install Python 3 from https://www.python.org/downloads/macos/"
    echo ""
    read -n 1 -s -r -p "Press any key to close..."
    echo ""
    exit 1
fi
