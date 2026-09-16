"""
core/tools/calculator_pp.py - A simple mock calculator tool.
"""
from colorama import Fore, Style

def main(args):
    """Entry point for the calculator++ tool."""
    print(f"{Fore.MAGENTA}  [Calculator++] {Style.RESET_ALL}Tool started successfully!")
    
    if not args:
        print(f"  {Fore.YELLOW}Usage: run calculator++ <num1> <operator> <num2>{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}Example: run calculator++ 5 + 3{Style.RESET_ALL}")
        return
        
    try:
        num1 = float(args[0])
        op = args[1]
        num2 = float(args[2])
        
        if op == "+": result = num1 + num2
        elif op == "-": result = num1 - num2
        elif op == "*": result = num1 * num2
        elif op == "/": result = num1 / num2 if num2 != 0 else "Error: Div by 0"
        else: result = "Error: Unknown operator"
        
        print(f"  {Fore.GREEN}Result: {num1} {op} {num2} = {result}{Style.RESET_ALL}")
        
    except IndexError:
        print(f"  {Fore.RED}Error: Missing arguments.{Style.RESET_ALL}")
    except ValueError:
        print(f"  {Fore.RED}Error: Invalid numbers provided.{Style.RESET_ALL}")