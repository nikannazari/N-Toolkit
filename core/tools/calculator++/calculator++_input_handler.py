"""
calculator++_input_handler.py - CLI interface for Calculator++.
"""

import importlib.util
import os

from colorama import Fore, Style
import pyfiglet


TOOL_NAME = "calculator++"


def load_calculator():
    """
    Dynamically load the Calculator++ core module.
    """

    current_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    calculator_file = os.path.join(
        current_dir,
        "calculator++.py"
    )

    spec = importlib.util.spec_from_file_location(
        "calculator_core",
        calculator_file
    )

    if spec is None or spec.loader is None:
        raise ImportError(
            "Could not load calculator++.py"
        )

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return module.Calculator


def show_help():
    """Show Calculator++ commands."""

    print()
    print(
        f"{Fore.CYAN}{Style.BRIGHT}"
        "  Calculator++ Help"
        f"{Style.RESET_ALL}"
    )
    
    print(f"  {Fore.YELLOW}{'─' * 45}{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}Basic Operations:{Style.RESET_ALL}")
    
    print(
        f"  {Fore.YELLOW}add <a> <b>"
        f"{Style.RESET_ALL}      Add"
    )

    print(
        f"  {Fore.YELLOW}sub <a> <b>"
        f"{Style.RESET_ALL}      Subtract"
    )

    print(
        f"  {Fore.YELLOW}mul <a> <b>"
        f"{Style.RESET_ALL}      Multiply"
    )

    print(
        f"  {Fore.YELLOW}div <a> <b>"
        f"{Style.RESET_ALL}      Divide"
    )

    print(f"\n  {Fore.MAGENTA}Advanced Commands (++):{Style.RESET_ALL}")
    
    print(
        f"  {Fore.YELLOW}sqrt <x>"
        f"{Style.RESET_ALL}         Square root of x"
    )

    print(
        f"  {Fore.YELLOW}power <b> <e>"
        f"{Style.RESET_ALL}     Base raised to exponent"
    )

    print(
        f"  {Fore.YELLOW}fact <n>"
        f"{Style.RESET_ALL}         Factorial of n"
    )

    print(
        f"  {Fore.YELLOW}eq2 <a1> <b1> <c1> <a2> <b2> <c2>"
        f"{Style.RESET_ALL}"
    )
    print(
        f"  {Fore.LIGHTBLACK_EX}          Solve: a1*x + b1*y = c1{Style.RESET_ALL}"
    )

    print(f"\n  {Fore.MAGENTA}System:{Style.RESET_ALL}")
    
    print(
        f"  {Fore.YELLOW}help"
        f"{Style.RESET_ALL}           Show help"
    )

    print(
        f"  {Fore.YELLOW}clear"
        f"{Style.RESET_ALL}          Clear screen"
    )

    print(
        f"  {Fore.YELLOW}exit"
        f"{Style.RESET_ALL}           Return to N-Toolkit"
    )
    print(f"  {Fore.YELLOW}{'─' * 45}{Style.RESET_ALL}")
    print()


def execute_command(calculator, command, args):
    """Execute a Calculator++ command."""

    # Commands that require exactly 2 arguments
    two_arg_cmds = {
        "add": calculator.add,
        "sub": calculator.subtract,
        "mul": calculator.multiply,
        "div": calculator.divide,
        "power": calculator.power
    }
    
    # Commands that require exactly 1 argument
    one_arg_cmds = {
        "sqrt": calculator.sqrt,
        "fact": calculator.factorial
    }

    try:
        # 1. Handle 2-argument commands
        if command in two_arg_cmds:
            if len(args) != 2:
                print(f"{Fore.RED}  Usage: {command} <number> <number>{Style.RESET_ALL}")
                return
            a, b = float(args[0]), float(args[1])
            result = two_arg_cmds[command](a, b)
            print(f"{Fore.GREEN}  Result: {result}{Style.RESET_ALL}")
            
        # 2. Handle 1-argument commands
        elif command in one_arg_cmds:
            if len(args) != 1:
                print(f"{Fore.RED}  Usage: {command} <number>{Style.RESET_ALL}")
                return
            a = float(args[0])
            result = one_arg_cmds[command](a)
            print(f"{Fore.GREEN}  Result: {result}{Style.RESET_ALL}")
            
        # 3. Handle Equation with 2 unknowns (6 arguments)
        elif command == "eq2":
            if len(args) != 6:
                print(f"{Fore.RED}  Usage: eq2 <a1> <b1> <c1> <a2> <b2> <c2>{Style.RESET_ALL}")
                return
            
            coeffs = [float(arg) for arg in args]
            result = calculator.solve_linear_eq2(*coeffs)
            print(f"{Fore.GREEN}  Solution: {result}{Style.RESET_ALL}")
            
        else:
            print(f"{Fore.RED}  Unknown command: {command}. Type 'help' for commands.{Style.RESET_ALL}")

    except ValueError as e:
        print(f"{Fore.RED}  [Math Error] {e}{Style.RESET_ALL}")
    except ZeroDivisionError as e:
        print(f"{Fore.RED}  [Math Error] {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}  [Error] {e}{Style.RESET_ALL}")


def start(args: list):
    """
    Entry point called by N-Toolkit.
    """

    calculator = load_calculator()
    
    art = pyfiglet.figlet_format(f"{TOOL_NAME}", font="slant")
    palette = [Fore.RED, Fore.MAGENTA, Fore.BLUE, Fore.CYAN]
    for i, line in enumerate(art.splitlines()):
        print(f"{palette[i % len(palette)]}{line}{Style.RESET_ALL}")

    print(
        f"{Fore.MAGENTA}{Style.BRIGHT}"
        "\n  ╭──────────── Calculator++ ─────────────╮"
        f"{Style.RESET_ALL}"
    )

    print(
        f"{Fore.MAGENTA}"
        "  │ Type 'help' or '?' for commands.      │"
        f"{Style.RESET_ALL}"
    )

    print(
        f"{Fore.MAGENTA}"
        "  │ Type 'exit' to return to N-Toolkit.   │"
        f"{Style.RESET_ALL}"
    )

    print(
        f"{Fore.MAGENTA}"
        "  ╰───────────────────────────────────────╯"
        f"{Style.RESET_ALL}\n"
    )

    # Handle arguments passed through:
    #
    # N-Toolkit ❯ run calculator++ add 5 10
    #
    if args:
        command = args[0].lower()

        if command in ("help", "?"):
            show_help()
        else:
            execute_command(
                calculator,
                command,
                args[1:]
            )

    # Calculator++ own prompt
    while True:

        try:
            user_input = input(
                f"{Fore.MAGENTA}"
                f"{TOOL_NAME}"
                f"{Style.RESET_ALL}"
                f"{Fore.YELLOW} ❯ {Style.RESET_ALL}"
            ).strip()

        except KeyboardInterrupt:
            print(
                f"\n{Fore.YELLOW}"
                "  Returning to N-Toolkit..."
                f"{Style.RESET_ALL}\n"
            )
            return True

        except EOFError:
            return True

        if not user_input:
            continue

        parts = user_input.split()

        command = parts[0].lower()
        command_args = parts[1:]

        # Leave Calculator++
        if command in ("exit", "quit", "q"):
            print(
                f"\n{Fore.CYAN}"
                "  Returning to N-Toolkit..."
                f"{Style.RESET_ALL}\n"
            )
            return True

        if command in ["help", "?"]:
            show_help()
            continue

        if command == "clear":
            os.system(
                "clear"
                if os.name == "posix"
                else "cls"
            )
            continue

        execute_command(
            calculator,
            command,
            command_args
        )