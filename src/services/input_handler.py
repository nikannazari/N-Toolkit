"""
input_handler.py - Handles framework-level tool launching.
"""

from colorama import Fore, Style

from src.validators.tool_validators import validate_tool_exists
from src.services.input_redirector import redirect_to_tool


def handle_input(user_input: str) -> bool:
    """
    Handles input that is not a built-in framework command.

    The framework only determines which tool the user wants to launch.
    Tool-specific input handling is completely delegated to the tool itself.
    """

    parts = user_input.strip().split()

    if not parts:
        return False

    tool_name = parts[0]
    args = parts[1:]

    # Check if the requested tool exists.
    if not validate_tool_exists(tool_name):
        print(
            f"{Fore.RED}{Style.BRIGHT}"
            f"  ╭─ [ERROR] Tool Not Found ───────────────╮"
            f"{Style.RESET_ALL}"
        )

        print(
            f"{Fore.RED}  │ The tool '{Fore.WHITE}{tool_name}"
            f"{Fore.RED}' is not recognized.   │"
            f"{Style.RESET_ALL}"
        )

        print(
            f"{Fore.RED}  ╰────────────────────────────────────────╯"
            f"{Style.RESET_ALL}"
        )

        print(
            f"{Fore.YELLOW}  💡 Tip: Type 'tools' to see available tools."
            f"{Style.RESET_ALL}\n"
        )

        return False

    print(
        f"{Fore.CYAN}  → Launching "
        f"{Fore.WHITE}{tool_name}"
        f"{Fore.CYAN}..."
        f"{Style.RESET_ALL}"
    )

    return redirect_to_tool(tool_name, args)