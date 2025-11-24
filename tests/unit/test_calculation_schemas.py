import pytest
from pydantic import ValidationError
from app.schemas.calculation import CalculationCreate


def test_valid_calculation_create():
    obj = CalculationCreate(a=5, b=3, type="add")
    assert obj.a == 5
    assert obj.b == 3
    assert obj.type == "add"


def test_invalid_type():
    with pytest.raises(ValidationError):
        CalculationCreate(a=5, b=3, type="power")


def test_divide_by_zero_invalid():
    with pytest.raises(ValidationError):
        CalculationCreate(a=5, b=0, type="div")
