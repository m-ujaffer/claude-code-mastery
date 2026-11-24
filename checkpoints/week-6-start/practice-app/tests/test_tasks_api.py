def test_create_task_defaults(client, project):
    resp = client.post("/tasks", json={"project_id": project["id"], "title": "Write docs"})
    assert resp.status_code == 201
    task = resp.json()
    assert task["status"] == "todo"
    assert task["priority"] == "medium"
    assert task["due_date"] is None
    assert task["is_overdue"] is False


def test_create_task_for_missing_project_is_404(client):
    resp = client.post("/tasks", json={"project_id": 42, "title": "Orphan"})
    assert resp.status_code == 404


def test_get_update_delete_task(client, project):
    task = client.post("/tasks", json={"project_id": project["id"], "title": "T"}).json()

    updated = client.patch(f"/tasks/{task['id']}", json={"status": "in_progress"}).json()
    assert updated["status"] == "in_progress"

    assert client.delete(f"/tasks/{task['id']}").status_code == 204
    assert client.get(f"/tasks/{task['id']}").status_code == 404


def test_list_tasks_pagination(client, project):
    for i in range(5):
        client.post("/tasks", json={"project_id": project["id"], "title": f"T{i}"})
    page = client.get("/tasks", params={"limit": 2, "offset": 2}).json()
    assert [t["title"] for t in page] == ["T2", "T3"]


def test_invalid_priority_rejected(client, project):
    resp = client.post(
        "/tasks", json={"project_id": project["id"], "title": "T", "priority": "urgent"}
    )
    assert resp.status_code == 422
