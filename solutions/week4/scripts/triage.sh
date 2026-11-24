#!/usr/bin/env bash
# Triage one TaskForge backlog issue into schema-validated JSON.
#   ./scripts/triage.sh TF-107
set -euo pipefail

id="${1:?usage: triage.sh TF-###}"
cd "$(dirname "$0")/.."
mkdir -p out
raw="out/triage-${id}.json"

prompt="Triage backlog issue ${id} from practice-app/ISSUES.md. Read the issue, then look at the code it
would touch under practice-app/src. Fill in every field of the schema. Example of a good answer for a
different issue:
{\"issue_id\": \"TF-101\", \"type\": \"bug\", \"severity\": \"high\",
 \"summary\": \"Tasks due today and completed tasks are wrongly flagged overdue.\",
 \"affected_files\": [\"practice-app/src/taskforge/services.py\"], \"estimated_effort\": \"S\"}"

claude -p "$prompt" \
  --output-format json \
  --json-schema "$(cat schemas/triage.schema.json)" \
  --allowedTools "Read,Grep,Glob" \
  --max-turns 4 \
  --max-budget-usd 0.25 > "$raw"

python3 - "$raw" <<'PY'
import json, sys
env = json.load(open(sys.argv[1]))
print(f"cost: ${env.get('total_cost_usd', 0):.4f}", file=sys.stderr)
if env.get("is_error") or "structured_output" not in env:
    print("no structured_output in the result: see " + sys.argv[1], file=sys.stderr)
    sys.exit(1)
print(json.dumps(env["structured_output"], indent=2))
PY
