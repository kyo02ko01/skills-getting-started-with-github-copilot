from uuid import uuid4


def test_signup_for_activity_registers_email(client):
    activity_name = "Chess Club"
    email = f"signup-{uuid4().hex[:8]}@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_duplicate_signup_for_activity_returns_400(client):
    activity_name = "Programming Class"
    email = f"duplicate-{uuid4().hex[:8]}@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown%20Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_without_email_returns_422(client):
    response = client.post("/activities/Chess%20Club/signup")

    assert response.status_code == 422