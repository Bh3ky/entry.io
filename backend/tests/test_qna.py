"""Q&A endpoint tests."""

from fastapi.testclient import TestClient

from app.models.user import UserRole


def test_create_question_and_reply(client: TestClient, require_db_driver, create_user) -> None:
    """Members can create questions and replies."""

    member_headers = create_user("member4@example.com", role=UserRole.MEMBER)

    question_response = client.post(
        "/api/v1/qna/questions",
        json={
            "title": "What is async in Python?",
            "body": "Can someone explain async and await?",
            "tags": ["python", "asyncio"],
        },
        headers=member_headers,
    )
    assert question_response.status_code == 201
    question_id = question_response.json()["id"]

    reply_response = client.post(
        f"/api/v1/qna/questions/{question_id}/replies",
        json={"body": "Async lets code wait on I/O without blocking."},
        headers=member_headers,
    )
    assert reply_response.status_code == 201

    list_response = client.get("/api/v1/qna/questions", headers=member_headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
