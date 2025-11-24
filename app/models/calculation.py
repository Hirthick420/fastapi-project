from sqlalchemy import Column, Integer, Float, String

# ⬇️ IMPORTANT: copy this line EXACTLY from app/models/user.py
from app.db.base import Base  # OR from app.db.base_class import Base — use whatever user.py uses


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(String, nullable=False, index=True)
    result = Column(Float, nullable=False)
