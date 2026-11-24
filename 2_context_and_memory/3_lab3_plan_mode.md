# Week 2 · Day 8: Plan mode for multi-file work (TF-104)

| | |
|---|---|
| **Level** | Intermediate |
| **CCA-F domain** | 1 · Agentic architecture (plan, then execute) · 2 · Claude Code workflows |
| **Time** | 5 min read · 45 min hands-on · 10 min verify & reflect |
| **Budget cap** | $1.00 |
| **Check** | `uv run labcheck w2d8` |

## 🎯 Goal

Deliver a feature that touches the schema, repository, models, API and tests by using the
**explore → plan → implement → verify** loop, and practise *editing a plan* before any code exists.

## 📖 Primer

For multi-file changes, the most expensive mistake is a wrong approach discovered halfway
through. Plan mode makes Claude investigate and propose **without editing**. You then:

1. **Challenge** the plan: ask about alternatives, edge cases and the migration story.
2. **Edit** it: tell Claude what to change.
3. **Approve** it. Only then does Claude switch to implementing.

A plan saved to a file is also a **handoff artefact**. A fresh session, or a colleague, can execute it.

## 🛠️ Steps

Read **TF-104** in [ISSUES.md](../practice-app/ISSUES.md). Note the "separate table" requirement.

**1. Enter plan mode.** `/clear`, then `Shift+Tab` to **plan mode**.

**2. Explore and plan.**

> Plan TF-104 (tags) from @practice-app/ISSUES.md. Investigate the schema, repository, models,
> services and API first. The plan must cover: the task_tags table, normalisation (where it
> lives and why), how list filtering by tag works in SQL, how PATCH replaces tags, the changes to
> the Task response model, and the exact tests you'll write first. List the files you'll touch.

**3. Challenge it.** Ask at least two of these (or your own):

> - What happens to tags when a task is deleted?
> - Why normalise in the Pydantic model rather than the repository (or vice versa)?
> - How does `to_task` get tags without an N+1 query problem, and does it matter at this scale?
> - What's the migration story for an existing dev database?

Ask Claude to revise the plan based on the answers you agree with.

**4. Save the plan.** Still in plan mode, approve the plan but tell Claude to **first** write it to
`notes/plans/tf-104-plan.md`. (You'll reuse this pattern in Week 5 for long tasks.)

**5. Implement in steps.** Let it execute: tests first, then code. Approve the edits. If it starts doing
something not in the plan, press **Esc** and point it back to the plan file.

**6. Verify.**

```
!rm -f practice-app/taskforge.db
!uv run pytest -q
!uv run labcheck w2d8
```

**7. Review** the full diff (`!git diff --stat`, then `!git diff`) and commit with a message mentioning TF-104.

## ✅ Checkpoint

```bash
uv run labcheck w2d8
```

## 💰 Budget & cost log

Cap: **$1.00**. Plan mode often makes the *total* cheaper, even though planning has a cost.

```bash
uv run labcheck log w2d8 0.85 "TF-104 plan mode"
```

## 🚀 Stretch

- In a **new** session, give Claude only `@notes/plans/tf-104-plan.md` and ask it to review the
  implementation against the plan. What did it find?
- Try the Opus model for the planning step only (`/model`), then switch back to Sonnet for implementation.
  Was the plan better? Was it worth the price difference?

## 💼 Commercial application

"Plan first, then execute" is the standard way teams run agents on anything non-trivial. The plan is
cheap to review in a PR comment or a standup, and a saved plan makes the work **resumable** and
**auditable**.

## 🤔 Reflect

1. What did your challenge questions change in the plan?
2. Where did the implementation deviate from the plan, and was that fine?
3. When would plan mode be overkill?

## ➡️ Next

[Day 9: Git and GitHub workflow](4_lab4_git_workflow.md)
