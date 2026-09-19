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


def print_help_row(cmd, desc):
    """Helper to print help rows cleanly."""
    print(f"  {Fore.YELLOW}{cmd:<30}{Style.RESET_ALL} {Fore.LIGHTBLACK_EX}{desc}{Style.RESET_ALL}")


def show_help():
    """Show Calculator++ commands."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  Calculator++ Help{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}{'─' * 60}{Style.RESET_ALL}")
    
    print(f"\n  {Fore.MAGENTA}Basic Operations:{Style.RESET_ALL}")
    print_help_row("add <a> <b>", "Addition")
    print_help_row("sub <a> <b>", "Subtraction")
    print_help_row("mul <a> <b>", "Multiplication")
    print_help_row("div <a> <b>", "Division")
    
    print(f"\n  {Fore.MAGENTA}Advanced & Roots:{Style.RESET_ALL}")
    print_help_row("sqrt <x>", "Square root")
    print_help_row("power <base> <exp>", "Base to the power of exp")
    print_help_row("fact <n>", "Factorial")
    print_help_row("cbrt <x>", "Cube root")
    print_help_row("nth_root <x> <n>", "Nth root of x")
    print_help_row("mod <a> <b>", "Modulo (a % b)")
    print_help_row("abs <x>", "Absolute value")
    print_help_row("floor <x>", "Floor value")
    print_help_row("ceil <x>", "Ceiling value")
    print_help_row("round <x> <digits>", "Round to digits")
    
    print(f"\n  {Fore.MAGENTA}Trigonometry (radians):{Style.RESET_ALL}")
    print_help_row("sin/cos/tan <x>", "Standard trig functions")
    print_help_row("asin/acos/atan <x>", "Inverse trig functions")
    print_help_row("sinh/cosh/tanh <x>", "Hyperbolic trig functions")
    
    print(f"\n  {Fore.MAGENTA}Logarithms & Exponentials:{Style.RESET_ALL}")
    print_help_row("ln <x>", "Natural log")
    print_help_row("log2 <x>", "Base-2 log")
    print_help_row("log <x> <base>", "Log with custom base")
    print_help_row("exp <x>", "Exponential (e^x)")
    
    print(f"\n  {Fore.MAGENTA}Number Theory:{Style.RESET_ALL}")
    print_help_row("gcd/lcm <a> <b>", "Greatest common divisor / LCM")
    print_help_row("is_prime <n>", "Check if prime")
    print_help_row("prime_factors <n>", "List prime factors")
    print_help_row("next_prime <n>", "Find next prime after n")
    print_help_row("fibonacci <n>", "Sequence up to index n")
    print_help_row("is_even/is_odd <n>", "Check parity")
    print_help_row("permutations <n> <r>", "nPr")
    print_help_row("combinations <n> <r>", "nCr")
    
    print(f"\n  {Fore.MAGENTA}Statistics (Enter multiple numbers):{Style.RESET_ALL}")
    print_help_row("mean <nums...>", "Mean")
    print_help_row("median <nums...>", "Median")
    print_help_row("mode <nums...>", "Mode")
    print_help_row("var <nums...>", "Variance (sample)")
    print_help_row("std <nums...>", "Standard deviation (sample)")
    print_help_row("min/max <nums...>", "Minimum / Maximum")
    print_help_row("sum/prod <nums...>", "Sum / Product of numbers")
    print_help_row("geomean <nums...>", "Geometric mean")
    print_help_row("harmmean <nums...>", "Harmonic mean")
    print_help_row("range <nums...>", "Range (max - min)")
    
    print(f"\n  {Fore.MAGENTA}Geometry (2D):{Style.RESET_ALL}")
    print_help_row("area_circle <r>", "Area of circle")
    print_help_row("circumference <r>", "Circumference of circle")
    print_help_row("area_rectangle <l> <w>", "Area of rectangle")
    print_help_row("perimeter_rectangle <l> <w>", "Perimeter of rectangle")
    print_help_row("area_triangle <b> <h>", "Area of triangle")
    print_help_row("area_triangle_sss <a> <b> <c>", "Area via Heron's formula")
    print_help_row("area_trapezoid <a> <b> <h>", "Area of trapezoid")
    print_help_row("distance_2d <x1> <y1> <x2> <y2>", "Distance between points")
    print_help_row("midpoint_2d <x1> <y1> <x2> <y2>", "Midpoint between points")
    print_help_row("slope_2d <x1> <y1> <x2> <y2>", "Slope of line")
    
    print(f"\n  {Fore.MAGENTA}Geometry (3D):{Style.RESET_ALL}")
    print_help_row("volume_sphere <r>", "Volume of sphere")
    print_help_row("surface_area_sphere <r>", "Surface area of sphere")
    print_help_row("volume_cylinder <r> <h>", "Volume of cylinder")
    print_help_row("volume_cone <r> <h>", "Volume of cone")
    print_help_row("volume_cube <side>", "Volume of cube")
    print_help_row("volume_rect_prism <l> <w> <h>", "Volume of rectangular prism")
    print_help_row("volume_pyramid <base> <h>", "Volume of pyramid")
    
    print(f"\n  {Fore.MAGENTA}Equations:{Style.RESET_ALL}")
    print_help_row("eq1 <a> <b>", "Solve a*x + b = 0")
    print_help_row("quad <a> <b> <c>", "Solve a*x^2 + b*x + c = 0")
    print_help_row("eq2 <a1> <b1> <c1> <a2> <b2> <c2>", "Solve system of 2 linear equations")
    
    print(f"\n  {Fore.MAGENTA}Finance & Percentages:{Style.RESET_ALL}")
    print_help_row("percentage <val> <percent>", "Calculate percentage")
    print_help_row("percentage_change <old> <new>", "Percentage change")
    print_help_row("simple_interest <p> <r> <t>", "Simple interest")
    print_help_row("compound_interest <p> <r> <t> <n>", "Compound interest")
    
    print(f"\n  {Fore.MAGENTA}Physics & Conversions:{Style.RESET_ALL}")
    print_help_row("celsius_to_fahrenheit <c>", "C to F")
    print_help_row("fahrenheit_to_celsius <f>", "F to C")
    print_help_row("celsius_to_kelvin <c>", "C to K")
    print_help_row("kelvin_to_celsius <k>", "K to C")
    print_help_row("kinetic_energy <mass> <vel>", "Kinetic energy")
    print_help_row("potential_energy <mass> <h>", "Potential energy")
    print_help_row("ohms_law <v> <i> [or any 2]", "Ohm's Law")
    print_help_row("speed <dist> <time>", "Speed")
    print_help_row("density <mass> <vol>", "Density")
    print_help_row("pressure <force> <area>", "Pressure")
    print_help_row("bmi <weight_kg> <height_m>", "Body Mass Index")
    
    print(f"\n  {Fore.MAGENTA}Pythagoras:{Style.RESET_ALL}")
    print_help_row("pythagorean_hypotenuse <a> <b>", "Hypotenuse from legs")
    print_help_row("pythagorean_leg <c> <a>", "Leg from hypotenuse and leg")
    
    print(f"\n  {Fore.MAGENTA}System:{Style.RESET_ALL}")
    print_help_row("help", "Show this help")
    print_help_row("clear", "Clear screen")
    print_help_row("exit", "Return to N-Toolkit")
    print(f"  {Fore.YELLOW}{'─' * 60}{Style.RESET_ALL}\n")


def execute_command(calculator, command, args):
    """Dynamically execute a Calculator++ command."""
    
    # Aliases mapping CLI commands to actual method names
    cmd_map = {
        "add": "add", "sub": "subtract", "mul": "multiply", "div": "divide",
        "power": "power", "sqrt": "sqrt", "fact": "factorial", "eq2": "solve_linear_eq2",
        "cbrt": "cube_root", "abs": "abs_val", "floor": "floor", "ceil": "ceiling", 
        "round": "round_num", "mod": "mod", "var": "variance", "std": "std_dev", 
        "min": "minimum", "max": "maximum", "sum": "sum_of", "prod": "product_of", 
        "geomean": "geometric_mean", "harmmean": "harmonic_mean", "range": "range_of",
        "eq1": "solve_linear_eq", "quad": "solve_quadratic_eq"
    }
    
    method_name = cmd_map.get(command, command)
    
    if not hasattr(calculator, method_name):
        print(f"{Fore.RED}  Unknown command: {command}. Type 'help' for commands.{Style.RESET_ALL}")
        return
        
    method = getattr(calculator, method_name)
    
    list_commands = ["mean", "median", "mode", "var", "std", "min", "max", "sum", "prod", "geomean", "harmmean", "range"]
    
    try:
        # 1. Handle list commands (Statistics)
        if command in list_commands:
            if not args:
                print(f"{Fore.RED}  Usage: {command} <num1> <num2> ...{Style.RESET_ALL}")
                return
            data = [float(x) for x in args]
            result = method(data)
            
        # 2. Special handling for round (requires int for digits)
        elif command == "round":
            if len(args) == 1:
                result = method(float(args[0]))
            elif len(args) == 2:
                result = method(float(args[0]), int(float(args[1])))
            else:
                print(f"{Fore.RED}  Usage: round <number> [digits]{Style.RESET_ALL}")
                return
                
        # 3. Handle all other mathematical commands dynamically
        else:
            float_args = [float(a) for a in args]
            result = method(*float_args)
            
        # Print the result
        print(f"{Fore.GREEN}  Result: {result}{Style.RESET_ALL}")
        
    except TypeError:
        print(f"{Fore.RED}  [Error] Invalid arguments for '{command}'. Type 'help' for usage.{Style.RESET_ALL}")
    except ValueError as e:
        print(f"{Fore.RED}  [Math Error] {e}{Style.RESET_ALL}")
    except ZeroDivisionError as e:
        print(f"{Fore.RED}  [Math Error] {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}  [Error] {e}{Style.RESET_ALL}")


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