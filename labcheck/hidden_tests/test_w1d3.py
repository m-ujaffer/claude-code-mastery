"""TF-101: overdue rules."""

from conftest import days


def test_due_today_is_not_overdue(make_task):
    assert make_task(due_date=days(0))["is_overdue"] is False


def test_due_yesterday_is_overdue(make_task):
    assert make_task(due_date=days(-1))["is_overdue"] is True


def test_done_task_is_never_overdue(make_task):
    assert make_task(due_date=days(-5), status="done")["is_overdue"] is False


def test_in_progress_past_due_is_overdue(make_task):
    assert make_task(due_date=days(-5), status="in_progress")["is_overdue"] is True


def test_no_due_date_is_not_overdue(make_task):
    assert make_task()["is_overdue"] is False


def test_future_is_not_overdue(make_task):
    assert make_task(due_date=days(1))["is_overdue"] is False
