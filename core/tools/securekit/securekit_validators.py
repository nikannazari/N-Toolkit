"""
securekit_validators.py - validate sub commands of tool
"""
import shutil


def is_installed(package: str) -> bool:
    return shutil.which(package) is not None