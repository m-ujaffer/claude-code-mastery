# Updating the course for a new cohort (maintainers)

Claude Code changes quickly: new slash commands, settings keys, hook events and flags.
Run through this checklist before each cohort, about 1–2 hours.

1. **Rebuild a Codespace from scratch** and run `uv run labcheck doctor`.
   - The devcontainer feature `ghcr.io/anthropics/devcontainer-features/claude-code:1.0`
     installs the **latest** Claude Code. The `:1.0` tag pins the feature script, not the CLI.
     If you need every learner on the same version for a cohort, pin it the way the current
     docs recommend (see code.claude.com/docs → Development containers) and note the version
     in the README.
2. **Re-verify the commands each lab uses** against https://code.claude.com/docs.
   The pages most likely to drift are the CLI reference, hooks, skills, plugins, statusline,
   settings, sub-agents, MCP, GitHub Actions and the Agent SDK.
3. **Run the solution check:**
   ```bash
   uv sync --all-groups      # the Week 4/6 checks need the MCP and Agent SDK packages
   uv run python scripts/build_checkpoints.py --verify
   ```
   This applies every overlay in `solutions/` to a temporary copy of the repo and runs all 30
   lab checks. All of them must pass.
4. **Rebuild the checkpoints** if you changed the practice app or any solution:
   ```bash
   git commit -am "..."   # build_checkpoints refuses to run on a dirty practice-app/
   uv run python scripts/build_checkpoints.py
   ```
5. **Lint the lab files** so every lab follows the template:
   ```bash
   uv run labcheck lint-labs
   ```
6. **Dry-run one lab per week** in a fresh Codespace and compare `/cost` with the lab's
   budget cap. Adjust caps in the lab header and in `WEEK_CAPS` (`labcheck/cli.py`).
7. **Refresh the exam guide.** Check the current CCA-F exam guide on Anthropic's site and update
   `guides/07_cca_f_exam_overview.md` and `assessments/mock_exam_cca_f.md` if domains or weights
   have changed.
8. **Pricing.** If model prices changed, update `guides/03_tokens_context_and_models.md`.
