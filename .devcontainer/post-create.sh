#!/bin/bash
set -e

echo "==================================="
echo "  Setting up Spearmint Dev Container"
echo "==================================="

# CRITICAL: Fix volume permissions (named volumes created as root)
echo "Fixing volume permissions..."
sudo chown -R $(id -u):$(id -g) /workspace/core-api/venv 2>/dev/null || true
sudo chown -R $(id -u):$(id -g) /workspace/web-app/node_modules 2>/dev/null || true
sudo chown -R $(id -u):$(id -g) /home/vscode/.vscode-server 2>/dev/null || true

# Create Python virtual environment
if [ ! -f "/workspace/core-api/venv/bin/activate" ]; then
    echo "Creating Python virtual environment..."
    python -m venv /workspace/core-api/venv
fi

# Install Python dependencies
echo "Installing Python dependencies..."
/workspace/core-api/venv/bin/pip install --upgrade pip
/workspace/core-api/venv/bin/pip install -r /workspace/core-api/requirements.txt

# Install web-app dependencies
if [ -f "/workspace/web-app/package.json" ]; then
    echo "Installing web-app dependencies..."
    cd /workspace/web-app
    timeout 300 npm install || echo "Warning: npm install timed out or failed"
    cd /workspace
fi

# Add user to docker group for Docker-outside-of-Docker
if [ -S /var/run/docker.sock ]; then
    echo "Configuring Docker access..."
    sudo usermod -aG docker $(whoami) 2>/dev/null || true
fi

echo ""
echo "==================================="
echo "  Setup Complete!"
echo ""
echo "  Core API:     cd core-api && source venv/bin/activate && python run_api.py"
echo "  Web App:      cd web-app && npm run dev"
echo "  Docker:       docker-compose up -d"
echo "==================================="
