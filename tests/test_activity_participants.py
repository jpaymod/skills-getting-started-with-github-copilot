from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    original_participants = list(activities[activity_name]["participants"])
    try:
        if email not in activities[activity_name]["participants"]:
            activities[activity_name]["participants"].append(email)

        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email},
        )

        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_missing_participant_returns_404():
    activity_name = "Programming Class"
    email = "missingstudent@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    assert response.status_code == 404
