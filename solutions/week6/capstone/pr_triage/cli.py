"""PR triage bot.

    uv run python -m pr_triage.cli --base main            (run from capstone/)
    uv run python -m pr_triage.cli --base main --dry-run  (print the prompt, no spend)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys

from pr_triage.gather import gather
from pr_triage.prompt import build_prompt
from pr_triage.render import render
from pr_triage.schema import TRIAGE_SCHEMA, validate


def call_model(prompt: str, budget: float) -> dict:
    proc = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "json",
         "--json-schema", json.dumps(TRIAGE_SCHEMA),
         "--tools", "", "--max-turns", "2", "--max-budget-usd", str(budget)],
        capture_output=True, text=True, timeout=300,
    )
    envelope = json.loads(proc.stdout or "{}")
    print(f"total_cost_usd={envelope.get('total_cost_usd', 0):.4f}", file=sys.stderr)
    if proc.returncode != 0 or envelope.get("is_error") or "structured_output" not in envelope:
        raise SystemExit("triage failed: no valid structured_output")
    return validate(envelope["structured_output"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="main")
    parser.add_argument("--budget", type=float, default=0.10)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    facts = gather(args.base)
    prompt = build_prompt(facts)
    if args.dry_run:
        print(prompt)
        return 0
    print(render(facts, call_model(prompt, args.budget)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
