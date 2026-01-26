#!/bin/bash
set -e

echo "==================================="
echo "  Setting up Spearmint Dev Container"
echo "==================================="

# CRITICAL: Fix volume permissions (named volumes created as root)
echo "Fixing volume permissions..."
sudo chown -R $(id -u):$(id -g) /workspace/core-api/venv 2>/dev/null || true
sudo chown -R $(id -u):$(id -g) /workspace/web-app/node_modules 2>/dev/null || true
sudo chown -R $(id -u):$(id -g) /workspace/worktree-cli/node_modules 2>/dev/null || true
sudo chown -R $(id -u):$(id -g) /workspace/worktree-cli/dist 2>/dev/null || true
sudo chown -R $(id -u):$(id -g) /home/vscode/.vscode-server 2>/dev/null || true

# Create Python virtual environment
# CRITICAL: Check for bin/activate, not just directory existence
if [ ! -f "/workspace/core-api/venv/bin/activate" ]; then
    echo "Creating Python virtual environment..."
    python -m venv /workspace/core-api/venv
fi

# Install Python dependencies
echo "Installing Python dependencies..."
/workspace/core-api/venv/bin/pip install --upgrade pip
/workspace/core-api/venv/bin/pip install -r /workspace/core-api/requirements.txt

# Install pre-commit hooks
echo "Setting up pre-commit hooks..."
/workspace/core-api/venv/bin/pip install pre-commit
cd /workspace
/workspace/core-api/venv/bin/pre-commit install || true

# Install web-app dependencies (with timeout to prevent hanging)
if [ -f "/workspace/web-app/package.json" ]; then
    echo "Installing web-app dependencies..."
    cd /workspace/web-app
    timeout 300 npm install || echo "Warning: npm install timed out or failed"
    cd /workspace
fi

# Build and link worktree CLI
if [ -f "/workspace/worktree-cli/package.json" ]; then
    echo "Building worktree CLI..."
    cd /workspace/worktree-cli
    timeout 120 npm install || echo "Warning: npm install timed out"
    npm run build
    # CRITICAL: sudo required for npm link (global installs to /usr/local/share/nvm/)
    sudo npm link
    cd /workspace
fi

# Create .worktrees directory
mkdir -p /workspace/.worktrees

# Install optional global tools (non-blocking with timeouts)
echo "Installing optional CLI tools..."
timeout 60 npm install -g pnpm 2>/dev/null || echo "Note: pnpm not installed"

# Install uv (Python package manager - REQUIRED for sandboxing)
echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
# Add uv to PATH for current and future sessions
if [ -f "$HOME/.local/bin/env" ]; then
    source "$HOME/.local/bin/env"
    # Also add to bashrc for future terminals
    if ! grep -q 'source.*\.local/bin/env' ~/.bashrc 2>/dev/null; then
        echo 'source "$HOME/.local/bin/env"' >> ~/.bashrc
    fi
fi
echo "uv version: $(uv --version)"

# Install Claude Code CLI
echo "Installing Claude Code..."
curl -fsSL https://claude.ai/install.sh | bash
# Add claude to PATH
if [ -f "$HOME/.claude/bin/claude" ]; then
    if ! grep -q 'export PATH="\$HOME/.claude/bin:\$PATH"' ~/.bashrc 2>/dev/null; then
        echo 'export PATH="$HOME/.claude/bin:$PATH"' >> ~/.bashrc
    fi
    export PATH="$HOME/.claude/bin:$PATH"
fi

# Install AI coding assistants (global npm packages)
echo "Installing AI coding assistants..."
sudo npm install -g @augmentcode/auggie || echo "Note: auggie install failed"
sudo npm install -g @github/copilot || echo "Note: copilot install failed"

# Install MemNexus CLI
echo "Installing MemNexus CLI..."
sudo npm install -g @memnexus-ai/cli || echo "Note: mx install failed"

# Add user to docker group for Docker-outside-of-Docker
if [ -S /var/run/docker.sock ]; then
    echo "Configuring Docker access..."
    sudo usermod -aG docker $(whoami) 2>/dev/null || true
fi

echo ""
echo "==================================="
echo "  Setup Complete!"
echo ""
echo "  Core API:     cd core-api && source venv/bin/activate"
echo "  Web App:      cd web-app && npm run dev"
echo "  Worktrees:    worktree --help"
echo "==================================="
