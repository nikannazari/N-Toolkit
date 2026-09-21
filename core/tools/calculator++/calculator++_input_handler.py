"""
calculator++_input_handler.py - CLI interface for Calculator++.
"""

import importlib.util
import os

from colorama import Fore, Style
import pyfiglet


TOOL_NAME = "calculator++"


def load_calculator():
    """Dynamically load the Calculator++ core module."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    calculator_file = os.path.join(current_dir, "calculator++.py")

    spec = importlib.util.spec_from_file_location("calculator_core", calculator_file)
    if spec is None or spec.loader is None:
        raise ImportError("Could not load calculator++.py")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Calculator


# ═══════════════════════════════════════════════════════════════
# Helper utilities
# ═══════════════════════════════════════════════════════════════

def _is_deg(args):
    """Return True if the last arg signals degree mode for trig functions."""
    return len(args) > 1 and args[-1].lower() in ("deg", "degrees", "d")


def _parse_matrix(args):
    """Parse a matrix from CLI args.

    Each arg is a comma-separated row.
    Example:  ['1,2', '3,4']  ->  [[1.0, 2.0], [3.0, 4.0]]
    """
    if not args:
        raise ValueError("Matrix requires at least one row (e.g. 1,2 3,4).")
    matrix = []
    for row_str in args:
        row = [float(x) for x in row_str.split(',')]
        matrix.append(row)
    n = len(matrix[0])
    for row in matrix:
        if len(row) != n:
            raise ValueError("All rows must have the same number of columns.")
    return matrix


def _two_list(method, args):
    """Call a method that takes two lists, separated by '|' in args.

    Example:  cov 1 2 3 | 4 5 6  ->  method([1, 2, 3], [4, 5, 6])
    """
    if '|' not in args:
        raise ValueError("Use '|' to separate x and y. Example: cov 1 2 3 | 4 5 6")
    idx = args.index('|')
    x = [float(v) for v in args[:idx]]
    y = [float(v) for v in args[idx + 1:]]
    if not x or not y:
        raise ValueError("Both lists must be non-empty.")
    return method(x, y)


def _print_result(result):
    """Pretty-print the result of a command."""
    if isinstance(result, list) and result and isinstance(result[0], list):
        print(f"{Fore.GREEN}  Result:{Style.RESET_ALL}")
        for row in result:
            print(f"    {Fore.CYAN}{row}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}  Result: {result}{Style.RESET_ALL}")


# ═══════════════════════════════════════════════════════════════
# Command categories
# ═══════════════════════════════════════════════════════════════

CONSTANTS = [
    "PI", "E", "GOLDEN_RATIO", "SPEED_OF_LIGHT", "GRAVITATIONAL_CONSTANT",
    "PLANCK_CONSTANT", "BOLTZMANN_CONSTANT", "AVOGADRO_NUMBER",
    "ELECTRON_MASS", "PROTON_MASS", "NEUTRON_MASS", "ELEMENTARY_CHARGE",
    "GAS_CONSTANT",
]

# Commands not supported in CLI mode (require callables or two matrices)
UNSUPPORTED_CLI = {
    "derivative", "second_derivative", "partial_derivative",
    "integral_trapezoidal", "integral_simpson", "riemann_sum",
    "limit", "newton_raphson",
    "matrix_add", "matrix_subtract", "matrix_scalar_multiply", "matrix_multiply",
}

# Commands that take a single list of floats
LIST_COMMANDS = {
    "mean", "median", "mode", "var", "std", "min", "max", "sum", "prod",
    "geomean", "harmmean", "range", "quartiles", "iqr", "skewness", "kurtosis",
    "resistance_series", "resistance_parallel",
    "cap_series", "cap_parallel", "ind_series", "ind_parallel",
}

# Commands that take raw string args (no float parsing)
STRING_COMMANDS = {
    "molar_mass", "from_hex", "from_bin", "from_oct",
    "char_to_ascii", "char_to_uni",
    "str_to_ascii", "str_to_uni",
    "b64_enc", "b64_dec",
    "md5", "sha1", "sha256", "sha512", "sha3_256", "blake2b", "blake2s",
}

# Commands that take integer args
INT_COMMANDS = {
    "to_hex", "to_bin", "to_oct",
    "bit_and", "bit_or", "bit_xor", "bit_not",
    "lshift", "rshift", "count_bits", "is_pow2",
    "ascii_to_char", "unicode_to_char",
}

# Maps CLI command -> Calculator method name (for non-special commands)
CMD_MAP = {
    # Basic
    "add": "add", "sub": "subtract", "mul": "multiply", "div": "divide",
    # Roots & rounding
    "sqrt": "sqrt", "power": "power", "fact": "factorial",
    "cbrt": "cube_root", "abs": "abs_val", "floor": "floor",
    "ceil": "ceiling", "mod": "mod", "nth_root": "nth_root",
    # Hyperbolic (no degrees option)
    "sinh": "sinh", "cosh": "cosh", "tanh": "tanh",
    "asinh": "asinh", "acosh": "acosh", "atanh": "atanh",
    # Logarithms & exponentials (log is special)
    "ln": "ln", "log2": "log2", "exp": "exp",
    # Angle conversion
    "deg2rad": "deg_to_rad", "rad2deg": "rad_to_deg",
    # Number theory & primes
    "gcd": "gcd", "lcm": "lcm", "is_prime": "is_prime",
    "prime_factors": "prime_factors", "next_prime": "next_prime",
    "prev_prime": "prev_prime", "primes_up_to": "primes_up_to",
    "prime_count": "prime_count", "nth_prime": "nth_prime",
    "is_coprime": "is_coprime", "euler_totient": "euler_totient",
    "divisors_of": "divisors_of", "divisor_count": "divisor_count",
    "sum_of_divisors": "sum_of_divisors",
    "is_perfect": "is_perfect_number", "is_abundant": "is_abundant_number",
    "is_deficient": "is_deficient_number",
    "goldbach": "goldbach_pair", "twin_primes": "twin_prime_pairs_up_to",
    "fibonacci": "fibonacci", "is_even": "is_even", "is_odd": "is_odd",
    "permutations": "permutations", "combinations": "combinations",
    # Statistics - list-of-floats
    "mean": "mean", "median": "median", "mode": "mode",
    "var": "variance", "std": "std_dev",
    "min": "minimum", "max": "maximum", "sum": "sum_of", "prod": "product_of",
    "geomean": "geometric_mean", "harmmean": "harmonic_mean",
    "range": "range_of",
    "quartiles": "quartiles", "iqr": "iqr",
    "skewness": "skewness", "kurtosis": "kurtosis",
    # Statistics - simple float args
    "z_score": "z_score",
    "binomial_pmf": "binomial_pmf", "binomial_cdf": "binomial_cdf",
    "poisson_pmf": "poisson_pmf", "poisson_cdf": "poisson_cdf",
    # Geometry (2D)
    "area_circle": "area_circle", "circumference": "circumference",
    "area_rectangle": "area_rectangle", "perimeter_rectangle": "perimeter_rectangle",
    "area_triangle": "area_triangle", "area_triangle_sss": "area_triangle_sss",
    "area_trapezoid": "area_trapezoid",
    "distance_2d": "distance_2d", "midpoint_2d": "midpoint_2d",
    "slope_2d": "slope_2d",
    # Geometry (3D)
    "volume_sphere": "volume_sphere", "surface_area_sphere": "surface_area_sphere",
    "volume_cylinder": "volume_cylinder", "volume_cone": "volume_cone",
    "volume_cube": "volume_cube", "volume_rect_prism": "volume_rect_prism",
    "volume_pyramid": "volume_pyramid",
    # Equations & finance
    "eq1": "solve_linear_eq", "quad": "solve_quadratic_eq",
    "eq2": "solve_linear_eq2",
    "percentage": "percentage", "pct_change": "percentage_change",
    "simple_interest": "simple_interest", "compound_interest": "compound_interest",
    # Physics conversions
    "c2f": "celsius_to_fahrenheit", "f2c": "fahrenheit_to_celsius",
    "c2k": "celsius_to_kelvin", "k2c": "kelvin_to_celsius",
    "ke": "kinetic_energy", "kinetic_energy": "kinetic_energy",
    "pe": "potential_energy", "potential_energy": "potential_energy",
    "density": "density", "pressure": "pressure", "bmi": "bmi", "speed": "speed",
    # Physics extended
    "force": "force", "momentum": "momentum", "impulse": "impulse",
    "work": "work", "power_mech": "power_mech",
    "g_force": "gravitational_force",
    "wavelength": "wavelength", "freq_from_wavelength": "frequency_from_wavelength",
    "photon_energy": "photon_energy",
    "photon_wavelength": "photon_wavelength_from_energy",
    "a_centripetal": "centripetal_acceleration",
    "f_centripetal": "centripetal_force",
    "torque": "torque", "omega": "angular_velocity", "v_escape": "escape_velocity",
    "heat_transfer": "heat_transfer", "c_specific": "specific_heat_capacity",
    "p_ideal": "ideal_gas_pressure", "v_ideal": "ideal_gas_volume",
    "t_ideal": "ideal_gas_temperature", "snell": "snell_law",
    # Pythagoras
    "pythag_hyp": "pythagorean_hypotenuse", "pythag_leg": "pythagorean_leg",
    # Chemistry
    "molar_mass": "molar_mass", "moles": "moles",
    "mass_from_moles": "mass_from_moles", "molarity": "molarity",
    "moles_from_molarity": "moles_from_molarity",
    "ph": "ph", "ph_to_h": "ph_to_h", "poh": "poh", "poh_to_oh": "poh_to_oh",
    "pct_mass_conc": "percent_mass_concentration",
    "half_life": "half_life_remaining", "half_life_decay": "half_life_from_decay",
    # Electronics
    "pow_vi": "electrical_power_vi", "pow_i2r": "electrical_power_i2r",
    "pow_v2r": "electrical_power_v2r",
    "resistance_series": "resistance_series",
    "resistance_parallel": "resistance_parallel",
    "cap_series": "capacitance_series", "cap_parallel": "capacitance_parallel",
    "ind_series": "inductance_series", "ind_parallel": "inductance_parallel",
    "xc": "reactance_capacitive", "xl": "reactance_inductive",
    "res_freq": "resonant_frequency_lc",
    "tau_rc": "time_constant_rc", "tau_rl": "time_constant_rl",
    "db_power": "decibel_power", "db_voltage": "decibel_voltage",
    "vdiv": "voltage_divider", "idiv": "current_divider",
    "rms2peak": "rms_to_peak", "peak2rms": "peak_to_rms",
    "freq": "frequency_from_period", "period": "period_from_frequency",
    "wheatstone": "wheatstone_bridge_balanced",
    # Programmer - number bases
    "to_hex": "to_hex", "to_bin": "to_binary", "to_oct": "to_octal",
    "from_hex": "from_hex", "from_bin": "from_binary", "from_oct": "from_octal",
    # Programmer - bitwise
    "bit_and": "bit_and", "bit_or": "bit_or", "bit_xor": "bit_xor",
    "bit_not": "bit_not", "lshift": "bit_lshift", "rshift": "bit_rshift",
    "count_bits": "count_set_bits", "is_pow2": "is_power_of_two",
    # Programmer - ASCII/Unicode
    "ascii_to_char": "ascii_to_char",
    "char_to_ascii": "char_to_ascii",
    "str_to_ascii": "string_to_ascii_codes",
    "ascii_to_str": "ascii_codes_to_string",
    "unicode_to_char": "unicode_to_char",
    "char_to_uni": "char_to_unicode",
    "str_to_uni": "string_to_unicode_codes",
    "uni_to_str": "unicode_codes_to_string",
    # Programmer - Base64
    "b64_enc": "encode_base64", "b64_dec": "decode_base64",
    # Programmer - Hash
    "md5": "md5", "sha1": "sha1", "sha256": "sha256", "sha512": "sha512",
    "sha3_256": "sha3_256", "blake2b": "blake2b", "blake2s": "blake2s",
}


# ═══════════════════════════════════════════════════════════════
# Special handlers (commands that need custom argument parsing)
# ═══════════════════════════════════════════════════════════════

def _trig_factory(method_name):
    """Create a trig handler with optional 'deg' suffix."""
    def handler(c, a):
        if not a:
            raise ValueError(f"Usage: {method_name} <x> [deg]")
        return getattr(c, method_name)(float(a[0]), degrees=_is_deg(a))
    return handler


def _log_handler(c, a):
    if not a:
        raise ValueError("Usage: log <x> [base]")
    if len(a) == 1:
        return c.log(float(a[0]))
    return c.log(float(a[0]), float(a[1]))


def _normal_factory(method_name):
    def handler(c, a):
        if not a:
            raise ValueError(f"Usage: {method_name} <x> [mu] [sigma]")
        x = float(a[0])
        if len(a) == 1:
            return getattr(c, method_name)(x)
        if len(a) == 2:
            return getattr(c, method_name)(x, float(a[1]))
        return getattr(c, method_name)(x, float(a[1]), float(a[2]))
    return handler


def _pendulum_handler(c, a):
    if not a:
        raise ValueError("Usage: t_pendulum <length> [g]")
    if len(a) == 1:
        return c.pendulum_period(float(a[0]))
    return c.pendulum_period(float(a[0]), float(a[1]))


def _round_handler(c, a):
    if not a:
        raise ValueError("Usage: round <x> [digits]")
    if len(a) == 1:
        return c.round_num(float(a[0]))
    return c.round_num(float(a[0]), int(float(a[1])))


def _percentile_handler(c, a):
    if len(a) < 2:
        raise ValueError("Usage: percentile <nums...> <p>")
    data = [float(x) for x in a[:-1]]
    p = float(a[-1])
    return c.percentile(data, p)


def _mov_avg_handler(c, a):
    if len(a) < 2:
        raise ValueError("Usage: mov_avg <nums...> <window>")
    data = [float(x) for x in a[:-1]]
    window = int(float(a[-1]))
    return c.moving_average(data, window)


def _ema_handler(c, a):
    if len(a) < 2:
        raise ValueError("Usage: ema <nums...> <alpha>")
    data = [float(x) for x in a[:-1]]
    alpha = float(a[-1])
    return c.exponential_moving_average(data, alpha)


def _cov_handler(c, a):
    return _two_list(c.covariance, a)


def _corr_handler(c, a):
    return _two_list(c.correlation, a)


def _linreg_handler(c, a):
    return _two_list(c.linear_regression, a)


def _mat_det_handler(c, a):
    return c.matrix_determinant(_parse_matrix(a))


def _mat_trace_handler(c, a):
    return c.matrix_trace(_parse_matrix(a))


def _mat_transpose_handler(c, a):
    return c.matrix_transpose(_parse_matrix(a))


def _mat_inv_handler(c, a):
    return c.matrix_inverse(_parse_matrix(a))


def _mat_ident_handler(c, a):
    if len(a) != 1:
        raise ValueError("Usage: mat_ident <n>")
    return c.matrix_identity(int(float(a[0])))


def _mat_zero_handler(c, a):
    if len(a) != 2:
        raise ValueError("Usage: mat_zero <rows> <cols>")
    return c.matrix_zero(int(float(a[0])), int(float(a[1])))


def _base_convert_handler(c, a):
    if len(a) != 3:
        raise ValueError("Usage: base_convert <value> <from_base> <to_base>")
    return c.base_convert(a[0], int(a[1]), int(a[2]))


def _ascii_to_str_handler(c, a):
    if not a:
        raise ValueError("Usage: ascii_to_str <code1> <code2> ...")
    return c.ascii_codes_to_string([int(float(x)) for x in a])


def _uni_to_str_handler(c, a):
    if not a:
        raise ValueError("Usage: uni_to_str <code1> <code2> ...")
    return c.unicode_codes_to_string([int(float(x)) for x in a])


def _doppler_recede_handler(c, a):
    if len(a) != 3:
        raise ValueError("Usage: doppler_recede <f_source> <v_obs> <v_src>")
    return c.doppler_effect(float(a[0]), float(a[1]), float(a[2]), approach=False)


def _ohm_v_handler(c, a):
    if len(a) != 2:
        raise ValueError("Usage: ohm_v <current> <resistance>")
    return c.ohms_law(i=float(a[0]), r=float(a[1]))


def _ohm_i_handler(c, a):
    if len(a) != 2:
        raise ValueError("Usage: ohm_i <voltage> <resistance>")
    return c.ohms_law(v=float(a[0]), r=float(a[1]))


def _ohm_r_handler(c, a):
    if len(a) != 2:
        raise ValueError("Usage: ohm_r <voltage> <current>")
    return c.ohms_law(v=float(a[0]), i=float(a[1]))


def _dil_factory(missing):
    """Make a dilution handler that solves for `missing` (one of c1/v1/c2/v2)."""
    order = ["c1", "v1", "c2", "v2"]
    def handler(c, a):
        if len(a) != 3:
            raise ValueError(f"Usage: dil_{missing} <{'> <'.join(v for v in order if v != missing)}>")
        kwargs = {}
        idx = 0
        for key in order:
            if key == missing:
                kwargs[key] = None
            else:
                kwargs[key] = float(a[idx])
                idx += 1
        return c.dilution(**kwargs)
    return handler


def _boyle_factory(missing):
    order = ["p1", "v1", "p2", "v2"]
    def handler(c, a):
        if len(a) != 3:
            raise ValueError(f"Usage: boyle_{missing} <{'> <'.join(v for v in order if v != missing)}>")
        kwargs = {}
        idx = 0
        for key in order:
            if key == missing:
                kwargs[key] = None
            else:
                kwargs[key] = float(a[idx])
                idx += 1
        return c.boyle_law(**kwargs)
    return handler


def _charles_factory(missing):
    order = ["v1", "t1", "v2", "t2"]
    def handler(c, a):
        if len(a) != 3:
            raise ValueError(f"Usage: charles_{missing} <{'> <'.join(v for v in order if v != missing)}>")
        kwargs = {}
        idx = 0
        for key in order:
            if key == missing:
                kwargs[key] = None
            else:
                kwargs[key] = float(a[idx])
                idx += 1
        return c.charles_law(**kwargs)
    return handler


SPECIAL_HANDLERS = {
    # Trig with optional 'deg' suffix
    "sin": _trig_factory("sin"),
    "cos": _trig_factory("cos"),
    "tan": _trig_factory("tan"),
    "asin": _trig_factory("asin"),
    "acos": _trig_factory("acos"),
    "atan": _trig_factory("atan"),
    "cot": _trig_factory("cot"),
    "sec": _trig_factory("sec"),
    "csc": _trig_factory("csc"),

    # log with optional base
    "log": _log_handler,

    # Normal distribution
    "normal_pdf": _normal_factory("normal_pdf"),
    "normal_cdf": _normal_factory("normal_cdf"),

    # Pendulum period
    "t_pendulum": _pendulum_handler,

    # Round with optional digits
    "round": _round_handler,

    # Doppler
    "doppler": lambda c, a: c.doppler_effect(float(a[0]), float(a[1]), float(a[2])),
    "doppler_recede": _doppler_recede_handler,

    # Ohm's law variants
    "ohm_v": _ohm_v_handler,
    "ohm_i": _ohm_i_handler,
    "ohm_r": _ohm_r_handler,

    # Dilution variants
    "dil_c1": _dil_factory("c1"),
    "dil_v1": _dil_factory("v1"),
    "dil_c2": _dil_factory("c2"),
    "dil_v2": _dil_factory("v2"),

    # Boyle's law variants
    "boyle_p1": _boyle_factory("p1"),
    "boyle_v1": _boyle_factory("v1"),
    "boyle_p2": _boyle_factory("p2"),
    "boyle_v2": _boyle_factory("v2"),

    # Charles's law variants
    "charles_v1": _charles_factory("v1"),
    "charles_t1": _charles_factory("t1"),
    "charles_v2": _charles_factory("v2"),
    "charles_t2": _charles_factory("t2"),

    # Stats with trailing arg
    "percentile": _percentile_handler,
    "mov_avg": _mov_avg_handler,
    "ema": _ema_handler,

    # Two-list stats
    "cov": _cov_handler,
    "corr": _corr_handler,
    "linreg": _linreg_handler,

    # Matrix
    "mat_det": _mat_det_handler,
    "mat_trace": _mat_trace_handler,
    "mat_transpose": _mat_transpose_handler,
    "mat_inv": _mat_inv_handler,
    "mat_ident": _mat_ident_handler,
    "mat_zero": _mat_zero_handler,

    # Programmer misc
    "base_convert": _base_convert_handler,
    "ascii_to_str": _ascii_to_str_handler,
    "uni_to_str": _uni_to_str_handler,
}


# ═══════════════════════════════════════════════════════════════
# Help
# ═══════════════════════════════════════════════════════════════

def print_help_row(cmd, desc):
    """Helper to print help rows cleanly."""
    print(f"  {Fore.YELLOW}{cmd:<38}{Style.RESET_ALL} {Fore.LIGHTBLACK_EX}{desc}{Style.RESET_ALL}")


def show_help():
    """Show Calculator++ commands."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  Calculator++ Help{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}{'─' * 78}{Style.RESET_ALL}")

    print(f"\n  {Fore.MAGENTA}Basic Operations:{Style.RESET_ALL}")
    print_help_row("add <a> <b>", "Addition")
    print_help_row("sub <a> <b>", "Subtraction")
    print_help_row("mul <a> <b>", "Multiplication")
    print_help_row("div <a> <b>", "Division")

    print(f"\n  {Fore.MAGENTA}Trigonometry:{Style.RESET_ALL}")
    print_help_row("sin/cos/tan <x> [deg]", "Trig functions (radians by default)")
    print_help_row("asin/acos/atan <x> [deg]", "Inverse trig functions")
    print_help_row("sinh/cosh/tanh <x>", "Hyperbolic trig functions")
    print_help_row("asinh/acosh/atanh <x>", "Inverse hyperbolic trig")
    print_help_row("cot/sec/csc <x> [deg]", "Reciprocal trig functions")

    print(f"\n  {Fore.MAGENTA}Logarithms & Exponentials:{Style.RESET_ALL}")
    print_help_row("log <x> [base]", "Logarithm (default base 10)")
    print_help_row("ln <x>", "Natural logarithm")
    print_help_row("log2 <x>", "Base-2 logarithm")
    print_help_row("exp <x>", "e^x")

    print(f"\n  {Fore.MAGENTA}Roots & Rounding:{Style.RESET_ALL}")
    print_help_row("sqrt <x>", "Square root")
    print_help_row("power <base> <exp>", "Base to the power of exp")
    print_help_row("fact <n>", "Factorial")
    print_help_row("cbrt <x>", "Cube root")
    print_help_row("nth_root <x> <n>", "Nth root of x")
    print_help_row("mod <a> <b>", "Modulo (a % b)")
    print_help_row("abs <x>", "Absolute value")
    print_help_row("floor <x>", "Floor value")
    print_help_row("ceil <x>", "Ceiling value")
    print_help_row("round <x> [digits]", "Round to digits")

    print(f"\n  {Fore.MAGENTA}Angle Conversion:{Style.RESET_ALL}")
    print_help_row("deg2rad <deg>", "Degrees to radians")
    print_help_row("rad2deg <rad>", "Radians to degrees")

    print(f"\n  {Fore.MAGENTA}Number Theory & Primes:{Style.RESET_ALL}")
    print_help_row("gcd/lcm <a> <b>", "Greatest common divisor / LCM")
    print_help_row("is_prime <n>", "Check if prime")
    print_help_row("prime_factors <n>", "List prime factors")
    print_help_row("next_prime <n>", "Find next prime after n")
    print_help_row("prev_prime <n>", "Find previous prime before n")
    print_help_row("primes_up_to <n>", "List primes up to n")
    print_help_row("prime_count <n>", "Count primes up to n")
    print_help_row("nth_prime <k>", "Find the k-th prime")
    print_help_row("is_coprime <a> <b>", "Check if coprime")
    print_help_row("euler_totient <n>", "Euler's Totient function")
    print_help_row("divisors_of <n>", "List divisors")
    print_help_row("divisor_count <n>", "Count divisors")
    print_help_row("sum_of_divisors <n>", "Sum of divisors")
    print_help_row("is_perfect <n>", "Check if perfect number")
    print_help_row("is_abundant <n>", "Check if abundant number")
    print_help_row("is_deficient <n>", "Check if deficient number")
    print_help_row("goldbach <n>", "Goldbach prime pair for even n >= 4")
    print_help_row("twin_primes <n>", "Twin prime pairs up to n")
    print_help_row("fibonacci <n>", "Sequence up to index n")
    print_help_row("is_even/is_odd <n>", "Check parity")
    print_help_row("permutations <n> <r>", "nPr")
    print_help_row("combinations <n> <r>", "nCr")

    print(f"\n  {Fore.MAGENTA}Statistics (single list of numbers):{Style.RESET_ALL}")
    print_help_row("mean/median/mode <nums...>", "Mean / Median / Mode")
    print_help_row("var/std <nums...>", "Variance / Std Dev (sample)")
    print_help_row("min/max <nums...>", "Minimum / Maximum")
    print_help_row("sum/prod <nums...>", "Sum / Product")
    print_help_row("geomean/harmmean <nums...>", "Geometric / Harmonic mean")
    print_help_row("range <nums...>", "Range (max - min)")
    print_help_row("quartiles <nums...>", "Q1, Q2, Q3")
    print_help_row("iqr <nums...>", "Interquartile range")
    print_help_row("percentile <nums...> <p>", "Percentile p (last arg)")
    print_help_row("skewness/kurtosis <nums...>", "Skewness / Kurtosis")
    print_help_row("mov_avg <nums...> <window>", "Moving average (window last)")
    print_help_row("ema <nums...> <alpha>", "Exp. moving avg (alpha last)")

    print(f"\n  {Fore.MAGENTA}Statistics (two lists, x | y):{Style.RESET_ALL}")
    print_help_row("cov <x...> | <y...>", "Covariance")
    print_help_row("corr <x...> | <y...>", "Pearson correlation")
    print_help_row("linreg <x...> | <y...>", "Linear regression (slope, intercept)")

    print(f"\n  {Fore.MAGENTA}Statistics (single values):{Style.RESET_ALL}")
    print_help_row("z_score <x> <mu> <sigma>", "Z-Score")
    print_help_row("binomial_pmf/cdf <k> <n> <p>", "Binomial distribution")
    print_help_row("poisson_pmf/cdf <k> <lam>", "Poisson distribution")
    print_help_row("normal_pdf/cdf <x> [mu] [sigma]", "Normal distribution")

    print(f"\n  {Fore.MAGENTA}Geometry (2D):{Style.RESET_ALL}")
    print_help_row("area_circle <r>", "Area of circle")
    print_help_row("circumference <r>", "Circumference of circle")
    print_help_row("area_rectangle <l> <w>", "Area of rectangle")
    print_help_row("perimeter_rectangle <l> <w>", "Perimeter of rectangle")
    print_help_row("area_triangle <b> <h>", "Area of triangle")
    print_help_row("area_triangle_sss <a> <b> <c>", "Area via Heron's formula")
    print_help_row("area_trapezoid <a> <b> <h>", "Area of trapezoid")
    print_help_row("distance_2d <x1> <y1> <x2> <y2>", "Distance between points")
    print_help_row("midpoint_2d <x1> <y1> <x2> <y2>", "Midpoint")
    print_help_row("slope_2d <x1> <y1> <x2> <y2>", "Slope")

    print(f"\n  {Fore.MAGENTA}Geometry (3D):{Style.RESET_ALL}")
    print_help_row("volume_sphere <r>", "Volume of sphere")
    print_help_row("surface_area_sphere <r>", "Surface area of sphere")
    print_help_row("volume_cylinder <r> <h>", "Volume of cylinder")
    print_help_row("volume_cone <r> <h>", "Volume of cone")
    print_help_row("volume_cube <side>", "Volume of cube")
    print_help_row("volume_rect_prism <l> <w> <h>", "Volume of rectangular prism")
    print_help_row("volume_pyramid <base> <h>", "Volume of pyramid")

    print(f"\n  {Fore.MAGENTA}Equations & Finance:{Style.RESET_ALL}")
    print_help_row("eq1 <a> <b>", "Solve a*x + b = 0")
    print_help_row("quad <a> <b> <c>", "Solve a*x^2 + b*x + c = 0")
    print_help_row("eq2 <a1> <b1> <c1> <a2> <b2> <c2>", "Solve 2x2 linear system")
    print_help_row("percentage <val> <percent>", "Percentage of value")
    print_help_row("pct_change <old> <new>", "Percentage change")
    print_help_row("simple_interest <p> <r> <t>", "Simple interest")
    print_help_row("compound_interest <p> <r> <t> [n]", "Compound interest")

    print(f"\n  {Fore.MAGENTA}Physics - Conversions:{Style.RESET_ALL}")
    print_help_row("c2f <celsius>", "Celsius to Fahrenheit")
    print_help_row("f2c <fahrenheit>", "Fahrenheit to Celsius")
    print_help_row("c2k <celsius>", "Celsius to Kelvin")
    print_help_row("k2c <kelvin>", "Kelvin to Celsius")

    print(f"\n  {Fore.MAGENTA}Physics - Mechanics:{Style.RESET_ALL}")
    print_help_row("force <m> <a>", "Force (F = m*a)")
    print_help_row("momentum <m> <v>", "Momentum (p = m*v)")
    print_help_row("impulse <F> <t>", "Impulse (J = F*t)")
    print_help_row("work <F> <d> [angle_deg]", "Work done")
    print_help_row("power_mech <W> <t>", "Mechanical power")
    print_help_row("ke <m> <v>", "Kinetic energy")
    print_help_row("pe <m> <h> [g]", "Potential energy")
    print_help_row("density <m> <V>", "Density")
    print_help_row("pressure <F> <A>", "Pressure")
    print_help_row("bmi <weight_kg> <height_m>", "Body Mass Index")
    print_help_row("speed <d> <t>", "Speed")

    print(f"\n  {Fore.MAGENTA}Physics - Gravitation & Waves:{Style.RESET_ALL}")
    print_help_row("g_force <m1> <m2> <r>", "Gravitational force")
    print_help_row("wavelength <freq>", "Wavelength from frequency")
    print_help_row("freq_from_wavelength <lambda>", "Frequency from wavelength")
    print_help_row("photon_energy <freq>", "Energy of a photon")
    print_help_row("photon_wavelength <energy>", "Wavelength from photon energy")
    print_help_row("v_escape <mass> <r>", "Escape velocity")
    print_help_row("t_pendulum <length> [g]", "Pendulum period")
    print_help_row("doppler <f> <v_obs> <v_src>", "Doppler effect (approaching)")
    print_help_row("doppler_recede <f> <v_obs> <v_src>", "Doppler effect (receding)")

    print(f"\n  {Fore.MAGENTA}Physics - Rotational & Thermo:{Style.RESET_ALL}")
    print_help_row("a_centripetal <v> <r>", "Centripetal acceleration")
    print_help_row("f_centripetal <m> <v> <r>", "Centripetal force")
    print_help_row("torque <F> <lever> [angle_deg]", "Torque")
    print_help_row("omega <angle_rad> <t>", "Angular velocity")
    print_help_row("heat_transfer <m> <c> <dt>", "Heat transfer (Q = m*c*dT)")
    print_help_row("c_specific <Q> <m> <dt>", "Specific heat capacity")
    print_help_row("p_ideal <n> <T> <V>", "Ideal gas pressure")
    print_help_row("v_ideal <n> <T> <P>", "Ideal gas volume")
    print_help_row("t_ideal <P> <V> <n>", "Ideal gas temperature")
    print_help_row("snell <theta1> <n1> <n2>", "Snell's Law (returns theta2 deg)")

    print(f"\n  {Fore.MAGENTA}Pythagoras:{Style.RESET_ALL}")
    print_help_row("pythag_hyp <a> <b>", "Hypotenuse from two legs")
    print_help_row("pythag_leg <c> <a>", "Missing leg from c and a")

    print(f"\n  {Fore.MAGENTA}Chemistry:{Style.RESET_ALL}")
    print_help_row("molar_mass <formula>", "Molar mass (e.g., H2O, Ca(OH)2)")
    print_help_row("moles <mass> <molar_mass>", "Moles from mass")
    print_help_row("mass_from_moles <moles> <mm>", "Mass from moles")
    print_help_row("molarity <moles> <vol_L>", "Molarity")
    print_help_row("moles_from_molarity <M> <vol_L>", "Moles from molarity")
    print_help_row("ph <H_concentration>", "pH from H+")
    print_help_row("ph_to_h <pH>", "H+ from pH")
    print_help_row("poh <OH_concentration>", "pOH from OH-")
    print_help_row("poh_to_oh <pOH>", "OH- from pOH")
    print_help_row("pct_mass_conc <solute> <solution>", "Percent mass concentration")
    print_help_row("half_life <initial> <half_life> <t>", "Remaining amount")
    print_help_row("half_life_decay <init> <remain> <t>", "Half-life from decay")
    print(f"  {Fore.CYAN}Dilution (M1V1=M2V2):{Style.RESET_ALL}")
    print_help_row("dil_c1 <v1> <c2> <v2>", "Solve for c1")
    print_help_row("dil_v1 <c1> <c2> <v2>", "Solve for v1")
    print_help_row("dil_c2 <c1> <v1> <v2>", "Solve for c2")
    print_help_row("dil_v2 <c1> <v1> <c2>", "Solve for v2")
    print(f"  {Fore.CYAN}Boyle's Law (P1V1=P2V2):{Style.RESET_ALL}")
    print_help_row("boyle_p1 <v1> <p2> <v2>", "Solve for p1")
    print_help_row("boyle_v1 <p1> <p2> <v2>", "Solve for v1")
    print_help_row("boyle_p2 <p1> <v1> <v2>", "Solve for p2")
    print_help_row("boyle_v2 <p1> <v1> <p2>", "Solve for v2")
    print(f"  {Fore.CYAN}Charles's Law (V1/T1=V2/T2):{Style.RESET_ALL}")
    print_help_row("charles_v1 <t1> <v2> <t2>", "Solve for v1")
    print_help_row("charles_t1 <v1> <v2> <t2>", "Solve for t1")
    print_help_row("charles_v2 <v1> <t1> <t2>", "Solve for v2")
    print_help_row("charles_t2 <v1> <t1> <v2>", "Solve for t2")

    print(f"\n  {Fore.MAGENTA}Electronics:{Style.RESET_ALL}")
    print_help_row("pow_vi <V> <I>", "Power (P = V*I)")
    print_help_row("pow_i2r <I> <R>", "Power (P = I^2*R)")
    print_help_row("pow_v2r <V> <R>", "Power (P = V^2/R)")
    print_help_row("resistance_series <r1> <r2>...", "Series resistance")
    print_help_row("resistance_parallel <r1> <r2>...", "Parallel resistance")
    print_help_row("cap_series <c1> <c2>...", "Series capacitance")
    print_help_row("cap_parallel <c1> <c2>...", "Parallel capacitance")
    print_help_row("ind_series <l1> <l2>...", "Series inductance")
    print_help_row("ind_parallel <l1> <l2>...", "Parallel inductance")
    print_help_row("xc <freq> <cap>", "Capacitive reactance")
    print_help_row("xl <freq> <ind>", "Inductive reactance")
    print_help_row("res_freq <L> <C>", "LC resonant frequency")
    print_help_row("tau_rc <R> <C>", "RC time constant")
    print_help_row("tau_rl <L> <R>", "RL time constant")
    print_help_row("db_power <p2> <p1>", "Decibels (power ratio)")
    print_help_row("db_voltage <v2> <v1>", "Decibels (voltage ratio)")
    print_help_row("vdiv <vin> <r1> <r2>", "Voltage divider")
    print_help_row("idiv <itotal> <r1> <r2>", "Current divider")
    print_help_row("rms2peak <rms>", "RMS to peak")
    print_help_row("peak2rms <peak>", "Peak to RMS")
    print_help_row("freq <period>", "Frequency from period")
    print_help_row("period <freq>", "Period from frequency")
    print_help_row("wheatstone <r1> <r2> <r3> <r4>", "Check if bridge balanced")

    print(f"\n  {Fore.MAGENTA}Programmer - Number Bases:{Style.RESET_ALL}")
    print_help_row("to_hex/to_bin/to_oct <n>", "Decimal to hex/binary/octal")
    print_help_row("from_hex/from_bin/from_oct <str>", "Base string to decimal")
    print_help_row("base_convert <val> <from> <to>", "Convert between bases (2-36)")

    print(f"\n  {Fore.MAGENTA}Programmer - Bitwise:{Style.RESET_ALL}")
    print_help_row("bit_and/bit_or/bit_xor <a> <b>", "Bitwise AND/OR/XOR")
    print_help_row("bit_not <a>", "Bitwise NOT")
    print_help_row("lshift/rshift <a> <n>", "Bitwise shifts")
    print_help_row("count_bits <n>", "Count set bits (popcount)")
    print_help_row("is_pow2 <n>", "Check if power of 2")

    print(f"\n  {Fore.MAGENTA}Programmer - ASCII & Unicode:{Style.RESET_ALL}")
    print_help_row("ascii_to_char <n>", "ASCII code to character")
    print_help_row("char_to_ascii <char>", "Character to ASCII code")
    print_help_row("str_to_ascii <string>", "String to ASCII codes list")
    print_help_row("ascii_to_str <code1> <code2>...", "ASCII codes to string")
    print_help_row("unicode_to_char <n>", "Unicode code to character")
    print_help_row("char_to_uni <char>", "Character to Unicode code")
    print_help_row("str_to_uni <string>", "String to Unicode codes list")
    print_help_row("uni_to_str <code1> <code2>...", "Unicode codes to string")

    print(f"\n  {Fore.MAGENTA}Programmer - Base64:{Style.RESET_ALL}")
    print_help_row("b64_enc <string>", "Encode string to Base64")
    print_help_row("b64_dec <base64>", "Decode Base64 to string")

    print(f"\n  {Fore.MAGENTA}Programmer - Hashing:{Style.RESET_ALL}")
    print_help_row("md5 <string>", "MD5 hash")
    print_help_row("sha1 <string>", "SHA-1 hash")
    print_help_row("sha256 <string>", "SHA-256 hash")
    print_help_row("sha512 <string>", "SHA-512 hash")
    print_help_row("sha3_256 <string>", "SHA3-256 hash")
    print_help_row("blake2b <string>", "BLAKE2b hash")
    print_help_row("blake2s <string>", "BLAKE2s hash")

    print(f"\n  {Fore.MAGENTA}Matrix (rows separated by space, columns by comma):{Style.RESET_ALL}")
    print_help_row("mat_det <r1,r2,...> <r1,r2,...>", "Determinant (e.g. 1,2 3,4)")
    print_help_row("mat_trace <matrix>", "Trace")
    print_help_row("mat_transpose <matrix>", "Transpose")
    print_help_row("mat_inv <matrix>", "Inverse")
    print_help_row("mat_ident <n>", "Identity matrix (n x n)")
    print_help_row("mat_zero <rows> <cols>", "Zero matrix")

    print(f"\n  {Fore.MAGENTA}Scientific Constants (no args):{Style.RESET_ALL}")
    print_help_row("PI, E, GOLDEN_RATIO", "Mathematical constants")
    print_help_row("SPEED_OF_LIGHT, GRAVITATIONAL_CONSTANT", "Physics constants")
    print_help_row("PLANCK_CONSTANT, BOLTZMANN_CONSTANT", "Quantum constants")
    print_help_row("AVOGADRO_NUMBER, GAS_CONSTANT", "Chemistry constants")
    print_help_row("ELECTRON_MASS, PROTON_MASS, NEUTRON_MASS", "Particle masses")
    print_help_row("ELEMENTARY_CHARGE", "Elementary charge")

    print(f"\n  {Fore.MAGENTA}System:{Style.RESET_ALL}")
    print_help_row("help", "Show this help")
    print_help_row("clear", "Clear screen")
    print_help_row("exit", "Return to N-Toolkit")

    print(f"\n  {Fore.LIGHTBLACK_EX}Note: Calculus (derivative, integral, etc.) and matrix")
    print(f"  arithmetic (add/subtract/multiply) require callables or two matrices")
    print(f"  and are not supported in CLI mode. Use the Python API directly.{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}{'─' * 78}{Style.RESET_ALL}\n")


