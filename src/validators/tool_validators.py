"""
tool_validators.py - Checks if a requested tool exists in the framework.
"""
import os
from constants.commands import AVAILABLE_TOOLS

def validate_tool_exists(tool_name: str) -> bool:
    """Checks if the tool is in the available tools list."""
    return tool_name in AVAILABLE_TOOLS

def get_tool_path(tool_name: str) -> str:
    """Returns the expected file path for the tool."""
    # Convert special chars like ++ to _ for python module names
    safe_name = tool_name.replace("++", "_pp").replace("-", "_")
    return os.path.join("core", "tools", f"{safe_name}.py")