# TaskForge backlog

Each issue below is picked up in a specific lab. The acceptance criteria are
exact: `labcheck` tests them, so read them carefully (and so should Claude).

---

## TF-101 · Bug · Tasks due today are shown as overdue  *(Week 1, Day 3)*

Customers report that a task due **today** shows `"is_overdue": true`. Tasks that are
already **done** also show as overdue when their date has passed.

**Acceptance criteria**
- A task is overdue only when `due_date` is **strictly before** today **and** its status is not `done`.
- A task with no due date is never overdue.
- A regression test covers each rule.

---

## TF-102 · Validation · Reject blank or very long task titles  *(Week 1, Day 4)*

**Acceptance criteria**
- Titles are trimmed of surrounding whitespace before they are saved (`"  Buy milk  "` is stored as `"Buy milk"`).
- An empty or whitespace-only title is rejected with **422**.
- A title longer than **200** characters (after trimming) is rejected with **422**. Exactly 200 characters is allowed.
- The rules apply to both `POST /tasks` and `PATCH /tasks/{id}`.

---

## TF-103 · Feature · Filter tasks by status and priority  *(Week 1, Day 5)*

**Acceptance criteria**
- `GET /tasks?status=done` returns only done tasks. `GET /tasks?priority=high` returns only high-priority tasks.
- Filters combine with each other and with `project_id`, `limit` and `offset`.
- Invalid values (for example `status=finished`) return **422**.

---

## TF-104 · Feature · Tags  *(Week 2, Day 8)*

**Acceptance criteria**
- `POST /tasks` accepts an optional `tags: list[str]`, and every task response includes `tags`.
- Tags are normalised before they are stored: trimmed, lower-cased, de-duplicated, and returned **sorted**. Empty tags are dropped.
- A task can have at most **10** tags; more returns **422**.
- `PATCH /tasks/{id}` with `tags` **replaces** the whole tag list.
- `GET /tasks?tag=urgent` returns only tasks with that tag (case-insensitive).
- Store tags in a separate `task_tags` table, not a comma-separated column.

---

## TF-105 · Feature · Record when a task was completed  *(Week 2, Day 9)*

**Acceptance criteria**
- Every task response has a `completed_at` field: a timestamp or `null`.
- Changing status **to** `done` sets `completed_at` to `clock.now()`.
- Changing status **away from** `done` sets it back to `null`.
- Updating a done task without changing its status does not change `completed_at`.

---

## TF-106 · Feature · Project statistics endpoint  *(Week 2, Day 10)*

`GET /projects/{id}/stats` returns:

```json
{
  "project_id": 1,
  "total": 4,
  "by_status": {"todo": 1, "in_progress": 1, "done": 2},
  "overdue": 1,
  "completion_rate": 0.5
}
```

**Acceptance criteria**
- All three statuses always appear in `by_status`, even when their count is 0.
- `completion_rate` is done / total, rounded to 2 decimals, and `0.0` when there are no tasks.
- `overdue` follows the TF-101 rules.
- A missing project returns **404**.
- The stats logic lives in `services.py`, and test coverage of `services.py` is at least **90%**.

---

## TF-107 · Feature · CSV export  *(Week 5, Day 22)*

**Acceptance criteria**
- `GET /tasks/export.csv` returns `text/csv` with the header row `id,project_id,title,status,priority,due_date`.
- An optional `project_id` filter is supported.
- Watch out: this route must not be swallowed by `GET /tasks/{task_id}`.

---

## TF-108 · Feature · Search  *(Week 5, Day 22)*

**Acceptance criteria**
- `GET /tasks?q=milk` returns tasks whose title **or** description contains `milk`, case-insensitively.
- `q` combines with every other filter.

---

## TF-109 · Tech debt · Refactor the legacy report builder  *(Week 5, Day 25)*

`legacy/report_builder.py` has the same counting logic copied three times.

**Acceptance criteria**
- The output of `build_report()` is **byte-for-byte identical** for `text`, `md` and `html`. Pin it with characterisation tests **before** you refactor.
- Characterisation tests live in `practice-app/tests/test_report_builder.py`.
- No function in `report_builder.py` is longer than **40 lines**.
- `build_report(conn, project_id, fmt)` keeps the same signature.
