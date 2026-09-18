"""
mpv++.py - Core logic of mpv++.
"""
import os
import json
import random
import shlex
import subprocess
import sys
import importlib.util
from colorama import init as colorama_init, Fore, Style
import pyfiglet

colorama_init()

# Dynamically load the validators
TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
def _load_validators():
    filepath = os.path.join(TOOL_DIR, "mpv++_validators.py")
    spec = importlib.util.spec_from_file_location("mpv_validators", filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_validators = _load_validators()
validate_directory = _validators.validate_directory
validate_file = _validators.validate_file
validate_name = _validators.validate_name
ensure_mpv = _validators.ensure_mpv
filter_files = _validators.filter_files
MUSIC_EXTS = _validators.MUSIC_EXTS
VIDEO_EXTS = _validators.VIDEO_EXTS

# ── paths ────────────────────────────────────────────────────────────────
# TOOL_DIR is: <project_root>/core/tools/mpv++
# We go up 3 directories to get to <project_root>
PROJECT_ROOT = os.path.abspath(os.path.join(TOOL_DIR, "..", "..", ".."))
CONFIG_DIR = os.path.join(PROJECT_ROOT, "saved_data", "mpv++")
CONFIG_FILE = os.path.join(CONFIG_DIR, "saved_paths.json")

# ── persistence ──────────────────────────────────────────────────────────
def ensure_config():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({}, f)
        # Optional: Print the path so you know exactly where it was created!
        info(f"Created config at: {CONFIG_FILE}")

def load_paths() -> dict:
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_paths(data: dict):
    # Ensure the directory exists just in case it was deleted
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ── color helpers ────────────────────────────────────────────────────────
def info(msg):  print(f"{Fore.CYAN}{msg}{Style.RESET_ALL}")
def ok(msg):    print(f"{Fore.GREEN}✔ {msg}{Style.RESET_ALL}")
def warn(msg):  print(f"{Fore.YELLOW}⚡ {msg}{Style.RESET_ALL}")
def err(msg):   print(f"{Fore.RED}✘ {msg}{Style.RESET_ALL}")

# ── banner ───────────────────────────────────────────────────────────────
def banner():
    art = pyfiglet.figlet_format("mpv++", font="slant")
    palette = [Fore.RED, Fore.MAGENTA, Fore.BLUE, Fore.CYAN]
    for i, line in enumerate(art.splitlines()):
        print(f"{palette[i % len(palette)]}{line}{Style.RESET_ALL}")
    print(
        f"{Fore.MAGENTA}{Style.BRIGHT}"
        "\n  ╭──────────── mpv++ ────────────────────╮"
        f"{Style.RESET_ALL}"
    )

    print(
        f"{Fore.MAGENTA}"
        "  │ Type 'help' for commands.             │"
        f"{Style.RESET_ALL}"
    )

    print(
        f"{Fore.MAGENTA}"
        "  │ Type 'exit' to return to N-Toolkit.   │"
        f"{Style.RESET_ALL}"
    )

    print(
        f"{Fore.MAGENTA}"
        "  ╰───────────────────────────────────────╯"
        f"{Style.RESET_ALL}\n"
    )

# ── help ─────────────────────────────────────────────────────────────────
def help_text():
    print(f"\n{Fore.YELLOW}╭─ Commands ───────────────────────────────────────────────────╮{Style.RESET_ALL}")
    rows = [
        ("1  random music [path|saved <name>]",  "play a random music file"),
        ("2  random video [path|saved <name>]",  "play a random movie/video"),
        ("3  play <file>",                       "play a specific file (full path)"),
        ("   play <saved_name> <filename>",      "play file inside a saved directory"),
        ("4  list",                              "show saved directories"),
        ("5  add [path] [name]",                 "save a new directory"),
        ("6  delete <name>",                     "remove a saved directory"),
        ("7  shuffle [path|saved <name>]",       "play whole directory shuffled"),
        ("8  help  /  ?",                        "show this help"),
        ("9  exit  /  quit",                     "leave mpv++"),
    ]
    for cmd, desc in rows:
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.CYAN}{cmd:<40}{Style.RESET_ALL} {Style.DIM}{desc}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}╰──────────────────────────────────────────────────────────────╯{Style.RESET_ALL}\n")

# ── playback ─────────────────────────────────────────────────────────────
def play_file(filepath: str):
    if not ensure_mpv():
        err("'mpv' binary not found. Install it first.")
        return
    ok_, result = validate_file(filepath)
    if not ok_:
        err(result)
        return
    ext = os.path.splitext(result)[1].lower()
    if ext and ext not in MUSIC_EXTS and ext not in VIDEO_EXTS:
        warn(f"Unknown extension '{ext}', trying anyway...")
    info(f"▶ Playing: {os.path.basename(result)}")
    try:
        subprocess.run(["mpv", result], stdin=sys.stdin)
    except KeyboardInterrupt:
        print(); warn("Playback interrupted.")

def play_random(directory: str, kind: str):
    files = filter_files(directory, kind)
    if not files:
        err(f"No {kind} files found in: {directory}")
        return
    play_file(random.choice(files))

def play_shuffle(directory: str):
    files = filter_files(directory, "music") + filter_files(directory, "video")
    if not files:
        err(f"No playable files found in: {directory}")
        return
    random.shuffle(files)
    info(f"▶ Shuffle-playing {len(files)} files from {os.path.basename(directory)}")
    try:
        subprocess.run(["mpv", "--shuffle", *files], stdin=sys.stdin)
    except KeyboardInterrupt:
        print(); warn("Playback interrupted.")

