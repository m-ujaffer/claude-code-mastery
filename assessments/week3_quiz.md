# Week 3 quiz: Configuration & Extensibility

10 questions · about 10 minutes · offline · answers in [answers/week3_answers.md](answers/week3_answers.md)

**1.** Your security team requires that no engineer can ever enable `bypassPermissions`, whatever their local settings say. Where does that go?
- A) The project `.claude/settings.json`
- B) Each user's `~/.claude/settings.json`
- C) Managed (enterprise) settings
- D) CLAUDE.md

**2.** `.claude/settings.json` allows `Bash(git log *)` and `.claude/settings.local.json` allows `Bash(gh pr view *)`. What's effective?
- A) Only the local file's rule
- B) Only the shared file's rule
- C) Both: permission lists merge across settings files
- D) Neither, because they conflict

**3.** You deny `Read(./.env)`, but Claude still prints the secrets with `cat .env`. Best fix?
- A) Add "never read .env" to CLAUDE.md
- B) Add a PreToolUse hook on Bash that blocks commands reading `.env` (and/or a matching Bash deny rule)
- C) Rename `.env`
- D) Use plan mode

**4.** A PreToolUse hook wants to block a tool call and tell Claude why. What should it do?
- A) Exit 2 and print the reason to stderr (or return a JSON deny decision)
- B) Exit 1 and print to stdout
- C) Exit 0 with no output
- D) Kill the Claude process

**5.** Which need is best served by a **hook** rather than a CLAUDE.md instruction?
- A) "Every edited Python file must be formatted with ruff"
- B) "We prefer descriptive variable names"
- C) "Explain trade-offs briefly"
- D) "The API layer handles HTTP concerns"

**6.** A skill edits code and should only run when a human explicitly asks for it. Which frontmatter achieves that?
- A) `model: haiku`
- B) `disable-model-invocation: true`
- C) `allowed-tools: Read`
- D) `user-invocable: false`

**7.** Why are skills cheap to have installed even when there are many of them?
- A) Only their short descriptions sit in context until a skill is actually used
- B) They're compressed
- C) They don't count towards tokens
- D) They run on Haiku

**8.** In a plugin, where does `plugin.json` go, and where do `skills/` and `hooks/` go?
- A) All inside `.claude-plugin/`
- B) `plugin.json` in `.claude-plugin/`; components at the plugin root
- C) All at the repo root
- D) `plugin.json` at the root; components in `.claude-plugin/`

**9.** A plugin hook script needs to reference a file shipped inside the plugin. Which variable should it use?
- A) `$HOME`
- B) `$PWD`
- C) `${CLAUDE_SESSION_ID}`
- D) `${CLAUDE_PLUGIN_ROOT}`

**10.** Your team wants everyone to get the same workflow skill, review command and guard hook, with versioned updates. Best distribution?
- A) Paste them into Slack
- B) Each engineer copies them into `~/.claude/`
- C) Put them all in CLAUDE.md
- D) A plugin in a team marketplace that engineers add and install
