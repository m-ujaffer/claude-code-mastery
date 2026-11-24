# Week 2 quiz: Context & Memory

10 questions · about 10 minutes · offline · answers in [answers/week2_answers.md](answers/week2_answers.md)

**1.** A teammate's CLAUDE.md is 400 lines, mostly copied from the README. What's the main problem?
- A) Every line is loaded into every request, so it costs tokens and dilutes the important instructions
- B) Claude can't read files that long
- C) CLAUDE.md must be under 100 characters
- D) Nothing; more context is always better

**2.** Where should a personal preference ("explain trade-offs before big edits") that only applies to you on this project go?
- A) `./CLAUDE.md`
- B) `.claude/settings.json`
- C) `practice-app/README.md`
- D) `./CLAUDE.local.md`

**3.** Testing conventions only matter when Claude edits test files. What's the best mechanism?
- A) Put them at the top of CLAUDE.md in caps
- B) A PreToolUse hook
- C) A comment in conftest.py
- D) A rule in `.claude/rules/` with `paths:` frontmatter matching the test directory

**4.** You added a rule but you're not sure it does anything. What's the reliable way to find out?
- A) Ask Claude whether it read the rule
- B) Run the same prompt in a fresh session with and without the rule, and compare behaviour
- C) Make the rule longer
- D) Check `/cost`

**5.** In the explore → plan → implement loop, what's the main value of challenging the plan before approving it?
- A) It makes the plan longer
- B) Plan mode is free
- C) Wrong approaches are cheap to fix in a plan and expensive to fix in code
- D) Claude needs encouragement

**6.** Why save an approved plan to a file such as `notes/plans/tf-104-plan.md`?
- A) It becomes a durable artefact: reviewable, and resumable by a fresh session or a colleague
- B) Claude Code can't hold plans in memory
- C) It's required for commits
- D) Files are cheaper than messages

**7.** CI fails on Claude's PR. What's the most effective first prompt?
- A) "Use gh to read the failing job's logs, explain the cause, then fix it and push"
- B) "Fix CI"
- C) "Rerun CI until it passes"
- D) "Disable the failing check"

**8.** In the TDD green phase, Claude proposes changing an assertion to make a test pass. What should you do?
- A) Accept; tests are just suggestions
- B) Refuse unless the test itself is wrong against the spec. The tests are the spec, and the code should change
- C) Delete the test
- D) Switch to Opus

**9.** What does 95% line coverage on `services.py` tell you?
- A) The code is correct
- B) The tests executed 95% of the lines. It says nothing about whether the assertions check the right behaviour
- C) There are no bugs in 95% of the code
- D) It's ready for production

**10.** Which belongs in a team CLAUDE.md?
- A) "Write good code"
- B) The full API reference
- C) How to run the tests and lint, and non-obvious conventions such as "get time from `taskforge.clock`"
- D) Yesterday's standup notes
