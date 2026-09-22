from copy import deepcopy
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

import src.app as app_module

client = TestClient(app_module.app)
ORIGINAL_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(deepcopy(ORIGINAL_ACTIVITIES))


def unique_email(prefix: str = "student") -> str:
    return f"{prefix}-{uuid4().hex[:8]}@mergington.edu"


def test_get_activities_returns_activity_list():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_registers_email():
    activity_name = "Chess Club"
    email = unique_email("signup")

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_duplicate_signup_for_activity_returns_400():
    activity_name = "Programming Class"
    email = unique_email("duplicate")

    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = unique_email("unregister")

    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"削除しました: {email} ({activity_name})"
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    response = client.delete(f"/activities/Chess Club/unregister?email={unique_email('missing')}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_unregister_participant_accepts_email_in_request_body():
    activity_name = "Programming Class"
    email = unique_email("body")

    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.request(
        "DELETE",
        f"/activities/{activity_name}/unregister",
        json={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"削除しました: {email} ({activity_name})"
    assert email not in client.get("/activities").json()[activity_name]["participants"]
