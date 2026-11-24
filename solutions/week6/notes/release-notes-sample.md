# TaskForge release notes

## Features
- **Tags** (TF-104): tasks accept up to 10 tags; filter with `GET /tasks?tag=`.
- **Completion timestamps** (TF-105): tasks report `completed_at` when done.
- **Project statistics** (TF-106): `GET /projects/{id}/stats` returns counts, overdue tasks and the completion rate.
- **CSV export and search** (TF-107, TF-108): `GET /tasks/export.csv` and `GET /tasks?q=`.

## Fixes
- Tasks due today, and completed tasks, are no longer flagged overdue (TF-101).
- Blank or over-long task titles are rejected with 422 (TF-102).

## Internal
- The legacy report builder was refactored behind characterisation tests, with no output changes (TF-109).
