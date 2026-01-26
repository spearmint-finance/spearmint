#!/bin/bash
# Start Spearmint Dev Container
# Run this script before opening in VS Code

echo "Starting Spearmint Dev Container..."

cd "$(dirname "$0")/.."

docker compose -f .devcontainer/docker-compose.yml up -d

if [ $? -eq 0 ]; then
    echo ""
    echo "Container started successfully!"
    echo ""
    echo "Next steps:"
    echo "  1. Open VS Code"
    echo "  2. Press Ctrl+Shift+P"
    echo "  3. Select 'Dev Containers: Attach to Running Container'"
    echo "  4. Choose 'devcontainer-app-1'"
    echo ""
else
    echo "Failed to start container. Check Docker Desktop is running."
fi
