# Week 1 · Day 3: Fix a bug test-first (TF-101)

| | |
|---|---|
| **Level** | Basics |
| **CCA-F domain** | 2 · Claude Code configuration & workflows · 3 · Prompt engineering |
| **Time** | 5 min read · 40 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $0.60 |
| **Check** | `uv run labcheck w1d3` |

## 🎯 Goal

Fix a real bug with the most reliable loop in agentic coding: **reproduce with a failing
test → fix → verify**. Then review the diff like an engineer, not a spectator.

## 📖 Primer

Agents are great at making tests pass, which is exactly why **you** must make sure the test
captures the real requirement *before* any fix exists. If the test is written after the fix,
it tends to bless whatever the fix does.

Read **TF-101** in [practice-app/ISSUES.md](../practice-app/ISSUES.md) now. Note that it has two rules.

## 🛠️ Steps

Start `claude`. Run `/clear` if you're continuing an old session.

**1. Reproduce first.**

> Read TF-101 in @practice-app/ISSUES.md. Add regression tests to
> @practice-app/tests/test_services.py that capture BOTH rules (due today → not overdue;
> done but past due → not overdue). Run only those tests and show me that they fail.
> Do not change any application code yet.

Check that the new tests fail **for the right reason**: an assertion on `is_overdue`, not an
import error.

**2. Fix.**

> Now fix is_overdue in @practice-app/src/taskforge/services.py so the tests pass.
> Keep the signature unchanged. Then run the full suite with `uv run pytest -q`.

**3. Review the diff.** Before accepting anything else:

```
!git diff
```

Check against [Guide 06](../guides/06_reviewing_ai_written_code.md):
- Did it change only `services.py` and the test file?
- Did it modify any *existing* test? (It shouldn't have needed to.)
- Does the fix use `Status.DONE` / `"done"` consistently with the rest of the code?

**4. Ask for a self-review.**

> Review your own diff as a skeptical senior engineer. What edge cases could still be wrong?

Decide whether any of its points matter. Not every suggestion should be accepted.

**5. Check with the hidden acceptance tests** (free):

```
!uv run labcheck w1d3
```

**6. Commit** (still inside Claude, or in another terminal):

> Commit this with a Conventional Commit message that mentions TF-101.

Read the message before approving.

## ✅ Checkpoint

```bash
uv run labcheck w1d3
```

## 💰 Budget & cost log

Cap: **$0.60**. `/cost`, then:

```bash
uv run labcheck log w1d3 0.45 "TF-101"
```

## 🚀 Stretch

- Ask Claude where else in the codebase "overdue" is computed. (Hint: `legacy/`.) Is it consistent with the fix?
  Don't change it. Write down what you find; it matters in Week 5.
- Ask for a **parametrised** pytest version of your regression tests.

## 💼 Commercial application

"Write a failing test first" is the single most effective instruction you can give a coding
agent. Teams that make it the default (in CLAUDE.md, which you'll do next week) see far
fewer "fixed it, broke something else" cycles.

## 🤔 Reflect

1. What would have gone wrong if you had asked "fix TF-101" in one step?
2. Did Claude's self-review find anything real? What did it miss?
3. How did you confirm the tests failed for the *right* reason?

## ➡️ Next

[Day 4: Prompting for code](4_lab4_prompting_for_code.md)
