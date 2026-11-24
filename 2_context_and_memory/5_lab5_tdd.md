# Week 2 · Day 10: TDD with Claude (TF-106)

| | |
|---|---|
| **Level** | Intermediate |
| **CCA-F domain** | 3 · Prompt engineering (specs as tests) · 2 · Workflows |
| **Time** | 5 min read · 35 min hands-on · 10 min verify · 10 min quiz |
| **Budget cap** | $0.90 |
| **Check** | `uv run labcheck w2d10` |

## 🎯 Goal

Use **red → green → refactor** with Claude, where *you* own the tests and the spec, and reach a
measurable coverage bar.

## 📖 Primer

The trick with TDD and an agent is **separation**: in the red phase Claude may only write tests; in
the green phase it may only change code, never the tests. Say so explicitly. Agents under pressure to
"make it pass" will otherwise tweak the tests.

Coverage tells you which lines your tests executed. It doesn't prove correctness, but under 90%
on business logic usually means untested branches.

## 🛠️ Steps

Read **TF-106** in [ISSUES.md](../practice-app/ISSUES.md). Note the exact JSON shape and the rounding rule.

**1. Red: tests only.** `/clear`, then:

> TDD, red phase. Write tests ONLY (no application code) for TF-106 in a new file
> practice-app/tests/test_stats.py: the exact JSON shape, all three statuses present when zero,
> completion_rate rounding (1 of 3 → 0.33) and the empty project (0.0), overdue using TF-101 rules,
> and 404 for a missing project. Run them and confirm they fail.

Read the tests. **Do they match the spec exactly?** Fix anything that doesn't, yourself or with Claude,
before going on. These tests *are* the spec now.

**2. Green: code only.**

> Green phase. Make the tests pass without modifying any test file. Put the stats logic in
> services.py (project_stats) and keep the endpoint thin.

If Claude asks to change a test, say no, unless the test itself is wrong.

**3. Refactor.**

> Refactor phase. Improve readability of project_stats without changing behaviour. Tests must stay green.

**4. Measure coverage.**

```
!uv run pytest --cov=taskforge.services --cov-report=term-missing
```

Under 90%? Ask Claude to add tests for the **missing lines it reports**, and to explain what behaviour each line represents.

**5. Verify and commit.**

```
!uv run labcheck w2d10
```

**6. Take the Week 2 quiz:** [assessments/week2_quiz.md](../assessments/week2_quiz.md).

## ✅ Checkpoint

```bash
uv run labcheck w2d10
uv run labcheck budget
```

## 💰 Budget & cost log

Cap: **$0.90**.

```bash
uv run labcheck log w2d10 0.75 "TF-106 TDD"
```

Week 2 total should be **≤ $4**.

## 🚀 Stretch

- Add a CLAUDE.md "Definition of done" line requiring coverage on `services.py` to stay above 90%.
- Ask Claude to write a **property-based** test idea for `completion_rate` (it doesn't need to add a dependency, just describe it).

## 💼 Commercial application

When an agent writes both the code and the tests, you can end up with code that is "tested" but
wrong. Teams that keep **humans in charge of the spec (tests)** and agents in charge of the
implementation get the speed without the false confidence.

## 🤔 Reflect

1. Did Claude ever try to touch tests during the green phase? How did you handle it?
2. Which test in the red phase did you have to correct, and why?
3. What does 90% coverage *not* tell you?

## ➡️ Next

Week 3: [Configuration & Extensibility](../3_configuration_and_extensibility/README.md)
