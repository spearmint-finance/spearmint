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

# Install pre-commit hooks
echo "Setting up pre-commit hooks..."
pip install pre-commit
cd /workspace
pre-commit install

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

# Install global npm packages
echo "Installing global npm packages..."
npm install -g pnpm @memnexus-ai/cli @github/copilot postman-cli @augmentcode/auggie

# Install uv (fast Python package manager)
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Install Claude Code CLI
if ! command -v claude &> /dev/null; then
    echo "Installing Claude Code CLI..."
    curl -fsSL https://claude.ai/install.sh | sh
fi

echo ""
echo "==================================="
echo "  Setup Complete!"
echo ""
echo "  Core API:     cd core-api && source venv/bin/activate"
echo "  Web App:      cd web-app && npm run dev"
echo "  Worktrees:    worktree --help"
echo "==================================="
