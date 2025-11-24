from abc import ABC, abstractmethod


# ----------------------------
# Base class for all operations
# ----------------------------
class BaseOperation(ABC):
    @abstractmethod
    def compute(self, a: float, b: float) -> float:
        """Compute the result of the operation."""
        pass


# ----------------------------
# Concrete Operations
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
