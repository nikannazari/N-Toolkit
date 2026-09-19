"""
calculator++.py - Core logic of Calculator++.
"""
import math

class Calculator:
    """Core Calculator++ operations."""

    # ── Basic Operations ──
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

    # ── Advanced Operations (The "++" features) ──
    @staticmethod
    def sqrt(x: float) -> float:
        if x < 0:
            raise ValueError("Cannot calculate square root of a negative number.")
        return math.sqrt(x)

    @staticmethod
    def power(base: float, exp: float) -> float:
        return math.pow(base, exp)

    @staticmethod
    def factorial(n: float) -> int:
        # Convert to int if it's a whole number (e.g., 5.0 -> 5)
        if not n.is_integer():
            raise ValueError("Factorial is only defined for integers.")
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        return math.factorial(int(n))

    @staticmethod
    def solve_linear_eq2(a1: float, b1: float, c1: float, a2: float, b2: float, c2: float) -> str:
        """
        Solves a system of 2 linear equations:
        a1*x + b1*y = c1
        a2*x + b2*y = c2
        """
        # Cramer's Rule: Determinant
        det = a1 * b2 - a2 * b1
        
        if det == 0:
            return "No unique solution (lines are parallel or identical)."
        
        x = (c1 * b2 - c2 * b1) / det
        y = (a1 * c2 - a2 * c1) / det
        
        return f"x = {x}, y = {y}"