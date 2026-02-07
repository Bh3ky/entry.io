"""RBAC enforcement tests."""

from fastapi.testclient import TestClient

from app.models.user import UserRole


def test_member_cannot_access_admin_user_list(
    client: TestClient,
    require_db_driver,
    create_user,
) -> None:
    """Only admin can access users list endpoint."""

    member_headers = create_user("member5@example.com", role=UserRole.MEMBER)

    response = client.get("/api/v1/users", headers=member_headers)

    assert response.status_code == 403


def test_member_cannot_moderate_qna_delete(
    client: TestClient,
    require_db_driver,
    create_user,
) -> None:
    """Only lead/admin can delete questions."""

    member_headers = create_user("member6@example.com", role=UserRole.MEMBER)

    question_response = client.post(
        "/api/v1/qna/questions",
        json={"title": "Need help", "body": "How do loops work?", "tags": ["python"]},
        headers=member_headers,
    )
    question_id = question_response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/qna/questions/{question_id}",
        headers=member_headers,
    )

    assert delete_response.status_code == 403
