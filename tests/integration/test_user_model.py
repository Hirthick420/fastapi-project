# tests/integration/test_user_model.py
import pytest
from sqlalchemy.exc import IntegrityError

from app.crud.user import create_user, get_user_by_username, get_user_by_email
from app.schemas.user import UserCreate


def test_create_user_and_read_back(db_session):
    user_in = UserCreate(
        username="uniqueuser",
        email="unique@example.com",
        password="strongpassword",
    )

    user = create_user(db_session, user_in)

    assert user.id is not None
    assert user.username == "uniqueuser"
    assert user.email == "unique@example.com"
    # password must be stored hashed
    assert user.password_hash != user_in.password

    by_username = get_user_by_username(db_session, "uniqueuser")
    by_email = get_user_by_email(db_session, "unique@example.com")

    assert by_username.id == user.id
    assert by_email.id == user.id


def test_username_uniqueness_constraint(db_session):
    user1 = UserCreate(
        username="duplicateuser",
        email="dup1@example.com",
        password="password1",
    )
    user2 = UserCreate(
        username="duplicateuser",
        email="dup2@example.com",
        password="password2",
    )

    create_user(db_session, user1)

    with pytest.raises(IntegrityError):
        create_user(db_session, user2)


def test_email_uniqueness_constraint(db_session):
    user1 = UserCreate(
        username="user1",
        email="same@example.com",
        password="password1",
    )
    user2 = UserCreate(
        username="user2",
        email="same@example.com",
        password="password2",
    )

    create_user(db_session, user1)

    with pytest.raises(IntegrityError):
        create_user(db_session, user2)
