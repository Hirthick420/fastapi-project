# app/routers/auth.py
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.dependencies import get_db
from app.models.user import User

SECRET_KEY = "change-me-in-real-life"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(tags=["auth"])


class RegisterRequest(BaseModel):
  username: str
  email: EmailStr
  password: str


class LoginRequest(BaseModel):
  email: EmailStr
  password: str


class TokenResponse(BaseModel):
  access_token: str
  token_type: str = "bearer"


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
  to_encode = data.copy()
  expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
  existing = (
      db.query(User)
      .filter((User.username == payload.username) | (User.email == payload.email))
      .first()
  )
  if existing:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Username or email already exists",
    )

  user = User(
      username=payload.username,
      email=payload.email,
      password_hash=get_password_hash(payload.password),
  )
  db.add(user)
  db.commit()
  db.refresh(user)
  return {"id": user.id, "username": user.username, "email": user.email}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):  # ✅
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token)

