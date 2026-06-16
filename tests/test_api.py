from copy import deepcopy
from src import app as app_module

def test_get_activities(client):
    # Arrange
    expected = deepcopy(app_module.activities)
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    assert resp.json() == expected


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    assert email not in app_module.activities[activity]["participants"]
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert resp.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in app_module.activities[activity]["participants"]


def test_signup_already_registered(client):
    # Arrange
    activity = "Chess Club"
    existing = app_module.activities[activity]["participants"][0]
    assert existing in app_module.activities[activity]["participants"]
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": existing})
    # Assert
    assert resp.status_code == 400
    assert resp.json().get("detail") == "Student already signed up"


def test_remove_participant_success(client):
    # Arrange
    activity = "Basketball Team"
    email = "alex@mergington.edu"
    assert email in app_module.activities[activity]["participants"]
    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert resp.json() == {"message": f"Removed {email} from {activity}"}
    assert email not in app_module.activities[activity]["participants"]


def test_remove_participant_not_found(client):
    # Arrange
    activity = "Basketball Team"
    missing = "noone@mergington.edu"
    assert missing not in app_module.activities[activity]["participants"]
    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": missing})
    # Assert
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Participant not found"
