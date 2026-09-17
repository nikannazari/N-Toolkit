"""
input_redirector.py - Loads and starts individual tools.
"""

import importlib.util
import os

from colorama import Fore, Style

from src.constants.commands import FRAMEWORK_NAME


def redirect_to_tool(tool_name: str, args: list) -> bool:
    """
    Load the tool-specific input handler and transfer control to it.
    """

    tool_dir = os.path.join(
        "core",
        "tools",
        tool_name
    )

    handler_file = os.path.join(
        tool_dir,
        f"{tool_name}_input_handler.py"
    )

    if not os.path.exists(handler_file):
        print(
            f"{Fore.RED}"
            f"  [Error] Input handler not found at:"
            f" {handler_file}"
            f"{Style.RESET_ALL}\n"
        )
        return False

    try:
        # Dynamically load the tool input handler.
        spec = importlib.util.spec_from_file_location(
            f"{tool_name}_input_handler",
            handler_file
        )

        if spec is None or spec.loader is None:
            print(
                f"{Fore.RED}"
                f"  [Error] Could not load input handler."
                f"{Style.RESET_ALL}\n"
            )
            return False

        handler_module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(handler_module)

        # Every tool input handler must provide start().
        if not hasattr(handler_module, "start"):
            print(
                f"{Fore.RED}"
                f"  [Error] '{tool_name}_input_handler.py' "
                f"must contain a start() function."
                f"{Style.RESET_ALL}\n"
            )
            return False

        print(
            f"{Fore.GREEN}"
            f"  ✓ {tool_name} loaded."
            f"{Style.RESET_ALL}\n"
        )

        # Transfer control to the tool.
        result = handler_module.start(args)

        print(
            f"\n{Fore.GREEN}"
            f"  ✓ Returning to {FRAMEWORK_NAME}."
            f"{Style.RESET_ALL}\n"
        )

        return True if result is None else bool(result)

    except Exception as e:
        print(
            f"{Fore.RED}"
            f"  [Error] An exception occurred while running "
            f"'{tool_name}': {e}"
            f"{Style.RESET_ALL}\n"
        )

        return False