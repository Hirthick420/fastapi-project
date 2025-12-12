# app/main.py

from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
from app.dependencies import get_db

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

from app.models.calculation import Calculation
from app.schemas.calculation import CalculationCreate, CalculationRead

from app.routers import auth
from app.core.calculation_factory import perform_calculation  # 🔹 NEW IMPORT
from app.routers import auth, reports

from app.schemas.user import UserCreate, UserRead, UserUpdate, PasswordChange, UserLogin
# ↑ add UserUpdate, PasswordChange to this import


# -------------------------
# DB setup
# -------------------------
Base.metadata.create_all(bind=engine)

# -------------------------
# FastAPI app
# -------------------------
app = FastAPI(title="FastAPI Calculator API")

# Routers (JWT auth router, etc.)
app.include_router(auth.router)
app.include_router(reports.router)   # NEW

# Static files (CSS/JS) for front-end
app.mount("/static", StaticFiles(directory="app/static"), name="static")




# -------------------------
# Root + HTML pages
# -------------------------
@app.get("/")
def root():
    return FileResponse("app/static/html/home.html")


@app.get("/register-page", include_in_schema=False)
def register_page():
    return FileResponse("app/static/html/register.html")


@app.get("/login-page", include_in_schema=False)
def login_page():
    return FileResponse("app/static/html/login.html")

@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/calculations-page", include_in_schema=False)
def calculations_page():
    return FileResponse("app/static/html/calculations.html")

@app.get("/reports-page", include_in_schema=False)
def reports_page():
    return FileResponse("app/static/html/reports.html")


@app.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # If username is changing, check uniqueness
    if user_in.username and user_in.username != user.username:
        existing = db.query(User).filter(User.username == user_in.username).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Username already taken",
            )
        user.username = user_in.username

    # If email is changing, check uniqueness
    if user_in.email and user_in.email != user.email:
        existing = db.query(User).filter(User.email == user_in.email).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already taken",
            )
        user.email = user_in.email

    db.commit()
    db.refresh(user)
    return user


# -------------------------
# USER ROUTES (existing)
# -------------------------
@app.post("/users/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(User)
        .filter((User.username == user_in.username) | (User.email == user_in.email))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )

    hashed_pw = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed_pw,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/users/login", response_model=UserRead)
def login_user(user_in: UserLogin, db: Session = Depends(get_db)):
    # Login by email + password
    db_user = db.query(User).filter(User.email == user_in.email).first()
    if not db_user or not verify_password(user_in.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    return db_user

@app.post("/users/{user_id}/change-password")
def change_password(
    user_id: int,
    pw: PasswordChange,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check old password
    if not verify_password(pw.old_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect",
        )

    # Hash and store new password
    user.password_hash = get_password_hash(pw.new_password)
    db.commit()

    return {"detail": "Password updated successfully"}


# -------------------------
# CALCULATION ROUTES
# -------------------------

@app.get("/profile-page", include_in_schema=False)
def profile_page():
    return FileResponse("app/static/html/profile.html")


def _compute_result(a: float, b: float, type_: str) -> float:
    """Pure function that actually does the math via the calculation factory."""
    try:
        return perform_calculation(a, b, type_)
    except ValueError as e:
        # Convert domain errors into HTTP 400
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@app.get("/calculations", response_model=List[CalculationRead])
def browse_calculations(db: Session = Depends(get_db)):
    calculations = db.query(Calculation).all()
    return calculations


@app.post(
    "/calculations",
    response_model=CalculationRead,
    status_code=status.HTTP_201_CREATED,
)
def add_calculation(
    calculation_in: CalculationCreate,
    db: Session = Depends(get_db),
):
    result = _compute_result(calculation_in.a, calculation_in.b, calculation_in.type)

    db_calc = Calculation(
        a=calculation_in.a,
        b=calculation_in.b,
        type=calculation_in.type,
        result=result,
    )
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc


@app.get("/calculations/{calc_id}", response_model=CalculationRead)
def read_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc


@app.put("/calculations/{calc_id}", response_model=CalculationRead)
def edit_calculation(
    calc_id: int,
    calculation_in: CalculationCreate,
    db: Session = Depends(get_db),
):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    result = _compute_result(calculation_in.a, calculation_in.b, calculation_in.type)

    calc.a = calculation_in.a
    calc.b = calculation_in.b
    calc.type = calculation_in.type
    calc.result = result

    db.commit()
    db.refresh(calc)
    return calc


@app.delete("/calculations/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    db.delete(calc)
    db.commit()
    return
