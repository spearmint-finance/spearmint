#!/bin/bash

# Auto-activate venv in new terminals
if ! grep -q "source /workspace/core-api/venv/bin/activate" ~/.bashrc; then
    echo "source /workspace/core-api/venv/bin/activate" >> ~/.bashrc
fi

echo ""
echo "==================================="
echo "  Spearmint Dev Container Ready"
echo "==================================="
echo ""
echo "  Create a worktree:  worktree create"
echo "  List worktrees:     worktree list"
echo "  Start core API:     cd core-api && python -m uvicorn src.financial_analysis.api.main:app --reload"
echo "  Start web app:      cd web-app && npm run dev"
echo ""
