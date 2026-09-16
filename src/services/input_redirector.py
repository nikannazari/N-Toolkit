"""
input_redirector.py - Routes input, launches Streamlit in background, and manages tool prompt.
"""
import os
import sys
import importlib.util
import subprocess
from colorama import Fore, Style

# Import FRAMEWORK_NAME to use in the return message
from src.constants.commands import FRAMEWORK_NAME

def redirect_to_tool(tool_name: str, args: list) -> bool:
    """
    Launches the Streamlit app and enters a tool-specific prompt loop.
    """
    # 1. Define paths exactly as they are in the OS (with the ++)
    tool_dir = os.path.join("core", "tools", tool_name)
    validator_file_path = os.path.join(tool_dir, f"{tool_name}_input_validator.py")
    app_file_path = os.path.join(tool_dir, f"{tool_name}_app.py")
    
    try:
        # 2. Check if files exist before trying to load them
        if not os.path.exists(validator_file_path):
            print(f"{Fore.RED}  [Error] Validator not found at: {validator_file_path}{Style.RESET_ALL}\n")
            return False
        if not os.path.exists(app_file_path):
            print(f"{Fore.RED}  [Error] Streamlit app not found at: {app_file_path}{Style.RESET_ALL}\n")
            return False

        # 3. Dynamically load the validator module from its file path
        # This bypasses Python's rule against '+' in module names
        spec = importlib.util.spec_from_file_location(f"{tool_name}_validator", validator_file_path)
        validator_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator_mod)
        
        # 4. Validate the input
        is_valid, mode_msg = validator_mod.validate(args)
        
        if not is_valid:
            print(f"{Fore.RED}  [Tool Error] {mode_msg}{Style.RESET_ALL}\n")
            return False
            
        print(f"{Fore.CYAN}  → Launching Streamlit Web UI for '{tool_name}'...{Style.RESET_ALL}")
        
        # 5. Start Streamlit in a background subprocess
        # We pass the exact file path to streamlit
        streamlit_proc = subprocess.Popen(
            ["streamlit", "run", app_file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        print(f"{Fore.GREEN}  ✓ Web UI launched in your browser.{Style.RESET_ALL}")
        
        # 6. Print Tool Help & Enter Tool Prompt Loop
        print(f"{Fore.YELLOW}  ════════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  {tool_name} is running in the background.{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}  Type 'exit', 'q', 'Q', or 'quit' to close the tool{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}  and return to the main framework.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  ════════════════════════════════════════════════{Style.RESET_ALL}\n")

        # Define the tool-specific prompt
        tool_prompt = f"{Fore.MAGENTA}{tool_name}{Style.RESET_ALL}{Fore.CYAN} ❯{Style.RESET_ALL} "

        # 7. Nested Prompt Loop for the Tool
        while True:
            try:
                user_cmd = input(tool_prompt).strip()
                
                # Check for exit commands (case-insensitive)
                if user_cmd.lower() in ["exit", "q", "quit"]:
                    print(f"\n{Fore.CYAN}  [!] Shutting down {tool_name}...{Style.RESET_ALL}")
                    
                    # Kill the Streamlit subprocess
                    streamlit_proc.terminate()
                    streamlit_proc.wait() # Wait for it to cleanly close
                    
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

    except Exception as e:
        print(f"{Fore.RED}  [Error] An exception occurred while running '{tool_name}': {e}{Style.RESET_ALL}\n")
        return False