"""
qr_validators.py - Validation utilities for QR tool.
"""
import os
from colorama import Fore, Style

def validate_file(path: str) -> tuple[bool, str]:
    if not path or not path.strip():
        return False, "Path is empty."
    path = os.path.expanduser(path.strip())
    if not os.path.exists(path):
        return False, f"File not found: {path}"
    if not os.path.isfile(path):
        return False, f"Not a file: {path}"
    return True, os.path.abspath(path)

def validate_directory(path: str) -> tuple[bool, str]:
    if not path or not path.strip():
        return False, "Path is empty."
    path = os.path.expanduser(path.strip())
    if not os.path.exists(path):
        return False, f"Directory not found: {path}"
    if not os.path.isdir(path):
        return False, f"Not a directory: {path}"
    return True, os.path.abspath(path)

def validate_text(text: str) -> tuple[bool, str]:
    if not text or not text.strip():
        return False, "Text/URL cannot be empty."
    return True, text.strip()