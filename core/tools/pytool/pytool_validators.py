"""
pytool_validators.py - Validation utilities for PyTool.
"""
import shutil
import sys
import subprocess
from colorama import Fore, Style

def validate_script(path: str) -> tuple[bool, str]:
    if not path or not path.strip():
        return False, "Script path is empty."
    path = path.strip()
    if not path.endswith('.py'):
        return False, "File must be a Python script (.py)."
    if not __import__('os').path.exists(path):
        return False, f"File not found: {path}"
    return True, path

def ensure_tool_installed(tool_name: str, pip_pkg: str = None) -> bool:
    """Checks if a system binary or python module is installed."""
    if shutil.which(tool_name) is None:
        print(f"{Fore.RED}  [Error] '{tool_name}' is not installed.{Style.RESET_ALL}")
        if pip_pkg:
            print(f"{Fore.YELLOW}  Install it with: pip install {pip_pkg}{Style.RESET_ALL}")
        return False
    return True