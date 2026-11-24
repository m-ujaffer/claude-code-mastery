# Week 5 quiz: Agents & Automation

10 questions · about 10 minutes · offline · answers in [answers/week5_answers.md](answers/week5_answers.md)

**1.** What's the main benefit of delegating "find every date comparison in the codebase" to a subagent?
- A) Subagents are always cheaper per token
- B) Subagents can edit more files
- C) Subagents skip permissions
- D) The heavy reading happens in the subagent's own context; the main session gets only the summary

**2.** You want a reviewer subagent that can't modify files. Which is the strongest setup?
- A) Say "don't edit" in its prompt
- B) `model: haiku`
- C) A `tools` list without Edit/Write, plus enforcement on Bash (for example a hook that only allows read-only git commands)
- D) Run it in the background

**3.** When is a subagent the *wrong* choice?
- A) Broad codebase search
- B) Independent research that returns a summary
- C) Reviewing a diff with fresh eyes
- D) A tightly coupled edit that depends on the details of the current conversation

**4.** Two Claude sessions must implement two features at the same time in one repo. What stops them interfering?
- A) Separate git worktrees on separate branches
- B) Different terminal colours
- C) Plan mode in both
- D) `/compact` in both

**5.** A headless nightly job must never spend more than about $0.30 per run. Which flags matter most?
- A) `--max-budget-usd 0.30` and `--max-turns`
- B) `--verbose`
- C) `--continue`
- D) `--model opus`

**6.** In `claude -p` with no permission mode set, Claude tries a tool that isn't in `--allowedTools` and would normally prompt. What happens?
- A) The script hangs waiting for input
- B) It's approved automatically
- C) The call is denied, and the run continues without it
- D) The run crashes with a stack trace

**7.** Which CI workflow setting prevents paying for reviews of commits that have already been superseded?
- A) `concurrency` with `cancel-in-progress: true`
- B) `timeout-minutes`
- C) `fetch-depth: 1`
- D) `runs-on: ubuntu-latest`

**8.** On a public repo, why restrict `@claude` comment triggers to trusted authors?
- A) To save GitHub minutes only
- B) Anyone could otherwise trigger runs that spend your budget and act with the workflow's permissions
- C) Claude can't read comments from strangers
- D) GitHub requires it

**9.** Before an agent refactors legacy code whose exact output customers depend on, what should exist first?
- A) A new CLAUDE.md
- B) Characterisation tests that pin the current output
- C) A faster model
- D) A plugin

**10.** A long refactor spans several sessions. What best preserves progress if a session ends unexpectedly?
- A) A very long conversation
- B) Small committed steps plus a handoff file (goal, done, next, risks, how to verify)
- C) Opus with maximum effort
- D) Turning off auto-compaction
