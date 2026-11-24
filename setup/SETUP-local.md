# Optional: running the course locally (Mac / Linux / WSL)

Codespaces is the supported path, and labs are written for it. If you must run locally:

1. Install **Python 3.12+**, **git**, the **GitHub CLI** (`gh`), and **uv**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Install **Claude Code** by following the current instructions at
   https://code.claude.com/docs (Getting started).
3. Clone the course repository (you need write access; see Step 1 of [SETUP-codespaces.md](SETUP-codespaces.md)),
   then run:
   ```bash
   cd <course-repo>
   bash .devcontainer/post-create.sh
   ```
   You'll create and push your `firstname-lastname` branch in Day 1, exactly as in Codespaces.
4. Export your course key **in your shell profile, not in a file inside the repo**:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```
5. Run `uv run labcheck doctor`.

Differences from Codespaces:
- Your machine is not a sandbox. Be extra careful with permission modes (Week 1, Day 2)
  and never use `bypassPermissions` outside a container.
- If you already use Claude Code with a personal subscription, make sure course sessions use
  the course key (run `/status` inside Claude Code to see which account is active).
