# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.init_db import init_db
from app.dependencies import get_db
from app.schemas.user import UserCreate, UserRead
from app.crud.user import (
    create_user,
    get_user_by_username,
    get_user_by_email,
)

app = FastAPI()

# Ensure tables exist on startup (simple way, fine for assignment)
@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/users/", response_model=UserRead)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = create_user(db, user_in)
    return user
