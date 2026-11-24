# Week 1 · Day 2: Permission modes, mentions, bash mode and rewind

| | |
|---|---|
| **Level** | Basics |
| **CCA-F domain** | 2 · Claude Code configuration & workflows |
| **Time** | 5 min read · 40 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $0.50 |
| **Check** | `uv run labcheck w1d2` |

## 🎯 Goal

Get fluent with the controls you'll use every day: permission modes, plan mode, `@` file
mentions, `!` bash mode, interrupting, and rewinding mistakes.

## 📖 Primer

| Control | What it does |
|---|---|
| **Default mode** | Claude asks before editing files or running most commands |
| **Accept-edits mode** | File edits are auto-approved for the session; commands still ask |
| **Plan mode** | Claude can read and think but **not** change anything. It proposes a plan for you to approve |
| `Shift+Tab` | Cycles through the modes. The current mode shows near the prompt |
| `@path` | Pulls a file straight into context, so Claude doesn't have to search for it |
| `!command` | Runs a shell command yourself; the output goes into the conversation |
| `Esc` | Interrupts Claude mid-action so you can redirect |
| `Esc Esc` / `/rewind` | Rolls the conversation and/or code back to an earlier checkpoint |

Permission modes are a **safety vs speed** dial. In a Codespace (a sandbox) you can be braver
than on your laptop, but you're still the reviewer.

## 🛠️ Steps

Copy the notes template first, and fill it in as you go:

```bash
cp notes/templates/w1d2-modes.md notes/w1d2-modes.md
```

Start `claude` from the repo root.

**1. Plan mode.** Press `Shift+Tab` until you see **plan mode**. Then:

> Plan how you'd add a GET /version endpoint to @practice-app/src/taskforge/main.py that
> returns {"version": ...}. Don't implement it.

Notice that it can read but proposes no edits. When it offers to proceed, **decline**.
Write in your notes what plan mode is good for.

**2. Default mode.** `Shift+Tab` back to default. Then:

> Implement that /version endpoint now.

Approve the edit **once** (not "always"). Write down what the permission prompt offered you.

**3. Bash mode.** Type:

```
!uv run pytest -q
```

The output is now part of the conversation. Ask: *"Did my change break anything?"*

**4. Accept-edits mode.** `Shift+Tab` to accept edits, then:

> Add a docstring to every function in @practice-app/src/taskforge/api/deps.py

No prompt this time. When is that OK, and when is it not? Note it down.

**5. Interrupt.** Ask:

> Add type hints and docstrings to every file in practice-app/src/taskforge

As soon as it starts editing the second file, press **Esc**. Tell it: *"Stop. Only do models.py."*

**6. Rewind.** Press **Esc Esc** (or type `/rewind`) and choose the checkpoint from **before step 2**.
Choose to restore **code and conversation**. Then check:

```
!git status
```

`main.py`, `deps.py` and `models.py` should be back to their originals. (If anything is left
over, run `!git restore practice-app` and make a note of it.)

**7. Run `/cost`**, then exit.

## ✅ Checkpoint

```bash
uv run labcheck w1d2
```

It checks that your notes are filled in and that the experiment was fully rewound.

## 💰 Budget & cost log

Cap: **$0.50**.

```bash
uv run labcheck log w1d2 0.30 "modes + rewind"
```

## 📤 Push your progress

```bash
git add -A && git commit -m "w1d2: Permission modes, mentions, bash mode and rewind" && git push
```

## 🚀 Stretch

- Try `@practice-app/src/taskforge/` (a directory) in a prompt. What does Claude get?
- Read `.claude/settings.json`. Some commands are pre-approved under `permissions.allow`.
  Which ones, and why do you think the course chose those? (Week 3 goes deep on this.)

## 💼 Commercial application

Teams standardise on **plan mode for anything multi-file** and **default mode for production
repos**. Accept-edits is popular for well-tested repos where `git diff` is the review step.
Knowing these trade-offs is what lets you use agents safely on real code.

## 🤔 Reflect

1. Rewind restores files Claude edited. What does it **not** undo? (Hint: think about commands it ran.)
2. When would you choose plan mode even for a "small" change?
3. Was `@file` cheaper than letting Claude search? How could you tell?

## ➡️ Next

[Day 3: Fix a bug test-first](3_lab3_fix_a_bug_test_first.md)
