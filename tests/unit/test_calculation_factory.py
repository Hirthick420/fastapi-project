# tests/unit/test_calculation_factory.py
import math
import pytest

from app.core.calculation_factory import (
    perform_calculation,
    CalculationFactory,
    AddOperation,
    SubOperation,
    MulOperation,
    DivOperation,
    PowerOperation,
    ModOperation,
    FloorDivOperation,
    SqrtOperation,
    LogOperation,
    FactorialOperation,
    AbsDiffOperation,
)


def test_factory_returns_correct_operation_basic():
    assert isinstance(CalculationFactory.get_operation("add"), AddOperation)
    assert isinstance(CalculationFactory.get_operation("sub"), SubOperation)
    assert isinstance(CalculationFactory.get_operation("mul"), MulOperation)
    assert isinstance(CalculationFactory.get_operation("div"), DivOperation)


def test_factory_returns_correct_operation_advanced():
    assert isinstance(CalculationFactory.get_operation("power"), PowerOperation)
    assert isinstance(CalculationFactory.get_operation("mod"), ModOperation)
    assert isinstance(CalculationFactory.get_operation("floordiv"), FloorDivOperation)
    assert isinstance(CalculationFactory.get_operation("sqrt"), SqrtOperation)
    assert isinstance(CalculationFactory.get_operation("log"), LogOperation)
    assert isinstance(CalculationFactory.get_operation("factorial"), FactorialOperation)
    assert isinstance(CalculationFactory.get_operation("absdiff"), AbsDiffOperation)


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


def test_power_operation():
    assert perform_calculation(2, 3, "power") == 8


def test_mod_operation():
    assert perform_calculation(10, 3, "mod") == 1


def test_floordiv_operation():
    assert perform_calculation(10, 3, "floordiv") == 3


def test_sqrt_operation():
    assert perform_calculation(9, 0, "sqrt") == 3  # b ignored


def test_sqrt_negative_raises():
    with pytest.raises(ValueError):
        perform_calculation(-1, 0, "sqrt")


def test_log_operation():
    # log base 10 of 100 = 2
    assert math.isclose(perform_calculation(100, 10, "log"), 2.0)


def test_log_invalid_a():
    with pytest.raises(ValueError):
        perform_calculation(0, 10, "log")


def test_log_invalid_base():
    with pytest.raises(ValueError):
        perform_calculation(10, 1, "log")


def test_factorial_operation():
    assert perform_calculation(5, 0, "factorial") == 120


def test_factorial_invalid():
    with pytest.raises(ValueError):
        perform_calculation(-1, 0, "factorial")


def test_absdiff_operation():
    assert perform_calculation(10, 7, "absdiff") == 3
    assert perform_calculation(7, 10, "absdiff") == 3
