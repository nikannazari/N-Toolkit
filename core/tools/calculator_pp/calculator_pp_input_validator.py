"""
calculator_pp_input_validator.py - Self-contained validator for the calculator++ tool.
"""
from colorama import Fore, Style

def validate(args: list) -> tuple[bool, str]:
    """
    Validates the arguments specific to Calculator++.
    Returns: (is_valid, message)
    """
    if not args:
        return False, "No arguments provided. Usage: run calculator++ ui | run calculator++ <num> <op> <num>"

    # If the user wants to launch the web UI
    if args[0].lower() == "ui":
        return True, "UI_MODE"

    # If the user wants CLI execution (e.g., run calculator++ 5 + 3)
    if len(args) != 3:
        return False, "CLI usage: run calculator++ <num1> <operator> <num2>"

    try:
        float(args[0])
        float(args[2])
    except ValueError:
        return False, "First and third arguments must be numbers."

    if args[1] not in ["+", "-", "*", "/"]:
        return False, f"Invalid operator '{args[1]}'. Use +, -, *, /"

    return True, "CLI_MODE"