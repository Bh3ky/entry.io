"""Authentication and health endpoint tests."""

from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient) -> None:
    """Smoke test for health endpoint."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_login_and_me_flow(client: TestClient, require_db_driver) -> None:
    """Register then login, then access authenticated profile."""

    register_payload = {
        "email": "member@example.com",
        "password": "Password123!",
        "full_name": "Member One",
    }
    register_response = client.post("/api/v1/auth/register", json=register_payload)
    assert register_response.status_code == 201
    assert register_response.json()["email"] == register_payload["email"]

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": register_payload["email"], "password": register_payload["password"]},
    )
    assert login_response.status_code == 200

    tokens = login_response.json()
    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == register_payload["email"]


def test_login_rejects_invalid_credentials(client: TestClient, require_db_driver) -> None:
    """Login must fail with wrong credentials."""

    response = client.post(
        "/api/v1/auth/login",
        data={"username": "unknown@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
