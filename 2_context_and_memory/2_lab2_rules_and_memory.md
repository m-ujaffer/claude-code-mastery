# Week 2 · Day 7: Rules, memory and checking that they work

| | |
|---|---|
| **Level** | Intermediate |
| **CCA-F domain** | 5 · Context management · 2 · Claude Code configuration |
| **Time** | 5 min read · 40 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $0.60 |
| **Check** | `uv run labcheck w2d7` |

## 🎯 Goal

Move instructions out of the always-loaded CLAUDE.md into **path-scoped rules** that load only
when relevant, and learn to **test** whether an instruction actually changes behaviour.

## 📖 Primer

- **`.claude/rules/*.md`**: rule files Claude Code discovers automatically. Add `paths:` frontmatter
  so a rule only loads when Claude works on matching files:

  ```markdown
  ---
  paths:
    - "practice-app/tests/**"
  ---
  # Testing rules
  - ...
  ```

- **`/memory`**: lists the memory files in play, opens them for editing, and controls **auto memory**
  (notes Claude keeps for itself between sessions).

Instructions are **advisory**: the model weighs them. Next week you'll meet **hooks**, which are
**deterministic**. Knowing which one to use is exam material.

## 🛠️ Steps

```bash
cp notes/templates/w2d7-memory.md notes/w2d7-memory.md
```

**1. See what's loaded.** Start `claude`, run `/memory`, and look at the list. Is your CLAUDE.md there?
Is auto memory on?

**2. Pick a rule to test.** Choose something testable and specific to tests. For example:

> In tests, freeze time with `monkeypatch.setattr(clock, "today", ...)`; never use real dates.
> Use the `client` and `project` fixtures from conftest.py. Name tests `test_<behaviour>`.

**3. Without the rule.** Make sure the rule is **not** in CLAUDE.md. `/clear`, then:

> Add a test to practice-app/tests that a task due tomorrow is not overdue.

Record what it did under **result without rule**. Then undo it (`/rewind` or `git restore practice-app`).

**4. Add the rule, scoped.** Create `.claude/rules/testing.md` with `paths:` frontmatter matching
`practice-app/tests/**` and your rule as the body.

**5. With the rule.** `/clear`, run the **same** prompt, and record under **result with rule**.
Did the behaviour change? If not, reword the rule (be concrete, and say *why*) and try once more.

**6. Move something out of CLAUDE.md.** Is there anything in your CLAUDE.md that only matters for a
subset of files? Move it into a rule with `paths:`. This makes CLAUDE.md smaller for every request.

**7. Conclude** in your notes: keep, reword or delete the rule. Commit `.claude/rules/`.

## ✅ Checkpoint

```bash
uv run labcheck w2d7
```

## 💰 Budget & cost log

Cap: **$0.60**.

```bash
uv run labcheck log w2d7 0.45 "rules experiment"
```

## 🚀 Stretch

- Add a rule for `practice-app/src/taskforge/legacy/**`: "Do not change behaviour; add
  characterisation tests first." You'll rely on it in Week 5.
- Look at auto memory via `/memory`. What has Claude chosen to remember about you so far? Edit or delete anything that's wrong.

## 💼 Commercial application

Large teams end up with dozens of conventions. Putting them all in one CLAUDE.md is slow, expensive
and less reliable. **Scoped rules** keep each session's context tight, and *testing* rules (the
before/after experiment you just ran) is how mature teams stop their instructions turning into folklore.

## 🤔 Reflect

1. Did your rule change behaviour on the first try? What made the wording work (or not)?
2. Give an example of an instruction that should be a **hook** instead of a rule.
3. What's the cost difference between a 200-line CLAUDE.md and 60 lines plus scoped rules?

## ➡️ Next

[Day 8: Plan mode for multi-file work](3_lab3_plan_mode.md)
