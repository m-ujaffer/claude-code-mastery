#!/usr/bin/env bash
# Runs once when the Codespace is created. Safe to re-run by hand:
#   bash .devcontainer/post-create.sh
set -euo pipefail

# PyPI downloads occasionally time out. Give each request longer than uv's
# 30-second default and retry a few times before giving up.
export UV_HTTP_TIMEOUT="${UV_HTTP_TIMEOUT:-120}"

retry() {
  local attempt
  for attempt in 1 2 3; do
    if "$@"; then
      return 0
    fi
    if [ "$attempt" -lt 3 ]; then
      echo "  ...attempt $attempt failed, retrying in 10 seconds"
      sleep 10
    fi
  done
  return 1
}

echo "==> Installing uv (Python package manager)"
if ! command -v uv >/dev/null 2>&1; then
  pipx install uv || python3 -m pip install --user uv
fi

echo "==> Installing core course dependencies"
if ! retry uv sync; then
  cat <<'MSG'

  Could not download the core course packages (usually a temporary network problem).
  Wait a minute, then run:   bash .devcontainer/post-create.sh
  See setup/troubleshooting.md ("Failed to download ... operation timed out").

MSG
  exit 1
fi

echo "==> Installing Week 4 and Week 6 packages (MCP, Claude Agent SDK)"
if ! retry uv sync --all-groups; then
  cat <<'MSG'

  The optional Week 4/6 packages did not download. You don't need them until Week 4.
  Install them later with:   uv sync --all-groups

MSG
fi

echo "==> Preparing your notes folder"
mkdir -p notes
[ -f notes/cost-log.csv ] || echo "lab,date,cost_usd,note" > notes/cost-log.csv

echo "==> Running environment checks"
uv run labcheck doctor || true

cat <<'MSG'

  All set! Open 1_foundations/1_lab1_first_session.md to begin.
  Always start Claude Code from the repo root:   claude

MSG
