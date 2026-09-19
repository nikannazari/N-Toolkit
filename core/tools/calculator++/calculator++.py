"""
calculator++.py - Core logic of Calculator++.
"""
import math
from collections import Counter


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

    # ── Helper ──
    @staticmethod
    def _as_int(n) -> int:
        """Convert a whole-number int/float into int, else raise."""
        if isinstance(n, bool):
            raise ValueError("Boolean is not a valid numeric input.")
        if isinstance(n, int):
            return n
        if isinstance(n, float) and n.is_integer():
            return int(n)
        raise ValueError(f"{n!r} is not an integer value.")

    # ── Trigonometry ──
    @staticmethod
    def sin(x: float, degrees: bool = False) -> float:
        return math.sin(math.radians(x) if degrees else x)

    @staticmethod
    def cos(x: float, degrees: bool = False) -> float:
        return math.cos(math.radians(x) if degrees else x)

    @staticmethod
    def tan(x: float, degrees: bool = False) -> float:
        return math.tan(math.radians(x) if degrees else x)

    @staticmethod
    def asin(x: float, degrees: bool = False) -> float:
        if not -1 <= x <= 1:
            raise ValueError("arcsin input must be in [-1, 1].")
        r = math.asin(x)
        return math.degrees(r) if degrees else r

    @staticmethod
    def acos(x: float, degrees: bool = False) -> float:
        if not -1 <= x <= 1:
            raise ValueError("arccos input must be in [-1, 1].")
        r = math.acos(x)
        return math.degrees(r) if degrees else r

    @staticmethod
    def atan(x: float, degrees: bool = False) -> float:
        r = math.atan(x)
        return math.degrees(r) if degrees else r

    @staticmethod
    def sinh(x: float) -> float:
        return math.sinh(x)

    @staticmethod
    def cosh(x: float) -> float:
        return math.cosh(x)

    @staticmethod
    def tanh(x: float) -> float:
        return math.tanh(x)

    # ── Logarithms & Exponentials ──
    @staticmethod
    def log(x: float, base: float = 10.0) -> float:
        if x <= 0:
            raise ValueError("Logarithm is only defined for positive numbers.")
        if base <= 0 or base == 1:
            raise ValueError("Base must be positive and not equal to 1.")
        return math.log(x, base)

    @staticmethod
    def ln(x: float) -> float:
        if x <= 0:
            raise ValueError("Natural logarithm is only defined for positive numbers.")
        return math.log(x)

    @staticmethod
    def log2(x: float) -> float:
        if x <= 0:
            raise ValueError("Logarithm is only defined for positive numbers.")
        return math.log2(x)

    @staticmethod
    def exp(x: float) -> float:
        return math.exp(x)

    # ── Roots & Rounding ──
    @staticmethod
    def cube_root(x: float) -> float:
        if x < 0:
            return -(-x) ** (1 / 3)
        return x ** (1 / 3)

    @staticmethod
    def nth_root(x: float, n: float) -> float:
        if n == 0:
            raise ValueError("n cannot be zero.")
        if x < 0:
            n_int = Calculator._as_int(n)
            if n_int % 2 == 0:
                raise ValueError("Even roots are not real for negative numbers.")
            return -((-x) ** (1 / n_int))
        return x ** (1 / n)

    @staticmethod
    def abs_val(x: float) -> float:
        return abs(x)

    @staticmethod
    def floor(x: float) -> int:
        return math.floor(x)

    @staticmethod
    def ceiling(x: float) -> int:
        return math.ceil(x)

    @staticmethod
    def round_num(x: float, digits: int = 0) -> float:
        return round(x, digits)

    @staticmethod
    def mod(a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot compute modulo with zero.")
        return a % b

    # ── Angle Conversion ──
    @staticmethod
    def deg_to_rad(x: float) -> float:
        return math.radians(x)

    @staticmethod
    def rad_to_deg(x: float) -> float:
        return math.degrees(x)

    # ── Number Theory ──
    @staticmethod
    def gcd(a: float, b: float) -> int:
        a, b = Calculator._as_int(a), Calculator._as_int(b)
        return math.gcd(abs(a), abs(b))

    @staticmethod
    def lcm(a: float, b: float) -> int:
        a, b = Calculator._as_int(a), Calculator._as_int(b)
        a, b = abs(a), abs(b)
        if a == 0 or b == 0:
            return 0
        return (a // math.gcd(a, b)) * b

    @staticmethod
    def is_prime(n: float) -> bool:
        n = Calculator._as_int(n)
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.isqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def prime_factors(n: float) -> list:
        n = Calculator._as_int(n)
        if n < 2:
            return []
        factors = []
        while n % 2 == 0:
            factors.append(2)
            n //= 2
        i = 3
        while i * i <= n:
            while n % i == 0:
                factors.append(i)
                n //= i
            i += 2
        if n > 1:
            factors.append(n)
        return factors

    @staticmethod
    def next_prime(n: float) -> int:
        n = Calculator._as_int(n)
        candidate = n + 1
        while not Calculator.is_prime(candidate):
            candidate += 1
        return candidate

    @staticmethod
    def fibonacci(n: float) -> list:
        n = Calculator._as_int(n)
        if n < 0:
            raise ValueError("Fibonacci is not defined for negative indices.")
        if n == 0:
            return [0]
        seq = [0, 1]
        for _ in range(2, n + 1):
            seq.append(seq[-1] + seq[-2])
        return seq

    @staticmethod
    def is_even(n: float) -> bool:
        return Calculator._as_int(n) % 2 == 0

    @staticmethod
    def is_odd(n: float) -> bool:
        return Calculator._as_int(n) % 2 != 0

    # ── Combinatorics ──
    @staticmethod
    def permutations(n: float, r: float) -> int:
        n, r = Calculator._as_int(n), Calculator._as_int(r)
        if n < 0 or r < 0 or r > n:
            raise ValueError("Invalid n or r values.")
        return math.perm(n, r)

    @staticmethod
    def combinations(n: float, r: float) -> int:
        n, r = Calculator._as_int(n), Calculator._as_int(r)
        if n < 0 or r < 0 or r > n:
            raise ValueError("Invalid n or r values.")
        return math.comb(n, r)

    # ── Statistics ──
    @staticmethod
    def mean(data: list) -> float:
        if not data:
            raise ValueError("Cannot compute mean of empty list.")
        return sum(data) / len(data)

    @staticmethod
    def median(data: list) -> float:
        if not data:
            raise ValueError("Cannot compute median of empty list.")
        s = sorted(data)
        n = len(s)
        mid = n // 2
        if n % 2 == 0:
            return (s[mid - 1] + s[mid]) / 2
        return s[mid]

    @staticmethod
    def mode(data: list) -> list:
        if not data:
            return []
        counts = Counter(data)
        max_count = max(counts.values())
        return sorted(k for k, v in counts.items() if v == max_count)

    @staticmethod
    def variance(data: list, sample: bool = True) -> float:
        if len(data) < 2:
            raise ValueError("Need at least 2 data points.")
        m = Calculator.mean(data)
        denom = len(data) - 1 if sample else len(data)
        return sum((x - m) ** 2 for x in data) / denom

    @staticmethod
    def std_dev(data: list, sample: bool = True) -> float:
        return math.sqrt(Calculator.variance(data, sample))

    @staticmethod
    def minimum(data: list) -> float:
        if not data:
            raise ValueError("Cannot compute minimum of empty list.")
        return min(data)

    @staticmethod
    def maximum(data: list) -> float:
        if not data:
            raise ValueError("Cannot compute maximum of empty list.")
        return max(data)

    @staticmethod
    def sum_of(data: list) -> float:
        return sum(data)

    @staticmethod
    def product_of(data: list) -> float:
        if not data:
            return 1
        result = 1
        for x in data:
            result *= x
        return result

    @staticmethod
    def geometric_mean(data: list) -> float:
        if not data:
            raise ValueError("Cannot compute geometric mean of empty list.")
        if any(x < 0 for x in data):
            raise ValueError("Geometric mean is not defined for negative numbers.")
        if any(x == 0 for x in data):
            return 0.0
        return math.pow(Calculator.product_of(data), 1 / len(data))

    @staticmethod
    def harmonic_mean(data: list) -> float:
        if not data:
            raise ValueError("Cannot compute harmonic mean of empty list.")
        if any(x <= 0 for x in data):
            raise ValueError("Harmonic mean requires all positive values.")
        return len(data) / sum(1 / x for x in data)

    @staticmethod
    def range_of(data: list) -> float:
        if not data:
            raise ValueError("Cannot compute range of empty list.")
        return max(data) - min(data)

    # ── Geometry (2D) ──
    @staticmethod
    def area_circle(r: float) -> float:
        if r < 0:
            raise ValueError("Radius cannot be negative.")
        return math.pi * r ** 2

    @staticmethod
    def circumference(r: float) -> float:
        if r < 0:
            raise ValueError("Radius cannot be negative.")
        return 2 * math.pi * r

    @staticmethod
    def area_rectangle(length: float, width: float) -> float:
        if length < 0 or width < 0:
            raise ValueError("Length and width cannot be negative.")
        return length * width

    @staticmethod
    def perimeter_rectangle(length: float, width: float) -> float:
        if length < 0 or width < 0:
            raise ValueError("Length and width cannot be negative.")
        return 2 * (length + width)

    @staticmethod
    def area_triangle(base: float, height: float) -> float:
        if base < 0 or height < 0:
            raise ValueError("Base and height cannot be negative.")
        return 0.5 * base * height

    @staticmethod
    def area_triangle_sss(a: float, b: float, c: float) -> float:
        """Area from three sides using Heron's formula."""
        sides = sorted([a, b, c])
        if sides[0] <= 0:
            raise ValueError("Sides must be positive.")
        if sides[0] + sides[1] <= sides[2]:
            raise ValueError("Triangle inequality violated.")
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))

    @staticmethod
    def area_trapezoid(a: float, b: float, h: float) -> float:
        if a < 0 or b < 0 or h < 0:
            raise ValueError("Sides and height cannot be negative.")
        return 0.5 * (a + b) * h

    @staticmethod
    def distance_2d(x1: float, y1: float, x2: float, y2: float) -> float:
        return math.hypot(x2 - x1, y2 - y1)

    @staticmethod
    def midpoint_2d(x1: float, y1: float, x2: float, y2: float) -> tuple:
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    @staticmethod
    def slope_2d(x1: float, y1: float, x2: float, y2: float) -> float:
        if x2 - x1 == 0:
            raise ValueError("Slope is undefined (vertical line).")
        return (y2 - y1) / (x2 - x1)

    # ── Geometry (3D / Volumes) ──
    @staticmethod
    def volume_sphere(r: float) -> float:
        if r < 0:
            raise ValueError("Radius cannot be negative.")
        return (4 / 3) * math.pi * r ** 3

    @staticmethod
    def surface_area_sphere(r: float) -> float:
        if r < 0:
            raise ValueError("Radius cannot be negative.")
        return 4 * math.pi * r ** 2

    @staticmethod
    def volume_cylinder(r: float, h: float) -> float:
        if r < 0 or h < 0:
            raise ValueError("Radius and height cannot be negative.")
        return math.pi * r ** 2 * h

    @staticmethod
    def volume_cone(r: float, h: float) -> float:
        if r < 0 or h < 0:
            raise ValueError("Radius and height cannot be negative.")
        return (1 / 3) * math.pi * r ** 2 * h

    @staticmethod
    def volume_cube(side: float) -> float:
        if side < 0:
            raise ValueError("Side cannot be negative.")
        return side ** 3

    @staticmethod
    def volume_rect_prism(l: float, w: float, h: float) -> float:
        if l < 0 or w < 0 or h < 0:
            raise ValueError("Dimensions cannot be negative.")
        return l * w * h

    @staticmethod
    def volume_pyramid(base_area: float, h: float) -> float:
        if base_area < 0 or h < 0:
            raise ValueError("Base area and height cannot be negative.")
        return (1 / 3) * base_area * h

    # ── Equations ──
    @staticmethod
    def solve_linear_eq(a: float, b: float) -> str:
        """Solves a*x + b = 0."""
        if a == 0:
            return "Infinite solutions." if b == 0 else "No solution."
        return f"x = {-b / a}"

    @staticmethod
    def solve_quadratic_eq(a: float, b: float, c: float) -> str:
        """Solves a*x^2 + b*x + c = 0."""
        if a == 0:
            return Calculator.solve_linear_eq(b, c)
        disc = b ** 2 - 4 * a * c
        if disc < 0:
            real = -b / (2 * a)
            imag = math.sqrt(-disc) / (2 * a)
            return f"x1 = {real} + {imag}i, x2 = {real} - {imag}i"
        if disc == 0:
            x = -b / (2 * a)
            return f"x = {x} (double root)"
        sqrt_d = math.sqrt(disc)
        x1 = (-b + sqrt_d) / (2 * a)
        x2 = (-b - sqrt_d) / (2 * a)
        return f"x1 = {x1}, x2 = {x2}"

    # ── Percentage & Finance ──
    @staticmethod
    def percentage(value: float, percent: float) -> float:
        return (value * percent) / 100

    @staticmethod
    def percentage_change(old: float, new: float) -> float:
        if old == 0:
            raise ValueError("Old value cannot be zero.")
        return ((new - old) / old) * 100

    @staticmethod
    def simple_interest(principal: float, rate: float, time: float) -> float:
        if principal < 0 or time < 0:
            raise ValueError("Principal and time cannot be negative.")
        return principal * rate * time / 100

    @staticmethod
    def compound_interest(principal: float, rate: float, time: float, n: float = 1) -> float:
        if principal < 0 or time < 0:
            raise ValueError("Principal and time cannot be negative.")
        if n <= 0:
            raise ValueError("Compounding frequency must be positive.")
        amount = principal * (1 + rate / (100 * n)) ** (n * time)
        return amount - principal

    # ── Physics / Conversions ──
    @staticmethod
    def celsius_to_fahrenheit(c: float) -> float:
        return (c * 9 / 5) + 32

    @staticmethod
    def fahrenheit_to_celsius(f: float) -> float:
        return (f - 32) * 5 / 9

    @staticmethod
    def celsius_to_kelvin(c: float) -> float:
        return c + 273.15

    @staticmethod
    def kelvin_to_celsius(k: float) -> float:
        return k - 273.15

    @staticmethod
    def kinetic_energy(mass: float, velocity: float) -> float:
        if mass < 0:
            raise ValueError("Mass cannot be negative.")
        return 0.5 * mass * velocity ** 2

    @staticmethod
    def potential_energy(mass: float, height: float, g: float = 9.81) -> float:
        if mass < 0 or height < 0:
            raise ValueError("Mass and height cannot be negative.")
        return mass * g * height

    @staticmethod
    def ohms_law(v: float = None, i: float = None, r: float = None) -> float:
        """V = I * R. Provide exactly two; the third is computed."""
        provided = sum(x is not None for x in (v, i, r))
        if provided != 2:
            raise ValueError("Exactly two of v, i, r must be provided.")
        if v is None:
            return i * r
        if i is None:
            if r == 0:
                raise ZeroDivisionError("Resistance cannot be zero when solving for current.")
            return v / r
        if i == 0:
            raise ZeroDivisionError("Current cannot be zero when solving for resistance.")
        return v / i

    @staticmethod
    def speed(distance: float = None, time: float = None) -> float:
        """speed = distance / time. Provide both."""
        if distance is None or time is None:
            raise ValueError("Both distance and time must be provided.")
        if time == 0:
            raise ZeroDivisionError("Time cannot be zero.")
        return distance / time

    @staticmethod
    def density(mass: float, volume: float) -> float:
        if volume == 0:
            raise ZeroDivisionError("Volume cannot be zero.")
        return mass / volume

    @staticmethod
    def pressure(force: float, area: float) -> float:
        if area == 0:
            raise ZeroDivisionError("Area cannot be zero.")
        return force / area

    @staticmethod
    def bmi(weight_kg: float, height_m: float) -> float:
        if weight_kg <= 0 or height_m <= 0:
            raise ValueError("Weight and height must be positive.")
        return weight_kg / (height_m ** 2)

    # ── Pythagoras ──
    @staticmethod
    def pythagorean_hypotenuse(a: float, b: float) -> float:
        if a < 0 or b < 0:
            raise ValueError("Sides cannot be negative.")
        return math.hypot(a, b)

    @staticmethod
    def pythagorean_leg(c: float, a: float) -> float:
        """Returns the missing leg b given hypotenuse c and leg a."""
        if c < 0 or a < 0:
            raise ValueError("Sides cannot be negative.")
        if a > c:
            raise ValueError("Leg cannot be longer than the hypotenuse.")
        return math.sqrt(c ** 2 - a ** 2)