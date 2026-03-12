#!/bin/bash
# Start the FastAPI backend server

echo ""
echo "========================================"
echo "  Starting Spearmint API Server"
echo "========================================"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "[WARNING] Virtual environment not detected"
    echo "Attempting to activate .venv..."

    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    else
        echo "[ERROR] Virtual environment not found at .venv"
        echo "Please create it with: python -m venv .venv"
        echo "Then activate it with: source .venv/bin/activate"
        exit 1
    fi
fi

echo "[OK] Virtual environment activated"
echo ""

# Set PYTHONPATH to include core-api directory
export PYTHONPATH="$PWD/core-api:$PYTHONPATH"

# Navigate to core-api directory
cd core-api

# Start the API server with uvicorn
echo "Starting API server..."
echo ""
uvicorn src.financial_analysis.api.main:app --host 0.0.0.0 --port 8000 --reload

# Return to root directory
cd ..
