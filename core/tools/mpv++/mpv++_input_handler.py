"""
mpv++_input_handler.py - N-Toolkit entry point for mpv++.
"""
import os
import sys
import importlib.util
from colorama import init as colorama_init, Fore, Style

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
TOOL_NAME = "mpv++"

def _load_module(filename, module_name):
    """Helper to dynamically load the tool's core logic."""
    filepath = os.path.join(TOOL_DIR, filename)
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Load the core mpv++ logic
mpv = _load_module("mpv++.py", "mpv_core")

def start(args: list):
    """
    Entry point called by N-Toolkit.
    """
    mpv.ensure_config()
    mpv.banner()
    
    if not mpv.ensure_mpv():
        mpv.warn("'mpv' binary not found. Install it before playing.")
    
    # Handle args if passed directly from N-Toolkit
    # e.g., N-Toolkit ❯ run mpv++ random music ~/Music
    if args:
        parsed = mpv.parse(" ".join(args))
        if parsed:
            cmd, cmd_args = parsed
            if cmd in ("exit", "quit", "q"):
                return True
            exit_signal = mpv.dispatch(cmd, cmd_args)
            if exit_signal:
                return True
    
    # mpv++ own prompt loop
    while True:
        try:
            raw = input(
                f"{Fore.GREEN}"
                f"{TOOL_NAME}"
                f"{Style.RESET_ALL}"
                f"{Fore.CYAN} ❯ {Style.RESET_ALL}"
            ).strip()

        except (EOFError, KeyboardInterrupt):
            print(f"\n{Fore.CYAN}  Returning to N-Toolkit...{Style.RESET_ALL}\n")
            return True
            
        parsed = mpv.parse(raw)
        if parsed is None:
            continue
            
        cmd, cmd_args = parsed
        
        if cmd in ("exit", "quit", "q"):
            print(f"\n{Fore.CYAN}  Returning to N-Toolkit...{Style.RESET_ALL}\n")
            return True
            
        try:
            exit_signal = mpv.dispatch(cmd, cmd_args)
            if exit_signal:
                print(f"\n{Fore.CYAN}  Returning to N-Toolkit...{Style.RESET_ALL}\n")
                return True
        except KeyboardInterrupt:
            print(); mpv.warn("Interrupted.")