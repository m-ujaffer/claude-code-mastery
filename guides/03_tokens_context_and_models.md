# Guide 03: Tokens, context and models

## Tokens

Models read and write **tokens**, chunks of text averaging about ¾ of an English word (code is
usually denser). You pay for:

- **Input tokens**: everything Claude reads on each request. That includes the system prompt, tool definitions, your CLAUDE.md, the conversation so far, file contents and command output.
- **Output tokens**: everything Claude writes, including tool calls. Output is about 5× the input price.
- **Cache reads**: repeated input, such as the same system prompt and history, is cached and costs a small fraction of the normal input price. Claude Code does this automatically. It's a big reason long sessions aren't as expensive as you'd expect.

## Context

Every turn re-sends the conversation. So:

1. **A long conversation makes every later turn more expensive.** Even with caching, new content keeps adding up.
2. **A big file read early on stays in the context** until you `/clear` or `/compact`.
3. **Irrelevant context makes answers worse, not just more expensive.**

Commands to manage context:

| Command | What it does | When |
|---|---|---|
| `/context` | Shows what's using your context window | Whenever a session feels slow or pricey |
| `/clear` | Starts a fresh conversation (CLAUDE.md is re-read) | **Between unrelated tasks.** This is your #1 habit. |
| `/compact <focus>` | Summarises the conversation so far, keeping what you name | Mid-task, when the context is big but you need continuity |
| `/cost` | Token usage and estimated cost for the session | End of every lab |

## Models

Claude Code lets you pick a model per session (`/model`), per subagent (`model:` frontmatter)
and per headless run (`--model`). Use the aliases `haiku`, `sonnet` and `opus`; they point at the
current version of each family.

| Alias | Use it for | Relative cost |
|---|---|---|
| `haiku` | Simple, well-specified work: search, summarising, boilerplate tests, subagent grunt work | $ |
| `sonnet` | **Everyday coding.** This is the course default. | $$ |
| `opus` | Hard design problems, gnarly debugging, big refactors you've already planned | $$$ |

Prices (per million tokens, input/output, at the time of writing): Haiku 5.5 $0.10/$0.50,
Sonnet 5.5 $2/$10, Opus 5.5 $4/$20. Always check the current pricing page.

**Effort** is a second dial: `/effort` sets how hard the model thinks. Lower effort means fewer
tokens and faster answers on easy tasks.

## Rules of thumb

- Start every new task with `/clear`.
- Mention the files that matter (`@practice-app/src/taskforge/services.py`) instead of asking Claude to "look around".
- Ask for **plans** before **code** on anything multi-file. A bad plan is cheap to fix; bad code isn't.
- Keep CLAUDE.md short. It's sent in **every** request.
- Use Haiku subagents for "read lots, return a little" work, so the reading never enters your main context.
