"""
input_handler.py - Handles tool execution requests.
"""

import time

from colorama import Fore, Style

from src.validators.tool_validators import validate_tool_exists
from src.services.input_redirector import redirect_to_tool


def handle_input(user_input: str) -> bool:
    """
    Processes input that isn't a built-in framework command.

    Framework syntax:

        run <tool> [args...]

    Example:

        run calculator++
        run calculator++ add 10 20

    Tool-specific input handling is delegated to the tool itself.
    """

    parts = user_input.strip().split()

    if not parts:
        return False

    # Framework expects:
    #
    # run <tool> [args...]
    #
    if parts[0].lower() != "run":
        print(
            f"{Fore.RED}"
            "  [Error] Unknown framework command."
            f"{Style.RESET_ALL}"
        )

        print(
            f"{Fore.YELLOW}"
            "  Usage: run <tool> [args...]"
            f"{Style.RESET_ALL}\n"
        )

        return False

    # Check that a tool name was provided.
    if len(parts) < 2:
        print(
            f"{Fore.RED}"
            "  [Error] Missing tool name."
            f"{Style.RESET_ALL}"
        )

        print(
            f"{Fore.YELLOW}"
            "  Usage: run <tool> [args...]"
            f"{Style.RESET_ALL}\n"
        )

        return False

    tool_name = parts[1]
    args = parts[2:]

    # Validate tool existence.
    if not validate_tool_exists(tool_name):
        print(
            f"{Fore.RED}{Style.BRIGHT}"
            "  ╭─ [ERROR] Tool Not Found ───────────────╮"
            f"{Style.RESET_ALL}"
        )

        print(
            f"{Fore.RED}"
            f"  │ The tool '{Fore.WHITE}{tool_name}"
            f"{Fore.RED}' is not recognized.   │"
            f"{Style.RESET_ALL}"
        )

        print(
            f"{Fore.RED}"
            "  ╰────────────────────────────────────────╯"
            f"{Style.RESET_ALL}"
        )

        print(
            f"{Fore.YELLOW}"
            "  💡 Tip: Type 'tools' to see available tools."
            f"{Style.RESET_ALL}\n"
        )

        return False

    # Framework-level routing message.
    print(
        f"{Fore.CYAN}"
        f"  → Routing to {Fore.WHITE}{tool_name}"
        f"{Fore.CYAN}..."
        f"{Fore.GREEN} ✓ Validated"
        f"{Style.RESET_ALL}"
    )

    time.sleep(0.3)

    # Transfer control to the tool.
    return redirect_to_tool(tool_name, args)