# ═══════════════════════════════════════════════════════════════
# Command execution
# ═══════════════════════════════════════════════════════════════

def execute_command(calculator, command, args):
    """Dynamically execute a Calculator++ command."""

    # 1. Constants (e.g., PI, E, SPEED_OF_LIGHT)
    if command in CONSTANTS and hasattr(calculator, command):
        print(f"{Fore.GREEN}  {command} = {getattr(calculator, command)}{Style.RESET_ALL}")
        return

    # 2. Special handlers (custom argument parsing)
    if command in SPECIAL_HANDLERS:
        try:
            result = SPECIAL_HANDLERS[command](calculator, args)
            _print_result(result)
        except TypeError as e:
            print(f"{Fore.RED}  [Error] Invalid arguments for '{command}'. {e}{Style.RESET_ALL}")
        except ValueError as e:
            print(f"{Fore.RED}  [Math Error] {e}{Style.RESET_ALL}")
        except ZeroDivisionError as e:
            print(f"{Fore.RED}  [Math Error] {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}  [Error] {e}{Style.RESET_ALL}")
        return

    # 3. Method lookup via CMD_MAP
    method_name = CMD_MAP.get(command, command)
    if not hasattr(calculator, method_name):
        print(f"{Fore.RED}  Unknown command: {command}. Type 'help' for commands.{Style.RESET_ALL}")
        return

    method = getattr(calculator, method_name)

    # 4. Unsupported in CLI
    if method_name in UNSUPPORTED_CLI:
        print(f"{Fore.RED}  [Error] '{command}' is not supported in CLI mode. "
              f"Use the Python API.{Style.RESET_ALL}")
        return

    try:
        # 5. String commands (no float parsing)
        if command in STRING_COMMANDS:
            result = method(*args)

        # 6. Int commands
        elif command in INT_COMMANDS:
            int_args = [int(float(a)) for a in args]
            result = method(*int_args)

        # 7. List-of-floats commands
        elif command in LIST_COMMANDS:
            if not args:
                print(f"{Fore.RED}  Usage: {command} <num1> <num2> ...{Style.RESET_ALL}")
                return
            data = [float(x) for x in args]
            result = method(data)

        # 8. Default: float args
        else:
            float_args = [float(a) for a in args]
            result = method(*float_args)

        _print_result(result)

    except TypeError as e:
        print(f"{Fore.RED}  [Error] Invalid arguments for '{command}'. {e}{Style.RESET_ALL}")
    except ValueError as e:
        print(f"{Fore.RED}  [Math Error] {e}{Style.RESET_ALL}")
    except ZeroDivisionError as e:
        print(f"{Fore.RED}  [Math Error] {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}  [Error] {e}{Style.RESET_ALL}")


