# tests/e2e/test_profile_e2e.py

import uuid
import httpx

BASE_URL = "http://127.0.0.1:8000"


def test_profile_password_change_flow(page, browser_name):
    # 1) Create a unique user via API
    suffix = uuid.uuid4().hex[:8]
    username = f"profilee2euser_{suffix}"
    email = f"profilee2e_{suffix}@example.com"
    old_password = "oldpass"
    new_password = "newpass"

    with httpx.Client() as client:
        resp = client.post(
            f"{BASE_URL}/users/register",
            json={
                "username": username,
                "email": email,
                "password": old_password,
            },
        )
        assert resp.status_code == 201, resp.json()
        user = resp.json()
        user_id = user["id"]

    # 2) Open profile page and inject the current user id into localStorage
    page.goto(f"{BASE_URL}/profile-page")
    page.evaluate(f"window.localStorage.setItem('currentUserId', '{user_id}')")
    page.reload()
    page.wait_for_timeout(500)

    # 3) Change the password using the PROFILE UI
    page.fill("#old-password", old_password)
    page.fill("#new-password", new_password)
    page.click("#change-password-button")
    page.wait_for_timeout(500)

    # 4) Verify that old password no longer works and new one does via API
    with httpx.Client() as client:
        old_login = client.post(
            f"{BASE_URL}/users/login",
            json={
                "username": username,
                "email": email,
                "password": old_password,
            },
        )
        assert old_login.status_code == 401

        new_login = client.post(
            f"{BASE_URL}/users/login",
            json={
                "username": username,
                "email": email,
                "password": new_password,
            },
        )
        assert new_login.status_code == 200, new_login.json()
