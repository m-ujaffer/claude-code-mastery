# TaskForge overview (example output from Week 1, Day 1)

TaskForge is a small FastAPI + SQLite REST API for tracking tasks inside projects.

## Layers
- **api/**: FastAPI routers (`projects.py`, `tasks.py`). HTTP only: parse the request, call the repository and services, map errors to status codes.
- **repository.py**: every SQL statement. Raises `NotFoundError` / `ConflictError`.
- **services.py**: business rules (`is_overdue`) and row → `Task` model conversion (`to_task`).
- **models.py**: Pydantic request/response models and the `Status` / `Priority` enums.
- **clock.py**: `today()` / `now()`. The single source of time, so tests can freeze it.
- **db.py**: schema and connection (`connect(path)`).
- **legacy/report_builder.py**: old report code with its own copy of the overdue logic.

## How POST /tasks flows
1. `api/tasks.create_task` validates the body as `TaskCreate`.
2. `repository.create_task` checks that the project exists, inserts the row, and returns it.
3. `services.to_task` converts the row into a `Task`, computing `is_overdue`.
4. FastAPI serialises the `Task` with status 201.

## Running tests
`uv run pytest` from the repo root.

## Suspicious
`is_overdue` uses `<=` and ignores status: a task due today, or one already done, shows as overdue.
