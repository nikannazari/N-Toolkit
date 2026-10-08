"""
pytool.py - Core logic of PyTool.
"""
import os
import sys
import json
import subprocess
from colorama import Fore, Style

import importlib.util
TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(TOOL_DIR, "..", "..", ".."))
CONFIG_DIR = os.path.join(PROJECT_ROOT, "saved_data", "pytool")
PROJECTS_FILE = os.path.join(CONFIG_DIR, "projects.json")

def _load_validators():
    filepath = os.path.join(TOOL_DIR, "pytool_validators.py")
    spec = importlib.util.spec_from_file_location("pytool_validators", filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_validators = _load_validators()

# ── State ──
_active_project_path = os.getcwd()
_active_project_name = None

def info(msg):  print(f"{Fore.CYAN}{msg}{Style.RESET_ALL}")
def ok(msg):    print(f"{Fore.GREEN}✔ {msg}{Style.RESET_ALL}")
def warn(msg):  print(f"{Fore.YELLOW}⚡ {msg}{Style.RESET_ALL}")
def err(msg):   print(f"{Fore.RED}✘ {msg}{Style.RESET_ALL}")

def get_active_name():
    return _active_project_name

def get_active_path():
    return _active_project_path

# ── Persistence ──
def ensure_config():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if not os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, "w") as f:
            json.dump({}, f)

def load_projects() -> dict:
    try:
        with open(PROJECTS_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_projects(data: dict):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(PROJECTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ── Project Actions ──
def add_project(name: str, path: str = None):
    global _active_project_path, _active_project_name
    if not path:
        path = os.getcwd()
        
    if not os.path.isdir(path):
        err(f"Directory does not exist: {path}")
        return
        
    projects = load_projects()
    projects[name] = os.path.abspath(path)
    save_projects(projects)
    ok(f"Project '{name}' saved.")
    
    # Auto-switch to it
    _active_project_path = projects[name]
    _active_project_name = name

def remove_project(name: str):
    global _active_project_name, _active_project_path
    projects = load_projects()
    if name in projects:
        del projects[name]
        save_projects(projects)
        ok(f"Project '{name}' removed.")
        if _active_project_name == name:
            _active_project_name = None
            _active_project_path = os.getcwd()
    else:
        err(f"Project '{name}' not found.")

def list_projects():
    projects = load_projects()
    if not projects:
        warn("No saved projects.")
        return
        
    print(f"\n{Fore.YELLOW}╭─ Saved PyTool Projects ───────────────────────╮{Style.RESET_ALL}")
    for name, path in projects.items():
        active_marker = f"{Fore.GREEN}*{Style.RESET_ALL}" if name == _active_project_name else " "
        print(f"{Fore.YELLOW}│{Style.RESET_ALL}{active_marker} {Fore.MAGENTA}{name}{Style.RESET_ALL}: {Style.DIM}{path}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}╰──────────────────────────────────────────────╯{Style.RESET_ALL}\n")

def use_project(name: str):
    global _active_project_path, _active_project_name
    projects = load_projects()
    if name in projects:
        _active_project_path = projects[name]
        _active_project_name = name
        ok(f"Switched to project '{name}' at {_active_project_path}")
    else:
        err(f"Project '{name}' not found. Use 'saved' to see list.")

def pwd():
    """Print working directory of active project."""
    info(f"Active Project: {Fore.MAGENTA}{_active_project_name or 'None'}{Style.RESET_ALL}")
    info(f"Path: {Style.DIM}{_active_project_path}{Style.RESET_ALL}")

# ── Helper ──
def _run_command(cmd: list, cwd: str = None):
    """Helper to run a command and stream output live."""
    if cwd is None:
        cwd = _active_project_path
    info(f"Running: {' '.join(cmd)} in {Style.DIM}{cwd}{Style.RESET_ALL}")
    try:
        process = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(f"  {line.rstrip()}")
        process.wait()
        if process.returncode == 0:
            ok("Command completed successfully.\n")
        else:
            err(f"Command failed with exit code {process.returncode}.\n")
        return process.returncode == 0
    except Exception as e:
        err(f"Error executing command: {e}\n")
        return False

# ── Python Dev Actions ──
def create_venv(venv_name: str = ".venv"):
    info(f"Creating virtual environment: {venv_name}...")
    return _run_command([sys.executable, "-m", "venv", venv_name])

def install_reqs(target: str = "."):
    if target == ".":
        req_file = os.path.join(_active_project_path, "requirements.txt")
        if not os.path.exists(req_file):
            err("requirements.txt not found in active project.")
            return
        info("Installing from requirements.txt...")
        return _run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        info(f"Installing package: {target}...")
        return _run_command([sys.executable, "-m", "pip", "install", target])

def freeze_reqs():
    info("Freezing dependencies to requirements.txt...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True, cwd=_active_project_path)
        req_file = os.path.join(_active_project_path, "requirements.txt")
        with open(req_file, "w") as f:
            f.write(result.stdout)
        ok("Dependencies saved to requirements.txt\n")
    except Exception as e:
        err(f"Failed to freeze requirements: {e}\n")

def lint(paths: list):
    if not _validators.ensure_tool_installed("flake8", "flake8"):
        return
    if not paths:
        paths = ["."]
    info(f"Linting: {' '.join(paths)}...")
    return _run_command(["flake8"] + paths)

def format_code(paths: list):
    if not _validators.ensure_tool_installed("black", "black"):
        return
    if not paths:
        paths = ["."]
    info(f"Formatting: {' '.join(paths)}...")
    return _run_command(["black"] + paths)

def run_script(script: str):
    ok_, script_path = _validators.validate_script(script)
    if not ok_:
        err(script_path)
        return
    info(f"Running: {script}...")
    code = os.system(f"cd {_active_project_path} && {sys.executable} {script_path}")
    if code == 0:
        ok("Script finished.\n")
    else:
        err(f"Script exited with code {code}.\n")

def package():
    if not _validators.ensure_tool_installed("build", "build"):
        return
    info("Building package (sdist and wheel)...")
    return _run_command([sys.executable, "-m", "build"])

def publish():
    if not _validators.ensure_tool_installed("twine", "twine"):
        return
    dist_dir = os.path.join(_active_project_path, "dist")
    if not os.path.exists(dist_dir):
        err("No 'dist' directory found in active project. Run 'package' first.")
        return
    info("Uploading to PyPI using Twine...")
    warn("You will be prompted for your PyPI credentials.")
    return _run_command(["twine", "upload", "dist/*"])