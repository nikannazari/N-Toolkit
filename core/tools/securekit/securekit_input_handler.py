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
securekit = _load_module("securekit.py" , "securekit_core")
validators = _load_module("securekit_validators.py" , "securekit_validators")

def show_help():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  SecureKit Tool Help{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}")

    print(f"  {Fore.MAGENTA}Commands:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}hash{Style.RESET_ALL}                      Generate file or text hashes")
    print(f"  {Fore.YELLOW}password{Style.RESET_ALL}                  Generate a secure password")
    print(f"  {Fore.YELLOW}encrypt{Style.RESET_ALL}                   Encrypt files or text")
    print(f"  {Fore.YELLOW}decrypt{Style.RESET_ALL}                   Decrypt files or text")
    print(f"  {Fore.YELLOW}ssh-key{Style.RESET_ALL}                   Generate or manage SSH keys")
    print(f"  {Fore.YELLOW}gpg{Style.RESET_ALL}                       Manage GPG encryption and keys")
    print(f"  {Fore.YELLOW}certificate{Style.RESET_ALL}               Inspect certificate information")
    print(f"  {Fore.YELLOW}integrity{Style.RESET_ALL}                 Check file integrity using hashes")
    print(f"  {Fore.YELLOW}permissions{Style.RESET_ALL}               Check file and directory permissions")

    print(f"\n  {Fore.MAGENTA}System:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}help{Style.RESET_ALL}                      Show this help")
    print(f"  {Fore.YELLOW}clear{Style.RESET_ALL}                     Clear screen")
    print(f"  {Fore.YELLOW}exit{Style.RESET_ALL}                      Return to N-Toolkit")

    print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}\n")
    
