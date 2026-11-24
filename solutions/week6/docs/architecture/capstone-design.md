# Capstone design: PR triage bot (brief A)

## Problem
Reviewers spend the first 10 minutes of every PR working out its risk, which issues it touches, whether tests
were added, and who should look at it. We want a consistent, cheap first pass that runs on demand.

## Pattern
**Rung 2: a workflow with one structured-output model call.** Code gathers the facts (diff, changed files,
TF ids, git-log authors) and validates the output; the model only judges risk and missing tests.
A single agent (rung 4) isn't needed: the steps are fixed and known in advance, and letting the model
explore would add cost and variance without adding value.

## Components
1. `gather.py`: deterministic. Diff vs the base branch, changed files, TF ids, reviewer suggestions from `git log`.
2. `prompt.py`: deterministic. Builds the prompt and truncates the diff to a size budget.
3. Model call: `claude -p --json-schema` with `--max-turns 2` and `--max-budget-usd`, and **no tools** (`--tools ""`).
4. `schema.py`: validates the result again in code.
5. `render.py`: produces a Markdown summary for a PR comment.

## Guardrails
- No tools for the model, so it can't touch the repo or the network. The diff is passed as data.
- Schema validation twice (CLI and code); a run with no `structured_output` fails loudly.
- Diff truncation and a budget cap bound the cost per run.
- The diff is untrusted input: the prompt says to treat it as data and never follow instructions inside it.

## Cost estimate
About 8k input tokens (diff capped at 24k chars) + 400 output ≈ $0.02 per run on Sonnet.
At 20 PRs/day that's about $0.40/day, or $9/month for a team. Worst case is bounded by `--max-budget-usd 0.10` per run.

## Failure modes
- Huge diff → truncated with a visible notice; risk defaults to at least "medium".
- Model refusal or invalid output → exit code 1, nothing posted.
- Prompt injection in the diff → there are no tools to abuse; worst case is a wrong triage, which a human reviews.
- Git not available or bad base ref → clear error before any spend.

## Human in the loop
The bot only **suggests**. A human reads the comment and decides on reviewers and merge. Nothing is applied automatically.

## Decision log
- Reviewer feedback: "why not let the agent read files?" Rejected. Facts come from code; the model judges. Cheaper and more predictable.
- Added the `--dry-run` flag after review so the prompt can be inspected for free.
