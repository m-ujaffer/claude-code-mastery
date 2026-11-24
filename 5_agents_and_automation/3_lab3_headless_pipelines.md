# Week 5 · Day 23: Headless mode and scripted pipelines

| | |
|---|---|
| **Level** | Advanced |
| **CCA-F domain** | 2 · Workflows · 3 · Structured output · 5 · Reliability |
| **Time** | 10 min read · 35 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $1.00 |
| **Check** | `uv run labcheck w5d23` |

## 🎯 Goal

Build a robust, cost-capped script that runs Claude Code unattended, the foundation for cron jobs,
CI steps and internal tools.

## 📖 Primer

| Flag | Why it matters in scripts |
|---|---|
| `-p "<prompt>"` | non-interactive: run, print, exit |
| `--output-format json` | one JSON envelope: `result`, `session_id`, `total_cost_usd`, `num_turns`, `is_error`, … |
| `--output-format stream-json --verbose` | one JSON event per line, for progress or logging |
| `--allowedTools "Read,Grep,Bash(uv run pytest *)"` | pre-approve exactly what's needed; anything else that would prompt is **denied** |
| `--max-turns N` | stop agent loops that go on too long |
| `--max-budget-usd X` | stop when estimated spend reaches X |
| `--continue` / `--resume <session_id>` | chain steps that share context |
| `--append-system-prompt "..."` | add role or rules for this run |
| `--bare` | skip auto-loading hooks, skills, plugins, MCP and CLAUDE.md for fast, reproducible runs |

Exit status: `0` on success, non-zero on failure. Always check it **and** `is_error` in the JSON.

> Headless runs don't show in your status line. Log their `total_cost_usd` yourself.

## 🛠️ Steps

**1. Warm-up: pipe data in.**

```bash
git log --oneline -20 | claude -p "Group these commits by TaskForge issue id. Output a Markdown list." --max-turns 1
```

**2. Inspect the JSON envelope.**

```bash
claude -p "How many test functions are in practice-app/tests? Answer with a number only." \
  --output-format json --allowedTools "Read,Grep,Glob" --max-turns 4 | python3 -m json.tool
```

Find `result`, `total_cost_usd`, `num_turns` and `session_id`.

**3. Build `scripts/nightly_report.sh`.** Ask Claude to write it to this spec, then **review it line by line**:

- `set -euo pipefail`, and a `BUDGET` variable defaulting to `0.30`
- step 1 runs the tests itself (no model) and captures the summary line
- step 2 calls `claude -p` with `--output-format json`, `--max-turns 6`, `--max-budget-usd "$BUDGET"`,
  `--allowedTools "Read,Grep,Glob,mcp__taskforge__project_stats,mcp__taskforge__find_tasks"`, and
  `--append-system-prompt` saying it is a read-only reporter. The prompt asks for a Markdown nightly report:
  the test status (passed in as text), project health from MCP, and the top 3 risks.
- it writes the `result` to `out/nightly-$(date +%F).md`
- it reads `total_cost_usd` and `is_error` with `python3`, prints the cost to stderr, and exits 1 if `is_error` is true
  or the exit status was non-zero

**4. Run it twice**, once normally and once with `BUDGET=0.01 ./scripts/nightly_report.sh`. What happens
when the budget is hit? Does your script handle it gracefully?

**5. Chain sessions (optional but instructive).**

```bash
sid=$(claude -p "Read practice-app/ISSUES.md and list open issues" --output-format json --max-turns 3 \
      --allowedTools "Read" | python3 -c "import sys,json; print(json.load(sys.stdin)['session_id'])")
claude -p "Which of those is riskiest and why? One paragraph." --resume "$sid" --max-turns 2
```

**6. Commit** the script (`chmod +x` first).

## ✅ Checkpoint

```bash
uv run labcheck w5d23
```

## 💰 Budget & cost log

Cap: **$1.00**. Add up the `total_cost_usd` values your runs printed:

```bash
uv run labcheck log w5d23 0.55 "headless pipeline"
```

## 🚀 Stretch

- Add `--bare` with an explicit `--mcp-config .mcp.json`. Compare startup time and cost.
- Use `--output-format stream-json --verbose` and print a live progress line for each tool call.

## 💼 Commercial application

Headless Claude Code is how agents become **infrastructure**: nightly dependency audits, release-note
drafts, flaky-test triage, doc freshness checks. The difference between a demo and production is exactly
what you built today: caps, exit codes, cost logging and least-privilege tool lists.

## 🤔 Reflect

1. What happened at `BUDGET=0.01`, and is that the behaviour you want at 3 a.m.?
2. Why is `--allowedTools` safer than `--permission-mode acceptEdits` for this job?
3. What would you monitor if this ran every night for a team of 50?

## ➡️ Next

[Day 24: Claude in CI](4_lab4_github_actions.md)
