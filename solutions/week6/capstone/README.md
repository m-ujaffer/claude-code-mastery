# Capstone: PR triage bot (brief A)

## Brief
A cheap, consistent first pass on every pull request: risk level, referenced TF issues, missing tests and
suggested reviewers, posted as a Markdown summary for a human to act on.

## How to run
```bash
cd capstone
uv run python -m pr_triage.cli --base main --dry-run   # see the exact prompt (free)
uv run python -m pr_triage.cli --base main             # real run (about $0.02)
uv run pytest -q                                       # shell tests, no API calls
```

## Architecture
A rung-2 workflow: deterministic code gathers facts (diff, files, TF ids, git-log reviewers), one
`claude -p --json-schema` call with **no tools** judges risk and missing tests, and code validates and renders the result.
Full design: [docs/architecture/capstone-design.md](../docs/architecture/capstone-design.md).

## Cost
Measured: $0.015–0.03 per run (Sonnet; diffs under 24k chars). At 20 PRs/day that's about $0.50/day, or $10/month for a
team of 10. Worst case per run is capped by `--max-budget-usd 0.10` and `--max-turns 2`.

## Limitations
- Judges only the diff. It doesn't run the tests or read surrounding code, so it can miss cross-file effects.
- Truncates very large diffs (with a notice); risk on those is a floor, not an assessment.
- Reviewer suggestions come from git history and favour frequent committers.
- It suggests; it never approves, merges or assigns. A human must review the output.
