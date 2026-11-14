"""
creator.py - Core logic of Creator
"""

import os
import json
from pprint import pprint
from pathlib import Path
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


# ===========================================
# Main Tool Functions
# ===========================================

# class Creator:
#     def __init__(self , directory) -> None:

#         self.workspace_json = Path(__file__).resolve().parents[3] / "saved_data" / "creator" / "workspaces.json"
#         self.directory = Path(directory)

        
class WorkspaceManager:
    def __init__(self) -> None:
        self.workspace_json = Path(__file__).resolve().parents[3] / "saved_data" / "creator" / "workspaces.json"

    def create_workspace(self , directory , name):
        with self.workspace_json.open("r",encoding="utf-8") as file:
            data = json.load(file)

        new_workspace = {
            "id": "ws_001",
            "name": name,
            "path": directory
        }

        data["workspaces"].append(new_workspace)

        with self.workspace_json.open("w") as file:
            json.dump(data, file, indent=4)
            
        ok("New workspace has created succesfully")
    
    def list_workspaces(self):
        with self.workspace_json.open("r", encoding="utf-8") as file:
            data = json.load(file)

        info("Workspaces : ")
        warn_2("─"*80)
        for i in data["workspaces"]:
            print(f"    {Fore.CYAN}{i["name"]}{Style.RESET_ALL} {Fore.RED}==>{Style.RESET_ALL} {Fore.YELLOW}{i["path"]}{Style.RESET_ALL}")