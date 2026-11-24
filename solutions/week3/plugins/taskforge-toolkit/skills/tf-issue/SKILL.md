---
name: tf-issue
description: Implement a TaskForge backlog issue (TF-###) test-first, following the team workflow. Use when asked to work on a TF issue.
argument-hint: TF-###
disable-model-invocation: true
---
# Implement $ARGUMENTS

1. Read the `$ARGUMENTS` entry in `practice-app/ISSUES.md`. Restate its acceptance criteria as a checklist.
2. Check whether it's already implemented: look for the behaviour in the code and tests, and run `uv run labcheck`
   for the matching lab if you know it. **If every criterion is already met, say so and stop.**
3. If the change touches more than two files, propose a short plan and wait for approval.
4. Write failing tests first (in `practice-app/tests/`). Run them and show that they fail for the right reason.
5. Implement the smallest change that makes them pass. Do not edit the tests you just wrote, or existing tests.
6. Run `uv run pytest -q` and `uv run ruff check practice-app`.
7. Review your diff against [checklist.md](checklist.md).
8. Finish with: files changed, the acceptance checklist ticked, and anything left over.
