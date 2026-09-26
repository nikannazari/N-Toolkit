"""
archiver_input_handler.py - N-Toolkit entry point for Archiver.
"""
import os
import importlib.util
from colorama import init as colorama_init, Fore, Style
import pyfiglet

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_module(filename, module_name):
    filepath = os.path.join(TOOL_DIR, filename)
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

archiver = _load_module("archiver.py", "archiver_core")
validators = _load_module("archiver_validators.py", "archiver_validators")

def show_help():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  Archiver Tool Help{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}")
    
    print(f"  {Fore.MAGENTA}Commands:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}compress <src> <name> <fmt> [pass]{Style.RESET_ALL}")
    print(f"          Compress a file/folder.")
    print(f"          Formats: zip, 7z, rar, tar.gz")
    
    print(f"  {Fore.YELLOW}extract <archive> [dest] [pass]{Style.RESET_ALL}")
    print(f"          Extract an archive.")
    
    print(f"\n  {Fore.MAGENTA}Examples:{Style.RESET_ALL}")
    print(f"  {Fore.LIGHTBLACK_EX}compress myfile.txt mybackup zip{Style.RESET_ALL}")
    print(f"  {Fore.LIGHTBLACK_EX}compress myfolder backup 7z mySecretPass{Style.RESET_ALL}")
    print(f"  {Fore.LIGHTBLACK_EX}extract backup.7z ./out_dir mySecretPass{Style.RESET_ALL}")
    
    print(f"\n  {Fore.MAGENTA}System:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}help{Style.RESET_ALL}          Show this help")
    print(f"  {Fore.YELLOW}clear{Style.RESET_ALL}         Clear screen")
    print(f"  {Fore.YELLOW}exit{Style.RESET_ALL}          Return to N-Toolkit")
    print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}\n")

def execute_command(command: str, args: list):
    if command == "compress":
        if len(args) < 3:
            archiver.err("Usage: compress <source> <archive_name> <format> [password]")
            return
        source = args[0]
        name = args[1]
        fmt = args[2].lower()
        password = args[3] if len(args) > 3 else None
        
        ok_, src_path = validators.validate_path(source)
        if ok_:
            archiver.compress(src_path, name, fmt, password)

    elif command == "extract":
        if len(args) < 1:
            archiver.err("Usage: extract <archive_file> [destination] [password]")
            return
        archive = args[0]
        dest = args[1] if len(args) > 1 else "."
        password = args[2] if len(args) > 2 else None
        
        ok_, arch_path = validators.validate_path(archive)
        ok_d, dest_path = validators.validate_output_dir(dest)
        if ok_ and ok_d:
            archiver.extract(arch_path, dest_path, password)

    else:
        archiver.err(f"Unknown command: {command}. Type 'help' for commands.")

def start(args: list):
    """Entry point called by N-Toolkit."""
    art = pyfiglet.figlet_format("Archiver", font="slant")
    palette = [Fore.RED, Fore.MAGENTA, Fore.BLUE, Fore.CYAN]
    for i, line in enumerate(art.splitlines()):
        print(f"{palette[i % len(palette)]}{line}{Style.RESET_ALL}")

    print(f"{Fore.MAGENTA}{Style.BRIGHT}\n  ╭──────────── Archiver Tool ─────────────╮{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'help' for commands.              │{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'exit' to return to N-Toolkit.    │{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  ╰─────────────────────────────────────────╯{Style.RESET_ALL}\n")

    if args:
        command = args[0].lower()
        if command in ("help", "?"):
            show_help()
        else:
            execute_command(command, args[1:])

    while True:
        try:
            user_input = input(
                f"{Fore.MAGENTA}archiver{Style.RESET_ALL}{Fore.YELLOW} ❯ {Style.RESET_ALL}"
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