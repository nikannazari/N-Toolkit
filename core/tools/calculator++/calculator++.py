"""
calculator++.py - Core logic for Calculator++.
"""


class Calculator:
    """
    Core calculator logic.

    This class contains no CLI or input handling.
    """

    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")

        return a / b