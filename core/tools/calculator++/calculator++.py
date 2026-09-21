"""
calculator++.py - Core logic of Calculator++.
"""
import math
import base64
import hashlib
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
        if c < 0 or a < 0:
            raise ValueError("Sides cannot be negative.")
        if a > c:
            raise ValueError("Leg cannot be longer than the hypotenuse.")
        return math.sqrt(c ** 2 - a ** 2)

    # ═══════════════════════════════════════════════════════════════
    # ── Scientific Functions & Constants ──
    # ═══════════════════════════════════════════════════════════════
    PI = math.pi
    E = math.e
    GOLDEN_RATIO = (1 + math.sqrt(5)) / 2
    SPEED_OF_LIGHT = 299_792_458          # m/s
    GRAVITATIONAL_CONSTANT = 6.67430e-11  # N·m²/kg²
    PLANCK_CONSTANT = 6.62607015e-34      # J·s
    BOLTZMANN_CONSTANT = 1.380649e-23     # J/K
    AVOGADRO_NUMBER = 6.02214076e23       # 1/mol
    ELECTRON_MASS = 9.1093837e-31         # kg
    PROTON_MASS = 1.6726219e-27           # kg
    NEUTRON_MASS = 1.6749275e-27          # kg
    ELEMENTARY_CHARGE = 1.602176634e-19   # C
    GAS_CONSTANT = 8.314462618            # J/(mol·K)

    @staticmethod
    def asinh(x: float) -> float:
        return math.asinh(x)

    @staticmethod
    def acosh(x: float) -> float:
        if x < 1:
            raise ValueError("arccosh requires x >= 1.")
        return math.acosh(x)

    @staticmethod
    def atanh(x: float) -> float:
        if not -1 < x < 1:
            raise ValueError("arctanh requires -1 < x < 1.")
        return math.atanh(x)

    @staticmethod
    def cot(x: float, degrees: bool = False) -> float:
        s = Calculator.sin(x, degrees)
        if s == 0:
            raise ZeroDivisionError("cot is undefined when sin = 0.")
        return 1 / s

    @staticmethod
    def sec(x: float, degrees: bool = False) -> float:
        c = Calculator.cos(x, degrees)
        if c == 0:
            raise ZeroDivisionError("sec is undefined when cos = 0.")
        return 1 / c

    @staticmethod
    def csc(x: float, degrees: bool = False) -> float:
        s = Calculator.sin(x, degrees)
        if s == 0:
            raise ZeroDivisionError("csc is undefined when sin = 0.")
        return 1 / s

    @staticmethod
    def gamma(x: float) -> float:
        return math.gamma(x)

    @staticmethod
    def lgamma(x: float) -> float:
        return math.lgamma(x)

    @staticmethod
    def erf(x: float) -> float:
        return math.erf(x)

    @staticmethod
    def normal_pdf(x: float, mu: float = 0, sigma: float = 1) -> float:
        if sigma <= 0:
            raise ValueError("Standard deviation must be positive.")
        return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)

    @staticmethod
    def normal_cdf(x: float, mu: float = 0, sigma: float = 1) -> float:
        if sigma <= 0:
            raise ValueError("Standard deviation must be positive.")
        return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))

    # ═══════════════════════════════════════════════════════════════
    # ── Prime Numbers ──
    # ═══════════════════════════════════════════════════════════════
    @staticmethod
    def prev_prime(n: float) -> int:
        n = Calculator._as_int(n)
        if n <= 2:
            raise ValueError("No prime smaller than 2.")
        candidate = n - 1
        while candidate >= 2 and not Calculator.is_prime(candidate):
            candidate -= 1
        if candidate < 2:
            raise ValueError("No prime smaller than 2.")
        return candidate

    @staticmethod
    def primes_up_to(n: float) -> list:
        """Sieve of Eratosthenes."""
        n = Calculator._as_int(n)
        if n < 2:
            return []
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        for i in range(2, int(math.isqrt(n)) + 1):
            if sieve[i]:
                for j in range(i * i, n + 1, i):
                    sieve[j] = False
        return [i for i, is_p in enumerate(sieve) if is_p]

    @staticmethod
    def prime_count(n: float) -> int:
        return len(Calculator.primes_up_to(n))

    @staticmethod
    def nth_prime(k: float) -> int:
        k = Calculator._as_int(k)
        if k < 1:
            raise ValueError("k must be >= 1.")
        count = 0
        candidate = 1
        while count < k:
            candidate += 1
            if Calculator.is_prime(candidate):
                count += 1
        return candidate

    @staticmethod
    def is_coprime(a: float, b: float) -> bool:
        return Calculator.gcd(a, b) == 1

    @staticmethod
    def euler_totient(n: float) -> int:
        n = Calculator._as_int(n)
        if n < 1:
            raise ValueError("Euler's totient is defined for n >= 1.")
        result = n
        temp = n
        p = 2
        while p * p <= temp:
            if temp % p == 0:
                while temp % p == 0:
                    temp //= p
                result -= result // p
            p += 1
        if temp > 1:
            result -= result // temp
        return result

    @staticmethod
    def divisors_of(n: float) -> list:
        n = Calculator._as_int(n)
        if n < 1:
            raise ValueError("n must be a positive integer.")
        divs = []
        i = 1
        while i * i <= n:
            if n % i == 0:
                divs.append(i)
                if i != n // i:
                    divs.append(n // i)
            i += 1
        return sorted(divs)

    @staticmethod
    def divisor_count(n: float) -> int:
        return len(Calculator.divisors_of(n))

    @staticmethod
    def sum_of_divisors(n: float) -> int:
        return sum(Calculator.divisors_of(n))

    @staticmethod
    def is_perfect_number(n: float) -> bool:
        n = Calculator._as_int(n)
        if n < 1:
            return False
        return sum(d for d in Calculator.divisors_of(n) if d != n) == n

    @staticmethod
    def is_abundant_number(n: float) -> bool:
        n = Calculator._as_int(n)
        if n < 1:
            return False
        return sum(d for d in Calculator.divisors_of(n) if d != n) > n

    @staticmethod
    def is_deficient_number(n: float) -> bool:
        n = Calculator._as_int(n)
        if n < 1:
            return False
        return sum(d for d in Calculator.divisors_of(n) if d != n) < n

    @staticmethod
    def goldbach_pair(n: float) -> tuple:
        """For an even n >= 4, return two primes (p1, p2) with p1 + p2 = n."""
        n = Calculator._as_int(n)
        if n < 4 or n % 2 != 0:
            raise ValueError("Goldbach requires an even integer >= 4.")
        primes = Calculator.primes_up_to(n)
        primes_set = set(primes)
        for p in primes:
            if (n - p) in primes_set:
                return (p, n - p)
        return None

    @staticmethod
    def twin_prime_pairs_up_to(n: float) -> list:
        n = Calculator._as_int(n)
        primes = Calculator.primes_up_to(n)
        primes_set = set(primes)
        return [(p, p + 2) for p in primes if (p + 2) in primes_set]

    # ═══════════════════════════════════════════════════════════════
    # ── Matrix Operations ──
    # ═══════════════════════════════════════════════════════════════
    @staticmethod
    def matrix_add(A: list, B: list) -> list:
        if not A or not B or len(A) != len(B) or any(len(ra) != len(rb) for ra, rb in zip(A, B)):
            raise ValueError("Matrices must have the same dimensions.")
        return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    @staticmethod
    def matrix_subtract(A: list, B: list) -> list:
        if not A or not B or len(A) != len(B) or any(len(ra) != len(rb) for ra, rb in zip(A, B)):
            raise ValueError("Matrices must have the same dimensions.")
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    @staticmethod
    def matrix_scalar_multiply(A: list, k: float) -> list:
        return [[k * v for v in row] for row in A]

    @staticmethod
    def matrix_multiply(A: list, B: list) -> list:
        if not A or not B or len(A[0]) != len(B):
            raise ValueError("Matrix dimensions do not match for multiplication.")
        return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
                for i in range(len(A))]

    @staticmethod
    def matrix_transpose(A: list) -> list:
        return [list(row) for row in zip(*A)]

    @staticmethod
    def matrix_trace(A: list) -> float:
        if len(A) != len(A[0]):
            raise ValueError("Trace requires a square matrix.")
        return sum(A[i][i] for i in range(len(A)))

    @staticmethod
    def matrix_identity(n: int) -> list:
        n = Calculator._as_int(n)
        return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    @staticmethod
    def matrix_zero(rows: int, cols: int) -> list:
        return [[0.0 for _ in range(cols)] for _ in range(rows)]

    @staticmethod
    def matrix_determinant(A: list) -> float:
        n = len(A)
        if any(len(row) != n for row in A):
            raise ValueError("Determinant requires a square matrix.")
        if n == 1:
            return A[0][0]
        if n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        det = 0.0
        for c in range(n):
            minor = [[A[r][cc] for cc in range(n) if cc != c] for r in range(1, n)]
            det += ((-1) ** c) * A[0][c] * Calculator.matrix_determinant(minor)
        return det

    @staticmethod
    def matrix_inverse(A: list) -> list:
        """Inverse via Gauss-Jordan elimination."""
        n = len(A)
        if any(len(row) != n for row in A):
            raise ValueError("Inverse requires a square matrix.")
        if Calculator.matrix_determinant(A) == 0:
            raise ValueError("Matrix is singular (not invertible).")
        M = [list(map(float, A[i])) + [1.0 if j == i else 0.0 for j in range(n)]
             for i in range(n)]
        for col in range(n):
            pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
            if abs(M[pivot][col]) < 1e-12:
                raise ValueError("Matrix is singular (not invertible).")
            M[col], M[pivot] = M[pivot], M[col]
            piv = M[col][col]
            for j in range(2 * n):
                M[col][j] /= piv
            for r in range(n):
                if r != col:
                    factor = M[r][col]
                    for j in range(2 * n):
                        M[r][j] -= factor * M[col][j]
        return [row[n:] for row in M]

    # ═══════════════════════════════════════════════════════════════
    # ── Advanced Statistics ──
    # ═══════════════════════════════════════════════════════════════
    @staticmethod
    def covariance(x: list, y: list, sample: bool = True) -> float:
        if len(x) != len(y):
            raise ValueError("Datasets must have equal length.")
        if len(x) < 2:
            raise ValueError("Need at least 2 data points.")
        mx, my = Calculator.mean(x), Calculator.mean(y)
        denom = len(x) - 1 if sample else len(x)
        return sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / denom

    @staticmethod
    def correlation(x: list, y: list) -> float:
        if len(x) != len(y):
            raise ValueError("Datasets must have equal length.")
        sx = Calculator.std_dev(x)
        sy = Calculator.std_dev(y)
        if sx == 0 or sy == 0:
            raise ValueError("Standard deviation is zero; correlation undefined.")
        return Calculator.covariance(x, y) / (sx * sy)

    @staticmethod
    def linear_regression(x: list, y: list) -> tuple:
        """Returns (slope, intercept) of best-fit line."""
        if len(x) != len(y) or len(x) < 2:
            raise ValueError("Need at least 2 (x, y) pairs.")
        n = len(x)
        mx, my = sum(x) / n, sum(y) / n
        num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
        den = sum((xi - mx) ** 2 for xi in x)
        if den == 0:
            raise ValueError("All x values are identical.")
        slope = num / den
        intercept = my - slope * mx
        return (slope, intercept)

    @staticmethod
    def percentile(data: list, p: float) -> float:
        if not 0 <= p <= 100:
            raise ValueError("Percentile must be in [0, 100].")
        if not data:
            raise ValueError("Empty data list.")
        s = sorted(data)
        if len(s) == 1:
            return s[0]
        k = (len(s) - 1) * (p / 100)
        f = int(k)
        c = k - f
        if f + 1 < len(s):
            return s[f] + c * (s[f + 1] - s[f])
        return s[f]

    @staticmethod
    def quartiles(data: list) -> tuple:
        if not data:
            raise ValueError("Empty data list.")
        return (Calculator.percentile(data, 25),
                Calculator.percentile(data, 50),
                Calculator.percentile(data, 75))

    @staticmethod
    def iqr(data: list) -> float:
        q1, _, q3 = Calculator.quartiles(data)
        return q3 - q1

    @staticmethod
    def z_score(x: float, mu: float, sigma: float) -> float:
        if sigma == 0:
            raise ValueError("Standard deviation cannot be zero.")
        return (x - mu) / sigma

    @staticmethod
    def binomial_pmf(k: float, n: float, p: float) -> float:
        if not 0 <= p <= 1:
            raise ValueError("Probability must be in [0, 1].")
        k, n = Calculator._as_int(k), Calculator._as_int(n)
        if k < 0 or n < 0 or k > n:
            return 0.0
        return Calculator.combinations(n, k) * (p ** k) * ((1 - p) ** (n - k))

    @staticmethod
    def binomial_cdf(k: float, n: float, p: float) -> float:
        k = Calculator._as_int(k)
        return sum(Calculator.binomial_pmf(i, n, p) for i in range(k + 1))

    @staticmethod
    def poisson_pmf(k: float, lam: float) -> float:
        if lam < 0:
            raise ValueError("Lambda must be non-negative.")
        k = Calculator._as_int(k)
        return math.exp(-lam) * (lam ** k) / math.factorial(k)

    @staticmethod
    def poisson_cdf(k: float, lam: float) -> float:
        k = Calculator._as_int(k)
        return sum(Calculator.poisson_pmf(i, lam) for i in range(k + 1))

    @staticmethod
    def skewness(data: list) -> float:
        if len(data) < 3:
            raise ValueError("Need at least 3 data points.")
        m = Calculator.mean(data)
        s = Calculator.std_dev(data, sample=False)
        if s == 0:
            raise ValueError("Standard deviation is zero.")
        n = len(data)
        return (n / ((n - 1) * (n - 2))) * sum(((x - m) / s) ** 3 for x in data)

    @staticmethod
    def kurtosis(data: list) -> float:
        if len(data) < 4:
            raise ValueError("Need at least 4 data points.")
        m = Calculator.mean(data)
        s = Calculator.std_dev(data, sample=False)
        if s == 0:
            raise ValueError("Standard deviation is zero.")
        n = len(data)
        return (n * (n + 1) / ((n - 1) * (n - 2) * (n - 3))) * \
               sum(((x - m) / s) ** 4 for x in data) - \
               (3 * (n - 1) ** 2) / ((n - 2) * (n - 3))

    @staticmethod
    def moving_average(data: list, window: int) -> list:
        if window <= 0:
            raise ValueError("Window must be positive.")
        if window > len(data):
            raise ValueError("Window larger than data length.")
        return [sum(data[i:i + window]) / window for i in range(len(data) - window + 1)]

    @staticmethod
    def exponential_moving_average(data: list, alpha: float) -> list:
        if not 0 < alpha <= 1:
            raise ValueError("Alpha must be in (0, 1].")
        ema = [data[0]]
        for x in data[1:]:
            ema.append(alpha * x + (1 - alpha) * ema[-1])
        return ema

    # ═══════════════════════════════════════════════════════════════
    # ── Calculus (Numerical) ──
    # ═══════════════════════════════════════════════════════════════
    @staticmethod
    def derivative(f, x: float, h: float = 1e-6) -> float:
        """Central difference derivative of f at x."""
        return (f(x + h) - f(x - h)) / (2 * h)

    @staticmethod
    def second_derivative(f, x: float, h: float = 1e-4) -> float:
        return (f(x + h) - 2 * f(x) + f(x - h)) / (h * h)

    @staticmethod
    def partial_derivative(f, x_vals: list, idx: int, h: float = 1e-6) -> float:
        """Partial derivative of f(x_vals) w.r.t. the idx-th variable."""
        x_plus = list(x_vals); x_plus[idx] += h
        x_minus = list(x_vals); x_minus[idx] -= h
        return (f(*x_plus) - f(*x_minus)) / (2 * h)

    @staticmethod
    def integral_trapezoidal(f, a: float, b: float, n: int = 1000) -> float:
        if n <= 0:
            raise ValueError("n must be positive.")
        h = (b - a) / n
        total = 0.5 * (f(a) + f(b))
        for i in range(1, n):
            total += f(a + i * h)
        return total * h

    @staticmethod
    def integral_simpson(f, a: float, b: float, n: int = 1000) -> float:
        if n <= 0 or n % 2 != 0:
            raise ValueError("n must be a positive even integer.")
        h = (b - a) / n
        total = f(a) + f(b)
        for i in range(1, n):
            x = a + i * h
            total += (4 if i % 2 else 2) * f(x)
        return total * h / 3

    @staticmethod
    def riemann_sum(f, a: float, b: float, n: int = 100, method: str = "left") -> float:
        if n <= 0:
            raise ValueError("n must be positive.")
        h = (b - a) / n
        if method == "left":
            return sum(f(a + i * h) for i in range(n)) * h
        if method == "right":
            return sum(f(a + (i + 1) * h) for i in range(n)) * h
        if method == "midpoint":
            return sum(f(a + (i + 0.5) * h) for i in range(n)) * h
        raise ValueError("method must be 'left', 'right', or 'midpoint'.")

    @staticmethod
    def limit(f, x: float, side: str = "both", h: float = 1e-6) -> float:
        if side == "left":
            return f(x - h)
        if side == "right":
            return f(x + h)
        if side == "both":
            left, right = f(x - h), f(x + h)
            if abs(left - right) > 1e-3:
                raise ValueError("Two-sided limit does not appear to exist.")
            return (left + right) / 2
        raise ValueError("side must be 'both', 'left', or 'right'.")

    @staticmethod
    def newton_raphson(f, df, x0: float, tol: float = 1e-10, max_iter: int = 50) -> float:
        x = x0
        for _ in range(max_iter):
            fx = f(x)
            if abs(fx) < tol:
                return x
            dfx = df(x)
            if dfx == 0:
                raise ValueError("Derivative is zero; Newton-Raphson failed.")
            x = x - fx / dfx
        raise ValueError("Newton-Raphson did not converge.")

    # ═══════════════════════════════════════════════════════════════
    # ── Physics Extended ──
    # ═══════════════════════════════════════════════════════════════
    @staticmethod
    def force(mass: float, acceleration: float) -> float:
        return mass * acceleration

    @staticmethod
    def momentum(mass: float, velocity: float) -> float:
        return mass * velocity

    @staticmethod
    def impulse(force: float, time: float) -> float:
        return force * time

    @staticmethod
    def work(force: float, distance: float, angle_deg: float = 0) -> float:
        return force * distance * math.cos(math.radians(angle_deg))

    @staticmethod
    def power_mech(work: float, time: float) -> float:
        if time == 0:
            raise ZeroDivisionError("Time cannot be zero.")
        return work / time

    @staticmethod
    def gravitational_force(m1: float, m2: float, r: float) -> float:
        if r <= 0:
            raise ValueError("Distance must be positive.")
        return Calculator.GRAVITATIONAL_CONSTANT * m1 * m2 / (r ** 2)

    @staticmethod
    def wavelength(frequency: float) -> float:
        if frequency == 0:
            raise ZeroDivisionError("Frequency cannot be zero.")
        return Calculator.SPEED_OF_LIGHT / frequency

    @staticmethod
    def frequency_from_wavelength(wavelength: float) -> float:
        if wavelength == 0:
            raise ZeroDivisionError("Wavelength cannot be zero.")
        return Calculator.SPEED_OF_LIGHT / wavelength

    @staticmethod
    def photon_energy(frequency: float) -> float:
        return Calculator.PLANCK_CONSTANT * frequency

    @staticmethod
    def photon_wavelength_from_energy(energy: float) -> float:
        if energy == 0:
            raise ZeroDivisionError("Energy cannot be zero.")
        return (Calculator.PLANCK_CONSTANT * Calculator.SPEED_OF_LIGHT) / energy

    @staticmethod
    def centripetal_acceleration(velocity: float, radius: float) -> float:
        if radius == 0:
            raise ZeroDivisionError("Radius cannot be zero.")
        return velocity ** 2 / radius

    @staticmethod
    def centripetal_force(mass: float, velocity: float, radius: float) -> float:
        return mass * Calculator.centripetal_acceleration(velocity, radius)

    @staticmethod
    def torque(force: float, lever_arm: float, angle_deg: float = 90) -> float:
        return force * lever_arm * math.sin(math.radians(angle_deg))

    @staticmethod
    def angular_velocity(angle_rad: float, time: float) -> float:
        if time == 0:
            raise ZeroDivisionError("Time cannot be zero.")
        return angle_rad / time

    @staticmethod
    def escape_velocity(mass: float, radius: float) -> float:
        if radius <= 0:
            raise ValueError("Radius must be positive.")
        return math.sqrt(2 * Calculator.GRAVITATIONAL_CONSTANT * mass / radius)

    @staticmethod
    def pendulum_period(length: float, g: float = 9.81) -> float:
        if length < 0:
            raise ValueError("Length cannot be negative.")
        return 2 * math.pi * math.sqrt(length / g)

    @staticmethod
    def doppler_effect(f_source: float, v_observer: float, v_source: float,
                       v_medium: float = 343.0, approach: bool = True) -> float:
        sign = 1 if approach else -1
        return f_source * (v_medium + sign * v_observer) / (v_medium - sign * v_source)

    @staticmethod
    def heat_transfer(mass: float, specific_heat: float, delta_temp: float) -> float:
        return mass * specific_heat * delta_temp

    @staticmethod
    def specific_heat_capacity(heat: float, mass: float, delta_temp: float) -> float:
        if mass == 0 or delta_temp == 0:
            raise ValueError("Mass and temperature change cannot be zero.")
        return heat / (mass * delta_temp)

    @staticmethod
    def ideal_gas_pressure(n: float, T: float, V: float) -> float:
        if V <= 0:
            raise ValueError("Volume must be positive.")
        if T < 0:
            raise ValueError("Temperature cannot be negative (Kelvin).")
        return n * Calculator.GAS_CONSTANT * T / V

    @staticmethod
    def ideal_gas_volume(n: float, T: float, P: float) -> float:
        if P <= 0:
            raise ValueError("Pressure must be positive.")
        return n * Calculator.GAS_CONSTANT * T / P

    @staticmethod
    def ideal_gas_temperature(P: float, V: float, n: float) -> float:
        if n <= 0:
            raise ValueError("Moles must be positive.")
        if V <= 0:
            raise ValueError("Volume must be positive.")
        return P * V / (n * Calculator.GAS_CONSTANT)

    @staticmethod
    def snell_law(theta1_deg: float, n1: float, n2: float):
        """Returns theta2 in degrees, or None for total internal reflection."""
        theta1 = math.radians(theta1_deg)
        sin_t2 = (n1 / n2) * math.sin(theta1)
        if abs(sin_t2) > 1:
            return None
        return math.degrees(math.asin(sin_t2))

    # ═══════════════════════════════════════════════════════════════
    # ── Chemistry ──
    # ═══════════════════════════════════════════════════════════════
    ELEMENT_MASSES = {
        'H': 1.008, 'He': 4.0026, 'Li': 6.94, 'Be': 9.0122, 'B': 10.81, 'C': 12.011,
        'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180, 'Na': 22.990, 'Mg': 24.305,
        'Al': 26.982, 'Si': 28.085, 'P': 30.974, 'S': 32.06, 'Cl': 35.45, 'Ar': 39.948,
        'K': 39.098, 'Ca': 40.078, 'Sc': 44.956, 'Ti': 47.867, 'V': 50.942, 'Cr': 51.996,
        'Mn': 54.938, 'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.38,
        'Ga': 69.723, 'Ge': 72.63, 'As': 74.922, 'Se': 78.971, 'Br': 79.904, 'Kr': 83.798,
        'Rb': 85.468, 'Sr': 87.62, 'Y': 88.906, 'Zr': 91.224, 'Nb': 92.906, 'Mo': 95.95,
        'Tc': 98.0, 'Ru': 101.07, 'Rh': 102.91, 'Pd': 106.42, 'Ag': 107.87, 'Cd': 112.41,
        'In': 114.82, 'Sn': 118.71, 'Sb': 121.76, 'Te': 127.60, 'I': 126.90, 'Xe': 131.29,
        'Cs': 132.91, 'Ba': 137.33, 'La': 138.91, 'Ce': 140.12, 'Pr': 140.91, 'Nd': 144.24,
        'W': 183.84, 'Re': 186.21, 'Os': 190.23, 'Ir': 192.22, 'Pt': 195.08, 'Au': 196.97,
        'Hg': 200.59, 'Tl': 204.38, 'Pb': 207.2, 'Bi': 208.98, 'Rn': 222.0, 'Ra': 226.0,
        'U': 238.03,
    }

    @staticmethod
    def _element_mass(symbol: str) -> float:
        if symbol not in Calculator.ELEMENT_MASSES:
            raise ValueError(f"Unknown element symbol: {symbol}")
        return Calculator.ELEMENT_MASSES[symbol]

    @staticmethod
    def _parse_formula_segment(s: str, i: int) -> tuple:
        """Recursive descent parser for chemical formulas. Returns (mass, next_i)."""
        mass = 0.0
        elem = ''
        while i < len(s):
            ch = s[i]
            if ch == '(':
                if elem:
                    mass += Calculator._element_mass(elem)
                    elem = ''
                sub, i = Calculator._parse_formula_segment(s, i + 1)
                if i >= len(s) or s[i] != ')':
                    raise ValueError("Unbalanced parentheses in formula.")
                i += 1
                count_str = ''
                while i < len(s) and s[i].isdigit():
                    count_str += s[i]
                    i += 1
                count = int(count_str) if count_str else 1
                mass += sub * count
            elif ch == ')':
                break
            elif ch.isupper():
                if elem:
                    mass += Calculator._element_mass(elem)
                elem = ch
                i += 1
            elif ch.islower():
                elem += ch
                i += 1
            elif ch.isdigit():
                count_str = ch
                i += 1
                while i < len(s) and s[i].isdigit():
                    count_str += s[i]
                    i += 1
                if not elem:
                    raise ValueError("Digit with no preceding element in formula.")
                mass += Calculator._element_mass(elem) * int(count_str)
                elem = ''
            else:
                raise ValueError(f"Invalid character {ch!r} in formula.")
        if elem:
            mass += Calculator._element_mass(elem)
        return mass, i

    @staticmethod
    def molar_mass(formula: str) -> float:
        """Compute molar mass (g/mol). Supports 'H2O', 'Ca(OH)2', 'H2SO4', etc."""
        if not formula:
            raise ValueError("Empty formula.")
        mass, idx = Calculator._parse_formula_segment(formula, 0)
        if idx != len(formula):
            raise ValueError(f"Invalid formula: {formula}")
        return mass

    @staticmethod
    def moles(mass_g: float, molar_mass_g_per_mol: float) -> float:
        if molar_mass_g_per_mol == 0:
            raise ZeroDivisionError("Molar mass cannot be zero.")
        return mass_g / molar_mass_g_per_mol

    @staticmethod
    def mass_from_moles(moles: float, molar_mass_g_per_mol: float) -> float:
        return moles * molar_mass_g_per_mol

    @staticmethod
    def molarity(moles_solute: float, volume_l: float) -> float:
        if volume_l <= 0:
            raise ValueError("Volume must be positive.")
        return moles_solute / volume_l

    @staticmethod
    def moles_from_molarity(molarity_M: float, volume_l: float) -> float:
        return molarity_M * volume_l

    @staticmethod
    def ph(h_concentration: float) -> float:
        if h_concentration <= 0:
            raise ValueError("Concentration must be positive.")
        return -math.log10(h_concentration)

    @staticmethod
    def ph_to_h(ph_value: float) -> float:
        return 10 ** (-ph_value)

    @staticmethod
    def poh(oh_concentration: float) -> float:
        if oh_concentration <= 0:
            raise ValueError("Concentration must be positive.")
        return -math.log10(oh_concentration)

    @staticmethod
    def poh_to_oh(poh_value: float) -> float:
        return 10 ** (-poh_value)

    @staticmethod
    def dilution(c1=None, v1=None, c2=None, v2=None) -> float:
        """M1V1 = M2V2. Provide three; returns the missing one."""
        provided = sum(x is not None for x in (c1, v1, c2, v2))
        if provided != 3:
            raise ValueError("Provide exactly three of c1, v1, c2, v2.")
        if c1 is None:
            return c2 * v2 / v1
        if v1 is None:
            return c2 * v2 / c1
        if c2 is None:
            return c1 * v1 / v2
        return c1 * v1 / c2

    @staticmethod
    def percent_mass_concentration(mass_solute: float, mass_solution: float) -> float:
        if mass_solution == 0:
            raise ZeroDivisionError("Total mass cannot be zero.")
        return (mass_solute / mass_solution) * 100

    @staticmethod
    def half_life_remaining(initial_amount: float, half_life: float, time_elapsed: float) -> float:
        if half_life == 0:
            raise ZeroDivisionError("Half-life cannot be zero.")
        return initial_amount * (0.5 ** (time_elapsed / half_life))

    @staticmethod
    def half_life_from_decay(initial_amount: float, remaining_amount: float, time_elapsed: float) -> float:
        if remaining_amount <= 0 or initial_amount <= 0:
            raise ValueError("Amounts must be positive.")
        if remaining_amount >= initial_amount:
            raise ValueError("Remaining amount must be less than initial.")
        return time_elapsed / math.log2(initial_amount / remaining_amount)

    @staticmethod
    def boyle_law(p1=None, v1=None, p2=None, v2=None) -> float:
        """P1V1 = P2V2 (isothermal). Provide three; return the missing one."""
        provided = sum(x is not None for x in (p1, v1, p2, v2))
        if provided != 3:
            raise ValueError("Provide exactly three values.")
        if p1 is None:
            return p2 * v2 / v1
        if v1 is None:
            return p2 * v2 / p1
        if p2 is None:
            return p1 * v1 / v2
        return p1 * v1 / p2

    @staticmethod
    def charles_law(v1=None, t1=None, v2=None, t2=None) -> float:
        """V1/T1 = V2/T2 (isobaric). Provide three; return the missing one."""
        provided = sum(x is not None for x in (v1, t1, v2, t2))
        if provided != 3:
            raise ValueError("Provide exactly three values.")
        if v1 is None:
            return v2 * t1 / t2
        if t1 is None:
            return v1 * t2 / v2
        if v2 is None:
            return v1 * t2 / t1
        return v1 * t1 / v2

    # ═══════════════════════════════════════════════════════════════
    # ── Electronics ──
    # ═══════════════════════════════════════════════════════════════
    @staticmethod
    def electrical_power_vi(voltage: float, current: float) -> float:
        return voltage * current

    @staticmethod
    def electrical_power_i2r(current: float, resistance: float) -> float:
        return current ** 2 * resistance

    @staticmethod
    def electrical_power_v2r(voltage: float, resistance: float) -> float:
        if resistance == 0:
            raise ZeroDivisionError("Resistance cannot be zero.")
        return voltage ** 2 / resistance

    @staticmethod
    def resistance_series(resistances: list) -> float:
        return sum(resistances)

    @staticmethod
    def resistance_parallel(resistances: list) -> float:
        if not resistances:
            raise ValueError("At least one resistance required.")
        if any(r == 0 for r in resistances):
            return 0.0
        return 1 / sum(1 / r for r in resistances)

    @staticmethod
    def capacitance_series(capacitances: list) -> float:
        if not capacitances:
            raise ValueError("At least one capacitance required.")
        if any(c == 0 for c in capacitances):
            return 0.0
        return 1 / sum(1 / c for c in capacitances)

    @staticmethod
    def capacitance_parallel(capacitances: list) -> float:
        return sum(capacitances)

    @staticmethod
    def inductance_series(inductances: list) -> float:
        return sum(inductances)

    @staticmethod
    def inductance_parallel(inductances: list) -> float:
        if not inductances:
            raise ValueError("At least one inductance required.")
        if any(l == 0 for l in inductances):
            return 0.0
        return 1 / sum(1 / l for l in inductances)

    @staticmethod
    def reactance_capacitive(frequency: float, capacitance: float) -> float:
        if frequency == 0 or capacitance == 0:
            raise ZeroDivisionError("Frequency and capacitance must be non-zero.")
        return 1 / (2 * math.pi * frequency * capacitance)

    @staticmethod
    def reactance_inductive(frequency: float, inductance: float) -> float:
        return 2 * math.pi * frequency * inductance

    @staticmethod
    def resonant_frequency_lc(inductance: float, capacitance: float) -> float:
        if inductance <= 0 or capacitance <= 0:
            raise ValueError("Inductance and capacitance must be positive.")
        return 1 / (2 * math.pi * math.sqrt(inductance * capacitance))

    @staticmethod
    def time_constant_rc(resistance: float, capacitance: float) -> float:
        return resistance * capacitance

    @staticmethod
    def time_constant_rl(inductance: float, resistance: float) -> float:
        if resistance == 0:
            raise ZeroDivisionError("Resistance cannot be zero.")
        return inductance / resistance

    @staticmethod
    def decibel_power(p2: float, p1: float) -> float:
        if p1 <= 0:
            raise ValueError("Reference power must be positive.")
        return 10 * math.log10(p2 / p1)

    @staticmethod
    def decibel_voltage(v2: float, v1: float) -> float:
        if v1 <= 0:
            raise ValueError("Reference voltage must be positive.")
        return 20 * math.log10(v2 / v1)

    @staticmethod
    def voltage_divider(vin: float, r1: float, r2: float) -> float:
        """Vout across R2 in a series R1-R2 divider."""
        if r1 + r2 == 0:
            raise ZeroDivisionError("Total resistance cannot be zero.")
        return vin * r2 / (r1 + r2)

    @staticmethod
    def current_divider(itotal: float, r1: float, r2: float) -> float:
        """Current through R2 in a parallel R1-R2 divider."""
        if r1 + r2 == 0:
            raise ZeroDivisionError("Total resistance cannot be zero.")
        return itotal * r1 / (r1 + r2)

    @staticmethod
    def rms_to_peak(rms: float) -> float:
        return rms * math.sqrt(2)

    @staticmethod
    def peak_to_rms(peak: float) -> float:
        return peak / math.sqrt(2)

    @staticmethod
    def frequency_from_period(period: float) -> float:
        if period == 0:
            raise ZeroDivisionError("Period cannot be zero.")
        return 1 / period

    @staticmethod
    def period_from_frequency(frequency: float) -> float:
        if frequency == 0:
            raise ZeroDivisionError("Frequency cannot be zero.")
        return 1 / frequency

    @staticmethod
    def wheatstone_bridge_balanced(r1: float, r2: float, r3: float, r4: float) -> bool:
        return abs(r1 * r3 - r2 * r4) < 1e-9

    # ═══════════════════════════════════════════════════════════════
    # ── Programmer: Number Bases ──
    # ═══════════════════════════════════════════════════════════════
    @staticmethod
    def to_hex(n) -> str:
        return hex(Calculator._as_int(n))

    @staticmethod
    def to_binary(n) -> str:
        return bin(Calculator._as_int(n))

    @staticmethod
    def to_octal(n) -> str:
        return oct(Calculator._as_int(n))

    @staticmethod
    def from_hex(s: str) -> int:
        return int(s, 16)

    @staticmethod
    def from_binary(s: str) -> int:
        return int(s, 2)

    @staticmethod
    def from_octal(s: str) -> int:
        return int(s, 8)

    @staticmethod
    def base_convert(s: str, from_base: int, to_base: int) -> str:
        if not (2 <= from_base <= 36) or not (2 <= to_base <= 36):
            raise ValueError("Bases must be in range [2, 36].")
        neg = s.strip().startswith('-')
        n = int(s, from_base)
        if n == 0:
            return "0"
        digits = "0123456789abcdefghijklmnopqrstuvwxyz"
        result = ""
        n_abs = abs(n)
        while n_abs > 0:
            result = digits[n_abs % to_base] + result
            n_abs //= to_base
        return ("-" + result) if neg else result

    # ═══════════════════════════════════════════════════════════════
    # ── Programmer: Bitwise ──
    # ═══════════════════════════════════════════════════════════════
    @staticmethod
    def bit_and(a, b) -> int:
        return Calculator._as_int(a) & Calculator._as_int(b)

    @staticmethod
    def bit_or(a, b) -> int:
        return Calculator._as_int(a) | Calculator._as_int(b)

    @staticmethod
    def bit_xor(a, b) -> int:
        return Calculator._as_int(a) ^ Calculator._as_int(b)

    @staticmethod
    def bit_not(a) -> int:
        return ~Calculator._as_int(a)

    @staticmethod
    def bit_lshift(a, n) -> int:
        return Calculator._as_int(a) << Calculator._as_int(n)

    @staticmethod
    def bit_rshift(a, n) -> int:
        return Calculator._as_int(a) >> Calculator._as_int(n)

    @staticmethod
    def count_set_bits(n) -> int:
        return bin(Calculator._as_int(n)).count('1')

    @staticmethod
    def is_power_of_two(n) -> bool:
        n = Calculator._as_int(n)
        return n > 0 and (n & (n - 1)) == 0

    # ═══════════════════════════════════════════════════════════════
    # ── Programmer: ASCII & Unicode ──
    # ═══════════════════════════════════════════════════════════════
    @staticmethod
    def ascii_to_char(n) -> str:
        n = Calculator._as_int(n)
        if not 0 <= n <= 127:
            raise ValueError("ASCII code must be in [0, 127].")
        return chr(n)

    @staticmethod
    def char_to_ascii(c: str) -> int:
        if len(c) != 1:
            raise ValueError("Input must be a single character.")
        o = ord(c)
        if not 0 <= o <= 127:
            raise ValueError("Character is not ASCII.")
        return o

    @staticmethod
    def string_to_ascii_codes(s: str) -> list:
        return [Calculator.char_to_ascii(c) for c in s]

    @staticmethod
    def ascii_codes_to_string(codes: list) -> str:
        return ''.join(Calculator.ascii_to_char(c) for c in codes)

    @staticmethod
    def unicode_to_char(n) -> str:
        return chr(Calculator._as_int(n))

    @staticmethod
    def char_to_unicode(c: str) -> int:
        if len(c) != 1:
            raise ValueError("Input must be a single character.")
        return ord(c)

    @staticmethod
    def string_to_unicode_codes(s: str) -> list:
        return [ord(c) for c in s]

    @staticmethod
    def unicode_codes_to_string(codes: list) -> str:
        return ''.join(chr(c) for c in codes)

    # ═══════════════════════════════════════════════════════════════
    # ── Programmer: Base64 ──
    # ═══════════════════════════════════════════════════════════════
    @staticmethod
    def encode_base64(s) -> str:
        if isinstance(s, str):
            s = s.encode('utf-8')
        return base64.b64encode(s).decode('ascii')

    @staticmethod
    def decode_base64(s: str):
        decoded = base64.b64decode(s)
        try:
            return decoded.decode('utf-8')
        except UnicodeDecodeError:
            return decoded

    # ═══════════════════════════════════════════════════════════════
    # ── Programmer: Hashing ──
    # ═══════════════════════════════════════════════════════════════
    @staticmethod
    def _to_bytes(s):
        return s.encode('utf-8') if isinstance(s, str) else s

    @staticmethod
    def md5(s) -> str:
        return hashlib.md5(Calculator._to_bytes(s)).hexdigest()

    @staticmethod
    def sha1(s) -> str:
        return hashlib.sha1(Calculator._to_bytes(s)).hexdigest()

    @staticmethod
    def sha256(s) -> str:
        return hashlib.sha256(Calculator._to_bytes(s)).hexdigest()

    @staticmethod
    def sha512(s) -> str:
        return hashlib.sha512(Calculator._to_bytes(s)).hexdigest()

    @staticmethod
    def sha3_256(s) -> str:
        return hashlib.sha3_256(Calculator._to_bytes(s)).hexdigest()

    @staticmethod
    def blake2b(s) -> str:
        return hashlib.blake2b(Calculator._to_bytes(s)).hexdigest()

    @staticmethod
    def blake2s(s) -> str:
        return hashlib.blake2s(Calculator._to_bytes(s)).hexdigest()