# Week 5 · Day 25: Reliability on long tasks (TF-109)

| | |
|---|---|
| **Level** | Advanced → Expert |
| **CCA-F domain** | 5 · Context management & reliability · 1 · Agentic architecture |
| **Time** | 5 min read · 40 min hands-on · 5 min verify · 10 min quiz |
| **Budget cap** | $1.40 |
| **Check** | `uv run labcheck w5d25` |

## 🎯 Goal

Complete a risky refactor of legacy code with an agent, safely, using **characterisation tests**,
**incremental checkpoints** and a **handoff document** that lets a fresh session (or a colleague) take over.

## 📖 Primer

Long tasks fail in predictable ways: context fills up, the agent drifts from the goal, a late change breaks
something early, or a session dies and the knowledge goes with it. The countermeasures:

| Failure | Countermeasure |
|---|---|
| Silent behaviour change | **Characterisation tests** pin current output *before* any change |
| Drift from the goal | A written plan or handoff file Claude re-reads |
| Context exhaustion | `/compact` with a focus, or `/clear` and resume from the handoff file |
| Big-bang breakage | Small steps, tests after each, **commit after each green step** |
| Lost knowledge | `notes/HANDOFF.md`: goal, done, next, risks, how to verify |
| Overconfident completion | A machine-checkable definition of done (tests and labcheck) |

Read **TF-109** in [ISSUES.md](../practice-app/ISSUES.md). Note "byte-for-byte identical", and the Markdown quirk where
in-progress tasks render as `[ ]`. That quirk must survive.

## 🛠️ Steps

```bash
cp notes/templates/HANDOFF.md notes/HANDOFF.md
```

**1. Pin the behaviour first.** `/clear`, then:

> Write characterisation tests in practice-app/tests/test_report_builder.py for
> @practice-app/src/taskforge/legacy/report_builder.py. Build a fixture with a frozen clock and tasks covering:
> done, in_progress, todo, overdue, high priority, no due date, and a title and project name containing & and <.
> Assert the EXACT full output for text, md and html, plus an empty project and an unknown format.
> Do not change report_builder.py. Run the tests. They must pass against the current code.

Commit: `test(legacy): characterise report builder output (TF-109)`.

**2. Plan and write the handoff.** Plan mode:

> Plan a refactor of report_builder.py into small functions (no function over 40 lines), with the counting
> logic shared across formats. Behaviour must stay byte-identical. Break it into 3–4 steps, each ending with
> the tests green and a commit. Write the plan into notes/HANDOFF.md under Goal / Next / Risks / How to verify.

**3. Execute step 1 only.** Approve, let it do **one** step, run the tests, and commit. Update `HANDOFF.md`
(move the step to **Done**).

**4. Simulate losing the session.** `/exit`. Start a **new** `claude` session and say only:

> Continue the task described in @notes/HANDOFF.md. Do the next step only, then update the handoff.

Did it pick up correctly with no other context? That's the test of a good handoff.

**5. Finish** the remaining steps the same way: one step, tests, commit, update the handoff. If context gets large,
`/compact keep: the handoff file and the current step`.

**6. Verify against the golden outputs.**

```
!uv run labcheck w5d25
```

**7. Take the Week 5 quiz:** [assessments/week5_quiz.md](../assessments/week5_quiz.md).

## ✅ Checkpoint

```bash
uv run labcheck w5d25
uv run labcheck budget
```

## 💰 Budget & cost log

Cap: **$1.40**.

```bash
uv run labcheck log w5d25 1.10 "TF-109 refactor with handoffs"
```

Week 5 total should be **≤ $7**.

## 🚀 Stretch

- Ask the Day 21 `code-reviewer` subagent to review the full refactor diff (`git diff <first-commit>..HEAD`).
- Point `services.is_overdue` and the report builder at **one** overdue rule. Is that safe given the golden tests? Prove it.

## 💼 Commercial application

Legacy modernisation is one of the highest-value uses of coding agents, and one of the riskiest. The
pattern you just used (pin behaviour, plan, small verified steps, durable handoffs) is how teams run
multi-day agent migrations without heroics.

## 🤔 Reflect

1. Would you have caught the `[ ]`-for-in-progress quirk without characterisation tests?
2. What did the fresh session in step 4 get wrong or right? What would improve your handoff?
3. Which countermeasure in the table did you actually need?

## ➡️ Next

Week 6: [Agent SDK, Capstone & Certification](../6_agent_sdk_capstone_certification/README.md)
