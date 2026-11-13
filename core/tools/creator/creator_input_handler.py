"""
creator_input_handler.py - N-toolkit entry point for Creator Tool
"""

import sys
import os
import importlib.util
import pyfiglet
import shlex

from colorama import Fore , Style   


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


creator = _load_module("creator.py" , "creator_core")
validator = _load_module("creator_validators.py" , "creator_validator")


def execute_command(command: str , args: list):
    pass


def show_help():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Creator Tool Help{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}")

    print(f"  {Fore.MAGENTA}Commads:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}python{Style.RESET_ALL}                    Create a Python project")
    print(f"  {Fore.YELLOW}django{Style.RESET_ALL}                    Create a Django project")
    print(f"  {Fore.YELLOW}flask{Style.RESET_ALL}                     Create a Flask project")
    print(f"  {Fore.YELLOW}fastapi{Style.RESET_ALL}                   Create a FastAPI project")
    print(f"  {Fore.YELLOW}react{Style.RESET_ALL}                     Create a React project")
    print(f"  {Fore.YELLOW}vue{Style.RESET_ALL}                       Create a Vue project")
    print(f"  {Fore.YELLOW}node{Style.RESET_ALL}                      Create a Node.js project")
    print(f"  {Fore.YELLOW}rust{Style.RESET_ALL}                      Create a Rust project")
    print(f"  {Fore.YELLOW}cpp{Style.RESET_ALL}                       Create a C++ project")
    print(f"  {Fore.YELLOW}cli{Style.RESET_ALL}                       Create a CLI tool project")

    print(f"\n  {Fore.MAGENTA}System:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}help{Style.RESET_ALL}                      Show this help")
    print(f"  {Fore.YELLOW}clear{Style.RESET_ALL}                     Clear screen")
    print(f"  {Fore.YELLOW}exit{Style.RESET_ALL}                      Return to N-Toolkit")

    print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}\n")


def start(args: list):
    """Entry point called by N-Toolkit."""
    
    art = pyfiglet.figlet_format("Creator", font="slant")
    palette = [Fore.RED, Fore.MAGENTA, Fore.BLUE, Fore.CYAN]
    for i, line in enumerate(art.splitlines()):
        print(f"{palette[i % len(palette)]}{line}{Style.RESET_ALL}")

    print(f"{Fore.MAGENTA}{Style.BRIGHT}\n  ╭──────────── Creator Tool ──────────────╮{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'help' for commands.              │{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'exit' to return to N-Toolkit     │{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  ╰────────────────────────────────────────╯{Style.RESET_ALL}\n")

    if args:
        command = args[0].lower()
        if command in ("help", "?"):
            show_help()
        else:
            execute_command(command, args[1:])

    creator_input = CustomInput()
    
    while True:
        try:
            prompt = f"{Fore.MAGENTA}Creator{Style.RESET_ALL}{Fore.YELLOW} ❯ {Style.RESET_ALL}"
                
            user_input = creator_input.get_input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Fore.CYAN}  Returning to N-Toolkit...{Style.RESET_ALL}\n")
            return True

        if not user_input:
            continue
        
        parts = shlex.split(user_input)
        command = parts[0].lower()
        command_args = parts[1:]
        
        if command in ["exit" , "quit" , "q"]:
            print(f"\n{Fore.CYAN}  Returning to N-Toolkit...{Style.RESET_ALL}\n")
            return True
        
        if command in ["help" , "?"]:
            show_help()
            continue
        
        if command == "clear":
            os.system("clear" if os.name == "posix" else "cls")    
            continue

        execute_command(command , command_args)
