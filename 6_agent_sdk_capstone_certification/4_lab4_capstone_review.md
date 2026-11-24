# Week 6 · Day 29: Capstone day 2, review, harden, ship

| | |
|---|---|
| **Level** | Expert |
| **CCA-F domain** | all five |
| **Time** | 5 min read · 45 min review and harden · 10 min write-up |
| **Budget cap** | $1.50 |
| **Check** | `uv run labcheck w6d29` |

## 🎯 Goal

Put your capstone through the same review and hardening a production agent would get, then document its
cost and limits honestly.

## 🛠️ Steps

**1. Independent review with subagents.** `/clear`, then:

> Use the code-reviewer subagent to review everything under capstone/ for correctness, security (prompt
> injection from untrusted inputs, over-broad tools, secrets) and cost risks (missing caps, unbounded loops).
> Then use the Explore subagent to check that the README's "How to run" actually works as written.
> Summarise the findings as a prioritised list. Don't fix anything yet.

**2. Triage the findings** in `capstone/REVIEW.md`: for each one, choose **fix**, **accept (with reason)** or **won't fix**.

**3. Fix the top findings**, test-first where possible. Keep `uv run pytest capstone -q` green.

**4. Score yourself** against the [capstone rubric](../assessments/capstone_rubric.md) and note the score in `REVIEW.md`.

**5. Finish the README** with two more sections:
- **Cost**: measured cost per run (from your logs), expected runs per day, and the monthly estimate for a team of 10.
  Name the caps that bound the worst case.
- **Limitations**: what it can't do, known failure modes, and when a human must step in.

**6. Ship it.** Open a PR for the capstone. If your Day 24 workflow is active, let Claude review it in CI. Merge when you're happy.

**7. Share** (optional): copy a short write-up into `community_contributions/` and open a PR to the course repo.

## ✅ Checkpoint

```bash
uv run labcheck w6d29
```

## 💰 Budget & cost log

Cap: **$1.50**.

```bash
uv run labcheck log w6d29 1.10 "capstone review"
uv run labcheck budget
```

Week 6 total (excluding Day 30, which is free) should be **≤ $6**.

## 🚀 Stretch

Write a tiny **eval**: five realistic inputs with expected properties (not exact outputs), and a script that runs the agent
on all five with a total budget cap and reports pass/fail. This is how you'd catch regressions when prompts or
models change.

## 💼 Commercial application

"It works on my machine" isn't enough for agents. Reviewers, security and finance will ask: what can it touch,
what does it cost, how does it fail, and how do you know it still works? Your README now answers all four.

## 🤔 Reflect

1. Which review finding surprised you most?
2. Which limitation would worry a security reviewer most, and how would you address it next?
3. What's the first eval you'd add before letting colleagues use it?

## ➡️ Next

[Day 30: Mock exam and readiness](5_lab5_mock_exam.md)
