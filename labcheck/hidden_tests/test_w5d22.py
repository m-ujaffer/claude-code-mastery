"""TF-107 (CSV export) and TF-108 (search)."""

import csv
import io


def test_csv_export(client, project, make_task):
    make_task("Write, docs", priority="high", due_date="2026-04-01")
    make_task("Ship")
    resp = client.get("/tasks/export.csv")
    assert resp.status_code == 200, resp.text
    assert resp.headers["content-type"].startswith("text/csv")
    rows = list(csv.reader(io.StringIO(resp.text)))
    assert rows[0] == ["id", "project_id", "title", "status", "priority", "due_date"]
    assert rows[1][2] == "Write, docs"
    assert rows[1][5] == "2026-04-01"
    assert len(rows) == 3


def test_csv_export_project_filter(client, project, make_task):
    other = client.post("/projects", json={"name": "Other"}).json()
    make_task("mine")
    client.post("/tasks", json={"project_id": other["id"], "title": "theirs"})
    resp = client.get("/tasks/export.csv", params={"project_id": other["id"]})
    rows = list(csv.reader(io.StringIO(resp.text)))
    assert [r[2] for r in rows[1:]] == ["theirs"]


def test_search_title_and_description(client, make_task):
    make_task("Buy MILK")
    make_task("Groceries", description="eggs and milk")
    make_task("Unrelated")
    resp = client.get("/tasks", params={"q": "milk"})
    assert sorted(t["title"] for t in resp.json()) == ["Buy MILK", "Groceries"]


def test_search_combines_with_filters(client, make_task):
    make_task("milk run", priority="high")
    make_task("milk later", priority="low")
    resp = client.get("/tasks", params={"q": "milk", "priority": "high"})
    assert [t["title"] for t in resp.json()] == ["milk run"]
