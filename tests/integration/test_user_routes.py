# tests/integration/test_user_routes.py

import uuid
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _unique_user_payload(password: str = "supersecretpassword"):
    """
    Generate a unique user payload each time so tests don't clash
    with existing users in the test database.
    """
    suffix = uuid.uuid4().hex[:8]
    return {
        "username": f"routes_user_{suffix}",
        "email": f"routes_user_{suffix}@example.com",
        "password": password,
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


def test_update_profile_and_read_back():
    # Register a user with unique data
    user_payload = _unique_user_payload(password="secret123")
    resp = client.post("/users/register", json=user_payload)
    assert resp.status_code == 201, resp.json()
    user = resp.json()
    user_id = user["id"]

    # Prepare new unique username/email based on original
    new_username = user_payload["username"] + "_new"
    local_part, domain = user_payload["email"].split("@", 1)
    new_email = f"{local_part}_new@{domain}"

    # Update username + email
    update_resp = client.put(
        f"/users/{user_id}",
        json={"username": new_username, "email": new_email},
    )
    assert update_resp.status_code == 200, update_resp.json()
    updated = update_resp.json()
    assert updated["username"] == new_username
    assert updated["email"] == new_email

    # Read back
    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["username"] == new_username
    assert fetched["email"] == new_email


def test_change_password_and_relogin():
    # Register user with unique payload and known old password
    user_payload = _unique_user_payload(password="oldpass")
    resp = client.post("/users/register", json=user_payload)
    assert resp.status_code == 201, resp.json()
    user = resp.json()
    user_id = user["id"]

    username = user_payload["username"]
    email = user_payload["email"]

    # Change password
    change_resp = client.post(
        f"/users/{user_id}/change-password",
        json={"old_password": "oldpass", "new_password": "newpass"},
    )
    assert change_resp.status_code == 200, change_resp.json()

    # Old password should no longer work
    old_login = client.post(
        "/users/login",
        json={
            "username": username,
            "email": email,
            "password": "oldpass",
        },
    )
    # now we expect proper 401 instead of 422
    assert old_login.status_code == 401

    # New password should work
    new_login = client.post(
        "/users/login",
        json={
            "username": username,
            "email": email,
            "password": "newpass",
        },
    )
    assert new_login.status_code == 200, new_login.json()
