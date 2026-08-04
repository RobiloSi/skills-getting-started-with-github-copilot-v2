from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def test_unregister_participant_removes_them_from_activity():
    activity_name = "Chess Club"
    email = "new-student@example.com"

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/signup?email={email}"
    )

    assert unregister_response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]
