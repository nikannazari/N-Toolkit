"""
input_redirector.py - Loads and launches individual tools.
"""

import importlib.util
import os

from colorama import Fore, Style

from src.constants.commands import FRAMEWORK_NAME


def redirect_to_tool(tool_name: str, args: list[str]) -> bool:
    """
    Loads the requested tool's input handler and transfers control to it.

    Every tool is responsible for its own:
        - prompt
        - input handling
        - validation
        - commands
        - execution
    """

    tool_dir = os.path.join("core", "tools", tool_name)

    input_handler_path = os.path.join(
        tool_dir,
        f"{tool_name}_input_handler.py"
    )

    if not os.path.isfile(input_handler_path):
        print(
            f"{Fore.RED}"
            f"  [Error] Input handler not found:"
            f" {input_handler_path}"
            f"{Style.RESET_ALL}\n"
        )
        return False

    try:
        # Create a unique module name for dynamic loading.
        module_name = f"{tool_name}_input_handler"

        spec = importlib.util.spec_from_file_location(
            module_name,
            input_handler_path
        )

        if spec is None or spec.loader is None:
            print(
                f"{Fore.RED}"
                f"  [Error] Could not load input handler for "
                f"'{tool_name}'."
                f"{Style.RESET_ALL}\n"
            )
            return False

        handler_module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(handler_module)

        # Every tool must expose a `start()` function.
        if not hasattr(handler_module, "start"):
            print(
                f"{Fore.RED}"
                f"  [Error] Tool '{tool_name}' does not provide "
                f"a start() function."
                f"{Style.RESET_ALL}\n"
            )
            return False

        print(
            f"{Fore.GREEN}"
            f"  ✓ {tool_name} loaded successfully."
            f"{Style.RESET_ALL}\n"
        )

        # Transfer control completely to the tool.
        result = handler_module.start(args)

        print(
            f"\n{Fore.GREEN}"
            f"  ✓ Returning to {FRAMEWORK_NAME}."
            f"{Style.RESET_ALL}\n"
        )

        return bool(result) if result is not None else True

    except Exception as e:
        print(
            f"{Fore.RED}"
            f"  [Error] Failed to launch '{tool_name}': {e}"
            f"{Style.RESET_ALL}\n"
        )

        return False