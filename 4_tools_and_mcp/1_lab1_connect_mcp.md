# Week 4 · Day 16: Connect an MCP server

| | |
|---|---|
| **Level** | Advanced |
| **CCA-F domain** | 4 · Tool design & MCP integration |
| **Time** | 10 min read · 35 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $0.80 |
| **Check** | `uv run labcheck w4d16` |

## 🎯 Goal

Connect an off-the-shelf MCP server, choose the right **scope**, keep secrets out of git, and see
exactly what it adds to Claude's context.

## 📖 Primer

The **Model Context Protocol (MCP)** is an open standard for connecting AI applications to tools and data.
An MCP **server** exposes:

| Primitive | What it is | In Claude Code |
|---|---|---|
| **Tools** | functions the model can call | appear as `mcp__<server>__<tool>` |
| **Resources** | readable data, addressed by URI | `@`-mentionable |
| **Prompts** | reusable prompt templates | appear as slash commands |

**Transports:** `stdio` (a local process Claude Code starts) or `http` (a remote server).

**Scopes**, set with `claude mcp add --scope ...`:

| Scope | Stored in | Shared? | Use for |
|---|---|---|---|
| `local` (default) | `~/.claude.json`, for this project | no | personal or experimental servers |
| `project` | `.mcp.json` in the repo | **yes, via git** | servers the whole team needs |
| `user` | `~/.claude.json` | no | your servers for every project |

`.mcp.json` supports **environment variable expansion**, `${VAR}` and `${VAR:-default}`, so tokens never
need to be committed.

## 🛠️ Steps

```bash
cp notes/templates/w4d16-mcp.md notes/w4d16-mcp.md
```

**1. Add a git MCP server at project scope.** The reference *git* server runs locally with `uvx`, with no account needed:

```bash
claude mcp add --scope project git -- uvx mcp-server-git --repository .
cat .mcp.json
claude mcp list
```

Everything after `--` is the command that starts the server.

**2. Approve and inspect.** Start `claude`. You'll be asked to approve the project-scoped server (a security
feature: a cloned repo can't silently start processes). Approve it, then:
- run `/mcp`, choose `git`, and look at its tools
- run `/context`. How many tokens do the tool definitions cost?

**3. Use it.**

> Using the git MCP tools (not Bash), summarise what changed in the last 5 commits and which
> TaskForge issues they relate to.

Watch for `mcp__git__...` tool calls. Approve them.

**4. A server that needs a secret.** This is the pattern for anything authenticated. Add a remote HTTP server
**with a token from an environment variable**. Edit `.mcp.json` to add a second entry (don't run it if you
don't have a token; the point is the *shape*):

```json
"github": {
  "type": "http",
  "url": "https://api.githubcopilot.com/mcp/",
  "headers": { "Authorization": "Bearer ${GITHUB_PAT}" }
}
```

The literal token never lands in the file. Each engineer sets `GITHUB_PAT` in their own environment, or as a
Codespaces secret. If you don't use it, remove the entry again. Unused servers cost context in **every** session.

**5. Fill in your notes** and commit `.mcp.json`.

## ✅ Checkpoint

```bash
uv run labcheck w4d16
```

It also checks that `.mcp.json` contains no literal secrets.

## 💰 Budget & cost log

Cap: **$0.80**.

```bash
uv run labcheck log w4d16 0.50 "first MCP server"
```

## 📤 Push your progress

```bash
git add -A && git commit -m "w4d16: Connect an MCP server" && git push
```

## 🚀 Stretch

- Add the `time` reference server at **local** scope (`claude mcp add time -- uvx mcp-server-time`). Where did
  it get stored? Why isn't it in `.mcp.json`?
- Use `/mcp` to **disable** a server for the session and compare `/context`.

## 💼 Commercial application

MCP is how Claude Code reaches issue trackers, databases, observability tools, design files and internal
APIs. Teams check a curated `.mcp.json` into each repo, so everyone gets the same integrations, and keep
credentials in each engineer's environment or secret store, never in git.

## 🤔 Reflect

1. Why does Claude Code ask for approval before starting servers from `.mcp.json`?
2. When is `project` scope the wrong choice?
3. What did the git server's tool definitions cost in context, and is that worth it every session?

## ➡️ Next

[Day 17: Build an MCP server for TaskForge](2_lab2_build_mcp_server.md)
