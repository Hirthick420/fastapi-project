# app/crud/user.py
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def create_user(db: Session, user_in: UserCreate) -> User:
    """Create a new user with a hashed password."""
    hashed_pw = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed_pw,   # ✅ matches model field
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str) -> User | None:
    """Return the first user with this username, or None."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Return the first user with this email, or None."""
    return db.query(User).filter(User.email == email).first()
