"""
welcome.py - Spectacular welcome message module for the framework.
Requires: pyfiglet, colorama, psutil (install via pip)
"""

import os
import sys
import time
import random
import platform
import getpass
from datetime import datetime
from typing import List

try:
    from pyfiglet import Figlet
    from colorama import Fore, Back, Style, init
    import psutil
    init(autoreset=True)
except ImportError as e:
    print(f"[!] Missing dependency: {e.name}")
    print("[!] Install with: pip install pyfiglet colorama psutil")
    sys.exit(1)


# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
FRAMEWORK_NAME = "N-Toolkit"   # Updated name
FRAMEWORK_VERSION = "1.0.0"
FRAMEWORK_AUTHOR = "Nikan Nazari"
TAGLINE = "The Ultimate Linux Utility Framework"  # Updated tagline

AVAILABLE_TOOLS: List[str] = [
    "calculator++",
    # "ffmpeg",
    # "autogit",
    # "sysinfo",
    # "filemanager",
    # "nettools",
]

TIPS: List[str] = [
    "Type 'help' to see all available commands.",
    "Use 'run <tool>' to launch a tool's Web UI.",
    "Press TAB for auto-completion (if supported).",
    "Use 'clear' to clean the terminal screen.",
    "Type 'exit' or press Ctrl+C to quit.",
    "You can chain commands with the ';' separator.",
    "Use 'history' to recall previous commands.",
]

# 'slant' and 'standard' look great with hyphens
BANNER_FONTS = ["slant", "standard", "big", "doom", "larry3d"]


# ─────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────
def _get_greeting() -> str:
    """Return a time-based greeting."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Good night"


def _get_uptime() -> str:
    """Return system uptime in a readable format."""
    try:
        boot_time = psutil.boot_time()
        uptime_sec = int(time.time() - boot_time)
        h, rem = divmod(uptime_sec, 3600)
        m, s = divmod(rem, 60)
        return f"{h}h {m}m {s}s"
    except Exception:
        return "unknown"


def _loading_bar(length: int = 30, delay: float = 0.02) -> None:
    """Print an animated loading bar."""
    sys.stdout.write(Fore.CYAN + "[")
    for i in range(length):
        sys.stdout.write(Fore.GREEN + "█")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(Fore.CYAN + "]")
    sys.stdout.write(Style.RESET_ALL + " OK\n")


def _print_separator(char: str = "─", length: int = 60, color=Fore.MAGENTA) -> None:
    """Print a colored separator line."""
    print(color + char * length + Style.RESET_ALL)


# ─────────────────────────────────────────────
# Main display functions
# ─────────────────────────────────────────────
def show_banner() -> None:
    """Print the big ASCII art banner."""
    figlet = Figlet(font=random.choice(BANNER_FONTS))
    art = figlet.renderText(FRAMEWORK_NAME)
    # Color each line with a gradient-like effect
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    for i, line in enumerate(art.splitlines()):
        color = colors[i % len(colors)]
        print(color + line.center(os.get_terminal_size().columns) + Style.RESET_ALL)


def show_tagline() -> None:
    """Print the framework tagline."""
    tag = f"✦ {TAGLINE} ✦"
    print(Fore.YELLOW + Style.BRIGHT + tag.center(os.get_terminal_size().columns))
    print(Style.RESET_ALL)


def show_version_info() -> None:
    """Print version and author info."""
    info = f"v{FRAMEWORK_VERSION}  •  by {FRAMEWORK_AUTHOR}"
    print(Fore.LIGHTBLACK_EX + info.center(os.get_terminal_size().columns))
    print()


def show_greeting() -> None:
    """Print a personalized greeting to the user."""
    user = getpass.getuser()
    greeting = f"{_get_greeting()}, {Fore.CYAN}{user}{Style.RESET_ALL}!"
    print(Fore.WHITE + Style.BRIGHT + greeting)
    print(f"{Fore.LIGHTBLACK_EX}It's {datetime.now().strftime('%A, %d %B %Y • %H:%M:%S')}")
    print()


def show_system_info() -> None:
    """Print a compact block of system information."""
    _print_separator()
    print(Fore.CYAN + Style.BRIGHT + "  SYSTEM INFORMATION")
    _print_separator()
    print(f"  {Fore.GREEN}OS        :{Style.RESET_ALL} {platform.system()} {platform.release()}")
    print(f"  {Fore.GREEN}Host      :{Style.RESET_ALL} {platform.node()}")
    print(f"  {Fore.GREEN}Machine   :{Style.RESET_ALL} {platform.machine()}")
    print(f"  {Fore.GREEN}Python    :{Style.RESET_ALL} {platform.python_version()}")
    print(f"  {Fore.GREEN}CPU       :{Style.RESET_ALL} {platform.processor() or 'N/A'}")
    try:
        mem = psutil.virtual_memory()
        print(f"  {Fore.GREEN}Memory    :{Style.RESET_ALL} "
              f"{mem.used // (1024**2)} MB / {mem.total // (1024**2)} MB "
              f"({mem.percent}%)")
        print(f"  {Fore.GREEN}CPU Usage :{Style.RESET_ALL} {psutil.cpu_percent(interval=0.5)}%")
    except Exception:
        pass
    print(f"  {Fore.GREEN}Uptime    :{Style.RESET_ALL} {_get_uptime()}")
    _print_separator()
    print()


def show_tools() -> None:
    """Print the list of available tools in a nice grid."""
    print(Fore.CYAN + Style.BRIGHT + "  AVAILABLE TOOLS")
    _print_separator()
    cols = 3
    for i in range(0, len(AVAILABLE_TOOLS), cols):
        row = AVAILABLE_TOOLS[i:i + cols]
        line = "  "
        for tool in row:
            line += f"{Fore.YELLOW}▸ {Fore.WHITE}{tool.ljust(18)}"
        print(line + Style.RESET_ALL)
    _print_separator()
    print()


def show_tip_of_the_day() -> None:
    """Print a random tip."""
    tip = random.choice(TIPS)
    print(f"  {Fore.MAGENTA}💡 Tip:{Style.RESET_ALL} {tip}")
    print()


def show_loading_sequence(steps: List[str]) -> None:
    """Display an animated loading sequence for the given steps."""
    print()
    for step in steps:
        sys.stdout.write(f"{Fore.CYAN}  → Loading {step}...")
        sys.stdout.flush()
        time.sleep(0.3)
        sys.stdout.write("\r" + " " * 60 + "\r")
        sys.stdout.write(f"{Fore.GREEN}  ✓ {step} loaded\n")
        sys.stdout.flush()
    print()


def show_startup_animation() -> None:
    """Boot-up animation before the main welcome screen."""
    boot_steps = ["core", "services", "validators", "tools registry"]
    print(Fore.CYAN + "\n  Booting " + FRAMEWORK_NAME + "...\n")
    _loading_bar()
    show_loading_sequence(boot_steps)
    # Clear screen for a clean welcome
    os.system("clear" if os.name == "posix" else "cls")


# ─────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────
def welcome() -> None:
    """Main entry point — shows the full welcome screen."""
    try:
        show_startup_animation()
        show_banner()
        show_tagline()
        show_version_info()
        show_greeting()
        show_system_info()
        show_tools()
        show_tip_of_the_day()
        _print_separator(char="═")
        prompt_text = f"{Fore.GREEN}{FRAMEWORK_NAME}{Style.RESET_ALL}" \
                      f"{Fore.CYAN} ❯{Style.RESET_ALL} "
        print(prompt_text, end="")
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Interrupted during welcome.{Style.RESET_ALL}")
        sys.exit(1)
    