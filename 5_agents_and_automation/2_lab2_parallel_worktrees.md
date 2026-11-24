# Week 5 · Day 22: Parallel work with git worktrees (TF-107 + TF-108)

| | |
|---|---|
| **Level** | Advanced |
| **CCA-F domain** | 1 · Agentic architecture & orchestration |
| **Time** | 5 min read · 45 min hands-on · 10 min verify & reflect |
| **Budget cap** | $1.60 (two sessions) |
| **Check** | `uv run labcheck w5d22` |

## 🎯 Goal

Run two Claude Code sessions in parallel on independent features without them stepping on each other,
then integrate the results, and learn when parallelism isn't worth it.

## 📖 Primer

Two agents editing the same checkout will corrupt each other's work. **Git worktrees** give each session its
own directory and branch, all sharing one repository:

```bash
git worktree add ../tf-107 -b feature/tf-107-csv-export
git worktree add ../tf-108 -b feature/tf-108-search
```

Parallelism pays when tasks are **independent** (different files or clear seams) and **well specified**. It
hurts when tasks overlap (you get merge conflicts and duplicated work) or when *you* become the bottleneck
reviewing two streams at once.

TF-107 and TF-108 both touch `api/tasks.py` and `repository.list_tasks`. That's deliberate: you'll get to
practise integration.

## 🛠️ Steps

Commit everything first (`git status` should be clean).

**1. Create the worktrees.**

```bash
git worktree add ../tf-107 -b feature/tf-107-csv-export
git worktree add ../tf-108 -b feature/tf-108-search
git worktree list
```

Each worktree needs its own environment. In each one, run `uv sync`.

**2. Start two sessions.** Open two terminals (the **+** button):

```bash
# terminal A
cd ../tf-107 && claude
# terminal B
cd ../tf-108 && claude
```

**3. Kick off both.** Use your `/tf-issue` skill from Week 3 if it's committed, or a precise prompt:

- A: `/tf-issue TF-107`. Remind it: the route must be declared before `/tasks/{task_id}`.
- B: `/tf-issue TF-108`

Alternate between the terminals, approving and reviewing. Notice how much attention two streams take.

**4. Commit each branch** with a message mentioning its issue ID.

**5. Integrate.** Back in the main checkout (the original folder):

```bash
git merge --no-ff feature/tf-107-csv-export
git merge --no-ff feature/tf-108-search      # expect a conflict in list_tasks / api/tasks.py
```

Resolve the conflict with Claude:

> There's a merge conflict between TF-107 and TF-108. Resolve it so both features work. Keep the
> export route before /{task_id}. Run the full test suite and the labcheck for w5d22.

**6. Clean up.**

```bash
git worktree remove ../tf-107
git worktree remove ../tf-108
```

## ✅ Checkpoint

```bash
uv run labcheck w5d22
```

## 💰 Budget & cost log

Cap: **$1.60** for both sessions plus the merge. Add up the `/cost` of each session:

```bash
uv run labcheck log w5d22 1.30 "TF-107+108 parallel"
```

## 🚀 Stretch

- Subagents can run in their own worktree too (`isolation: worktree` in the agent's frontmatter). Read the docs:
  when would you prefer that over two interactive sessions?
- Time yourself: was parallel actually faster than doing the two issues one after the other?

## 💼 Commercial application

Engineers who get the most out of agents often run 2–4 sessions on independent tickets while they review and
integrate. The skill is in **decomposition**, choosing tasks with clean seams, and in **integration
discipline**: tests and review, not "it merged, ship it".

## 🤔 Reflect

1. What made the merge conflict happen, and how could you have decomposed the work to avoid it?
2. Where were you the bottleneck?
3. What's the maximum number of parallel sessions *you* could review well?

## ➡️ Next

[Day 23: Headless pipelines](3_lab3_headless_pipelines.md)
