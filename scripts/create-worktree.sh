#!/bin/bash
set -e

REPO_NAME="scrappers-mock"

if [ -z "$1" ]; then
    echo "Usage: $0 <worktree-name>"
    echo "Example: $0 task1"
    exit 1
fi

WORKTREE_NAME="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MONOREPO_ROOT="$(cd "$REPO_ROOT/.." && pwd)"
WORKTREE_PATH="$MONOREPO_ROOT/worktrees/$REPO_NAME/$WORKTREE_NAME"

mkdir -p "$(dirname "$WORKTREE_PATH")"

cd "$REPO_ROOT"
git worktree add "$WORKTREE_PATH"

echo "Worktree created at: $WORKTREE_PATH"
