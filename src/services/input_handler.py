"""
input_handler.py - Handles tool execution requests.
"""

import time

from colorama import Fore, Style

from src.validators.prompt_validator import validate_prompt_syntax
from src.validators.tool_validators import validate_tool_exists
from src.services.input_redirector import redirect_to_tool


def handle_input(user_input: str) -> bool:
    """
    Processes input that isn't a built-in framework command.
    """

    # 1. Validate syntax
    is_valid, parsed_data, error_msg = validate_prompt_syntax(user_input)

    if not is_valid:
        print(
            f"{Fore.RED}  [Syntax Error] "
            f"{error_msg}{Style.RESET_ALL}\n"
        )
        return False

    tool_name, args = parsed_data

    # 2. Validate tool existence
    if not validate_tool_exists(tool_name):
        print(
            f"{Fore.RED}{Style.BRIGHT}"
            "  ╭─ [ERROR] Tool Not Found ───────────────╮"
            f"{Style.RESET_ALL}"
        )

        print(
            f"{Fore.RED}  │ The tool '{Fore.WHITE}{tool_name}"
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
            "  💡 Tip: Type 'tools' to see a list of "
            f"available tools."
            f"{Style.RESET_ALL}\n"
        )

        return False

    # 3. Small framework UI
    print(
        f"{Fore.CYAN}  → Routing to "
        f"{Fore.WHITE}{tool_name}"
        f"{Fore.CYAN}..."
        f"{Fore.GREEN} ✓ Validated"
        f"{Style.RESET_ALL}"
    )

    time.sleep(0.3)

    # 4. Give control to the tool
    return redirect_to_tool(tool_name, args)