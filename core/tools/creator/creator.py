"""
creator.py - Core logic of Creator
"""

import os
from colorama import Fore , Style


TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(TOOL_DIR, "..", "..", ".."))

# ===========================================
# Terminal Color
# ===========================================

def info(msg):  print(f"{Fore.CYAN}{msg}{Style.RESET_ALL}")
def ok(msg):    print(f"{Fore.GREEN}✔ {msg}{Style.RESET_ALL}")
def warn(msg):  print(f"{Fore.YELLOW}⚡ {msg}{Style.RESET_ALL}")
def err(msg):   print(f"{Fore.RED}✘ {msg}{Style.RESET_ALL}")
def ok_2(msg): print(f"{Fore.GREEN}{msg}{Style.RESET_ALL}")
def warn_2(msg): print(f"{Fore.YELLOW}{msg}{Style.RESET_ALL}")
def err_2(msg): print(f"{Fore.RED}{msg}{Style.RESET_ALL}")
