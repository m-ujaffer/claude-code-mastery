"""Tests for the backlog features TF-102 to TF-108."""

import datetime as dt

import pytest

from taskforge import clock

NOW = dt.datetime(2026, 3, 10, 9, 0, tzinfo=dt.UTC)


@pytest.fixture(autouse=True)
def frozen(monkeypatch):
    monkeypatch.setattr(clock, "today", lambda: NOW.date())
    monkeypatch.setattr(clock, "now", lambda: NOW)


def new(client, project, **fields):
    resp = client.post("/tasks", json={"project_id": project["id"], "title": "T", **fields})
    assert resp.status_code == 201, resp.text
    return resp.json()


# TF-102 -------------------------------------------------------------------
@pytest.mark.parametrize("title", ["", "   ", "x" * 201])
def test_invalid_titles_rejected(client, project, title):
    resp = client.post("/tasks", json={"project_id": project["id"], "title": title})
    assert resp.status_code == 422


def test_title_trimmed_and_patch_validated(client, project):
    task = new(client, project, title="  Buy milk  ")
    assert task["title"] == "Buy milk"
    assert client.patch(f"/tasks/{task['id']}", json={"title": " "}).status_code == 422


# TF-103 -------------------------------------------------------------------
def test_status_and_priority_filters(client, project):
    a = new(client, project, title="a", priority="high")
    new(client, project, title="b", priority="low")
    client.patch(f"/tasks/{a['id']}", json={"status": "done"})
    resp = client.get("/tasks", params={"status": "done", "priority": "high"})
    assert [t["title"] for t in resp.json()] == ["a"]
    assert client.get("/tasks", params={"status": "nope"}).status_code == 422


# TF-104 -------------------------------------------------------------------
def test_tags_lifecycle(client, project):
    task = new(client, project, tags=["B", " a ", "b", ""])
    assert task["tags"] == ["a", "b"]
    assert client.patch(f"/tasks/{task['id']}", json={"tags": ["Z"]}).json()["tags"] == ["z"]
    assert [t["id"] for t in client.get("/tasks", params={"tag": "z"}).json()] == [task["id"]]
    too_many = [str(i) for i in range(11)]
    resp = client.post("/tasks", json={"project_id": project["id"], "title": "x", "tags": too_many})
    assert resp.status_code == 422


# TF-105 -------------------------------------------------------------------
def test_completed_at_follows_status(client, project):
    task = new(client, project)
    done = client.patch(f"/tasks/{task['id']}", json={"status": "done"}).json()
    assert done["completed_at"].startswith("2026-03-10T09:00:00")
    reopened = client.patch(f"/tasks/{task['id']}", json={"status": "todo"}).json()
    assert reopened["completed_at"] is None


# TF-106 -------------------------------------------------------------------
def test_stats(client, project):
    new(client, project, due_date="2026-03-01")
    done = new(client, project)
    client.patch(f"/tasks/{done['id']}", json={"status": "done"})
    body = client.get(f"/projects/{project['id']}/stats").json()
    assert body == {
        "project_id": project["id"],
        "total": 2,
        "by_status": {"todo": 1, "in_progress": 0, "done": 1},
        "overdue": 1,
        "completion_rate": 0.5,
    }
    assert client.get("/projects/999/stats").status_code == 404


def test_stats_empty_project(client, project):
    assert client.get(f"/projects/{project['id']}/stats").json()["completion_rate"] == 0.0


# TF-107 / TF-108 ------------------------------------------------------------
def test_csv_export(client, project):
    new(client, project, title="Hello, world")
    resp = client.get("/tasks/export.csv")
    assert resp.headers["content-type"].startswith("text/csv")
    assert resp.text.splitlines()[0] == "id,project_id,title,status,priority,due_date"
    assert '"Hello, world"' in resp.text


def test_search(client, project):
    new(client, project, title="Buy MILK")
    new(client, project, title="Other", description="milk too")
    new(client, project, title="Nope")
    assert len(client.get("/tasks", params={"q": "milk"}).json()) == 2
