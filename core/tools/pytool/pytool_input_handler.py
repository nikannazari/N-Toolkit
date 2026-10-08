"""
pytool_input_handler.py - N-Toolkit entry point for PyTool.
"""
import os
import sys
import importlib.util
from colorama import init as colorama_init, Fore, Style
import pyfiglet

# Add project root to sys.path so we can import CustomInput
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from src.services.custom_input import CustomInput

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_module(filename, module_name):
    filepath = os.path.join(TOOL_DIR, filename)
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

pytool = _load_module("pytool.py", "pytool_core")

def show_help():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  PyTool Help{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}")
    
    print(f"  {Fore.MAGENTA}Commands:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}venv [name]{Style.RESET_ALL}                Create virtual environment (default: .venv)")
    print(f"  {Fore.YELLOW}install [pkg]{Style.RESET_ALL}              Install from requirements.txt or a specific package")
    print(f"  {Fore.YELLOW}freeze{Style.RESET_ALL}                     Save current dependencies to requirements.txt")
    print(f"  {Fore.YELLOW}lint [files...]{Style.RESET_ALL}            Lint code with flake8 (default: current dir)")
    print(f"  {Fore.YELLOW}format [files...]{Style.RESET_ALL}          Format code with black (default: current dir)")
    print(f"  {Fore.YELLOW}run <script.py>{Style.RESET_ALL}            Run a Python script")
    print(f"  {Fore.YELLOW}package{Style.RESET_ALL}                    Build sdist and wheel using python-build")
    print(f"  {Fore.YELLOW}publish{Style.RESET_ALL}                    Upload package to PyPI using twine")
    
    print(f"\n  {Fore.MAGENTA}System:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}help{Style.RESET_ALL}                       Show this help")
    print(f"  {Fore.YELLOW}clear{Style.RESET_ALL}                      Clear screen")
    print(f"  {Fore.YELLOW}exit{Style.RESET_ALL}                       Return to N-Toolkit")
    print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}\n")

def execute_command(command: str, args: list):
    if command == "venv":
        venv_name = args[0] if args else ".venv"
        pytool.create_venv(venv_name)

    elif command == "install":
        target = args[0] if args else "."
        pytool.install_reqs(target)

    elif command == "freeze":
        pytool.freeze_reqs()

    elif command == "lint":
        pytool.lint(args)

    elif command == "format":
        pytool.format_code(args)

    elif command == "run":
        if not args:
            pytool.err("Usage: run <script.py>")
            return
        pytool.run_script(args[0])

    elif command == "package":
        pytool.package()

    elif command == "publish":
        pytool.publish()

    else:
        pytool.err(f"Unknown command: {command}. Type 'help' for commands.")

def start(args: list):
    """Entry point called by N-Toolkit."""
    art = pyfiglet.figlet_format("PyTool", font="slant")
    palette = [Fore.RED, Fore.MAGENTA, Fore.BLUE, Fore.CYAN]
    for i, line in enumerate(art.splitlines()):
        print(f"{palette[i % len(palette)]}{line}{Style.RESET_ALL}")

    print(f"{Fore.MAGENTA}{Style.BRIGHT}\n  ╭──────────── PyTool ──────────────╮{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'help' for commands.        │{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'exit' to return to N-Toolkit│{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  ╰──────────────────────────────────╯{Style.RESET_ALL}\n")

    if args:
        command = args[0].lower()
        if command in ("help", "?"):
            show_help()
        else:
            execute_command(command, args[1:])

    pytool_input = CustomInput()

    while True:
        try:
            user_input = pytool_input.get_input(
                f"{Fore.MAGENTA}pytool{Style.RESET_ALL}{Fore.YELLOW} ❯ {Style.RESET_ALL}"
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Fore.CYAN}  Returning to N-Toolkit...{Style.RESET_ALL}\n")
            return True

        if not user_input:
            continue

        parts = user_input.split()
        command = parts[0].lower()
        command_args = parts[1:]

        if command in ("exit", "quit", "q"):
            print(f"\n{Fore.CYAN}  Returning to N-Toolkit...{Style.RESET_ALL}\n")
            return True

        if command in ("help", "?"):
            show_help()
            continue

        if command == "clear":
            os.system("clear" if os.name == "posix" else "cls")
            continue

        execute_command(command, command_args)