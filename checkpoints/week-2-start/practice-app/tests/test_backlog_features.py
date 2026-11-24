"""Tests for the backlog features TF-102 and TF-103."""

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

