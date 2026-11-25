# Troubleshooting

Start with `uv run labcheck doctor`. It checks most of the things below.

## `claude: command not found` {#claude-not-found}

The devcontainer feature didn't finish. Try, in order:
1. Open a **new terminal** (the PATH may only be updated in new shells).
2. Command palette (`Ctrl/Cmd+Shift+P`) → **Codespaces: Rebuild Container**.
3. Install it by hand using the current command from https://code.claude.com/docs (Getting started).

## `ANTHROPIC_API_KEY` is not set

- Check the secret exists: github.com → Settings → Codespaces → Secrets, and that **your repo**
  is selected under *Repository access*.
- Secrets are injected when the Codespace **starts**. After adding one, rebuild the container
  or stop and restart the Codespace.
- Check from the terminal without printing the key: `test -n "$ANTHROPIC_API_KEY" && echo set`

## Claude Code asks me to log in instead of using the key

Choose the option to use the API key from the environment. If you logged in with a personal
account by mistake, run `/logout` inside Claude Code and start `claude` again.

## "Credit balance too low", "spend limit reached" or 429 errors

You've reached your workspace's monthly limit (or the org's). Tell your admin. Meanwhile, you
can still do everything that's offline: read ahead, take quizzes, run `labcheck`.

## The status line is missing or says `statusline: no data`

- Start Claude Code from the **repo root**. Project settings are read from the directory you
  launch from.
- Check the script runs: `echo '{}' | python3 .claude/statusline.py`

## labcheck fails but I think my work is right

- Run it with `-v` to see the hidden test output: `uv run labcheck w2d8 -v`
- Re-read the acceptance criteria in `practice-app/ISSUES.md`. They're precise on purpose.
- Compare with `solutions/`. Different code is fine as long as the behaviour matches.

## My practice-app is a mess and I'm behind

```bash
bash scripts/reset_to.sh week-3-start   # your current version is backed up to .backup/
```

## SQLite errors after a schema change ("no such column", "no such table")

The dev database was created with the old schema. It's disposable:
```bash
rm practice-app/taskforge.db
```

## `git push` is rejected, or says "no upstream branch"

- **"no upstream branch"**: you haven't pushed your branch yet. Run `git push -u origin <your-branch>` once.
- **Rejected on `main`**: `main` is protected. Make sure you're on your branch: `git branch --show-current`.
  If you committed on `main` by mistake: `git switch <your-branch> && git merge main`.
- **"fetch first" / non-fast-forward**: your branch changed elsewhere (another Codespace, or a PR merge).
  Run `git pull`, then push again.

## Port 8000 doesn't open

Open the **Ports** tab, find 8000 and click the globe icon. Add `/docs` to the URL for Swagger.
