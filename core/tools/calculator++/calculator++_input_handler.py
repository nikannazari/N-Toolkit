"""
calculator++_input_handler.py - CLI and prompt for Calculator++.
"""

import importlib.util
import os

from colorama import Fore, Style


TOOL_NAME = "calculator++"


def load_calculator():
    """
    Dynamically load calculator++.py.

    The tool name contains '++', which is not valid in a normal
    Python import statement.
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))

    calculator_path = os.path.join(
        current_dir,
        "calculator++.py"
    )

    spec = importlib.util.spec_from_file_location(
        "calculator_core",
        calculator_path
    )

    if spec is None or spec.loader is None:
        raise ImportError(
            "Could not load calculator++.py"
        )

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return module.Calculator


def show_help() -> None:
    """Display Calculator++ commands."""

    print()
    print(
        f"{Fore.CYAN}{Style.BRIGHT}"
        "  Calculator++ Commands"
        f"{Style.RESET_ALL}"
    )

    print(
        f"  {Fore.YELLOW}add <a> <b>"
        f"{Style.RESET_ALL}       Add two numbers"
    )

    print(
        f"  {Fore.YELLOW}sub <a> <b>"
        f"{Style.RESET_ALL}       Subtract two numbers"
    )

    print(
        f"  {Fore.YELLOW}mul <a> <b>"
        f"{Style.RESET_ALL}       Multiply two numbers"
    )

    print(
        f"  {Fore.YELLOW}div <a> <b>"
        f"{Style.RESET_ALL}       Divide two numbers"
    )

    print(
        f"  {Fore.YELLOW}clear"
        f"{Style.RESET_ALL}             Clear screen"
    )

    print(
        f"  {Fore.YELLOW}help"
        f"{Style.RESET_ALL}              Show this help"
    )

    print(
        f"  {Fore.YELLOW}exit / quit / q"
        f"{Style.RESET_ALL}  Return to N-Toolkit"
    )

    print()


def execute_command(
    calculator,
    command: str,
    args: list[str]
) -> None:
    """
    Execute a Calculator++ command.
    """

    if command in ("add", "sub", "mul", "div"):

        if len(args) != 2:
            print(
                f"{Fore.RED}"
                f"  Usage: {command} <number> <number>"
                f"{Style.RESET_ALL}"
            )
            return

        try:
            a = float(args[0])
            b = float(args[1])

        except ValueError:
            print(
                f"{Fore.RED}"
                "  [Error] Arguments must be numbers."
                f"{Style.RESET_ALL}"
            )
            return

        try:
            if command == "add":
                result = calculator.add(a, b)

            elif command == "sub":
                result = calculator.subtract(a, b)

            elif command == "mul":
                result = calculator.multiply(a, b)

            else:
                result = calculator.divide(a, b)

            print(
                f"{Fore.GREEN}"
                f"  Result: {result}"
                f"{Style.RESET_ALL}"
            )

        except ZeroDivisionError as e:
            print(
                f"{Fore.RED}"
                f"  [Error] {e}"
                f"{Style.RESET_ALL}"
            )

        return

    print(
        f"{Fore.RED}"
        f"  Unknown command: {command}"
        f"{Style.RESET_ALL}"
    )


def start(args: list[str] | None = None) -> bool:
    """
    Start the Calculator++ CLI.

    This function is the entry point expected by N-Toolkit.
    """

    calculator = load_calculator()

    print(
        f"{Fore.MAGENTA}{Style.BRIGHT}"
        "\n  ╭────────────── Calculator++ ──────────────╮"
        f"{Style.RESET_ALL}"
    )

    print(
        f"{Fore.MAGENTA}"
        "  │ Type 'help' for available commands.       │"
        f"{Style.RESET_ALL}"
    )

    print(
        f"{Fore.MAGENTA}"
        "  │ Type 'exit' to return to N-Toolkit.       │"
        f"{Style.RESET_ALL}"
    )

    print(
        f"{Fore.MAGENTA}"
        "  ╰───────────────────────────────────────────╯"
        f"{Style.RESET_ALL}\n"
    )

    # If arguments were passed from N-Toolkit,
    # execute them as an initial command.
    if args:
        command = args[0].lower()
        command_args = args[1:]

        if command == "help":
            show_help()

        else:
            execute_command(
                calculator,
                command,
                command_args
            )

    while True:

        try:
            user_input = input(
                f"{Fore.GREEN}"
                f"{TOOL_NAME}"
                f"{Style.RESET_ALL}"
                f"{Fore.CYAN} ❯ {Style.RESET_ALL}"
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

        if command in ("exit", "quit", "q"):
            print(
                f"\n{Fore.CYAN}"
                "  Returning to N-Toolkit..."
                f"{Style.RESET_ALL}"
            )
            return True

        if command == "help":
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