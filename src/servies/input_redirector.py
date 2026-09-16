"""
input_redirector.py - Routes input to the tool's validator and launches UI or CLI logic.
"""
import os
import importlib
import subprocess
from colorama import Fore, Style

def redirect_to_tool(tool_name: str, args: list) -> bool:
    """
    Dynamically imports the tool's validator, validates input, and executes.
    """
    safe_name = tool_name.replace("++", "_pp").replace("-", "_")
    tool_pkg_path = f"core.tools.{safe_name}"
    validator_module_path = f"{tool_pkg_path}.{safe_name}_input_validator"
    app_file_path = os.path.join("core", "tools", safe_name, f"{safe_name}_app.py")
    
    try:
        # 1. Import the tool's specific validator
        validator_mod = importlib.import_module(validator_module_path)
        
        # 2. Validate the input
        is_valid, mode_msg = validator_mod.validate(args)
        
        if not is_valid:
            print(f"{Fore.RED}  [Tool Error] {mode_msg}{Style.RESET_ALL}\n")
            return False
            
        # 3. Execute based on mode (UI vs CLI)
        if mode_msg == "UI_MODE":
            if not os.path.exists(app_file_path):
                print(f"{Fore.RED}  [Error] Streamlit app file not found at: {app_file_path}{Style.RESET_ALL}\n")
                return False
                
            print(f"{Fore.CYAN}  → Launching Streamlit Web UI for '{tool_name}'...{Style.RESET_ALL}")
            
            # Launch Streamlit in a new subprocess so it runs in the background
            # while the CLI framework continues running.
            subprocess.Popen(["streamlit", "run", app_file_path])
            
            print(f"{Fore.GREEN}  ✓ Web UI launched in your browser.{Style.RESET_ALL}\n")
            return True
            
        elif mode_msg == "CLI_MODE":
            # Future CLI execution logic goes here
            print(f"{Fore.MAGENTA}  [CLI Mode] Executing {tool_name} with args: {args}{Style.RESET_ALL}\n")
            
            # Example of what the CLI math would look like:
            num1 = float(args[0])
            op = args[1]
            num2 = float(args[2])
            
            if op == "+": result = num1 + num2
            elif op == "-": result = num1 - num2
            elif op == "*": result = num1 * num2
            elif op == "/": result = num1 / num2
            
            print(f"  {Fore.GREEN}Result: {num1} {op} {num2} = {result}{Style.RESET_ALL}\n")
            return True

    except ModuleNotFoundError:
        print(f"{Fore.RED}  [Error] Validator module '{safe_name}_input_validator.py' not found.{Style.RESET_ALL}\n")
        return False
    except Exception as e:
        print(f"{Fore.RED}  [Error] An exception occurred while running '{tool_name}': {e}{Style.RESET_ALL}\n")
        return False