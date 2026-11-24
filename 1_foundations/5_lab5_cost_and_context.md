# Week 1 · Day 5: Context and cost hygiene + mini-feature (TF-103)

| | |
|---|---|
| **Level** | Basics |
| **CCA-F domain** | 5 · Context management & reliability |
| **Time** | 5 min read · 35 min hands-on · 10 min verify · 10 min quiz |
| **Budget cap** | $0.80 |
| **Check** | `uv run labcheck w1d5` |

## 🎯 Goal

See what's actually in your context window, learn the four commands that control it, and
ship a small feature end to end using everything from this week.

## 📖 Primer

Read [Guide 03: Tokens, context and models](../guides/03_tokens_context_and_models.md) if you
haven't already. The key idea: **every turn re-sends the conversation**, so old, irrelevant
context costs you on every later request and can confuse the model.

| Command | Use it |
|---|---|
| `/context` | to see what's taking up the window |
| `/compact <what to keep>` | mid-task, to shrink history but keep continuity |
| `/clear` | between tasks, as a fresh start |
| `/model`, `/effort` | to match horsepower to the job |

## 🛠️ Steps

```bash
cp notes/templates/w1d5-context.md notes/w1d5-context.md
```

**1. Look inside.** Start `claude` and immediately run `/context`. What's using space before
you've typed anything? (System prompt, tools, memory files…) Note the number.

**2. Bloat it on purpose.** Ask:

> Read every file in practice-app/src/taskforge and practice-app/tests and summarise each in one line.

Run `/context` again. Write the size in your notes under **before /compact**.

**3. Compact with a focus.**

```
/compact Keep only: the layering rules and where filtering would be implemented for GET /tasks
```

Run `/context` and record the size under **after /compact**.

**4. Choose a model on purpose.** Run `/model` and look at the options. TF-103 is a
well-specified, small change. Is it a Sonnet job or a Haiku job? Pick one, and record it under **model used**,
with your reason.

**5. Ship TF-103.** Read TF-103 in [ISSUES.md](../practice-app/ISSUES.md), then write a precise prompt
(use Day 4's five parts). Include: tests first, filters combine with `project_id`/`limit`/`offset`,
invalid values return 422, and keep SQL in `repository.py`.

Review the diff (`!git diff`), run `!uv run labcheck w1d5`, then commit.

**6. `/clear` and verify** that a fresh session is small again with `/context`. Then `/cost`.

**7. Take the Week 1 quiz:** [assessments/week1_quiz.md](../assessments/week1_quiz.md) (offline).

## ✅ Checkpoint

```bash
uv run labcheck w1d5
uv run labcheck budget
```

## 💰 Budget & cost log

Cap: **$0.80**.

```bash
uv run labcheck log w1d5 0.60 "context + TF-103"
```

Week 1 total should be **≤ $3**. If it isn't, look at your log: which lab ran over, and why?

## 📤 Push your progress

```bash
git add -A && git commit -m "w1d5: Context and cost hygiene + mini-feature (TF-103)" && git push
```

## 🚀 Stretch

- Try `/effort` at a lower setting for a trivial request, such as renaming a variable. Did it change the cost or the quality?
- Ask Claude to explain the difference between `/compact` and `/clear` *in terms of what it will remember*.

## 💼 Commercial application

At company scale, context hygiene is the difference between a $6/day and a $30/day developer
habit. The teams with the best results also tend to have the lowest bills, because focused
context gives better answers.

## 🤔 Reflect

1. What surprised you in the very first `/context`?
2. When would `/compact` be the wrong choice, and `/clear` the right one?
3. Did your model choice for TF-103 hold up? Would you choose differently next time?

## ➡️ Next

Week 2: [Context & Memory](../2_context_and_memory/README.md)
