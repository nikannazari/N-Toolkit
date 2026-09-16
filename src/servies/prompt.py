"""
prompt.py - Interactive prompt and command dispatcher.
"""

import os
import sys
from colorama import Fore, Style, init

# Import from our new modules
from src.commands import BUILTIN_COMMANDS, AVAILABLE_TOOLS, FRAMEWORK_NAME
from src.servies.input_handler import handle_input

init(autoreset=True)

PROMPT_TEXT = f"{Fore.GREEN}{FRAMEWORK_NAME}{Style.RESET_ALL}{Fore.CYAN} ❯{Style.RESET_ALL} "

def show_options() -> None:
    """Displays the available commands in a formatted layout."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  ╭──────── AVAILABLE OPTIONS ────────╮{Style.RESET_ALL}")
    
    cmd_width = max(len(cmd) for cmd in BUILTIN_COMMANDS.keys()) + 2
    
    for cmd, desc in BUILTIN_COMMANDS.items():
        formatted_cmd = f"{Fore.YELLOW}{cmd.ljust(cmd_width)}"
        formatted_desc = f"{Fore.WHITE}{desc}"
        print(f"  {Fore.CYAN}│{Style.RESET_ALL} {formatted_cmd} {formatted_desc}")
        
    print(f"{Fore.CYAN}{Style.BRIGHT}  ╰───────────────────────────────────╯{Style.RESET_ALL}\n")

def show_tools_list() -> None:
    """Displays the available tools from constants."""
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}  ⚙ INSTALLED TOOLS{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}{'─' * 35}{Style.RESET_ALL}")
    
    for tool in AVAILABLE_TOOLS:
        print(f"  {Fore.GREEN}▸ {Fore.WHITE}{tool}")
        
    print(f"  {Fore.MAGENTA}{'─' * 35}{Style.RESET_ALL}\n")

def start_prompt() -> None:
    """The main loop that waits for user input and dispatches commands."""
    history = []
    
    while True:
        try:
            user_input = input(PROMPT_TEXT).strip()
            
            if not user_input:
                continue
                
            history.append(user_input)
            parts = user_input.lower().split()
            main_cmd = parts[0]
            
            # ─────────────────────────────────────
            # Built-in Commands Handling
            # ─────────────────────────────────────
            if main_cmd in ["exit", "quit"]:
                print(f"\n{Fore.YELLOW}  [!] Shutting down framework safely...{Style.RESET_ALL}")
                sys.exit(0)
                
            elif main_cmd == "help":
                show_options()
                
            elif main_cmd == "tools":
                show_tools_list()
                
            elif main_cmd == "clear":
                os.system("clear" if os.name == "posix" else "cls")
                
            elif main_cmd == "history":
                print(f"\n{Fore.CYAN}  Command History:{Style.RESET_ALL}")
                for idx, cmd in enumerate(history, 1):
                    print(f"  {Fore.LIGHTBLACK_EX}{idx}.{Style.RESET_ALL} {cmd}")
                print()
                
            # ─────────────────────────────────────
            # Delegate to Input Handler (Tools & Errors)
            # ─────────────────────────────────────
            else:
                handle_input(user_input)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}  [!] Interrupted. Type 'exit' to quit.{Style.RESET_ALL}")
            
        except EOFError:
            print(f"\n{Fore.YELLOW}  [!] EOF received. Exiting...{Style.RESET_ALL}")
            sys.exit(0)

if __name__ == "__main__":
    show_options()
    start_prompt()