# TaskForge course repo

Learning repo for Claude Code. The code you change lives in `practice-app/` (TaskForge).
See @practice-app/README.md for the layout; the backlog with acceptance criteria is practice-app/ISSUES.md.

## Commands
- Tests: `uv run pytest -q` (run from the repo root)
- Lint: `uv run ruff check practice-app` · format: `uv run ruff format practice-app`
- Run the API: `uv run uvicorn taskforge.main:app --reload`
- Lab checks (free, offline): `uv run labcheck wNdM`

## Architecture and conventions
- SQL only in `repository.py`; business rules in `services.py`; HTTP concerns in `api/`.
- Get time from `taskforge.clock` (`clock.today()` / `clock.now()`), never `date.today()`, so tests can freeze it.
- Validation lives in Pydantic models (`models.py`) and is shared by POST and PATCH.
- The dev database is disposable; after a schema change, delete `practice-app/taskforge.db`.

## Definition of done
- A failing test was written first; existing tests were not edited to make them pass.
- `uv run pytest -q` and `uv run ruff check practice-app` pass.
- Commit messages follow Conventional Commits and mention the TF issue id.

## Course rules
- Never edit files under `labcheck/`, `solutions/` or `checkpoints/`.
- Keep this file under 60 lines; put file-specific rules in `.claude/rules/`.
