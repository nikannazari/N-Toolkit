"""
input_redirector.py - Dynamically loads and executes tools from core/tools.
"""
import importlib
from colorama import Fore, Style

def redirect_to_tool(tool_name: str, args: list) -> bool:
    """
    Dynamically imports the tool module and calls its main() function.
    """
    # Convert tool name to a valid Python module path (e.g., calculator++ -> calculator_pp)
    safe_name = tool_name.replace("++", "_pp").replace("-", "_")
    module_path = f"core.tools.{safe_name}"
    
    try:
        # Dynamically import the tool module
        tool_module = importlib.import_module(module_path)
        
        # Check if the module has a main() function
        if hasattr(tool_module, 'main'):
            print(f"{Fore.CYAN}  ──────────────────────────────────────{Style.RESET_ALL}")
            # Execute the tool, passing the arguments
            tool_module.main(args)
            print(f"{Fore.CYAN}  ──────────────────────────────────────{Style.RESET_ALL}\n")
            return True
        else:
            print(f"{Fore.RED}  [Error] The tool '{tool_name}' is missing a main() function.{Style.RESET_ALL}\n")
            return False
            
    except ModuleNotFoundError:
        print(f"{Fore.RED}  [Error] Tool module '{tool_name}' not found in /core/tools/.{Style.RESET_ALL}\n")
        return False
    except Exception as e:
        print(f"{Fore.RED}  [Error] An exception occurred while running '{tool_name}': {e}{Style.RESET_ALL}\n")
        return False