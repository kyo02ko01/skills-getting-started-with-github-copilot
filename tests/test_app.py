from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "student@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"削除しました: {email} ({activity_name})"
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    response = client.delete("/activities/Chess Club/unregister?email=missing@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_unregister_participant_accepts_email_in_request_body():
    activity_name = "Programming Class"
    email = "newstudent@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")

    response = client.request(
        "DELETE",
        f"/activities/{activity_name}/unregister",
        json={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"削除しました: {email} ({activity_name})"
    assert email not in client.get("/activities").json()[activity_name]["participants"]
