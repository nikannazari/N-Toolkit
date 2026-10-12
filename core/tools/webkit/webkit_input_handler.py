"""
webkit_input_handler.py - N-Toolkit entry point for WebKit.
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

webkit = _load_module("webkit.py", "webkit_core")
validators = _load_module("webkit_validators.py", "webkit_validators")

# Tool state
_target_url = None

def show_help():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  WebKit Tool Help{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}")
    
    print(f"  {Fore.MAGENTA}Setup:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}url <website>{Style.RESET_ALL}             Set target URL (e.g., url example.com)")
    
    print(f"\n  {Fore.MAGENTA}Commands:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}download{Style.RESET_ALL}                  Download website HTML")
    print(f"  {Fore.YELLOW}links{Style.RESET_ALL}                     Extract all links from page")
    print(f"  {Fore.YELLOW}images{Style.RESET_ALL}                    Download all images from page")
    print(f"  {Fore.YELLOW}screenshot{Style.RESET_ALL}                Take a screenshot (requires Chrome)")
    print(f"  {Fore.YELLOW}status{Style.RESET_ALL}                    Check HTTP status & headers")
    print(f"  {Fore.YELLOW}seo{Style.RESET_ALL}                       Extract SEO info (Title, Desc, H1)")
    print(f"  {Fore.YELLOW}ssl{Style.RESET_ALL}                       Check SSL certificate info")
    print(f"  {Fore.YELLOW}robots{Style.RESET_ALL}                    Fetch robots.txt")
    print(f"  {Fore.YELLOW}sitemap{Style.RESET_ALL}                   Fetch sitemap.xml")
    
    print(f"\n  {Fore.MAGENTA}System:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}help{Style.RESET_ALL}                      Show this help")
    print(f"  {Fore.YELLOW}clear{Style.RESET_ALL}                     Clear screen")
    print(f"  {Fore.YELLOW}exit{Style.RESET_ALL}                      Return to N-Toolkit")
    print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}\n")

def execute_command(command: str, args: list):
    global _target_url
    
    # Command to set URL
    if command == "url":
        if not args:
            webkit.err("Usage: url <website>")
            return
        ok_, res = validators.validate_url(args[0])
        if ok_:
            _target_url = res
            webkit.ok(f"Target URL set to: {_target_url}")
        else:
            webkit.err(res)
        return

    # Commands that require URL to be set first
    if not _target_url:
        webkit.err("No target URL set. Use 'url <website>' first.")
        return

    if command == "download":
        webkit.download_website(_target_url)
    elif command == "links":
        webkit.extract_links(_target_url)
    elif command == "images":
        webkit.download_images(_target_url)
    elif command == "screenshot":
        webkit.website_screenshot(_target_url)
    elif command == "status":
        webkit.check_status(_target_url)
    elif command == "seo":
        webkit.seo_info(_target_url)
    elif command == "ssl":
        webkit.ssl_info(_target_url)
    elif command == "robots":
        webkit.fetch_robots(_target_url)
    elif command == "sitemap":
        webkit.fetch_sitemap(_target_url)
    else:
        webkit.err(f"Unknown command: {command}. Type 'help' for commands.")

def start(args: list):
    """Entry point called by N-Toolkit."""
    art = pyfiglet.figlet_format("WebKit", font="slant")
    palette = [Fore.RED, Fore.MAGENTA, Fore.BLUE, Fore.CYAN]
    for i, line in enumerate(art.splitlines()):
        print(f"{palette[i % len(palette)]}{line}{Style.RESET_ALL}")

    print(f"{Fore.MAGENTA}{Style.BRIGHT}\n  ╭──────────── WebKit ───────────────╮{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'help' for commands.         │{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'exit' to return to N-Toolkit│{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  ╰───────────────────────────────────╯{Style.RESET_ALL}\n")

    # If launched with args: e.g. N-Toolkit ❯ run WebKit url example.com
    if args:
        command = args[0].lower()
        if command in ("help", "?"):
            show_help()
        else:
            execute_command(command, args[1:])

    webkit_input = CustomInput()

    while True:
        try:
            # Dynamic prompt showing active URL
            if _target_url:
                prompt = f"{Fore.MAGENTA}WebKit{Fore.BLUE}({urlparse(_target_url).netloc}){Style.RESET_ALL}{Fore.YELLOW} ❯ {Style.RESET_ALL}"
            else:
                prompt = f"{Fore.MAGENTA}WebKit{Style.RESET_ALL}{Fore.YELLOW} ❯ {Style.RESET_ALL}"
                
            user_input = webkit_input.get_input(prompt).strip()
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

# Need to import urlparse for the dynamic prompt
from urllib.parse import urlparse
