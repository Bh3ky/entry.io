"""Enrollment endpoint tests."""

from fastapi.testclient import TestClient

from app.models.user import UserRole


def test_enroll_and_prevent_duplicate_enrollment(
    client: TestClient,
    require_db_driver,
    create_user,
) -> None:
    """Member can enroll once and duplicate enrollments are rejected."""

    lead_headers = create_user("lead2@example.com", role=UserRole.LEAD)
    member_headers = create_user("member3@example.com", role=UserRole.MEMBER)

    class_response = client.post(
        "/api/v1/classes",
        json={"title": "Data Structures", "description": "Core concepts", "is_published": True},
        headers=lead_headers,
    )
    class_id = class_response.json()["id"]

    first_enroll = client.post(
        "/api/v1/enrollment",
        json={"class_id": class_id},
        headers=member_headers,
    )
    assert first_enroll.status_code == 201

    duplicate_enroll = client.post(
        "/api/v1/enrollment",
        json={"class_id": class_id},
        headers=member_headers,
    )
    assert duplicate_enroll.status_code == 409
