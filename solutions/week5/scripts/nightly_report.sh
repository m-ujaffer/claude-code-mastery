#!/usr/bin/env bash
# Nightly TaskForge report: deterministic test run + a read-only Claude summary.
#   ./scripts/nightly_report.sh            (BUDGET=0.30 by default)
#   BUDGET=0.10 ./scripts/nightly_report.sh
set -euo pipefail

BUDGET="${BUDGET:-0.30}"
cd "$(dirname "$0")/.."
mkdir -p out
day="$(date +%F)"
raw="out/nightly-${day}.json"
report="out/nightly-${day}.md"

# Step 1: no model needed for facts we can compute.
tests="$(uv run pytest -q 2>&1 | tail -n 1 || true)"

# Step 2: the model only summarises and prioritises.
set +e
claude -p "Write a Markdown nightly report for TaskForge. Test status (already measured): ${tests}.
Use the taskforge MCP tools for project health. Sections: Tests, Project health (one line each), Top 3 risks.
Under 200 words." \
  --output-format json \
  --max-turns 6 \
  --max-budget-usd "$BUDGET" \
  --allowedTools "Read,Grep,Glob,mcp__taskforge__project_stats,mcp__taskforge__find_tasks,mcp__taskforge__list_projects" \
  --append-system-prompt "You are a read-only reporter. Never modify files or tasks." > "$raw"
status=$?
set -e

python3 - "$raw" "$report" "$status" <<'PY'
import json, sys
raw, report, status = sys.argv[1], sys.argv[2], int(sys.argv[3])
try:
    env = json.load(open(raw))
except ValueError:
    print(f"claude produced no JSON (exit {status})", file=sys.stderr)
    sys.exit(1)
print(f"cost: ${env.get('total_cost_usd', 0):.4f}  turns: {env.get('num_turns')}", file=sys.stderr)
if status != 0 or env.get("is_error"):
    print(f"run failed ({env.get('subtype', 'error')}); see {raw}", file=sys.stderr)
    sys.exit(1)
open(report, "w").write(env.get("result", "") + "\n")
print(f"wrote {report}", file=sys.stderr)
PY
