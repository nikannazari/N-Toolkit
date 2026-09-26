"""
archiver_validators.py - Validation utilities for Archiver tool.
"""
import os
import shutil
from colorama import Fore, Style

def validate_path(path: str) -> tuple[bool, str]:
    if not path or not path.strip():
        return False, "Path is empty."
    path = os.path.expanduser(path.strip())
    if not os.path.exists(path):
        return False, f"Path not found: {path}"
    return True, os.path.abspath(path)

def validate_output_dir(path: str) -> tuple[bool, str]:
    if not path or not path.strip():
        return True, os.getcwd() # Default to current dir
    path = os.path.expanduser(path.strip())
    if not os.path.isdir(path):
        return False, f"Output directory does not exist: {path}"
    return True, os.path.abspath(path)

def ensure_tool_installed(tool_name: str) -> bool:
    """Checks if a system binary like 'zip' or '7z' is installed."""
    if shutil.which(tool_name) is None:
        print(f"{Fore.RED}  [Error] System utility '{tool_name}' is not installed.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Please install it via your package manager (e.g., sudo apt install {tool_name}).{Style.RESET_ALL}")
        return False
    return True