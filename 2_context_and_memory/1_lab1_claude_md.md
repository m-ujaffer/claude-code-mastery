# Week 2 · Day 6: CLAUDE.md, your project's memory

| | |
|---|---|
| **Level** | Intermediate |
| **CCA-F domain** | 2 · Claude Code configuration · 5 · Context management |
| **Time** | 5 min read · 40 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $0.60 |
| **Check** | `uv run labcheck w2d6` |

## 🎯 Goal

Create a **lean, high-signal** `CLAUDE.md` so every session starts out knowing how this project
works, and prove that it changes Claude's behaviour.

## 📖 Primer

`CLAUDE.md` is loaded into **every** session's context. That makes it powerful, and also a
cost: every line is paid for on every request.

Where memory files live (most general first):

| Location | Scope | Commit it? |
|---|---|---|
| `~/.claude/CLAUDE.md` | You, every project | n/a |
| `./CLAUDE.md` (or `./.claude/CLAUDE.md`) | The project, shared with the team | ✅ |
| `./CLAUDE.local.md` | You, this project only | ❌ (git-ignored) |
| `sub/dir/CLAUDE.md` | Loaded on demand, when Claude works in that directory | ✅ |

`@path/to/file.md` inside a CLAUDE.md **imports** that file. Use it to point at docs that already
exist instead of copying them.

**What belongs in CLAUDE.md:** commands (build, test, lint), conventions Claude can't infer,
architecture "gotchas", and the definition of done.
**What doesn't:** things obvious from the code, long docs, aspirations, or rules you never check.

## 🛠️ Steps

**1. Baseline (no memory).** Start `claude` and ask:

> Add a test that a task's updated_at changes when it's patched. Run it.

Watch for two things: does it use `clock.now()` / freeze time, and does it run tests the right way
(`uv run pytest`)? Then `/rewind` (or `git restore practice-app`) to undo, and `/clear`.

**2. Generate.** Run `/init`. It analyses the repo and writes `CLAUDE.md` at the root. Approve it.

**3. Trim ruthlessly.** Open `CLAUDE.md` in the editor. `/init` is a first draft. Rewrite it by
hand (or with Claude) to **≤ 60 lines** with exactly these sections:

```markdown
# TaskForge course repo

## Commands
## Architecture and conventions
## Definition of done
## Course rules
```

Make sure it includes:
- `uv run pytest` and `uv run ruff check practice-app`
- "Get time from `taskforge.clock` (`clock.today()`/`clock.now()`), never `date.today()`"
- "SQL only in repository.py, rules in services.py, HTTP in api/"
- "Write a failing test first; don't edit existing tests to make them pass"
- an import instead of a copy: `See @practice-app/README.md for the layout.`
- one course rule, for example: "Never edit files under labcheck/ or solutions/."

**4. Verify that it changes behaviour.** `/clear` (CLAUDE.md is re-read), then repeat the step 1 prompt
**exactly**. Compare: did it follow the conventions without being told?

**5. Check the cost of memory.** Run `/context` and find the memory files line. How many tokens does
your CLAUDE.md cost per request? Is every line worth it?

**6. Commit** `CLAUDE.md` (keep the test if you like it).

## ✅ Checkpoint

```bash
uv run labcheck w2d6
```

## 💰 Budget & cost log

Cap: **$0.60**.

```bash
uv run labcheck log w2d6 0.50 "CLAUDE.md"
```

## 🚀 Stretch

- Create `CLAUDE.local.md` with a personal preference (for example, "Explain trade-offs briefly before large edits").
  Check that `git status` doesn't show it. Why does this file exist?
- Create `practice-app/src/taskforge/legacy/CLAUDE.md` saying "Characterisation tests before any change."
  When is it loaded?

## 💼 Commercial application

A good team CLAUDE.md is a **living onboarding doc that machines follow**. Treat changes to it like
code: review them in PRs, and delete rules that don't earn their keep.

## 🤔 Reflect

1. Which `/init` lines did you delete, and why were they not worth their tokens?
2. Did step 4 behave differently from step 1? Which line caused it?
3. What belongs in `CLAUDE.local.md` rather than `CLAUDE.md`?

## ➡️ Next

[Day 7: Rules, memory and testing them](2_lab2_rules_and_memory.md)