# ═══════════════════════════════════════════════════════════════
# Entry point
# ═══════════════════════════════════════════════════════════════

def start(args: list):
    """Entry point called by N-Toolkit."""
    calculator = load_calculator()

    art = pyfiglet.figlet_format(f"{TOOL_NAME}", font="slant")
    palette = [Fore.RED, Fore.MAGENTA, Fore.BLUE, Fore.CYAN]
    for i, line in enumerate(art.splitlines()):
        print(f"{palette[i % len(palette)]}{line}{Style.RESET_ALL}")

    print(f"{Fore.MAGENTA}{Style.BRIGHT}\n  ╭──────────── Calculator++ ─────────────╮{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'help' or '?' for commands.      │{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'exit' to return to N-Toolkit.   │{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  ╰───────────────────────────────────────╯{Style.RESET_ALL}\n")

    # Handle arguments passed directly from N-Toolkit
    if args:
        command = args[0].lower()
        if command in ("help", "?"):
            show_help()
        else:
            execute_command(calculator, command, args[1:])

    # Calculator++ own prompt loop
    while True:
        try:
            user_input = input(
                f"{Fore.MAGENTA}{TOOL_NAME}{Style.RESET_ALL}{Fore.YELLOW} ❯ {Style.RESET_ALL}"
            ).strip()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}  Returning to N-Toolkit...{Style.RESET_ALL}\n")
            return True
        except EOFError:
            return True

        if not user_input:
            continue

        parts = user_input.split()
        command = parts[0].lower()
        command_args = parts[1:]

        if command in ("exit", "quit", "q"):
            print(f"\n{Fore.CYAN}  Returning to N-Toolkit...{Style.RESET_ALL}\n")
            return True

        if command in ("help", "?"):
            show_help()
            continue

        if command == "clear":
            os.system("clear" if os.name == "posix" else "cls")
            continue

        execute_command(calculator, command, command_args)