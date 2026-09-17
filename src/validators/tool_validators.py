"""
tool_validators.py - Validates and locates N-Toolkit tools.
"""

import os

from constants.commands import AVAILABLE_TOOLS


def validate_tool_exists(tool_name: str) -> bool:
    """
    Check whether a tool is registered in N-Toolkit.
    """

    return tool_name in AVAILABLE_TOOLS


def get_tool_path(tool_name: str) -> str:
    """
    Return the main Python file path of a tool.
    """

    return os.path.join(
        "core",
        "tools",
        tool_name,
        f"{tool_name}.py"
    )


def get_tool_input_handler_path(tool_name: str) -> str:
    """
    Return the input handler path of a tool.
    """

    return os.path.join(
        "core",
        "tools",
        tool_name,
        f"{tool_name}_input_handler.py"
    )