# tests/unit/test_schemas.py
import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate, UserRead

def test_usercreate_valid():
    user = UserCreate(
        username="hirthick",
        email="test@example.com",
        password="strongpassword",
    )
    assert user.username == "hirthick"
    assert user.email == "test@example.com"

def test_usercreate_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            username="user1",
            email="not-an-email",
            password="strongpassword",
        )

def test_usercreate_short_password():
    with pytest.raises(ValidationError):
        UserCreate(
            username="user1",
            email="test@example.com",
            password="123",
        )

def test_userread_serialization():
    user = UserRead(
        id=1,
        username="user1",
        email="test@example.com",
        created_at="2025-01-01T00:00:00Z",
    )
    assert user.id == 1
