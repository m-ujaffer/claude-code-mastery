# TaskForge: the practice app

TaskForge is a small task-tracking REST API: **projects** hold **tasks**. It has
just enough real-world mess to practise on: a couple of bugs, missing
validation, thin test coverage, and a legacy module nobody wants to touch.

You will improve it with Claude Code throughout the course. The app is kept
**deliberately small** (about 600 lines). Small codebases mean small contexts,
and small contexts mean your US$30/month budget goes a long way.

## Run it

Run everything from the **repo root**:

```bash
uv run pytest                                  # run the test suite
uv run python -m taskforge.seed                # load demo data
uv run uvicorn taskforge.main:app --reload     # start the API on port 8000
```

In Codespaces, open the **Ports** tab and click the globe icon next to port 8000,
then add `/docs` to the URL to get the interactive Swagger UI.

## Layout

```
src/taskforge/
  main.py          app factory: create_app(db_path)
  models.py        Pydantic request/response models (Status, Priority, Task, ...)
  repository.py    all SQL lives here
  services.py      business rules (e.g. is_overdue) and row -> model conversion
  clock.py         clock.today() / clock.now(): always use these, never date.today()
  db.py            SQLite schema and connection
  api/             FastAPI routers: projects.py, tasks.py
  legacy/          report_builder.py: old, ugly, load-bearing
  seed.py          demo data
tests/             pytest suite (TestClient + a temporary SQLite file per test)
```

## Conventions

- Keep SQL in `repository.py`, rules in `services.py`, and HTTP concerns in `api/`.
- Get time from `taskforge.clock` so tests can freeze it.
- Every behaviour change comes with a test.
- The database is disposable: after a schema change, run `rm practice-app/taskforge.db`.

## Backlog

The work you will do in the labs is tracked in [ISSUES.md](ISSUES.md).
