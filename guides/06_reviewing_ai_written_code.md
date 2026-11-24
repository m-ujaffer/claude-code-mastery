# Guide 06: Reviewing AI-written code

You are the engineer of record for every line Claude writes. These are the checks that
catch most problems.

## The 60-second diff review

1. **Scope.** Did it change only what you asked for? Unexpected files are a red flag.
2. **Tests.** Were tests added or updated? Did it *weaken* any existing test to make it pass?
3. **Behaviour at the edges.** Empty input, `None`, boundaries (199/200/201), "today", "done".
4. **Conventions.** Layering (SQL in `repository.py`), `clock.today()`, naming, error codes.
5. **Security.** Injection (string-built SQL with user input), secrets, permission changes, new dependencies.
6. **Leftovers.** Debug prints, commented-out code, TODOs, unused imports.

## Red flags specific to AI-written code

| Smell | What to do |
|---|---|
| A test was changed so it passes | Ask why. Usually the code is wrong, not the test. |
| Over-engineering: new abstractions, config options, "future-proofing" | Ask for the simplest version that meets the acceptance criteria. |
| A confident claim it "ran the tests" | Check the tool output yourself, or run `uv run pytest` yourself. |
| An invented API (a method that doesn't exist) | Run it. Check the docs. |
| Broad `except Exception: pass` | Ask for specific errors and a failing case. |
| A silent behaviour change in untouched code | Characterisation tests (Week 5, Day 25). |

## Make Claude help you review

- "Review your own diff as a skeptical senior engineer. List risks, not praise."
- A **read-only reviewer subagent** (Week 5, Day 21) gives a second opinion with fresh context.
- In CI, `anthropics/claude-code-action` can review every PR (Week 5, Day 24).

You'll still read the diff yourself. Two independent reviews beat one.
