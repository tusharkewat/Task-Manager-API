
def test_register_rejects_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "not-an-email",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 422



def test_register_rejects_short_password(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "validuser@example.com",
            "password": "123",
        },
    )

    assert response.status_code == 422
    


def test_login_rejects_invalid_email(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "invalid-email",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 422


def test_get_current_user_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_list_tasks_without_token(client):
    response = client.get("/tasks/")

    assert response.status_code == 401


def test_login_rejects_missing_password(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "validuser@example.com",
        },
    )

    assert response.status_code == 422


def test_login_rejects_empty_password(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "validuser@example.com",
            "password": "",
        },
    )

    assert response.status_code == 422


def test_get_current_user_with_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid.token.value"},
    )

    assert response.status_code == 401


def test_get_current_user_with_malformed_authorization_header(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "NotBearer sometoken"},
    )

    assert response.status_code == 401
