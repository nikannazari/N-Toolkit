"""
securekit_input_handler.py - N-toolkit entry point for Secure ToolKit
"""
import os
import sys
import importlib.util
from colorama import init as colorama_init , Fore , Style

# Add project root to sys.path so we can import CustomInput
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from src.services.custom_input import CustomInput

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_module(filename , module_name):
    """Helper to dynamically load the tool's core logic."""
    filepath = os.path.join(TOOL_DIR, filename)
    spec = importlib.util.spec_from_file_location(module_name,filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

#load the core securekit logic