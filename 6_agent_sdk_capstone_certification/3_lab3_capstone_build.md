# Week 6 · Day 28: Capstone day 1, build

| | |
|---|---|
| **Level** | Expert |
| **CCA-F domain** | all five |
| **Time** | 5 min read · 50 min build · 5 min checkpoint |
| **Budget cap** | $2.50 (the biggest single day of the course) |
| **Check** | `uv run labcheck w6d28` |

## 🎯 Goal

Build a small but real agentic tool on top of TaskForge, end to end, using the design you defended yesterday.

## 📖 Primer: the deterministic shell

The most reliable agent systems put a **deterministic shell** around the model:

```
input → [validate / gather context in code] → model (agent) → [validate output in code] → effect
```

Everything outside the model is ordinary code you can **unit test without API calls**: input parsing, prompt
building, schema validation, file writing, retries and caps. Your capstone tests should cover that shell. They
must not call the API (and so must cost nothing).

## The briefs (pick one)

### A. PR triage bot
Working on a feature branch made from your personal branch, take its diff (`git diff jane-doe...HEAD`) and produce a schema-validated triage: risk level, affected TF issues,
missing tests, suggested reviewers (from `git log`). It posts a Markdown summary.
*Uses:* Agent SDK or `claude -p --json-schema`, structured output, read-only tools.

### B. Ops assistant
An assistant that answers "what should the team work on today?" from TaskForge data, *proposes* status changes, and
applies them only after the human confirms.
*Uses:* your MCP server, a skill, a read-only subagent, human-in-the-loop for writes.

### C. Legacy refactor agent
An agent that refactors one target function in `practice-app/` under an evaluator loop: the golden or characterisation
tests are the evaluator, with a maximum of N iterations and automatic rollback on failure.
*Uses:* Agent SDK, evaluator-optimizer pattern, git as the safety net.

## 🛠️ Steps

**1. Scaffold** `capstone/`:

```
capstone/
├── README.md        # sections: Brief, How to run, Architecture (Cost and Limitations come tomorrow)
├── <package>/       # your code
└── tests/           # tests of the deterministic shell, with no API calls
```

**2. Build the shell first**, test-first, with no model calls: input gathering, the prompt builder, the output
schema and validator, and side-effect functions. Run `uv run pytest capstone -q`.

**3. Add the agent layer.** Wire the model in (SDK, `claude -p`, or skill + MCP, depending on your design), with caps:
`max_turns`, `max_budget_usd`, least-privilege tools.

**4. Run it for real once or twice** on TaskForge. Log each run's `total_cost_usd`.

**5. Write the README** sections **Brief**, **How to run** and **Architecture** (link to your design doc).

**6. Commit.** Tomorrow you'll review, harden and write it up.

## ✅ Checkpoint

```bash
uv run labcheck w6d28
```

## 💰 Budget & cost log

Cap: **$2.50**. If you're approaching it, stop running the full agent and keep building the tested shell.

```bash
uv run labcheck log w6d28 1.80 "capstone build"
```

## 📤 Push your progress

```bash
git add -A && git commit -m "w6d28: Capstone day 1, build" && git push
```

## 🚀 Stretch

Add a `--dry-run` flag that prints the exact prompt and tool list the agent *would* use, without calling the model.
It's a great debugging aid and costs nothing.

## 💼 Commercial application

This is a portfolio piece: a working agentic tool with tests, guardrails and a cost model. It's also
exactly the shape of a first internal pilot you could propose at work next week.

## 🤔 Reflect

1. What share of your code is the deterministic shell vs the model call? Is that what you expected?
2. What did the first real run get wrong?
3. What's the cost per run, and per month at realistic usage?

## ➡️ Next

[Day 29: Capstone day 2](4_lab4_capstone_review.md)
