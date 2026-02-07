"""Class management endpoint tests."""

from fastapi.testclient import TestClient

from app.models.user import UserRole


def test_lead_can_create_and_member_can_list_classes(
    client: TestClient,
    require_db_driver,
    create_user,
) -> None:
    """Lead creates class, member can list it."""

    lead_headers = create_user("lead@example.com", role=UserRole.LEAD)
    member_headers = create_user("member@example.com", role=UserRole.MEMBER)

    create_response = client.post(
        "/api/v1/classes",
        json={
            "title": "Intro to Python",
            "description": "Beginner friendly class",
            "is_published": True,
        },
        headers=lead_headers,
    )
    assert create_response.status_code == 201

    list_response = client.get("/api/v1/classes", headers=member_headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["title"] == "Intro to Python"


def test_member_cannot_create_class(client: TestClient, require_db_driver, create_user) -> None:
    """Members should be blocked by RBAC from creating classes."""

    member_headers = create_user("member2@example.com", role=UserRole.MEMBER)

    response = client.post(
        "/api/v1/classes",
        json={"title": "Blocked", "description": "No access", "is_published": True},
        headers=member_headers,
    )

    assert response.status_code == 403
