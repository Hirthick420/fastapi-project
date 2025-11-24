from typing import Literal, Optional

from pydantic import BaseModel, model_validator


# ----------------------------
# Base schema
# ----------------------------
class CalculationBase(BaseModel):
    a: float
    b: float
    type: Literal["add", "sub", "mul", "div"]


# ----------------------------
# Schema for creation (input)
# ----------------------------
class CalculationCreate(CalculationBase):
    @model_validator(mode="after")
    def check_division_by_zero(self):
        """
        Cross-field validation:
        if type == 'div' and b == 0 -> raise error
        """
        if self.type == "div" and self.b == 0:
            raise ValueError("Division by zero is not allowed.")
        return self


# ----------------------------
# Schema for reading (output)
# ----------------------------
class CalculationRead(CalculationBase):
    id: int
    result: float
    user_id: Optional[int] = None

    class Config:
        orm_mode = True
