
from uuid import uuid4


def test_register_user(client):
    email = f"{uuid4().hex}@example.com"

    response = client.post(
        "/auth/register",
        json={
            "name": "Automated Test User",
            "email": email,
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email
    assert data["name"] == "Automated Test User"
    assert "user_id" in data


def test_duplicate_email_registration(client):
    email = f"{uuid4().hex}@example.com"
    payload = {
        "name": "Automated Test User",
        "email": email,
        "password": "TestPassword123!",
    }

    first = client.post("/auth/register", json=payload)
    second = client.post("/auth/register", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409


def test_successful_login(client):
    email = f"{uuid4().hex}@example.com"
    password = "TestPassword123!"

    registration = client.post(
        "/auth/register",
        json={
            "name": "Login Test User",
            "email": email,
            "password": password,
        },
    )
    assert registration.status_code == 201

    response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_login_wrong_password(client):
    email = f"{uuid4().hex}@example.com"

    registration = client.post(
        "/auth/register",
        json={
            "name": "Login Test User",
            "email": email,
            "password": "TestPassword123!",
        },
    )
    assert registration.status_code == 201

    response = client.post(
        "/auth/login",
        json={"email": email, "password": "WrongPassword123!"},
    )

    assert response.status_code == 401


def test_login_unknown_email(client):
    response = client.post(
        "/auth/login",
        json={
            "email": f"{uuid4().hex}@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 401


def test_current_user_with_valid_token(client):
    email = f"{uuid4().hex}@example.com"
    password = "TestPassword123!"

    registration = client.post(
        "/auth/register",
        json={
            "name": "Profile Test User",
            "email": email,
            "password": password,
        },
    )
    assert registration.status_code == 201

    login = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert login.status_code == 200

    token = login.json()["access_token"]
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["name"] == "Profile Test User"
