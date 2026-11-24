from datetime import date

from taskforge.services import is_overdue

TODAY = date(2026, 3, 10)


def test_no_due_date_is_never_overdue():
    assert is_overdue(None, "todo", today=TODAY) is False


def test_past_due_date_is_overdue():
    assert is_overdue(date(2026, 3, 1), "todo", today=TODAY) is True


def test_future_due_date_is_not_overdue():
    assert is_overdue(date(2026, 4, 1), "todo", today=TODAY) is False


# TF-101 regression tests
def test_due_today_is_not_overdue():
    assert is_overdue(TODAY, "todo", today=TODAY) is False


def test_done_task_is_never_overdue():
    assert is_overdue(date(2026, 3, 1), "done", today=TODAY) is False


def test_in_progress_past_due_is_overdue():
    assert is_overdue(date(2026, 3, 9), "in_progress", today=TODAY) is True


def test_uses_clock_when_today_not_given(monkeypatch):
    from taskforge import clock

    monkeypatch.setattr(clock, "today", lambda: TODAY)
    assert is_overdue(date(2026, 3, 9), "todo") is True
