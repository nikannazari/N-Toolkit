"""
securekit.py - Core logic of SecureKit
"""
import os
import subprocess
import hashlib
from colorama import Fore , Style

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(TOOL_DIR, "..", "..", ".."))

def info(msg):  print(f"{Fore.CYAN}{msg}{Style.RESET_ALL}")
def ok(msg):    print(f"{Fore.GREEN}✔ {msg}{Style.RESET_ALL}")
def warn(msg):  print(f"{Fore.YELLOW}⚡ {msg}{Style.RESET_ALL}")
def err(msg):   print(f"{Fore.RED}✘ {msg}{Style.RESET_ALL}")

def _to_bytes(s):
        return s.encode('utf-8') if isinstance(s, str) else s

def hash(input_text, algorithms):

    if algorithms == "md5":
        print(hashlib.md5(_to_bytes(input_text)).hexdigest())
    elif algorithms == "sha1":
        print(hashlib.sha1(_to_bytes(input_text)).hexdigest())
    elif algorithms == "sha256":
        print(hashlib.sha256(_to_bytes(input_text)).hexdigest())
    else: 
        print(hashlib.sha512(_to_bytes(input_text)).hexdigest())
