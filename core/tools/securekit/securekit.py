"""
securekit.py - Core logic of SecureKit
"""
import os
import subprocess
from abc import ABC
import hashlib
import nltk
from cachetools import cached , TTLCache
from pathlib import Path
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

import hashlib
import subprocess


def hash(hash_type, input_text, algorithms):
    algorithms = algorithms.lower()

    text_algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha224": hashlib.sha224,
        "sha256": hashlib.sha256,
        "sha384": hashlib.sha384,
        "sha512": hashlib.sha512,
    }

    if hash_type == "text":
        if algorithms not in text_algorithms:
            err(f"Unsupported hash algorithm: {algorithms}")
            return

        digest = text_algorithms[algorithms](
            _to_bytes(input_text)
        ).hexdigest()

        ok(f"{input_text} hashed by {algorithms}: {digest}")

    elif hash_type == "file":
        if algorithms not in text_algorithms:
            err(f"Unsupported hash algorithm: {algorithms}")
            return

        command = f"{algorithms}sum"

        try:
            result = subprocess.run(
                [command, input_text],
                capture_output=True,
                text=True,
                check=True
            )

            digest = result.stdout.split()[0]
            ok(f"{input_text} hashed by {algorithms}: {digest}")

        except FileNotFoundError:
            err(f"Command not found: {command}")

        except subprocess.CalledProcessError as exc:
            err(exc.stderr.strip() or "File hashing failed.")

    else:
        err("Available hash types are <text> and <file>")
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
    "apple","bridge","castle","cloud","coffee","forest","garden","guitar","island","jungle",
    "keyboard","lemon","mountain","ocean","orange","planet","python","river","rocket","shadow",
    "silver","summer","thunder","tiger","window",
    "apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon",
    "mango", "nectarine", "orange", "pineapple", "quince", "raspberry", "strawberry", "tangerine", "ugli", "victoria plum",
    "watermelon", "xigua", "yellow passion fruit", "zucchini",
    "house", "car", "dog", "cat", "book", "pen", "computer", "phone", "table", "chair",
    "sun", "moon", "stars", "sky", "ocean", "river", "mountain", "forest", "desert", "city",
    "food", "drink", "pizza", "burger", "steak", "sushi", "tea", "coffee", "water", "milk",
    "science", "math", "history", "literature", "art", "music", "dance", "games", "movies", "books",
    "friend", "family", "love", "peace", "happiness", "sadness", "angry", "happy", "surprised", "excited",
    "yes", "no", "maybe", "when", "where", "why", "how", "what", "who", "it",
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "sun", "moon", "stars", "sky", "ocean", "river", "mountain", "forest", "desert", "city",
    "red", "green", "blue", "yellow", "black", "white", "purple", "orange", "brown", "gray",
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
        
CACHE = TTLCache(
    maxsize=100,
    ttl=60 * 60 * 24 * 7
)

# @cached(CACHE)
# def update_curpos():
#     nltk.download('words')

class MemorablePassword(PasswordGenerator):
    def __init__(self,easy,num_of_words,seprator,captalization):
        if num_of_words < 1:
            err("Number of words most beat least 1")
            
        self.easy = easy
        self.num_of_words = num_of_words
        self.seprator = seprator
        self.captalization = True if captalization.lower() == "yes" else False

        # update_curpos()
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

class Encryptor:
    def __init__(
        self,
        user_input,
        user_output,
        password,
        iteration="60000",
        salt=True,
    ):
        self.user_input = user_input
        self.user_output = user_output
        self.password = password
        self.iteration = str(iteration)
        self.salt = salt

    def encrypt(self):
        command = [
            "openssl",
            "enc",
            "-aes-256-cbc",
            "-pbkdf2",
            "-iter", self.iteration,
            "-pass", "stdin",
            "-in", self.user_input,
            "-out", self.user_output,
        ]

        if self.salt:
            command.append("-salt")
        else:
            command.append("-nosalt")

        result = subprocess.run(
            command,
            input=self.password + "\n",
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            ok("Encryption completed successfully.")

        else:
            err("Encryption failed.")
            warn(result.stderr)
            
class Decryptor:
    def __init__(
        self,
        user_input,
        user_output,
        iteration,
    ):
        self.iteration = str(iteration)
        self.user_input = user_input
        self.user_output = user_output
    
    def decrypt(self):
        command = [
            "openssl",
            "enc",
            "-d",
            "-aes-256-cbc",
            "-pbkdf2",
            "-iter", self.iteration,
            "-in", self.user_input,
            "-out", self.user_output,
        ]
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            ok("Decryption completed successfully.")
            
        else:
            err("Decryption failed.")
            warn(result.stderr)


class SSH_Generator:
    def __init__(
        self,
        key_name,
        comment,
    ):
        self.key_name = key_name
        self.comment = comment

    def generate_key(self):
        
        ssh_dir = Path.home() / ".ssh"
        ssh_dir.mkdir(mode=0o700 , parents=True , exist_ok=True)
        
        key_path = ssh_dir / self.key_name
        public_key_path = Path(f"{key_path}.pub")
        
        if key_path.exists() or public_key_path.exists():
            err(f"A key is already exist in {key_path}")
            
        command = [
            "ssh-keygen",
            "-t" , "ed25519",
            "-C" , self.comment,
            "-f" , key_path
        ]
        
        try:
            result = subprocess.run(command , check=False)            
            if result.returncode == 0:
                ok(f"Key successfully generated in {key_path}")
                
            else:
                err("SSH key generation was cancelled or failed")
                
        except FileNotFoundError:
            err("ssh-keygen is not installed")
            
        
def show_public_key(key_name):

    public_key_path = Path.home() / ".ssh" / f"{key_name}.pub"
    
    if not public_key_path.is_file():
        err("Error: Public key not found.")
        return
        
    result = subprocess.run(
        ["cat", str(public_key_path)],
        check=False
    )
    
    if result.returncode != 0:
        err("Error: Could not display public key.")
        
def show_fingerprint(key_name):
    public_key_path = Path.home() / ".ssh" / f"{key_name}.pub"
    
    if not public_key_path.is_file():
        err("Error: Public key not found.")
        return
    
    result = subprocess.run(
        ["ssh-keygen", "-lf", str(public_key_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    
    if result.returncode == 0:
        ok(result.stdout.strip())
        
    else:
        err("Error : Could not calculate fingerprint.")
        if result.stderr :
             warn(result.stderr.strip())
             
def list_key():
    ssh_dir = Path.home() / ".ssh"
    
    if not ssh_dir.is_dir():
        err("SSH directory does not exist.")
        return
    
    public_keys = sorted(ssh_dir.glob("*.pub"))
    
    if not public_keys:
        err("No public SSH keys found.")
        return
    
    ok("SSH Keys : ")
    print("-" * 40)

    for public_key in public_keys:
        private_key = public_key.with_suffix("")

        info(f"Key name: {private_key.name}")
        ok(f"Public key: {public_key.name}")

        if private_key.is_file():
            warn("Private key: Found")
        else:
            err("Private key: Not found")

        print("-" * 40)