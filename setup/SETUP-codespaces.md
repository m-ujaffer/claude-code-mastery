# Setup: GitHub Codespaces (about 10 minutes)

Welcome! This is the only setup you need. Everything runs in a cloud
sandbox called a **Codespace**, so there's nothing to install on your laptop, and if
anything ever gets into a weird state you can throw the Codespace away and make a new one.

## Before you begin

You need:
- a **GitHub account** (your work account is fine)
- the **Anthropic API key** your course admin sent you. It starts with `sk-ant-`.
  Treat it like a password: never paste it into a file, a chat or a commit.

---

## Step 1: Make your own copy of the course

You need your **own** repository because in Weeks 2 and 5 you'll open pull requests and
run GitHub Actions against it.

1. Open the course repository on GitHub.
2. Click **Use this template**, then **Create a new repository**.
3. Owner: you (or your team's org, if your admin says so). Name: `claude-code-mastery`. Visibility: **Private**.
4. Click **Create repository**.

## Step 2: Store your API key as a Codespaces secret

Codespaces secrets are encrypted and injected as environment variables, so your key
never touches the repository.

1. Go to **github.com → your avatar → Settings → Codespaces**.
2. Under **Secrets**, click **New secret**.
3. Name: `ANTHROPIC_API_KEY`. Value: your key.
4. **Repository access**: choose your new `claude-code-mastery` repository.
5. Click **Add secret**.

> If you skip this step, GitHub will ask for the secret when you create the Codespace,
> because the course declares it as a recommended secret. Either way works.

## Step 3: Create the Codespace

1. On *your* repository page, click **Code → Codespaces → Create codespace on main**.
2. Wait 2–4 minutes for the first build. It installs Python 3.12, `uv`, the GitHub CLI and
   **Claude Code**, then runs `.devcontainer/post-create.sh`.
3. When the terminal shows **"All set!"**, you're ready.

## Step 4: Check everything works (free)

In the Codespace terminal:

```bash
uv run labcheck doctor
```

Every line should show a green ✔. If one doesn't, see [troubleshooting.md](troubleshooting.md).

## Step 5: Start Claude Code for the first time

Always launch Claude Code from the **repo root**:

```bash
claude
```

On the first run:
1. Pick a theme.
2. Claude Code detects `ANTHROPIC_API_KEY` and asks whether to use it. Choose **Yes**.
   (Don't log in with a personal Claude subscription for this course. Course work should
   be billed to the course key so your admin can see usage.)
3. Trust the folder when asked.
4. Look at the bottom of the screen. You should see the course **status line**, something like:
   `[Sonnet] | session $0.00 | month ~$0.00/$30 | ctx 2%`

Type `/exit` (or press `Ctrl+D` twice) to quit for now.

## Step 6: Good Codespace habits

- **Stop your Codespace when you're done for the day**: Codespaces menu → *Stop current codespace*.
  It also stops automatically when idle. Your files are kept.
- **Don't delete it** until the course is over. Your work and your cost ledger live in it.
  (Your *commits* live on GitHub, so push regularly: `git push`.)
- A 2-core machine is plenty.

---

## And that's it!

Open [`1_foundations/1_lab1_first_session.md`](../1_foundations/1_lab1_first_session.md) and let's begin.
