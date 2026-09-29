from uuid import uuid4


def test_unregister_participant_removes_email(client):
    activity_name = "Chess Club"
    email = f"unregister-{uuid4().hex[:8]}@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"削除しました: {email} ({activity_name})"
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_participant_accepts_email_in_request_body(client):
    activity_name = "Programming Class"
    email = f"body-{uuid4().hex[:8]}@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.request(
        "DELETE",
        f"/activities/{activity_name}/unregister",
        json={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"削除しました: {email} ({activity_name})"
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_without_email_returns_400(client):
    response = client.delete("/activities/Chess%20Club/unregister")

    assert response.status_code == 400
    assert response.json()["detail"] == "Email is required"


def test_unregister_from_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown%20Club/unregister?email=student@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/unregister?email=missing@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"