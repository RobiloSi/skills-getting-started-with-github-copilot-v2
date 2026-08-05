import copy

from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def setup_function():
    setup_function.original_activities = copy.deepcopy(activities)


def teardown_function():
    activities.clear()
    activities.update(copy.deepcopy(setup_function.original_activities))


def test_get_activities_returns_activities():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert expected_activity in response.json()
    assert isinstance(response.json()[expected_activity]["participants"], list)


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    student_email = "teststudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {student_email} for {activity_name}"
    assert student_email in activities[activity_name]["participants"]


def test_signup_duplicate_returns_400():
    # Arrange
    activity_name = "Chess Club"
    student_email = "duplicate@mergington.edu"
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email},
    )

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_remove_participant_removes_student():
    # Arrange
    activity_name = "Programming Class"
    student_email = "newstudent@mergington.edu"
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email},
    )
    assert student_email in activities[activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": student_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {student_email} from {activity_name}"
    assert student_email not in activities[activity_name]["participants"]


def test_remove_unknown_participant_returns_404():
    # Arrange
    activity_name = "Gym Class"
    student_email = "missing@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": student_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found for this activity"
