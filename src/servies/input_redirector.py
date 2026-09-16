"""
input_redirector.py - Routes input, launches Streamlit in background, and manages tool prompt.
"""
import os
import sys
import importlib
import subprocess
from colorama import Fore, Style

# Import FRAMEWORK_NAME to use in the return message
from src.constants.commands import FRAMEWORK_NAME

def redirect_to_tool(tool_name: str, args: list) -> bool:
    """
    Launches the Streamlit app and enters a tool-specific prompt loop.
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
            
        # 3. Check if app file exists
        if not os.path.exists(app_file_path):
            print(f"{Fore.RED}  [Error] Streamlit app file not found at: {app_file_path}{Style.RESET_ALL}\n")
            return False
            
        print(f"{Fore.CYAN}  → Launching Streamlit Web UI for '{tool_name}'...{Style.RESET_ALL}")
        
        # 4. Start Streamlit in a background subprocess
        streamlit_proc = subprocess.Popen(
            ["streamlit", "run", app_file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        print(f"{Fore.GREEN}  ✓ Web UI launched in your browser.{Style.RESET_ALL}")
        
        # 5. Print Tool Help & Enter Tool Prompt Loop
        print(f"{Fore.YELLOW}  ════════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  {tool_name} is running in the background.{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}  Type 'exit', 'q', 'Q', or 'quit' to close the tool{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}  and return to the main framework.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  ════════════════════════════════════════════════{Style.RESET_ALL}\n")

        # Define the tool-specific prompt
        tool_prompt = f"{Fore.MAGENTA}{tool_name}{Style.RESET_ALL}{Fore.CYAN} ❯{Style.RESET_ALL} "

        # 6. Nested Prompt Loop for the Tool
        while True:
            try:
                user_cmd = input(tool_prompt).strip()
                
                # Check for exit commands (case-insensitive)
                if user_cmd.lower() in ["exit", "q", "quit"]:
                    print(f"\n{Fore.CYAN}  [!] Shutting down {tool_name}...{Style.RESET_ALL}")
                    
                    # Kill the Streamlit subprocess
                    streamlit_proc.terminate()
                    streamlit_proc.wait() # Wait for it to cleanly close
                    
                    # Updated this line to use FRAMEWORK_NAME
                    print(f"{Fore.GREEN}  ✓ Tool closed. Returning to {FRAMEWORK_NAME}.{Style.RESET_ALL}\n")
                    break 
                
                elif not user_cmd:
                    continue 
                
                else:
                    print(f"{Fore.LIGHTBLACK_EX}  [Tool Mode] Commands are disabled here. Type 'exit' to close {tool_name}.{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}  [!] Interrupted. Force closing {tool_name}...{Style.RESET_ALL}")
                streamlit_proc.terminate()
                break
                
            except EOFError:
                print(f"\n{Fore.RED}  [!] EOF received. Force closing {tool_name}...{Style.RESET_ALL}")
                streamlit_proc.terminate()
                sys.exit(0)

        return True

    except ModuleNotFoundError:
        print(f"{Fore.RED}  [Error] Validator module '{safe_name}_input_validator.py' not found.{Style.RESET_ALL}\n")
        return False
    except Exception as e:
        print(f"{Fore.RED}  [Error] An exception occurred while running '{tool_name}': {e}{Style.RESET_ALL}\n")
        return False