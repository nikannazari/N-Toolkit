"""
securekit.py - Core logic of SecureKit
"""
import os
import subprocess
from abc import ABC, abstractmethod
import hashlib
import nltk
import string
import secrets
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
        ok(f"{input_text} hashed by {algorithms} : {hashlib.md5(_to_bytes(input_text)).hexdigest()}")
    elif algorithms == "sha1":
        ok(f"{input_text} hashed by {algorithms} : {hashlib.sha1(_to_bytes(input_text)).hexdigest()}")
    elif algorithms == "sha256":
        ok(f"{input_text} hashed by {algorithms} : {hashlib.sha256(_to_bytes(input_text)).hexdigest()}")
    elif algorithms == "sha224":
        ok(f"{input_text} hashed by {algorithms} : {hashlib.sha224(_to_bytes(input_text)).hexdigest()}")
    elif algorithms == "sha384":
        ok(f"{input_text} hashed by {algorithms} : {hashlib.sha384(_to_bytes(input_text)).hexdigest()}")
    elif algorithms == "sha512":
        ok(f"{input_text} hashed by {algorithms} : {hashlib.sha512(_to_bytes(input_text)).hexdigest()}")
class PasswordGenerator(ABC):
    """Abstract base class for password generators."""
    def generate(self):
        raise NotImplementedError    


class PinGenerator(PasswordGenerator):
    def __init__(self , lenght=10) -> None:
        self.lenght = int(lenght)
        if lenght < 2:
            err("Yout pin lenght must be at least 2")
            return
        
    def generate(self):
        password =  "".join(
            secrets.choice(string.digits)
            for _ in range(self.lenght)
        )
        ok(f"Pin : {password}")

DEFAULT_WORDS = [
    "apple",
    "bridge",
    "castle",
    "cloud",
    "coffee",
    "forest",
    "garden",
    "guitar",
    "island",
    "jungle",
    "keyboard",
    "lemon",
    "mountain",
    "ocean",
    "orange",
    "planet",
    "python",
    "river",
    "rocket",
    "shadow",
    "silver",
    "summer",
    "thunder",
    "tiger",
    "window",
]
class RandomPasswordGenerator(PasswordGenerator):
    """Generate random passwords."""

    def __init__(
        self,
        length,
        include_numbers,
        include_symbols,
    ):
        if length < 1:
            err("Password length must be at least 1.")

        self.length = length
        self.include_numbers = True if include_numbers.lower() == "yes" else False
        self.include_symbols = True if include_symbols.lower() == "yes" else False

        self.characters = string.ascii_letters

        if self.include_numbers:
            self.characters += string.digits

        if self.include_symbols:
            self.characters += string.punctuation

    def generate(self) -> str:
        """Generate a random password."""

        password =  "".join(
            secrets.choice(self.characters)
            for _ in range(self.length)
        )
        ok(f"Random Password : {password}")
        
        
nltk.download('words')

class MemorablePassword(PasswordGenerator):
    def __init__(self,easy,num_of_words,seprator,captalization):
        if num_of_words < 1:
            err("Number of words most beat least 1")
            
        self.easy = easy
        self.num_of_words = num_of_words
        self.seprator = seprator
        self.captalization = True if captalization.lower() == "yes" else False
        self.vocabulary = DEFAULT_WORDS if self.easy.lower() == "yes" else nltk.corpus.words.words()
        
    def generate(self):
        words = [
            secrets.choice(self.vocabulary)
            for _ in range(self.num_of_words)
        ]
        if self.captalization:
            words = [
                word.capitalize()
                for word in words
            ]
        ok(f"Memorable Password : {self.seprator.join(words)}")