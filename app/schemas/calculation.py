# app/schemas/calculation.py
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

# All allowed calculation types for this project
ALLOWED_CALC_TYPES = {
    "add",
    "sub",
    "mul",
    "div",
    "power",
    "mod",
    "floordiv",
    "sqrt",
    "log",
    "factorial",
    "absdiff",
}


# ----------------------------
# Base schema
# ----------------------------
class CalculationBase(BaseModel):
    a: float
    b: float
    type: str  # validated via field + model validators

    # 1) Validate *just* the type value itself
    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v not in ALLOWED_CALC_TYPES:
            # This becomes a pydantic ValidationError in tests
            raise ValueError(f"Invalid calculation type: {v}")
        return v

    # 2) Cross-field validation for a, b, and type together
    @model_validator(mode="after")
    def validate_all(self):
        """
        Cross-field validation for:
        - division/mod/floordiv by zero
        - sqrt/log/factorial constraints
        """
        t = self.type
        a = self.a
        b = self.b

        # Division-like operations cannot have b == 0
        if t in {"div", "floordiv", "mod"} and b == 0:
            raise ValueError("Division, floor division, and modulus by zero are not allowed.")

        # Advanced operations constraints
        if t == "sqrt":
            if a < 0:
                raise ValueError("Square root of negative number is not allowed.")

        if t == "log":
            if a <= 0:
                raise ValueError("Logarithm is only defined for a > 0.")
            if b <= 0 or b == 1:
                raise ValueError("Logarithm base must be > 0 and != 1.")

        if t == "factorial":
            if a < 0 or int(a) != a:
                raise ValueError("Factorial is only defined for non-negative integers.")

        # absdiff, power, etc. don't need extra schema-level checks
        return self


# ----------------------------
# Schema for creation (input)
# ----------------------------
class CalculationCreate(CalculationBase):
    # All validation is done in CalculationBase
    pass


# ----------------------------
# Schema for reading (output)
# ----------------------------
class CalculationRead(CalculationBase):
    id: int
    result: float
    user_id: Optional[int] = None

    class Config:
        orm_mode = True
