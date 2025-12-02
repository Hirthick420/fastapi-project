# app/main.py (only the *relevant* parts shown)

from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.core.security import get_password_hash, verify_password

from app.models.calculation import Calculation
from app.schemas.calculation import CalculationCreate, CalculationRead

app = FastAPI(title="FastAPI Calculator API")

@app.get("/")
def root():
    return {"message": "FastAPI Calculator API is running. Go to /docs for Swagger UI."}

# -------------------------
# USER ROUTES (already working – keep yours)
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
def login_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # assuming same schema as register (username, email, password)
    db_user = db.query(User).filter(User.username == user_in.username).first()
    if not db_user or not verify_password(user_in.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return db_user


# -------------------------
# CALCULATION ROUTES (NEW / FIXED)
# -------------------------

def _compute_result(a: float, b: float, type_: str) -> float:
    """Pure function that actually does the math."""
    if type_ == "add":
        return a + b
    if type_ == "sub":
        return a - b
    if type_ == "mul":
        return a * b
    if type_ == "div":
        if b == 0:
            # This should already be blocked by the Pydantic validator,
            # but we double-check to avoid 500s.
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Division by zero is not allowed",
            )
        return a / b
    # Should never happen because schema restricts type, but just in case:
    raise HTTPException(status_code=400, detail="Invalid calculation type")


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
    # 204 means "No Content" -> we just return nothing
    return
