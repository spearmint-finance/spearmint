#!/bin/bash

# Auto-activate venv in new terminals
if [ -f /workspace/core-api/venv/bin/activate ]; then
    if ! grep -q "source /workspace/core-api/venv/bin/activate" ~/.bashrc 2>/dev/null; then
        echo "source /workspace/core-api/venv/bin/activate" >> ~/.bashrc
    fi
fi

# Configure persistent shell history (if shell-history volume is mounted)
if [ -d /commandhistory ]; then
    touch /commandhistory/.bash_history
    if ! grep -q "HISTFILE=/commandhistory/.bash_history" ~/.bashrc 2>/dev/null; then
        echo 'export HISTFILE=/commandhistory/.bash_history' >> ~/.bashrc
    fi
fi

echo ""
echo "Spearmint Dev Container Ready"
echo "  Start API:        cd core-api && python run_api.py"
echo "  Start Frontend:   cd web-app && npm run dev"
echo ""
