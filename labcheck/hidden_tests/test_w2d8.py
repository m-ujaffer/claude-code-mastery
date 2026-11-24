"""TF-104: tags."""

import sqlite3


def test_tags_normalised(make_task):
    task = make_task(tags=[" Urgent", "backend", "URGENT", "", "  "])
    assert task["tags"] == ["backend", "urgent"]


def test_tags_default_empty(make_task):
    assert make_task()["tags"] == []


def test_too_many_tags_rejected(client, project):
    tags = [f"t{i}" for i in range(11)]
    resp = client.post("/tasks", json={"project_id": project["id"], "title": "x", "tags": tags})
    assert resp.status_code == 422
    ten = [f"t{i}" for i in range(10)]
    resp = client.post("/tasks", json={"project_id": project["id"], "title": "y", "tags": ten})
    assert resp.status_code == 201


def test_patch_replaces_tags(client, make_task):
    task = make_task(tags=["a", "b"])
    resp = client.patch(f"/tasks/{task['id']}", json={"tags": ["C"]})
    assert resp.status_code == 200
    assert resp.json()["tags"] == ["c"]
    assert client.get(f"/tasks/{task['id']}").json()["tags"] == ["c"]


def test_patch_without_tags_keeps_them(client, make_task):
    task = make_task(tags=["keep"])
    resp = client.patch(f"/tasks/{task['id']}", json={"priority": "high"})
    assert resp.json()["tags"] == ["keep"]


def test_filter_by_tag(client, make_task):
    make_task("one", tags=["urgent"])
    make_task("two", tags=["later"])
    resp = client.get("/tasks", params={"tag": "URGENT"})
    assert [t["title"] for t in resp.json()] == ["one"]


def test_tags_stored_in_separate_table(app, make_task):
    make_task(tags=["x"])
    conn: sqlite3.Connection = app.state.db
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert "task_tags" in tables
