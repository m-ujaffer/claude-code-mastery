# Week 1 · Day 4: Prompting for code (TF-102)

| | |
|---|---|
| **Level** | Basics |
| **CCA-F domain** | 3 · Prompt engineering & structured output |
| **Time** | 5 min read · 40 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $0.70 (both attempts together) |
| **Check** | `uv run labcheck w1d4` |

## 🎯 Goal

Measure, in dollars and in quality, the difference between a vague prompt and a precise one,
then ship TF-102 with the precise one.

## 📖 Primer

Read [Guide 05: Prompting for code](../guides/05_prompting_for_code.md) (3 minutes). The five parts
of a strong prompt are **Goal, Context, Constraints, Verification, Output**.

Today is an experiment: you'll implement the same issue twice and compare.

## 🛠️ Steps

```bash
cp notes/templates/w1d4-prompts.md notes/w1d4-prompts.md
git status   # start from a clean practice-app (commit Day 3's work first)
```

**1. The vague attempt.** Start a fresh `claude` session. Type exactly:

> add validation to task titles

Let it run, approving what it asks. Don't help it. When it's done:
- run `/cost` and record the cost in your notes under **Vague prompt**
- run `!uv run labcheck w1d4` and record how many acceptance tests passed
- `/exit`

**2. Reset.** Put the vague attempt aside (you can still look at it later):

```bash
git stash push --include-untracked -m "vague attempt" -- practice-app
git status            # practice-app should be clean again
git stash show -p     # optional: what did the vague attempt actually do?
```

**3. The precise attempt.** Start a **new** `claude` session (a fresh session gives a fair cost comparison). Write
your own prompt using all five parts before you send it. Here's the shape. Don't just copy it; improve it:

> **Goal:** implement TF-102 in @practice-app/ISSUES.md (title validation).
> **Context:** request models are in @practice-app/src/taskforge/models.py (TaskCreate, TaskUpdate).
> **Constraints:** use a Pydantic field validator shared by both models; trimming happens
> before the length check; don't touch the repository layer.
> **Verification:** first add API tests to practice-app/tests/test_tasks_api.py for blank,
> whitespace-only, 200 and 201 characters, trimming, and PATCH. Run them, see them fail, implement,
> then run `uv run pytest -q`.
> **Output:** a short summary of what changed and the final test result.

Record the cost and the labcheck result under **Precise prompt**.

**4. Compare** and write 3–5 sentences under **What I learned**. Consider cost, number of turns,
acceptance tests passed, and how much *you* had to check.

**5. Commit** the precise version, then drop the stash: `git stash drop`.

## ✅ Checkpoint

```bash
uv run labcheck w1d4
```

## 💰 Budget & cost log

Cap: **$0.70** for both attempts. Log the sum:

```bash
uv run labcheck log w1d4 0.55 "vague vs precise"
```

## 🚀 Stretch

Add one more variation: the precise prompt **plus** "Ask me up to 3 clarifying questions before
you start." Did the questions catch anything the issue didn't say?

## 💼 Commercial application

Most engineers judge an AI tool by their first, vague prompts. Teams that turn their good prompts
into **shared templates** (in Week 3 you'll make them into skills) get consistent, reviewable
results and predictable costs.

## 🤔 Reflect

1. Which part of the precise prompt (goal, context, constraints, verification or output) made the biggest difference?
2. Was the vague attempt actually cheaper? Why or why not?
3. Which of the vague attempt's choices would have passed a quick code review, but failed the acceptance criteria?

## ➡️ Next

[Day 5: Context and cost hygiene + mini-feature](5_lab5_cost_and_context.md)
