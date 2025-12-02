# tests/integration/test_user_routes.py

import uuid
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _unique_user_payload():
    """
    Generate a unique user payload each time so tests don't clash
    with existing users in the test database.
    """
    suffix = uuid.uuid4().hex[:8]
    return {
        "username": f"routes_user_{suffix}",
        "email": f"routes_user_{suffix}@example.com",
        "password": "supersecretpassword",
    }


def test_register_user_and_login_round_trip():
    user_payload = _unique_user_payload()

    # 1) Register
    resp = client.post("/users/register", json=user_payload)
    # If this fails, show the body to help debug
    assert resp.status_code in (200, 201), resp.json()

    data = resp.json()
    assert data["username"] == user_payload["username"]
    assert data["email"] == user_payload["email"]
    assert "id" in data
    assert "created_at" in data

    # 2) Login with the same credentials
    login_resp = client.post("/users/login", json=user_payload)
    assert login_resp.status_code == 200, login_resp.json()

    login_data = login_resp.json()
    assert login_data["username"] == user_payload["username"]
    assert login_data["email"] == user_payload["email"]
    assert "id" in login_data
    assert "created_at" in login_data


def test_register_duplicate_user_fails():
    # First registration with a unique payload
    user_payload = _unique_user_payload()

    resp1 = client.post("/users/register", json=user_payload)
    assert resp1.status_code in (200, 201), resp1.json()

    # Second registration with the same username/email should fail
    resp2 = client.post("/users/register", json=user_payload)
    # depending on how you raised the error, this will usually be 400 or 409
    assert resp2.status_code in (400, 409), resp2.json()
