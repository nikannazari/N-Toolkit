"""
calculator_pp_input_validator.py - Validator for the calculator++ tool.
"""
from colorama import Fore, Style

def validate(args: list) -> tuple[bool, str]:
    """
    Validates the arguments. For now, we ignore args and just start the UI.
    """
    # We don't parse CLI args anymore, just tell the redirector to start
    return True, "START_UI"