"""
securekit_input_handler.py - N-toolkit entry point for Secure ToolKit
"""
import os
import sys
import importlib.util
import pyfiglet
import shlex
from colorama import init as colorama_init , Fore , Style

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

#load the core securekit logic
securekit = _load_module("securekit.py" , "securekit_core")
validators = _load_module("securekit_validators.py" , "securekit_validators")

def show_help():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  SecureKit Tool Help{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}")

    print(f"  {Fore.MAGENTA}Commands:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}hash{Style.RESET_ALL}                      Generate file or text hashes")
    print(f"  {Fore.YELLOW}password{Style.RESET_ALL}                  Generate a secure password")
    print(f"  {Fore.YELLOW}encrypt{Style.RESET_ALL}                   Encrypt files or text")
    print(f"  {Fore.YELLOW}decrypt{Style.RESET_ALL}                   Decrypt files or text")
    print(f"  {Fore.YELLOW}ssh-key{Style.RESET_ALL}                   Generate or manage SSH keys")
    print(f"  {Fore.YELLOW}gpg{Style.RESET_ALL}                       Manage GPG encryption and keys")
    print(f"  {Fore.YELLOW}certificate{Style.RESET_ALL}               Inspect certificate information")
    print(f"  {Fore.YELLOW}integrity{Style.RESET_ALL}                 Check file integrity using hashes")
    print(f"  {Fore.YELLOW}permissions{Style.RESET_ALL}               Check file and directory permissions")

    print(f"\n  {Fore.MAGENTA}System:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}help{Style.RESET_ALL}                      Show this help")
    print(f"  {Fore.YELLOW}clear{Style.RESET_ALL}                     Clear screen")
    print(f"  {Fore.YELLOW}exit{Style.RESET_ALL}                      Return to N-Toolkit")

    print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}\n")
    
def execute_command(command: str , args: list):
    if command == "hash":
        if not args:
            securekit.err("Usage: hash <algorithm> <type> <input text>")
            securekit.info("Available algorithms are : mda5 , sha1 , sha256 , sha224 , sha384 , sha512")
            return
        
        if len(args) != 3:
            securekit.err("Usage: hash <algorithm> <type> <input text or file>")
            securekit.warn("hash sha1 file ../../../file.txt")
            securekit.warn("hash sha1 text hello world")
            return
        
        algorithm = args[0].lower()
        hash_type = args[1].lower()
        input_text = args[2]
    
        if algorithm not in ["md5","sha1","sha224","sha256","sha512","sha384"]:
            securekit.info("Available algorithms are : mda5 , sha1 , sha256 , sha224 , sha384 , sha512")
            return

        securekit.hash(hash_type,input_text,algorithm)
        
    if command == "password":
        if not args:
            securekit.err("Usage : password <type> <features>")
            securekit.info("    password pin <lenght>")
            securekit.warn("        password pin 4")
            securekit.info("    password random <lenght> <include numbers> <include symbols>")
            securekit.warn("        password random 12 yes no")
            securekit.info("    password memorable <easy> <number of words> <seprator> <capitalization>")
            securekit.warn("        password memorable no 4 _ yes")
            return
        elif len(args) < 2:
            securekit.err("Usage : password <type> <features>")
            securekit.info("    password pin <lenght>")
            securekit.info("    password random <lenght> <include numbers> <include symbols>")
            securekit.warn("        password random 12 yes no")
            securekit.info("    password memorable <easy> <number of words> <seprator> <capitalization>")
            securekit.warn("        password memorable no 4 _ yes")
            return     
        
        password_type = args[0]
        if password_type == "pin":
            password_lenght = int(args[1])
            generator = securekit.PinGenerator(password_lenght)
            generator.generate()

        elif password_type == "random":
            password_lenght = int(args[1])
            include_numbers = (args[2] if args[2] else "no")
            include_symbols = (args[3]if args[3] else "no")
            generator = securekit.RandomPasswordGenerator(password_lenght,include_numbers,include_symbols)
            generator.generate()
            
        elif password_type == "memorable":
            easy = args[1]
            number_of_words = int(args[2])
            seprator = args[3]
            capitalization = args[4]
            generator = securekit.MemorablePassword(easy,number_of_words,seprator,capitalization)
            generator.generate()
        
def start(args: list):
    """Entry point called by N-Toolkit."""
    
    art = pyfiglet.figlet_format("SecureKit", font="slant")
    palette = [Fore.RED, Fore.MAGENTA, Fore.BLUE, Fore.CYAN]
    for i, line in enumerate(art.splitlines()):
        print(f"{palette[i % len(palette)]}{line}{Style.RESET_ALL}")

    print(f"{Fore.MAGENTA}{Style.BRIGHT}\n  ╭──────────── SecureKit ──────────────╮{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'help' for commands.        │{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  │ Type 'exit' to return to N-Toolkit│{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  ╰──────────────────────────────────╯{Style.RESET_ALL}\n")

    if args:
        command = args[0].lower()
        if command in ("help", "?"):
            show_help()
        else:
            execute_command(command, args[1:])

    securekit_input = CustomInput()

    while True:
        try:
            prompt = f"{Fore.MAGENTA}SecureKit{Style.RESET_ALL}{Fore.YELLOW} ❯ {Style.RESET_ALL}"
                
            user_input = securekit_input.get_input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Fore.CYAN}  Returning to N-Toolkit...{Style.RESET_ALL}\n")
            return True

        if not user_input:
            continue

        parts = shlex.split(user_input)
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
        
        if command not in ["hash", "password"]:
            securekit.err(f"command {command} not found")

        execute_command(command, command_args)