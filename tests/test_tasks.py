
from uuid import uuid4


def create_authenticated_user(client):
    """Register a unique user and return their access token."""
    email = f"{uuid4().hex}@example.com"
    password = "TestPassword123"

    register_response = client.post(
        "/auth/register",
        json={
            "name": "Task Test User",
            "email": email,
            "password": password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_task(client, headers, title="Test Task"):
    """Create a task and return its response."""
    return client.post(
        "/tasks/",
        headers=headers,
        json={
            "title": title,
            "description": "Created during automated testing",
            "priority": "high",
        },
    )


def test_create_task(client):
    headers = create_authenticated_user(client)

    response = create_task(client, headers, "Learn FastAPI")

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Created during automated testing"
    assert data["priority"] == "high"
    assert "id" in data or "task_id" in data


def test_list_tasks(client):
    headers = create_authenticated_user(client)
    create_task(client, headers, "Task One")
    create_task(client, headers, "Task Two")

    response = client.get("/tasks/", headers=headers)

    assert response.status_code == 200
    titles = [task["title"] for task in response.json()]
    assert "Task One" in titles
    assert "Task Two" in titles


def test_get_task_by_id(client):
    headers = create_authenticated_user(client)
    created = create_task(client, headers, "Find This Task")
    assert created.status_code == 201

    task = created.json()
    task_id = task.get("id", task.get("task_id"))

    response = client.get(f"/tasks/{task_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == "Find This Task"


def test_update_task(client):
    headers = create_authenticated_user(client)
    created = create_task(client, headers, "Original Title")
    assert created.status_code == 201

    task = created.json()
    task_id = task.get("id", task.get("task_id"))

    response = client.patch(
        f"/tasks/{task_id}",
        headers=headers,
        json={"title": "Updated Title", "status": "completed"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["status"] == "completed"


def test_delete_task(client):
    headers = create_authenticated_user(client)
    created = create_task(client, headers, "Task to Delete")
    assert created.status_code == 201

    task = created.json()
    task_id = task.get("id", task.get("task_id"))

    delete_response = client.delete(
        f"/tasks/{task_id}", headers=headers
    )
    assert delete_response.status_code == 204

    get_response = client.get(
        f"/tasks/{task_id}", headers=headers
    )
    assert get_response.status_code == 404


def test_user_cannot_access_another_users_task(client):
    owner_headers = create_authenticated_user(client)
    other_headers = create_authenticated_user(client)

    created = create_task(client, owner_headers, "Private Task")
    assert created.status_code == 201

    task = created.json()
    task_id = task.get("id", task.get("task_id"))

    response = client.get(
        f"/tasks/{task_id}", headers=other_headers
    )

    assert response.status_code == 404


def test_invalid_task_id_returns_error(client):
    headers = create_authenticated_user(client)

    response = client.get(
        "/tasks/not-a-valid-object-id", headers=headers
    )

    assert response.status_code in (400, 422)


def test_create_task_without_authentication(client):
    response = client.post(
        "/tasks/",
        json={"title": "Unauthorized Task"},
    )

    assert response.status_code == 401



def test_filter_tasks_by_status(client):
    headers = create_authenticated_user(client)

    first = create_task(client, headers, "Pending Task")
    second = create_task(client, headers, "Completed Task")

    assert first.status_code == 201
    assert second.status_code == 201

    task_id = second.json()["id"]
    update_response = client.patch(
        f"/tasks/{task_id}",
        headers=headers,
        json={"status": "completed"},
    )
    assert update_response.status_code == 200

    response = client.get(
        "/tasks/?status=completed",
        headers=headers,
    )

    assert response.status_code == 200
    assert all(task["status"] == "completed" for task in response.json())
    assert any(task["title"] == "Completed Task" for task in response.json())


def test_filter_tasks_by_priority(client):
    headers = create_authenticated_user(client)

    low_response = client.post(
        "/tasks/",
        headers=headers,
        json={"title": "Low Priority Task", "priority": "low"},
    )
    high_response = client.post(
        "/tasks/",
        headers=headers,
        json={"title": "High Priority Task", "priority": "high"},
    )

    assert low_response.status_code == 201
    assert high_response.status_code == 201

    response = client.get(
        "/tasks/?priority=high",
        headers=headers,
    )

    assert response.status_code == 200
    assert all(task["priority"] == "high" for task in response.json())
    assert any(task["title"] == "High Priority Task" for task in response.json())


def test_update_task_with_empty_body_returns_400(client):
    headers = create_authenticated_user(client)
    created = create_task(client, headers, "Keep This Task")
    task_id = created.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        headers=headers,
        json={},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "No fields provided for update"


def test_update_task_with_invalid_id_returns_400(client):
    headers = create_authenticated_user(client)

    response = client.patch(
        "/tasks/not-a-valid-object-id",
        headers=headers,
        json={"title": "Updated"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid task ID"


def test_delete_task_with_invalid_id_returns_400(client):
    headers = create_authenticated_user(client)

    response = client.delete(
        "/tasks/not-a-valid-object-id",
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid task ID"


def test_get_nonexistent_task_returns_404(client):
    headers = create_authenticated_user(client)
    nonexistent_id = "000000000000000000000001"

    response = client.get(
        f"/tasks/{nonexistent_id}",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_nonexistent_task_returns_404(client):
    headers = create_authenticated_user(client)
    nonexistent_id = "000000000000000000000001"

    response = client.patch(
        f"/tasks/{nonexistent_id}",
        headers=headers,
        json={"title": "Updated"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"



def test_delete_nonexistent_task_returns_404(client):
    headers = create_authenticated_user(client)
    nonexistent_id = "000000000000000000000001"

    response = client.delete(
        f"/tasks/{nonexistent_id}",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"



def test_user_cannot_update_another_users_task(client):
    owner_headers = create_authenticated_user(client)
    other_headers = create_authenticated_user(client)

    created = create_task(client, owner_headers, "Owner Task")
    task_id = created.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        headers=other_headers,
        json={"title": "Unauthorized Change"},
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_task(client):
    owner_headers = create_authenticated_user(client)
    other_headers = create_authenticated_user(client)

    created = create_task(client, owner_headers, "Owner Task")
    task_id = created.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers=other_headers,
    )

    assert response.status_code == 404

    owner_response = client.get(
        f"/tasks/{task_id}",
        headers=owner_headers,
    )
    assert owner_response.status_code == 200
