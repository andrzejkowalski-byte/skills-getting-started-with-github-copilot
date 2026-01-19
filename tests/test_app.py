import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data
    assert "participants" in data["Basketball"]

def test_signup_for_activity_success():
    email = "testuser@mergington.edu"
    activity = "Basketball"
    # Remove if already present
    client.post(f"/activities/{activity}/unregister", json={"email": email})
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json().get("message", "")
    # Clean up
    client.post(f"/activities/{activity}/unregister", json={"email": email})

def test_signup_for_activity_duplicate():
    email = "testuser2@mergington.edu"
    activity = "Tennis"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")
    # Clean up
    client.post(f"/activities/{activity}/unregister", json={"email": email})

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")
