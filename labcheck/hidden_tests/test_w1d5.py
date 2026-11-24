"""TF-103: status and priority filters."""


def _titles(resp):
    assert resp.status_code == 200, resp.text
    return sorted(t["title"] for t in resp.json())


def test_filter_by_status(client, make_task):
    make_task("a")
    make_task("b", status="done")
    make_task("c", status="in_progress")
    assert _titles(client.get("/tasks", params={"status": "done"})) == ["b"]
    assert _titles(client.get("/tasks", params={"status": "in_progress"})) == ["c"]


def test_filter_by_priority(client, make_task):
    make_task("a", priority="high")
    make_task("b", priority="low")
    assert _titles(client.get("/tasks", params={"priority": "high"})) == ["a"]


def test_filters_combine(client, make_task):
    make_task("a", priority="high", status="done")
    make_task("b", priority="high")
    make_task("c", priority="low", status="done")
    resp = client.get("/tasks", params={"priority": "high", "status": "done"})
    assert _titles(resp) == ["a"]


def test_filters_combine_with_project_and_paging(client, make_task):
    other = client.post("/projects", json={"name": "Other"}).json()
    for i in range(3):
        make_task(f"h{i}", priority="high")
    client.post("/tasks", json={"project_id": other["id"], "title": "x", "priority": "high"})
    resp = client.get(
        "/tasks", params={"priority": "high", "project_id": other["id"]}
    )
    assert _titles(resp) == ["x"]
    page = client.get("/tasks", params={"priority": "high", "limit": 2, "offset": 1})
    assert [t["title"] for t in page.json()] == ["h1", "h2"]


def test_invalid_filter_values_rejected(client):
    assert client.get("/tasks", params={"status": "finished"}).status_code == 422
    assert client.get("/tasks", params={"priority": "urgent"}).status_code == 422
