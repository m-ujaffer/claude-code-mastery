"""TF-105: completed_at."""

from conftest import NOW, parse_ts

from taskforge import clock


def test_new_task_has_null_completed_at(make_task):
    assert make_task()["completed_at"] is None


def test_done_sets_completed_at(make_task):
    task = make_task(status="done")
    assert parse_ts(task["completed_at"]) == NOW


def test_reopen_clears_completed_at(client, make_task):
    task = make_task(status="done")
    resp = client.patch(f"/tasks/{task['id']}", json={"status": "todo"})
    assert resp.json()["completed_at"] is None


def test_editing_done_task_keeps_completed_at(client, make_task, monkeypatch):
    import datetime as dt

    task = make_task(status="done")
    later = NOW + dt.timedelta(hours=5)
    monkeypatch.setattr(clock, "now", lambda: later)
    resp = client.patch(f"/tasks/{task['id']}", json={"title": "Renamed"})
    assert parse_ts(resp.json()["completed_at"]) == NOW
    resp = client.patch(f"/tasks/{task['id']}", json={"status": "done"})
    assert parse_ts(resp.json()["completed_at"]) == NOW
