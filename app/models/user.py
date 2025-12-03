# app/models/user.py
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)

    # 🔴 THIS is the important part: the attribute MUST be named password_hash
    password_hash = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