# ── interactive prompts ──────────────────────────────────────────────────
def ask_directory(prompt="Directory path: ") -> str:
    while True:
        raw = input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}").strip()
        if not raw:
            return ""
        ok_, result = validate_directory(raw)
        if ok_:
            return result
        err(result)

def ask_name(existing: dict, prompt="Name: ") -> str:
    while True:
        raw = input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}").strip()
        ok_, result = validate_name(raw, existing)
        if ok_:
            return result
        err(result)

def ask_kind() -> str:
    while True:
        raw = input(f"{Fore.CYAN}Type 'm' for music, 'v' for video: {Style.RESET_ALL}").strip().lower()
        if raw in ("m", "music"):
            return "music"
        if raw in ("v", "video"):
            return "video"
        err("Type 'm' or 'v'.")

def ask_play_target() -> list:
    raw = input(
        f"{Fore.CYAN}File path or '<saved_name> <filename>': {Style.RESET_ALL}"
    ).strip()
    if not raw:
        return []
    try:
        return shlex.split(raw)
    except ValueError as e:
        err(f"Parse error: {e}")
        return []

# ── actions ───────────────────────────────────────────────────────────────
def act_random(kind: str, args):
    paths = load_paths()
    
    if args:
        target = args[0]
        
        if target in paths:
            play_random(paths[target], kind)
            
        else:
            ok_, result = validate_directory(target)
            if not ok_:
                err(result)
                return
            play_random(result, kind)
            
    else:
        directory = ask_directory()
        if directory:
            play_random(directory, kind)

def act_play(args):
    if not args:
        args = ask_play_target()
        if not args:
            return
    paths = load_paths()
    if len(args) >= 2 and args[0] in paths:
        candidate = os.path.join(paths[args[0]], args[1])
        play_file(candidate)
        return
    play_file(args[0])

def act_list():
    paths = load_paths()
    if not paths:
        warn("No saved directories yet.")
        return
    print(f"\n{Fore.YELLOW}╭─ Saved directories ──────────────────────────╮{Style.RESET_ALL}")
    for i, (name, path) in enumerate(paths.items(), 1):
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.MAGENTA}{i:>2}{Style.RESET_ALL}. "
              f"{Fore.CYAN}{name}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}│{Style.RESET_ALL}      {Style.DIM}{path}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}╰─────────────────────────────────────────────╯{Style.RESET_ALL}\n")

def act_add(args):
    paths = load_paths()
    directory = ""
    name = ""
    if len(args) >= 1:
        ok_, result = validate_directory(args[0])
        if not ok_:
            err(result); return
        directory = result
    else:
        directory = ask_directory()
        if not directory:
            return
    if len(args) >= 2:
        ok_, result = validate_name(args[1], paths)
        if not ok_:
            err(result); return
        name = result
    else:
        name = ask_name(paths)
    paths[name] = directory
    save_paths(paths)
    ok(f"Saved '{name}' → {directory}")

def act_delete(args):
    paths = load_paths()
    if not paths:
        warn("Nothing to delete.")
        return
    if args:
        name = args[0]
    else:
        act_list()
        name = input(f"{Fore.CYAN}Name to delete: {Style.RESET_ALL}").strip()
    if name in paths:
        del paths[name]
        save_paths(paths)
        ok(f"Deleted '{name}'.")
    else:
        err(f"'{name}' not found.")

def act_shuffle(args):
    paths = load_paths()
    if args:
        target = args[0]        
        if target in paths:
            play_shuffle(paths[target])            
        else:
            ok_, result = validate_directory(target)
            if not ok_:
                err(result)
                return
            play_shuffle(result)

    else:
        directory = ask_directory()
        if directory:
            play_shuffle(directory)

# ── dispatch ──────────────────────────────────────────────────────────────
NUM_SHORTCUTS = {
    "1": ("random", ["music"]),
    "2": ("random", ["video"]),
    "3": ("play",   []),
    "4": ("list",   []),
    "5": ("add",    []),
    "6": ("delete", []),
    "7": ("shuffle", []),
    "8": ("help",   []),
    "9": ("exit",   []),
}

CMD_ALIASES = {
    "random": "random", "r": "random",
    "play":   "play",   "p": "play",
    "list":   "list",   "ls": "list", "saved": "list",
    "add":    "add",    "a": "add",
    "delete": "delete", "del": "delete", "rm": "delete",
    "shuffle":"shuffle","shuf": "shuffle", "s": "shuffle",
    "help":   "help",   "h": "help", "?": "help",
    "exit":   "exit",   "quit": "exit", "q": "exit",
}

def dispatch(cmd: str, args: list):
    target = CMD_ALIASES.get(cmd.lower())
    if target is None:
        err(f"Unknown command '{cmd}'. Type 'help' for the list.")
        return
    if target == "random":
        if not args:
            kind = ask_kind()
        elif args[0] in ("music", "m"):
            kind, args = "music", args[1:]
        elif args[0] in ("video", "v"):
            kind, args = "video", args[1:]
        else:
            err("Usage: random <music|video> [path|saved <name>]")
            return
        act_random(kind, args)
    elif target == "play":    act_play(args)
    elif target == "list":    act_list()
    elif target == "add":     act_add(args)
    elif target == "delete":  act_delete(args)
    elif target == "shuffle": act_shuffle(args)
    elif target == "help":    help_text()
    elif target == "exit":
        return True # Signal to exit

def parse(raw: str):
    """Return (cmd, args) or None."""
    raw = raw.strip()
    if not raw:
        return None
    if raw in NUM_SHORTCUTS:
        return NUM_SHORTCUTS[raw]
    try:
        parts = shlex.split(raw)
    except ValueError as e:
        err(f"Parse error: {e}")
        return None
    if not parts:
        return None
    return (parts[0], parts[1:])