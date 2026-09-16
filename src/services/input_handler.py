"""
input_handler.py - Orchestrates the parsing, validation, and execution of tools.
"""
import time
from colorama import Fore, Style

# Import our new pipeline modules
from src.validators.prompt_validator import validate_prompt_syntax
from src.validators.tool_validators import validate_tool_exists
from src.services.input_redirector import redirect_to_tool

def handle_input(user_input: str) -> bool:
    """
    Processes user input that isn't a built-in shell command.
    """
    # 1. Validate Syntax
    is_valid, parsed_data, error_msg = validate_prompt_syntax(user_input)
    
    if not is_valid:
        print(f"{Fore.RED}  [Syntax Error] {error_msg}{Style.RESET_ALL}\n")
        return False
        
    tool_name, args = parsed_data

    # 2. Validate Tool Existence
    if not validate_tool_exists(tool_name):
        print(f"{Fore.RED}{Style.BRIGHT}  ╭─ [ERROR] Tool Not Found ───────────────╮{Style.RESET_ALL}")
        print(f"{Fore.RED}  │ The tool '{Fore.WHITE}{tool_name}{Fore.RED}' is not recognized.   │{Style.RESET_ALL}")
        print(f"{Fore.RED}  ╰────────────────────────────────────────╯{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  💡 Tip: Type 'tools' to see a list of available tools.{Style.RESET_ALL}\n")
        return False

    # 3. Execute Tool (with a tiny bit of UI flair)
    print(f"{Fore.CYAN}  → Routing to {Fore.WHITE}{tool_name}{Fore.CYAN}...", end="")
    print(f"{Fore.GREEN} ✓ Validated{Style.RESET_ALL}")
    time.sleep(0.3) # Tiny delay for a smooth UI feel

    # 4. Redirect to actual tool
    return redirect_to_tool(tool_name, args)