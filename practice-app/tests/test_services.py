from datetime import date

from taskforge.services import is_overdue

TODAY = date(2026, 3, 10)


def test_no_due_date_is_never_overdue():
    assert is_overdue(None, "todo", today=TODAY) is False


def test_past_due_date_is_overdue():
    assert is_overdue(date(2026, 3, 1), "todo", today=TODAY) is True


def test_future_due_date_is_not_overdue():
    assert is_overdue(date(2026, 4, 1), "todo", today=TODAY) is False
