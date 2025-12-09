import pytest
from app.core.calculation_factory import (
    perform_calculation,
    CalculationFactory,
    AddOperation,
    SubOperation,
    MulOperation,
    DivOperation,
)


def test_factory_returns_correct_operation():
    assert isinstance(CalculationFactory.get_operation("add"), AddOperation)
    assert isinstance(CalculationFactory.get_operation("sub"), SubOperation)
    assert isinstance(CalculationFactory.get_operation("mul"), MulOperation)
    assert isinstance(CalculationFactory.get_operation("div"), DivOperation)


def test_factory_invalid_type():
    with pytest.raises(ValueError):
        CalculationFactory.get_operation("invalid_type")


def test_add_operation():
    assert perform_calculation(5, 3, "add") == 8


def test_sub_operation():
    assert perform_calculation(5, 3, "sub") == 2


def test_mul_operation():
    assert perform_calculation(5, 3, "mul") == 15


def test_div_operation():
    assert perform_calculation(6, 3, "div") == 2


def test_divide_by_zero():
    with pytest.raises(ValueError):
        perform_calculation(5, 0, "div")
