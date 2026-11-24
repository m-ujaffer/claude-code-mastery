#!/usr/bin/env bash
# Restore practice-app/ to the state it should be in at the start of a week.
#
#   bash scripts/reset_to.sh week-3-start
#
# Your current practice-app/ is copied to .backup/practice-app-<timestamp>/ first,
# so nothing is lost.
set -euo pipefail

cd "$(dirname "$0")/.."
target="${1:-}"
if [[ -z "$target" || ! -d "checkpoints/$target/practice-app" ]]; then
  echo "Usage: bash scripts/reset_to.sh <checkpoint>"
  echo "Available:"; ls checkpoints | grep -- '-start$' | sed 's/^/  /'
  exit 1
fi

stamp="$(date +%Y%m%d-%H%M%S)"
mkdir -p .backup
cp -r practice-app ".backup/practice-app-$stamp"
echo "Backed up current practice-app to .backup/practice-app-$stamp"

rm -rf practice-app
cp -r "checkpoints/$target/practice-app" practice-app
rm -f practice-app/taskforge.db
echo "practice-app restored to $target. Running tests..."
uv run pytest -q
