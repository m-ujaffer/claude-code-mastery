# Week 3 · Day 13: Hooks, deterministic guardrails and automation

| | |
|---|---|
| **Level** | Intermediate → Advanced |
| **CCA-F domain** | 2 · Claude Code configuration · 5 · Reliability |
| **Time** | 10 min read · 35 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $1.00 |
| **Check** | `uv run labcheck w3d13` |

## 🎯 Goal

Write hooks that **always** run: one that blocks dangerous shell commands, one that formats every
Python file Claude edits, and one that tells you when Claude is done.

## 📖 Primer

**Hooks** are your own commands that Claude Code runs at lifecycle events. They're deterministic:
they don't depend on the model remembering an instruction.

| Event | When | Typical use |
|---|---|---|
| `PreToolUse` | before a tool runs | block or modify risky actions |
| `PostToolUse` | after a tool succeeds | format, lint, log |
| `UserPromptSubmit` | when you send a prompt | add context, block secrets in prompts |
| `Stop` | when Claude finishes responding | notify, run final checks |
| `SessionStart` | when a session starts | load dynamic context |

Configured in settings:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/block-dangerous.py\"" }
        ]
      }
    ]
  }
}
```

The hook gets JSON on **stdin**, with fields like `tool_name` and `tool_input` (for Bash, `tool_input.command`).
**Exit code 2 blocks** the action, and whatever you print to **stderr** is shown to Claude as the reason.
Exit 0 means carry on. Other exit codes are non-blocking errors.

⚠️ Hooks run with **your** permissions, automatically. Review hook code like production code.

## 🛠️ Steps

**1. The guard (PreToolUse).** Ask Claude to help you write `.claude/hooks/block-dangerous.py`, but
specify the behaviour precisely:

> Write a Python script .claude/hooks/block-dangerous.py for a Claude Code PreToolUse hook on Bash.
> It reads JSON from stdin, takes tool_input.command, and exits 2 with a clear message on stderr if the
> command does a recursive force delete (rm -rf / rm -fr in any flag order), a git push with --force or -f,
> a git reset --hard, pipes curl/wget into sh/bash, or reads a .env file (cat/less/head/tail .env).
> Otherwise exit 0. Standard library only.

**Test it without Claude**, by piping fake events into it:

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | python3 .claude/hooks/block-dangerous.py; echo "exit=$?"
echo '{"tool_name":"Bash","tool_input":{"command":"uv run pytest"}}' | python3 .claude/hooks/block-dangerous.py; echo "exit=$?"
```

**2. Register it** in `.claude/settings.json` under `hooks.PreToolUse` with matcher `Bash` (see the primer).
Restart Claude (or run `/hooks` to review the configured hooks). Then ask Claude: *"print the contents of .env with cat"*.
Day 11's gap is now closed.

**3. Auto-format (PostToolUse).** Create `.claude/hooks/format-python.py`, which reads `tool_input.file_path` and,
if it's a `.py` file, runs `uv run ruff format <file>` and `uv run ruff check --fix --quiet <file>`. Register it on
matcher `Edit|Write`. Test it: ask Claude to add a badly formatted function and watch it get formatted.

**4. Done notification (Stop).** Add a `Stop` hook that rings the terminal bell or writes a line to
`notes/.claude-activity.log` with a timestamp. (Tiny, but you'll appreciate it in long tasks.)

**5. Watch hooks fail safely.** Break the format hook on purpose (a typo in the path). What does Claude Code show?
Fix it.

**6. Commit** `.claude/hooks/` and the settings change.

## ✅ Checkpoint

```bash
uv run labcheck w3d13
```

It runs your guard with test inputs and checks the exit codes.

## 💰 Budget & cost log

Cap: **$1.00**.

```bash
uv run labcheck log w3d13 0.70 "hooks"
```

## 🚀 Stretch

- Instead of blocking, use the JSON output form to **ask** the user: print
  `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask", "permissionDecisionReason": "..."}}`
  and exit 0 for `git push` without `--force`.
- Add a `UserPromptSubmit` hook that blocks prompts containing something that looks like an API key (`sk-ant-`).

## 💼 Commercial application

Hooks are how platform teams make guarantees: "every file is formatted", "nothing touches prod
credentials", "every session is logged for audit". Unlike instructions, hooks are something a security
reviewer can **verify**.

## 🤔 Reflect

1. What's the difference between denying `Bash(rm -rf *)` in permissions and blocking it in a hook? When do you need both?
2. Your guard uses regexes. Name a command that slips past it. Is "perfect" possible here?
3. Which of your CLAUDE.md rules would be better as a hook?

## ➡️ Next

[Day 14: Output styles, status line and plugins](4_lab4_styles_statusline_plugins.md)
