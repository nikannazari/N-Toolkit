"""
mpv++_validators.py - Validation utilities for mpv++.
"""
import os
import shutil
from typing import List, Tuple

MUSIC_EXTS = {".mp3", ".flac", ".wav", ".ogg", ".m4a", ".opus", ".aac", ".wma"}
VIDEO_EXTS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv",
              ".wmv", ".mpg", ".mpeg", ".ts", ".m4v", ".webm"}

def validate_directory(path: str) -> Tuple[bool, str]:
    if not path or not path.strip():
        return False, "Path is empty."
    path = os.path.expanduser(path.strip())
    if not os.path.exists(path):
        return False, f"Path does not exist: {path}"
    if not os.path.isdir(path):
        return False, f"Not a directory: {path}"
    if not os.access(path, os.R_OK):
        return False, f"Directory not readable: {path}"
    return True, os.path.abspath(path)

def validate_file(path: str) -> Tuple[bool, str]:
    if not path or not path.strip():
        return False, "File path is empty."
    path = os.path.expanduser(path.strip())
    if not os.path.isfile(path):
        return False, f"File not found: {path}"
    return True, os.path.abspath(path)

def validate_name(name: str, existing: dict) -> Tuple[bool, str]:
    if not name or not name.strip():
        return False, "Name cannot be empty."
    name = name.strip()
    if any(c in name for c in "/\\:"):
        return False, "Name cannot contain '/', '\\', or ':'."
    if name in existing:
        return False, f"'{name}' already exists. Pick another or delete the old one."
    return True, name

def ensure_mpv() -> bool:
    return shutil.which("mpv") is not None

def filter_files(directory: str, kind: str) -> List[str]:
    exts = MUSIC_EXTS if kind == "music" else VIDEO_EXTS
    out = []
    for entry in os.listdir(directory):
        full = os.path.join(directory, entry)
        if os.path.isfile(full) and os.path.splitext(entry)[1].lower() in exts:
            out.append(full)
    return out