#!/usr/bin/env bash
# Commit and push every change to the canonical repo.
#
#   ./scripts/sync.sh "Add Card Payz homepage"
#
# Runs the health check first and refuses to push if it fails. Wires the remote
# on first run. Handles the case where the remote already has commits this
# folder does not share, which is what happens the first time a local copy that
# was never cloned tries to push.

set -uo pipefail
cd "$(dirname "$0")/.."

REMOTE="https://github.com/knivef/payment-brand-wireframes.git"
BRANCH="main"

MSG="${1:-}"
if [ -z "$MSG" ]; then
  echo "Usage: ./scripts/sync.sh \"commit message, imperative, one line, no em dashes\""
  exit 1
fi
if printf '%s' "$MSG" | grep -q "$(printf '\342\200\224')"; then
  echo "Commit message contains an em dash. Rewrite it."
  exit 1
fi

echo "1. Health check"
./scripts/check.sh || { echo; echo "check.sh failed. Nothing pushed."; exit 1; }
echo

echo "2. Git"
FIRST_RUN=0
if [ ! -d .git ]; then
  git init -b "$BRANCH" >/dev/null
  FIRST_RUN=1
  echo "  initialised a repository on $BRANCH"
fi

CURRENT=$(git symbolic-ref --short HEAD 2>/dev/null || echo "$BRANCH")
[ "$CURRENT" != "$BRANCH" ] && { echo "  on branch $CURRENT, pushing there"; BRANCH="$CURRENT"; }

if git remote get-url origin >/dev/null 2>&1; then
  HAVE=$(git remote get-url origin)
  if [ "${HAVE%.git}" != "${REMOTE%.git}" ]; then
    echo "  origin points at $HAVE"
    echo "  expected       $REMOTE"
    echo "  Fix or remove the remote, then run this again. Nothing pushed."
    exit 1
  fi
  echo "  origin ok"
else
  git remote add origin "$REMOTE"
  echo "  added origin $REMOTE"
fi

echo
echo "3. Reconcile with the remote"
if ! git fetch origin "$BRANCH" --quiet 2>/dev/null; then
  echo "  remote branch $BRANCH does not exist yet, or the repo is empty"
  REMOTE_HAS=0
else
  REMOTE_HAS=1
fi

if [ "$REMOTE_HAS" = "1" ]; then
  AHEAD=$(git rev-list --count HEAD..origin/"$BRANCH" 2>/dev/null || echo 0)
  BASE=$(git merge-base HEAD origin/"$BRANCH" 2>/dev/null || echo "")

  if [ -z "$BASE" ]; then
    # No shared history. This folder was created separately from the repo.
    echo
    echo "  The remote has commits this folder does not share."
    echo "  Nothing has been pushed, and nothing has been changed locally."
    echo
    echo "  Pick one:"
    echo
    echo "  A. Keep the remote history and replay this folder on top. Recommended."
    echo "       git fetch origin $BRANCH"
    echo "       git reset --soft origin/$BRANCH   # keeps every file as it is now"
    echo "       git add -A"
    echo "       git commit -m \"$MSG\""
    echo "       git push origin $BRANCH"
    echo
    echo "  B. Start clean from the remote, then copy this folder's work in."
    echo "       cd .. && git clone $REMOTE fresh"
    echo "       then move your changed files into fresh/ and run sync.sh there"
    echo
    echo "  Do not force push. The remote history is the one that matters."
    exit 1
  fi

  if [ "$AHEAD" -gt 0 ]; then
    echo "  remote is $AHEAD commit(s) ahead, rebasing"
    if ! git pull --rebase origin "$BRANCH"; then
      echo
      echo "  Rebase hit a conflict. Resolve it, then run:"
      echo "    git rebase --continue && ./scripts/sync.sh \"$MSG\""
      echo "  Or back out with: git rebase --abort"
      exit 1
    fi
    echo "  rebased, re-running the check"
    ./scripts/check.sh >/dev/null || { echo "  check failed after rebase. Nothing pushed."; exit 1; }
  else
    echo "  up to date with the remote"
  fi
fi

echo
echo "4. Commit"
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
  echo "  nothing to commit"
else
  git add -A
  git commit -m "$MSG" >/dev/null && echo "  committed: $MSG"
fi

echo
echo "5. Push"
if git push -u origin "$BRANCH"; then
  echo
  echo "Pushed to https://github.com/knivef/payment-brand-wireframes"
  echo "Vercel deploys on push."
else
  echo
  echo "Push rejected. Do not force push. Run this script again, it will rebase."
  exit 1
fi
