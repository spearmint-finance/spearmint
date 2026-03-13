#!/usr/bin/env bash
# worktree-guard.sh — Claude Code PreToolUse hook
# Blocks dangerous git operations in worktrees.
# Customise this file for your project's safety requirements.

set -euo pipefail

TOOL_NAME="${CLAUDE_TOOL_NAME:-}"
TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"

if [[ "$TOOL_NAME" != "Bash" ]]; then
  exit 0
fi

# Block checkout/switch to base branch
if echo "$TOOL_INPUT" | grep -qE 'git (checkout|switch) (main|master|develop)'; then
  echo "Blocked: cannot switch to base branch from a worktree." >&2
  exit 1
fi

# Block force push to base branch
if echo "$TOOL_INPUT" | grep -qE 'git push .*(--force|-f).*(main|master|develop)'; then
  echo "Blocked: force push to base branch is not allowed." >&2
  exit 1
fi

exit 0
