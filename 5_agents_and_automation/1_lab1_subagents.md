# Week 5 · Day 21: Subagents

| | |
|---|---|
| **Level** | Advanced |
| **CCA-F domain** | 1 · Agentic architecture · 5 · Context management |
| **Time** | 10 min read · 35 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $1.20 |
| **Check** | `uv run labcheck w5d21` |

## 🎯 Goal

Use subagents to keep your main context clean, give specialists only the tools they need, and run
cheap work on a cheap model.

## 📖 Primer

A **subagent** runs in its **own context window** with its own system prompt, tools and model. It does the
work and returns only a summary to the main conversation. That gives you two benefits:

1. **Context isolation.** Reading 30 files happens *there*, not in your main session.
2. **Specialisation and least privilege.** A reviewer that *can't* edit files can't "fix" things it should only report.

Built-in subagents include **Explore** (read-only, fast search), **Plan** (research for plan mode) and
**general-purpose**. Custom ones live in `.claude/agents/<name>.md`:

```markdown
---
name: code-reviewer
description: Reviews diffs for correctness, security and TaskForge conventions. Use after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---
You are a senior reviewer. Only run read-only git commands (git diff, git log, git show).
Report findings as: severity, file:line, problem, suggested fix. Never edit files.
```

Claude delegates automatically when a description matches, or you can ask explicitly
("use the code-reviewer subagent to…"). Manage them with `/agents`.

**Trade-offs:** subagents start cold (they re-read what they need), add latency, and the main agent only sees
their summary. They're bad for tightly coupled work that needs shared context.

## 🛠️ Steps

```bash
cp notes/templates/w5d21-subagents.md notes/w5d21-subagents.md
```

**1. Measure the baseline.** `/clear`, then:

> Find every place in practice-app where dates or times are created or compared, and list
> file:line with a one-line note on each. Do it yourself, without subagents.

Run `/context` and record the main context size under **main context before**. `/clear`.

**2. Delegate the same task.**

> Use the Explore subagent to find every place in practice-app where dates or times are created
> or compared. Return only file:line plus a one-line note for each.

Run `/context`. Record **main context after**. What did the main session receive?

**3. Create a read-only reviewer.** Run `/agents` → create a project agent, or write
`.claude/agents/code-reviewer.md` yourself (see the primer). Its tools list must **not** include Edit or Write.

**4. Create a cheap test writer.** `.claude/agents/test-writer.md` with `model: haiku`, tools
`Read, Grep, Glob, Edit, Write, Bash`, and a body that says: write pytest tests only under `practice-app/tests/`,
follow the conventions in `.claude/rules/`, run them, and never change application code.

**5. Use them together.**

> Use the test-writer subagent to add tests for the uncovered lines in
> practice-app/src/taskforge/repository.py (run coverage to find them). Then use the code-reviewer
> subagent to review the resulting diff.

Was Haiku good enough for the tests? Did the reviewer find anything?

**6. Notes and commit.** Answer **when not to use a subagent**, then commit `.claude/agents/`.

## ✅ Checkpoint

```bash
uv run labcheck w5d21
```

## 💰 Budget & cost log

Cap: **$1.20**. Subagent token use is included in `/cost`.

```bash
uv run labcheck log w5d21 0.90 "subagents"
```

## 🚀 Stretch

- Give the reviewer a `PreToolUse` hook in its frontmatter that only allows `git diff|log|show` Bash
  commands. Now "read-only" is **enforced**, not just requested.
- Add `memory: project` to the reviewer and run it twice. What does it remember?

## 💼 Commercial application

Subagents are the simplest **multi-agent architecture**: an orchestrator that delegates to specialists with
isolated contexts and scoped tools. Getting the boundaries right (what each agent can see, do and return)
is exactly the design skill the certification's largest domain tests.

## 🤔 Reflect

1. How much main-context did delegation save in step 2? What was lost?
2. The reviewer has Bash. Is it really read-only? How would you enforce it?
3. Give one task where a subagent would make things *worse*.

## ➡️ Next

[Day 22: Parallel work with worktrees](2_lab2_parallel_worktrees.md)
