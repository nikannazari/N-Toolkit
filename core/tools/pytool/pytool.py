"""
pytool.py - Core logic of PyTool.
"""
import os
import sys
import subprocess
from colorama import Fore, Style

import importlib.util
TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
def _load_validators():
    filepath = os.path.join(TOOL_DIR, "pytool_validators.py")
    spec = importlib.util.spec_from_file_location("pytool_validators", filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_validators = _load_validators()

def info(msg):  print(f"{Fore.CYAN}{msg}{Style.RESET_ALL}")
def ok(msg):    print(f"{Fore.GREEN}✔ {msg}{Style.RESET_ALL}")
def warn(msg):  print(f"{Fore.YELLOW}⚡ {msg}{Style.RESET_ALL}")
def err(msg):   print(f"{Fore.RED}✘ {msg}{Style.RESET_ALL}")

def _run_command(cmd: list, cwd: str = "."):
    """Helper to run a command and stream output live."""
    info(f"Running: {' '.join(cmd)}")
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

def create_venv(venv_name: str = ".venv"):
    info(f"Creating virtual environment: {venv_name}...")
    return _run_command([sys.executable, "-m", "venv", venv_name])

def install_reqs(target: str = "."):
    """Install from requirements.txt or a specific package."""
    if target == ".":
        req_file = os.path.join(os.getcwd(), "requirements.txt")
        if not os.path.exists(req_file):
            err("requirements.txt not found in current directory.")
            return
        info("Installing from requirements.txt...")
        return _run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        info(f"Installing package: {target}...")
        return _run_command([sys.executable, "-m", "pip", "install", target])

def freeze_reqs():
    info("Freezing dependencies to requirements.txt...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True)
        with open("requirements.txt", "w") as f:
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
    # We use os.system here so the script can take over stdin/stdout interactively
    code = os.system(f"{sys.executable} {script_path}")
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
    dist_dir = os.path.join(os.getcwd(), "dist")
    if not os.path.exists(dist_dir):
        err("No 'dist' directory found. Run 'package' first.")
        return
    info("Uploading to PyPI using Twine...")
    warn("You will be prompted for your PyPI credentials.")
    return _run_command(["twine", "upload", "dist/*"])