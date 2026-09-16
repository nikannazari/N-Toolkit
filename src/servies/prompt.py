"""
prompt.py - Interactive prompt and command dispatcher for the framework.
Requires: colorama
"""

import os
import sys
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# ─────────────────────────────────────────────
# Temporary mock for input_handler 
# (Replace this with: from src.servies.input_handler import handle_input)
# ─────────────────────────────────────────────
def mock_input_handler(command: str) -> bool:
    """Temporary handler to simulate tool execution."""
    print(f"{Fore.LIGHTBLACK_EX}  [Mock Handler] Received command: '{command}'")
    print(f"{Fore.LIGHTBLACK_EX}  [Mock Handler] Executing logic...\n")
    return True

# Assign the mock handler (change this to your actual handler later)
input_handler = mock_input_handler


# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
PROMPT_TEXT = f"{Fore.GREEN}PyNIX{Style.RESET_ALL}{Fore.CYAN} ❯{Style.RESET_ALL} "

COMMANDS = {
    "help": "Show this help menu and available options",
    "tools": "List all available integrated tools",
    "run <tool>": "Execute a specific tool (e.g., run calculator++)",
    "clear": "Clear the terminal screen",
    "history": "Show command history (mock)",
    "exit": "Exit the framework safely"
}


# ─────────────────────────────────────────────
# Display Functions
# ─────────────────────────────────────────────
def show_options() -> None:
    """Displays the available commands in a formatted layout."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  ╭──────── AVAILABLE OPTIONS ────────╮{Style.RESET_ALL}")
    
    # Calculate column widths for nice alignment
    cmd_width = max(len(cmd) for cmd in COMMANDS.keys()) + 2
    
    for cmd, desc in COMMANDS.items():
        # Format the command and description
        formatted_cmd = f"{Fore.YELLOW}{cmd.ljust(cmd_width)}"
        formatted_desc = f"{Fore.WHITE}{desc}"
        
        print(f"  {Fore.CYAN}│{Style.RESET_ALL} {formatted_cmd} {formatted_desc}")
        
    print(f"{Fore.CYAN}{Style.BRIGHT}  ╰───────────────────────────────────╯{Style.RESET_ALL}\n")


def show_tools_list() -> None:
    """Displays the available tools (simulating the core/tools directory)."""
    tools = ["calculator++", "ffmpeg", "autogit", "sysinfo", "nettools", "filemanager"]
    
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}  ⚙ INSTALLED TOOLS{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}{'─' * 35}{Style.RESET_ALL}")
    
    for tool in tools:
        print(f"  {Fore.GREEN}▸ {Fore.WHITE}{tool}")
        
    print(f"  {Fore.MAGENTA}{'─' * 35}{Style.RESET_ALL}\n")


# ─────────────────────────────────────────────
# Core Prompt Loop
# ─────────────────────────────────────────────
def start_prompt() -> None:
    """The main loop that waits for user input and dispatches commands."""
    history = []
    
    while True:
        try:
            # Get input from user using the styled prompt
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
            # External Tools Handling
            # ─────────────────────────────────────
            elif main_cmd == "run" and len(parts) > 1:
                tool_name = user_input.split(" ", 1)[1] # Preserve original casing
                print(f"\n{Fore.CYAN}  → Launching {Fore.WHITE}{tool_name}{Fore.CYAN}...{Style.RESET_ALL}")
                # Here you would route to your input_redirector/tool_validator
                input_handler(tool_name)
                
            else:
                # Pass unknown commands to your input_handler or show error
                input_handler(user_input)
                
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print(f"\n{Fore.RED}  [!] Interrupted. Type 'exit' to quit.{Style.RESET_ALL}")
            
        except EOFError:
            # Handle Ctrl+D gracefully
            print(f"\n{Fore.YELLOW}  [!] EOF received. Exiting...{Style.RESET_ALL}")
            sys.exit(0)


# ─────────────────────────────────────────────
# Entry point for testing
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # If run directly, show options and start the loop
    show_options()
    start_prompt()