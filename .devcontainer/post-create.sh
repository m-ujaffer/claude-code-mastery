#!/usr/bin/env bash
# Runs once when the Codespace is created. Safe to re-run by hand:
#   bash .devcontainer/post-create.sh
set -euo pipefail

echo "==> Installing uv (Python package manager)"
if ! command -v uv >/dev/null 2>&1; then
  pipx install uv || python3 -m pip install --user uv
fi

echo "==> Installing course dependencies"
uv sync

echo "==> Preparing your notes folder"
mkdir -p notes
[ -f notes/cost-log.csv ] || echo "lab,date,cost_usd,note" > notes/cost-log.csv

echo "==> Running environment checks"
uv run labcheck doctor || true

cat <<'MSG'

  All set! Open 1_foundations/1_lab1_first_session.md to begin.
  Always start Claude Code from the repo root:   claude

MSG
