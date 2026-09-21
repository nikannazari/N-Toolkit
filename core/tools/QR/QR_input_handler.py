"""
qr_input_handler.py - N-Toolkit entry point for QR.
"""
import os
import importlib.util
from colorama import init as colorama_init, Fore, Style
import pyfiglet

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_module(filename, module_name):
    """Helper to dynamically load the tool's core logic."""
    filepath = os.path.join(TOOL_DIR, filename)
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Load the core qr logic
qr = _load_module("QR.py", "qr_core")
validators = _load_module("QR_validators.py", "qr_validators")

def show_help():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  QR Tool Help{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}{'─' * 45}{Style.RESET_ALL}")
    
    print(f"  {Fore.MAGENTA}Commands:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}gen <text or url> [filename]{Style.RESET_ALL} Generate QR Code")
    print(f"  {Fore.YELLOW}decode <image_path>{Style.RESET_ALL}          Decode from image file")
    print(f"  {Fore.YELLOW}batch <directory>{Style.RESET_ALL}            Decode all images in a folder")
    print(f"  {Fore.YELLOW}webcam{Style.RESET_ALL}                       Scan QR code using webcam")
    print(f"  {Fore.YELLOW}screen{Style.RESET_ALL}                       Scan QR code on current screen")
    print(f"  {Fore.YELLOW}history{Style.RESET_ALL}                      Show decode history")
    print(f"  {Fore.YELLOW}clear_hist{Style.RESET_ALL}                   Clear history")
    
    print(f"\n  {Fore.MAGENTA}System:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}help{Style.RESET_ALL}                         Show this help")
    print(f"  {Fore.YELLOW}clear{Style.RESET_ALL}                        Clear screen")
    print(f"  {Fore.YELLOW}exit{Style.RESET_ALL}                         Return to N-Toolkit")
    print(f"  {Fore.YELLOW}{'─' * 45}{Style.RESET_ALL}\n")

def start(args: list):
    """Entry point called by N-Toolkit."""
    qr.ensure_config()
    
    # Banner
    art = pyfiglet.figlet_format("QR", font="slant")
    palette = [Fore.RED, Fore.MAGENTA, Fore.BLUE, Fore.CYAN]
    for i, line in enumerate(art.splitlines()):
        print(f"{palette[i % len(palette)]}{line}{Style.RESET_ALL}")

    print(f"{Fore.MAGENTA}{Style.BRIGHT}\n  ╭──────────── QR Tool ─────────────╮{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'help' for commands.         │{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'exit' to return to N-Toolkit│{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  ╰───────────────────────────────────╯{Style.RESET_ALL}\n")

    # Handle args passed directly from N-Toolkit
    if args:
        command = args[0].lower()
        if command in ("help", "?"):
            show_help()
        else:
            execute_command(command, args[1:])

    # QR own prompt loop
    while True:
        try:
            user_input = input(
                f"{Fore.MAGENTA}QR{Style.RESET_ALL}{Fore.YELLOW} ❯ {Style.RESET_ALL}"
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

def execute_command(command: str, args: list):
    if command == "gen":
        if not args:
            qr.err("Usage: gen <text or url> [filename.png]")
            return
            
        # Check if the last argument is a filename (ends with .png/.jpg/.jpeg)
        if len(args) > 1 and args[-1].lower().endswith(('.png', '.jpg', '.jpeg')):
            filename = args[-1]
            text = " ".join(args[:-1])  # Join everything else as the sentence
        else:
            filename = "qr_code.png"
            text = " ".join(args)  # Join all arguments as the sentence
            
        ok_, text = validators.validate_text(text)
        if ok_:
            qr.generate_qr(text, filename)

    elif command == "decode":
        if not args:
            qr.err("Usage: decode <image_path>")
            return
        ok_, path = validators.validate_file(args[0])
        if ok_:
            qr.decode_image(path)

    elif command == "batch":
        if not args:
            qr.err("Usage: batch <directory>")
            return
        ok_, path = validators.validate_directory(args[0])
        if ok_:
            qr.batch_decode(path)

    elif command == "webcam":
        qr.decode_webcam()

    elif command == "screen":
        qr.decode_screen()

    elif command == "history":
        qr.show_history()

    elif command == "clear_hist":
        qr.clear_history()

    else:
        qr.err(f"Unknown command: {command}. Type 'help' for commands.")