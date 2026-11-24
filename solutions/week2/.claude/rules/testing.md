---
paths:
  - "practice-app/tests/**"
---
# Testing rules

- Freeze time with `monkeypatch.setattr(clock, "today", lambda: date(...))` (and `clock.now` if needed).
  Real dates make tests flaky on the day they cross a boundary.
- Use the `client` and `project` fixtures from `conftest.py` instead of building apps by hand.
- Name tests `test_<behaviour>`, for example `test_due_today_is_not_overdue`.
- Test through the HTTP API unless the unit under test is a pure function in `services.py`.
