# app/db/init_db.py
from app.db.base import Base
from app.db.session import engine
import app.models  # noqa: F401  # ensures models are imported


def init_db():
    Base.metadata.create_all(bind=engine)
