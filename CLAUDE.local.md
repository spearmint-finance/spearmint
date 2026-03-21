# Worktree Isolation Context

You are working in an isolated worktree. Follow these rules strictly.

## Your Environment

- **Worktree name:** accounts-20260315
- **Worktree path:** /workspace/.worktrees/accounts-20260315
- **Branch:** worktree/accounts-20260315
- **Slot:** 3

## Critical Rules

1. **Stay in your worktree.** Your working directory is `/workspace/.worktrees/accounts-20260315`. All file paths must be relative to or within this directory.
2. **Never reference `/workspace` directly.** That is the main repo. Use your worktree path instead. For example:
   - Wrong: `cd /workspace/cli` or `npm install --prefix /workspace/cli`
   - Right: `cd /workspace/.worktrees/accounts-20260315/cli` or `npm install --prefix /workspace/.worktrees/accounts-20260315/cli`
3. **Use environment variables** when available: `$CLAUDE_WORKTREE_PATH` points to your worktree root.
4. **Do not switch branches.** Stay on `worktree/accounts-20260315`. Branch switching is blocked.
5. **Do not merge or push to main.** Create a PR instead using `gh pr create`.
6. **Push to your branch** with `git push -u origin worktree/accounts-20260315`.

## Memory Key Scope

This project uses a scoped prefix for all named memories to prevent collisions across projects sharing the same MemNexus account.

- **Project slug:** `spearmint`
- **Named memory key format:** `spearmint-<team>-<type>`
- **Example:** `spearmint-product-leader-state` (never `product-leader-state`)

All `mx memories create --name` and `mx memories update --name` calls MUST use the `spearmint-` prefix. This is enforced — keys without the prefix will collide with other projects on this account.

# currentDate
Today's date is 2026-03-21.
