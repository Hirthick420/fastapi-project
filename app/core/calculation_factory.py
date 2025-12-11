# app/core/calculation_factory.py
from abc import ABC, abstractmethod
import math


# ----------------------------
# Base class for all operations
# ----------------------------
class BaseOperation(ABC):
    @abstractmethod
    def compute(self, a: float, b: float) -> float:
        """Compute the result of the operation."""
        pass


# ----------------------------
# Concrete Basic Operations
# ----------------------------
class AddOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        return a + b


class SubOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        return a - b


class MulOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        return a * b


class DivOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b


# ----------------------------
# Concrete Advanced Operations
# ----------------------------
class PowerOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        return a ** b


class ModOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Modulus by zero is not allowed.")
        return a % b


class FloorDivOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Floor division by zero is not allowed.")
        return a // b


class SqrtOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        # b is ignored; kept for consistent interface
        if a < 0:
            raise ValueError("Square root of negative number is not allowed.")
        return math.sqrt(a)


class LogOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        """
        Compute logarithm of a with base b: log_b(a).
        a must be > 0, b must be > 0 and != 1.
        """
        if a <= 0:
            raise ValueError("Logarithm is only defined for a > 0.")
        if b <= 0 or b == 1:
            raise ValueError("Logarithm base must be > 0 and != 1.")
        return math.log(a, b)


class FactorialOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        # b is ignored; factorial only uses a
        if a < 0 or int(a) != a:
            raise ValueError("Factorial is only defined for non-negative integers.")
        return math.factorial(int(a))


class AbsDiffOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        return abs(a - b)


# ----------------------------
# Factory Class
# ----------------------------
class CalculationFactory:
    @staticmethod
    def get_operation(calc_type: str) -> BaseOperation:
        calc_type = calc_type.lower()

        if calc_type == "add":
            return AddOperation()
        elif calc_type == "sub":
            return SubOperation()
        elif calc_type == "mul":
            return MulOperation()
        elif calc_type == "div":
            return DivOperation()
        elif calc_type == "power":
            return PowerOperation()
        elif calc_type == "mod":
            return ModOperation()
        elif calc_type == "floordiv":
            return FloorDivOperation()
        elif calc_type == "sqrt":
            return SqrtOperation()
        elif calc_type == "log":
            return LogOperation()
        elif calc_type == "factorial":
            return FactorialOperation()
        elif calc_type == "absdiff":
            return AbsDiffOperation()
        else:
            raise ValueError(f"Invalid calculation type: {calc_type}")


# ----------------------------
# Helper function
# ----------------------------
def perform_calculation(a: float, b: float, calc_type: str) -> float:
    """
    Simple helper that:
    1. Gets the correct operation class using the factory
    2. Computes the result
    """
    operation = CalculationFactory.get_operation(calc_type)
    return operation.compute(a, b)
