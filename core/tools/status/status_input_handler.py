"""
status_input_handler.py - N-Toolkit entry point for Status.
"""
import os
import sys
import time
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

status = _load_module("status.py", "status_core")
validators = _load_module("status_validators.py", "status_validators")

def show_help():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  Status Tool Help{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}{'─' * 45}{Style.RESET_ALL}")
    
    print(f"  {Fore.MAGENTA}Commands:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}all{Style.RESET_ALL}                Show all system stats")
    print(f"  {Fore.YELLOW}cpu{Style.RESET_ALL}                Show CPU usage")
    print(f"  {Fore.YELLOW}ram{Style.RESET_ALL}                Show Memory usage")
    print(f"  {Fore.YELLOW}gpu{Style.RESET_ALL}                Show GPU usage (NVIDIA only)")
    print(f"  {Fore.YELLOW}disk{Style.RESET_ALL}               Show Disk usage")
    print(f"  {Fore.YELLOW}net{Style.RESET_ALL}                Show Network usage")
    print(f"  {Fore.YELLOW}battery{Style.RESET_ALL}            Show Battery status")
    print(f"  {Fore.YELLOW}fans{Style.RESET_ALL}               Show Fans speed")
    print(f"  {Fore.YELLOW}temp{Style.RESET_ALL}               Show Temperatures")
    print(f"  {Fore.YELLOW}procs{Style.RESET_ALL}              Show Top Processes")
    print(f"  {Fore.YELLOW}watch <cmd> [secs]{Style.RESET_ALL} Live monitor (e.g., watch all 2)")
    
    print(f"\n  {Fore.MAGENTA}System:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}help{Style.RESET_ALL}               Show this help")
    print(f"  {Fore.YELLOW}clear{Style.RESET_ALL}              Clear screen")
    print(f"  {Fore.YELLOW}exit{Style.RESET_ALL}               Return to N-Toolkit")
    print(f"  {Fore.YELLOW}{'─' * 45}{Style.RESET_ALL}\n")

def execute_command(command: str, args: list):
    cmd_map = {
        "all": status.show_all,
        "cpu": status.show_cpu,
        "ram": status.show_ram,
        "gpu": status.show_gpu,
        "disk": status.show_disk,
        "net": status.show_network,
        "network": status.show_network,
        "battery": status.show_battery,
        "fans": status.show_fans,
        "temp": status.show_temp,
        "procs": status.show_procs,
    }

    if command in cmd_map:
        cmd_map[command]()
        return

    elif command == "watch":
        if not args:
            status.err("Usage: watch <cmd> [secs] (e.g., watch all 2)")
            return
            
        target_cmd = args[0]
        if target_cmd not in cmd_map:
            status.err(f"Unknown watch target: {target_cmd}")
            return
            
        secs = 2
        if len(args) > 1:
            ok_, res = validators.validate_interval(args[1])
            if ok_:
                secs = res
            else:
                status.err(res)
                return
                
        status.info(f"Live monitoring {target_cmd} every {secs}s. Press Ctrl+C to stop.")
        try:
            while True:
                os.system("clear" if os.name == "posix" else "cls")
                print(f"{Fore.CYAN}Live Status (Press Ctrl+C to exit){Style.RESET_ALL}\n")
                cmd_map[target_cmd]()
                time.sleep(secs)
        except KeyboardInterrupt:
            status.info("Live monitoring stopped.")
            print()
            
    else:
        status.err(f"Unknown command: {command}. Type 'help' for commands.")

def start(args: list):
    """Entry point called by N-Toolkit."""
    art = pyfiglet.figlet_format("Status", font="slant")
    palette = [Fore.RED, Fore.MAGENTA, Fore.BLUE, Fore.CYAN]
    for i, line in enumerate(art.splitlines()):
        print(f"{palette[i % len(palette)]}{line}{Style.RESET_ALL}")

    print(f"{Fore.MAGENTA}{Style.BRIGHT}\n  ╭──────────── Status Tool ──────────────╮{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'help' for commands.             │{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'exit' to return to N-Toolkit.   │{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  ╰────────────────────────────────────────╯{Style.RESET_ALL}\n")

    if args:
        command = args[0].lower()
        if command in ("help", "?"):
            show_help()
        else:
            execute_command(command, args[1:])

    status_input = CustomInput()

    while True:
        try:
            user_input = status_input.get_input(
                f"{Fore.MAGENTA}status{Style.RESET_ALL}{Fore.YELLOW} ❯ {Style.RESET_ALL}"
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