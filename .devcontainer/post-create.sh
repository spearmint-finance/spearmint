#!/bin/bash
set -e

echo "==================================="
echo "  Setting up Spearmint Dev Container"
echo "==================================="

# Create Python virtual environment for core-api
if [ ! -d "/workspace/core-api/venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv /workspace/core-api/venv
fi

# Install Python dependencies
echo "Installing Python dependencies..."
source /workspace/core-api/venv/bin/activate
pip install --upgrade pip
pip install -r /workspace/core-api/requirements.txt

# Install web-app frontend dependencies
if [ -f "/workspace/web-app/package.json" ]; then
    echo "Installing web-app dependencies..."
    cd /workspace/web-app
    npm install
    cd /workspace
fi

# Build and link worktree CLI
if [ -f "/workspace/worktree-cli/package.json" ]; then
    echo "Building worktree CLI..."
    cd /workspace/worktree-cli
    npm install
    npm run build
    npm link
    cd /workspace
fi

# Create .worktrees directory
mkdir -p /workspace/.worktrees

echo ""
echo "==================================="
echo "  Setup Complete!"
echo ""
echo "  Core API:     cd core-api && source venv/bin/activate"
echo "  Web App:      cd web-app && npm run dev"
echo "  Worktrees:    worktree --help"
echo "==================================="
