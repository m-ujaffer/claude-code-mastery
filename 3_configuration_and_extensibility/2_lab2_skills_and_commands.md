# Week 3 · Day 12: Skills and slash commands

| | |
|---|---|
| **Level** | Intermediate |
| **CCA-F domain** | 2 · Claude Code configuration & workflows |
| **Time** | 5 min read · 40 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $0.90 |
| **Check** | `uv run labcheck w3d12` |

## 🎯 Goal

Turn the prompts that worked best in Weeks 1–2 into **reusable skills** your whole team can run
with one slash command.

## 📖 Primer

A **skill** is a folder with a `SKILL.md`. Its frontmatter says when and how it's used; its body is
the instructions Claude follows.

```
.claude/skills/tf-issue/
├── SKILL.md            # required
└── checklist.md        # optional supporting files, read only when needed
```

```markdown
---
name: tf-issue
description: Implement a TaskForge backlog issue test-first. Use when asked to work on a TF-### issue.
argument-hint: TF-###
disable-model-invocation: true
---
Implement $ARGUMENTS from practice-app/ISSUES.md ...
```

- The folder name becomes the command: `/tf-issue TF-107`.
- `$ARGUMENTS` is replaced by what you type after the command; `$0`, `$1`, … are positional arguments.
- **Model-invoked vs manual.** By default Claude can load a skill *by itself* when the description
  matches the task. `disable-model-invocation: true` makes it manual only.
- Only the **description** sits in context until the skill is used, so skills are cheap to have around.
- Classic **slash commands** (`.claude/commands/name.md`) still work and are fine for simple prompts.
  Skills are preferred for anything with supporting files.

## 🛠️ Steps

**1. Write the `tf-issue` skill.** Create `.claude/skills/tf-issue/SKILL.md`. Write the body yourself,
distilling Days 3, 4, 8 and 10:

- read the issue `$ARGUMENTS` in `practice-app/ISSUES.md` and restate the acceptance criteria
- if it touches more than two files, propose a plan and wait for approval
- write failing tests first and show that they fail
- implement without editing the new tests
- run `uv run pytest -q` and `uv run ruff check practice-app`
- finish with a summary: files changed, criteria met (as a checklist), anything left over

Frontmatter: a **specific** `description` (at least 30 characters), `argument-hint`, and
`disable-model-invocation: true`. (Why manual? This skill edits code. You want to decide when it runs.)

**2. Add a supporting file.** Create `.claude/skills/tf-issue/checklist.md` with the review checklist from
[Guide 06](../guides/06_reviewing_ai_written_code.md), and reference it from SKILL.md:
"Before finishing, review the diff against checklist.md." Claude only reads it when it gets to that step.

**3. Try it.** `/clear`, then:

```
/tf-issue TF-101
```

TF-101 is already done, so a good skill should notice and **stop** rather than re-implement it. If it
doesn't, improve the instructions. (Testing a skill on a "should do nothing" case is a great habit.)

**4. A classic command.** Create `.claude/commands/review-diff.md`:

```markdown
---
description: Review the current git diff against the team checklist
---
Run `git diff` (and `git diff --staged`). Review the changes against
@.claude/skills/tf-issue/checklist.md. Report risks first, then nits. Do not edit files.
```

Run `/review-diff` on any small change.

**5. A model-invoked skill.** Create `.claude/skills/taskforge-conventions/SKILL.md` **without**
`disable-model-invocation`, with a description like "TaskForge layering and time conventions. Use when
writing or reviewing TaskForge code." and move the detailed conventions from CLAUDE.md into it. Keep one line in
CLAUDE.md pointing to it. What does this do to the size of your always-loaded context?

**6. Commit** `.claude/skills/` and `.claude/commands/`.

## ✅ Checkpoint

```bash
uv run labcheck w3d12
```

## 💰 Budget & cost log

Cap: **$0.90**.

```bash
uv run labcheck log w3d12 0.70 "skills"
```

## 📤 Push your progress

```bash
git add -A && git commit -m "w3d12: Skills and slash commands" && git push
```

## 🚀 Stretch

- Add `allowed-tools` to the `review-diff` command so it can only run `git diff` (no edits). Test it.
- Write a skill that takes **two** arguments (`$0`, `$1`), for example `/compare-approaches <file> <goal>`.

## 💼 Commercial application

Skills are how a team's **best prompts become shared infrastructure**. A senior engineer's
"how we do a migration here" becomes `/migration`, versioned in git, so everyone gets the same quality, and
it costs almost nothing in context until someone uses it.

## 🤔 Reflect

1. Did `/tf-issue TF-101` correctly stop? What instruction made the difference?
2. When should a skill be model-invoked, and when should it be manual?
3. What's the context cost of 20 skills you're not using right now?

## ➡️ Next

[Day 13: Hooks](3_lab3_hooks.md)
