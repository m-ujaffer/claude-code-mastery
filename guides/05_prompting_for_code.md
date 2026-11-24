# Guide 05: Prompting for code

Claude Code is very capable, but it's working from **your words plus what it can see**. Good
prompts close the gap between what's in your head and what's in the repo.

## The anatomy of a strong task prompt

1. **Goal**: what should be true when you're done.
2. **Context**: where to look, using `@file` mentions or issue IDs.
3. **Constraints**: conventions, things not to touch, libraries to use or avoid.
4. **Verification**: how Claude should prove it works (which tests to run, what to check).
5. **Output**: what you want back (a plan, a diff, a summary, a commit).

### Vague

> fix the overdue thing

### Precise

> Fix TF-101 in @practice-app/ISSUES.md. The rule lives in `is_overdue` in
> @practice-app/src/taskforge/services.py. First add failing tests to
> practice-app/tests/test_services.py for "due today" and "done but past due", run them to
> confirm they fail, then fix the function. Don't change its signature. Run `uv run pytest -q`
> and show me the diff.

The precise version is usually **cheaper** as well as better. Claude spends fewer turns
exploring and guessing.

## Patterns that work

| Pattern | Example |
|---|---|
| **Test first** | "Write a failing test that reproduces X, run it, *then* fix." |
| **Explore, plan, then code** | "Read A and B. Propose a plan. Don't write code yet." |
| **Name the convention** | "Get time from `taskforge.clock`, not `date.today()`." |
| **Ask for options** | "Give me two approaches with trade-offs, then recommend one." |
| **Bound the change** | "Only touch files under practice-app/src/taskforge/api/." |
| **Make it verify** | "Run the tests and the linter before you say you're done." |
| **Interview me** | "Ask me up to three clarifying questions before you start." |

## Anti-patterns

- **Kitchen-sink prompts**: five unrelated tasks in one message. Do them one at a time and `/clear` between.
- **Correcting by accretion**: ten follow-ups patching a bad approach. Rewind instead (`Esc Esc`) and re-prompt with what you learned.
- **Trusting without reading**: you approve every diff, so read it (see [Guide 06](06_reviewing_ai_written_code.md)).
- **Shouting**: "YOU MUST NEVER…" in caps rarely helps modern models. Explain *why* the rule exists instead.

## Structured output (Week 4)

When a program, not a person, will read the answer, ask for JSON and **enforce** it:
`claude -p --json-schema schema.json`. Describe each field's meaning in the schema's `description`s.
