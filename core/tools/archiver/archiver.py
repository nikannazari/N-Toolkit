"""
archiver.py - Core logic of Archiver tool.
"""
import os
import subprocess
from colorama import Fore, Style

# Import validators
import importlib.util
TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
def _load_validators():
    filepath = os.path.join(TOOL_DIR, "archiver_validators.py")
    spec = importlib.util.spec_from_file_location("archiver_validators", filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_validators = _load_validators()

def info(msg):  print(f"{Fore.CYAN}{msg}{Style.RESET_ALL}")
def ok(msg):    print(f"{Fore.GREEN}✔ {msg}{Style.RESET_ALL}")
def warn(msg):  print(f"{Fore.YELLOW}⚡ {msg}{Style.RESET_ALL}")
def err(msg):   print(f"{Fore.RED}✘ {msg}{Style.RESET_ALL}")

def compress(source: str, archive_name: str, fmt: str, password: str = None):
    fmt = fmt.lower()
    source = os.path.expanduser(source)
    archive_name = os.path.expanduser(archive_name)
    
    # Append extension if not present
    ext_map = {"zip": ".zip", "7z": ".7z", "rar": ".rar", "tar.gz": ".tar.gz"}
    ext = ext_map.get(fmt)
    if ext and not archive_name.endswith(ext):
        archive_name += ext

    if not os.path.exists(source):
        err(f"Source not found: {source}")
        return

    try:
        if fmt == "zip":
            if not _validators.ensure_tool_installed("zip"): return
            cmd = ["zip", "-r", archive_name, os.path.basename(source)]
            if password: cmd.insert(2, "-P"); cmd.insert(3, password)
            cwd = os.path.dirname(source) or "."
            
        elif fmt == "tar.gz":
            if not _validators.ensure_tool_installed("tar"): return
            if password:
                warn("tar.gz does not natively support passwords. Use 7z or zip for encryption.")
            cmd = ["tar", "-czf", archive_name, "-C", os.path.dirname(source) or ".", os.path.basename(source)]
            cwd = os.getcwd()
            
        elif fmt == "7z":
            if not _validators.ensure_tool_installed("7z"): return
            cmd = ["7z", "a", archive_name, source]
            if password: cmd.insert(2, f"-p{password}")
            cwd = os.getcwd()
            
        elif fmt == "rar":
            if not _validators.ensure_tool_installed("rar"): return
            cmd = ["rar", "a", archive_name, source]
            if password: cmd.insert(2, f"-p{password}")
            cwd = os.getcwd()
            
        else:
            err(f"Unsupported format: {fmt}")
            return

        info(f"Compressing '{source}' -> '{archive_name}'...")
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        
        if result.returncode == 0:
            ok(f"Successfully created {archive_name}")
        else:
            err(f"Compression failed:\n{result.stderr}")
            
    except Exception as e:
        err(f"An error occurred: {e}")

def extract(archive: str, output_dir: str = ".", password: str = None):
    archive = os.path.expanduser(archive)
    output_dir = os.path.expanduser(output_dir)
    
    if not os.path.exists(archive):
        err(f"Archive not found: {archive}")
        return
        
    os.makedirs(output_dir, exist_ok=True)

    try:
        if archive.endswith(".zip"):
            if not _validators.ensure_tool_installed("unzip"): return
            cmd = ["unzip", "-o", archive, "-d", output_dir]
            if password: cmd.insert(2, "-P"); cmd.insert(3, password)
            
        elif archive.endswith(".tar.gz") or archive.endswith(".tgz"):
            if not _validators.ensure_tool_installed("tar"): return
            cmd = ["tar", "-xzf", archive, "-C", output_dir]
            
        elif archive.endswith(".7z"):
            if not _validators.ensure_tool_installed("7z"): return
            cmd = ["7z", "x", archive, f"-o{output_dir}", "-y"]
            if password: cmd.insert(2, f"-p{password}")
            
        elif archive.endswith(".rar"):
            if not _validators.ensure_tool_installed("unrar"): return
            cmd = ["unrar", "x", "-y", archive, output_dir]
            if password: cmd.insert(2, f"-p{password}")
            
        else:
            err("Unknown archive format. Supported: zip, tar.gz, 7z, rar")
            return

        info(f"Extracting '{archive}' -> '{output_dir}'...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            ok("Extraction complete.")
        else:
            err(f"Extraction failed:\n{result.stderr}")
            
    except Exception as e:
        err(f"An error occurred: {e}")