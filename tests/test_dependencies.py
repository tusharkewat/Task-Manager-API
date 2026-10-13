
from uuid import uuid4


def create_user_token(client):
    email = f"{uuid4().hex}@example.com"
    password = "TestPassword123"

    register_response = client.post(
        "/auth/register",
        json={
            "name": "Dependency Test User",
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

    return login_response.json()["access_token"]


def test_token_with_invalid_user_id_is_rejected(client):
    import jwt
    from app.config.settings import settings

    token = jwt.encode(
        {"sub": "not-an-object-id"},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


def test_token_for_nonexistent_user_is_rejected(client):
    import jwt
    from app.config.settings import settings

    token = jwt.encode(
        {"sub": "000000000000000000000001"},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
