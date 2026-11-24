---
name: taskforge-conventions
description: TaskForge layering, validation and time conventions. Use when writing or reviewing code under practice-app/.
---
# TaskForge conventions

- **Layering:** SQL only in `repository.py`; business rules in `services.py`; HTTP mapping in `api/`.
  The repository raises `NotFoundError` / `ConflictError`; the API maps them to 404 / 409.
- **Validation:** in Pydantic models, shared by create and update (see `clean_title`, `clean_tags`).
- **Time:** `from taskforge import clock`, then `clock.today()` / `clock.now()`. Never `date.today()`.
- **Responses:** convert rows with `services.to_task(conn, row)` so computed fields stay consistent.
- **Routes:** declare static paths (`/tasks/export.csv`) before parameterised ones (`/tasks/{task_id}`).
