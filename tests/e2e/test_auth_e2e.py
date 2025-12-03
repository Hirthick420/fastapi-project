# tests/e2e/test_auth_e2e.py
import uuid
from playwright.sync_api import Page

BASE_URL = "http://127.0.0.1:8000"


def unique_email() -> str:
    return f"play_{uuid.uuid4().hex[:8]}@example.com"


def test_register_positive(page: Page):
    email = unique_email()
    username = "user_" + uuid.uuid4().hex[:5]
    password = "StrongPass123"

    page.goto(f"{BASE_URL}/register-page")

    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#password", password)

    page.click("text=Register")

    page.wait_for_timeout(500)
    assert "Registered successfully!" in page.text_content("#message")


def test_login_positive(page: Page):
    # first register a fresh user
    email = unique_email()
    username = "user_" + uuid.uuid4().hex[:5]
    password = "StrongPass123"

    # register
    page.goto(f"{BASE_URL}/register-page")
    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("text=Register")
    page.wait_for_timeout(300)

    # login
    page.goto(f"{BASE_URL}/login-page")
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("text=Login")
    page.wait_for_timeout(500)

    text = page.text_content("#message")
    assert "Login successful!" in text


def test_register_short_password_shows_error(page: Page):
    email = unique_email()
    username = "shortpass_user"

    page.goto(f"{BASE_URL}/register-page")
    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#password", "123")  # too short
    page.click("text=Register")
    page.wait_for_timeout(300)

    text = page.text_content("#message")
    assert "Password must be at least 8 characters." in text


def test_login_wrong_password_shows_error(page: Page):
    email = unique_email()
    username = "user_" + uuid.uuid4().hex[:5]
    real_password = "StrongPass123"

    # register with real password
    page.goto(f"{BASE_URL}/register-page")
    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#password", real_password)
    page.click("text=Register")
    page.wait_for_timeout(300)

    # try wrong password
    page.goto(f"{BASE_URL}/login-page")
    page.fill("#email", email)
    page.fill("#password", "WrongPassword1")
    page.click("text=Login")
    page.wait_for_timeout(500)

    text = page.text_content("#message")
    assert "Invalid email or password." in text
