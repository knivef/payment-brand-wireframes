#!/usr/bin/env bash
# One-time setup. Creates the GitHub repo, pushes, and links Vercel.
# Run once from the repo root on a machine where `gh` and `vercel` are logged in.
#
#   ./scripts/bootstrap.sh [repo-name] [--public]
#
# Defaults to a private repo named payment-brand-wireframes.

set -euo pipefail
cd "$(dirname "$0")/.."

REPO="${1:-payment-brand-wireframes}"
VIS="--private"
[ "${2:-}" = "--public" ] && VIS="--public"

command -v gh >/dev/null || { echo "gh CLI not found. Install it first: https://cli.github.com"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "gh is not authenticated. Run: gh auth login"; exit 1; }

echo "Running health check first."
./scripts/check.sh

if [ ! -d .git ]; then
  git init -b main
fi

git add -A
git commit -m "Add payment brand wireframe scaffold and prompt chain" || echo "Nothing new to commit."

if git remote get-url origin >/dev/null 2>&1; then
  echo "Remote origin already set. Pushing."
  git push -u origin main
else
  gh repo create "$REPO" $VIS --source=. --remote=origin --push
fi

echo
echo "Repo: $(gh repo view --json url --jq .url)"
echo

if command -v vercel >/dev/null 2>&1; then
  echo "Linking Vercel. Choose framework preset 'Other', no build command, output directory '.'"
  vercel link
  vercel --prod
else
  echo "Vercel CLI not installed. Import the repo at https://vercel.com/new instead."
  echo "Framework preset: Other. Build command: none. Output directory: ."
fi
