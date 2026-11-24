# Week 1 · Day 1: Your first Claude Code session

| | |
|---|---|
| **Level** | Basics |
| **CCA-F domain** | 2 · Claude Code configuration & workflows |
| **Time** | 5 min read · 40 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $0.40 |
| **Check** | `uv run labcheck w1d1` |

## 🎯 Goal

Start Claude Code, use it to understand an unfamiliar codebase, approve your first
file write, and find out exactly what that cost.

## 📖 Primer

Claude Code is an **agent** in your terminal. You describe a goal. It reads files, runs
commands and edits code using **tools**, and asks your permission before doing anything
that changes things. You stay in charge: you approve, reject, interrupt and redirect.

Three things to notice today:
1. **Tool calls.** Watch Claude decide *which* files to read. That reading is what you pay for.
2. **Permission prompts.** Reading is allowed by default; writing a file asks first.
3. **The status line** at the bottom shows the model, this session's cost and your month-to-date estimate.

## 🛠️ Steps

**1. Make sure you're set up.** In the terminal, from the repo root:

```bash
uv run labcheck doctor
```

**2. Start Claude Code** from the repo root and look around:

```bash
claude
```

Type `/help` and skim the list of slash commands. Then type `/status` to see the model,
account and working directory. Confirm it's using your **API key**.

**3. Ask your first question.** Type:

> What is in this repository? Give me a 5-bullet overview. Don't read more than you need.

Watch the tool calls scroll by (`Read`, `Glob`, `Grep`, …). Notice which files it chose.

**4. Narrow the question.** Now ask about the practice app specifically:

> Explain the architecture of practice-app/src/taskforge. How does a request to
> POST /tasks flow through main.py, api/tasks.py, repository.py and services.py?

**5. Ask something you'd normally grep for:**

> Where is "overdue" decided, and is there anything suspicious about how it's done?

(Don't fix anything yet! That's Day 3. Just notice what it finds.)

**6. Your first file write.** Ask:

> Write what you've told me into notes/taskforge-overview.md: purpose, the layers
> (api, repository, services, clock, db, legacy), how a POST /tasks request flows,
> and how to run the tests. Keep it under 60 lines.

Claude will ask permission to create the file. Read the proposed content, then approve it.

**7. Check the cost.** Type `/cost`. (Some newer versions call this `/usage`.) Note:
- the total cost
- input vs output tokens. Which dominates, and why?

Compare it with the `session $` in the status line.

**8. Exit** with `/exit`.

## ✅ Checkpoint

```bash
uv run labcheck w1d1
```

## 💰 Budget & cost log

Cap: **$0.40**. Log what `/cost` said:

```bash
uv run labcheck log w1d1 0.25 "first session"
```

## 🚀 Stretch

- Run `claude -p "In one sentence, what does practice-app/src/taskforge/clock.py do?"` in the shell.
  That's **headless mode**: one question, one answer, no session. You'll use it heavily in Week 5.
- Ask Claude to draw an ASCII diagram of the request flow and add it to your overview.

## 💼 Commercial application

The fastest win most teams get from Claude Code is **onboarding**: a new engineer can ask
"how does X work here?" and get a grounded answer in minutes instead of a day of code archaeology.
Today you produced exactly that kind of document.

## 🤔 Reflect

1. Which files did Claude read in step 3, and which did it skip? Was that the right call?
2. Why was the output-token count so much smaller than the input-token count?
3. What would you have done differently in step 3 to make it cheaper?

## ➡️ Next

[Day 2: Modes, mentions and rewind](2_lab2_modes_and_rewind.md)
