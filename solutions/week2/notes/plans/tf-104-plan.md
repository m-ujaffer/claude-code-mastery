# Plan: TF-104 tags

## Approach
1. Schema: add the `task_tags(task_id, tag)` table with a composite PK, `ON DELETE CASCADE`, and an index on `tag`.
2. Models: `TaskCreate.tags: list[str] = []`, `TaskUpdate.tags: list[str] | None`, `Task.tags: list[str]`.
   Normalise in a shared validator (`clean_tags`): trim, lower-case, drop empties, de-duplicate, sort, max 10 (else 422).
   Why in the model: the HTTP and (later) MCP paths share one rule, and the repository stays dumb.
3. Repository: `_replace_tags(conn, task_id, tags)`, `get_tags(conn, task_id)`; `create_task` writes tags;
   `update_task` replaces tags only when `tags` is present; `list_tasks(tag=...)` filters with a subquery.
4. Services: `to_task(conn, row)` loads tags (N+1 queries are acceptable at this scale; revisit if lists get big).
5. API: `GET /tasks?tag=`; route signatures otherwise unchanged.

## Tests first
normalisation · default [] · 10 ok / 11 rejected · PATCH replaces · PATCH without tags keeps them ·
tag filter is case-insensitive · tags removed when a task is deleted.

## Migration
Dev DB is disposable: `rm practice-app/taskforge.db`. A real system would need a migration.

## Files
db.py, models.py, repository.py, services.py, api/tasks.py, api/projects.py, tests/.
