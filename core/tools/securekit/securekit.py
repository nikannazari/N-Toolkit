"""
securekit.py - Core logic of SecureKit
"""
import os
import json
import subprocess
from abc import ABC
import hashlib
import nltk
from cachetools import cached , TTLCache
from pathlib import Path
import string
import secrets
from datetime import datetime, timezone
from cryptography import x509
import tempfile
import stat
import pwd
import grp
import getpass
from pprint import pprint
from colorama import Fore , Style
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import (
    rsa,
    ec,
    dsa,
    ed25519,
    ed448
)

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

from colorama import Fore, Style, init

init(autoreset=True)

COLORS = {
    "info": Fore.CYAN,
    "success": Fore.GREEN,
    "warning": Fore.YELLOW,
    "error": Fore.RED,
    "key": Fore.RED,
    "value": Fore.WHITE,
    "border": Fore.BLUE,
}

def _print(color, symbol, *msg):
    print(f"{color}{symbol}", *msg, Style.RESET_ALL)


def info_3(*msg):
    _print(COLORS["info"], "ℹ", *msg)


def ok_3(*msg):
    _print(COLORS["success"], "✔", *msg)


def warn_3(*msg):
    _print(COLORS["warning"], "⚡", *msg)


def err_3(*msg):
    _print(COLORS["error"], "✘", *msg)


def section(title):
    width = 70
    print(f"\n{COLORS['border']}{'━' * width}")
    print(f"  {Fore.CYAN}{title}")
    print(f"{COLORS['border']}{'━' * width}")


def field(key, value, indent=2):
    spaces = " " * indent

    if isinstance(value, dict):
        print(f"{spaces}{COLORS['key']}{key}{Style.RESET_ALL}:")
        for sub_key, sub_value in value.items():
            field(sub_key, sub_value, indent + 4)

    elif isinstance(value, (list, tuple)):
        if not value:
            value = "Empty"
        else:
            value = ", ".join(str(i) for i in value)

        print(
            f"{spaces}{COLORS['key']}{key}{Style.RESET_ALL}: "
            f"{COLORS['value']}{value}"
        )

    else:
        print(
            f"{spaces}{COLORS['key']}{key}{Style.RESET_ALL}: "
            f"{COLORS['value']}{value}"
        )
        

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
        
def generate_gpg_key(name, email):
    if "\n" in name or "\n" in email:
        err("Error: Invalid input.")
        return

    passphrase = getpass.getpass("Enter passphrase: ")

    if not passphrase:
        err("Please choose a passphrase.")
        return

    key_config = f"""Key-Type: eddsa
Key-Curve: ed25519
Key-Usage: sign cert auth
Subkey-Type: ecdh
Subkey-Curve: cv25519
Subkey-Usage: encrypt
Name-Real: {name}
Name-Email: {email}
Expire-Date: 1y
Passphrase: {passphrase}
%commit
"""

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=True
        ) as config_file:

            config_file.write(key_config)
            config_file.flush()

            result = subprocess.run(
                [
                    "gpg",
                    "--batch",
                    "--generate-key",
                    config_file.name
                ],
                capture_output=True,
                text=True,
                check=False
            )

        if result.returncode == 0:
            ok("GPG key generated successfully!")
        else:
            err("Error generating GPG key:")
            warn(result.stderr)

    except FileNotFoundError:
        err("Error: GPG is not installed.")


def list_gpg_keys():
    try:
        commands = {
            "PUBLIC KEYS": ["gpg", "--list-keys", "--keyid-format", "LONG"],
            "PRIVATE KEYS": ["gpg", "--list-secret-keys", "--keyid-format", "LONG"]
        }

        for title, command in commands.items():
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False
            )

            print(f"{Fore.GREEN}\n{'=' * 50}{Style.RESET_ALL}")
            info(title)
            print(f"{Fore.GREEN}{'=' * 50}{Style.RESET_ALL}")

            if result.returncode != 0:
                err("Error retrieving keys.")
                continue

            if not result.stdout.strip():
                err("No keys found.")
            else:
                warn(result.stdout)

    except FileNotFoundError:
        err("Error: GPG is not installed.")
 

def encrypt_gpg():

    info("\nGPG FILE ENCRYPTION")
    warn_2("=" * 40)
    ok_2("[1] Public Key Encryption")
    ok_2("[2] Symmetric Encryption")
    err_2("[0] Back")

    mode = input("\nSelect encryption mode: ").strip()

    if mode == "0":
        return

    if mode not in ("1", "2"):
        err("Error: Invalid option.")
        return

    # Input file
    input_path = input("\nEnter input file path: ").strip()

    if not input_path:
        err("Error: Input file path is required.")
        return

    input_file = Path(input_path).expanduser()

    if not input_file.is_file():
        err("Error: Input file does not exist.")
        return

    # Output file
    default_output = Path(str(input_file) + ".gpg")

    output_path = input(
        f"Enter output file path [{default_output}]: "
    ).strip()

    output_file = (
        Path(output_path).expanduser()
        if output_path
        else default_output
    )

    if output_file.resolve() == input_file.resolve():
        err("Error: Input and output files cannot be the same.")
        return

    if output_file.exists():
        err("Error: Output file already exists.")
        return

    # Build GPG command
    command = ["gpg", "--batch", "--yes", "--output", str(output_file)]

    if mode == "1":

        info("\nPUBLIC KEY ENCRYPTION")

        recipient = input(
            "Enter recipient email, Key ID or Fingerprint: "
        ).strip()

        if not recipient:
            err("Error: Recipient is required.")
            return

        command.extend([
            "--encrypt",
            "--recipient", recipient
        ])

    elif mode == "2":

        info("\nSYMMETRIC ENCRYPTION")

        passphrase = getpass.getpass("Enter passphrase: ")
        confirm = getpass.getpass("Confirm passphrase: ")

        if not passphrase:
            err("Error: Passphrase cannot be empty.")
            return

        if passphrase != confirm:
            err("Error: Passphrases do not match.")
            return

        command.extend([
            "--symmetric",
            "--cipher-algo", "AES256",
            "--pinentry-mode", "loopback",
            "--passphrase-fd", "0"
        ])

    # Input file
    command.append(str(input_file))

    try:

        if mode == "2":
            result = subprocess.run(
                command,
                input=passphrase + "\n",
                capture_output=True,
                text=True,
                check=False
            )
        else:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False
            )

        if result.returncode == 0:

            if output_file.is_file():
                ok("\nFile encrypted successfully!")
                warn(f"Output: {output_file}")
            else:
                err("Error: GPG did not create the output file.")

        else:
            err("\nEncryption failed.")

            if result.stderr:
                warn(result.stderr.strip())

    except FileNotFoundError:
        err("Error: GPG is not installed.")

    except OSError as error:
        err(f"System error: {error}")


def decrypt_file():

    info("\nGPG FILE DECRYPTION")
    warn_2("=" * 40)

    # Input encrypted file
    input_path = input("\nEnter encrypted file path: ").strip()

    if not input_path:
        err("Error: Input file path is required.")
        return

    input_file = Path(input_path).expanduser()

    if not input_file.is_file():
        err("Error: Encrypted file does not exist.")
        return

    # Output file
    default_output = (
        input_file.with_suffix("")
        if input_file.suffix == ".gpg"
        else Path(str(input_file) + ".decrypted")
    )

    output_path = input(
        f"Enter output file path [{default_output}]: "
    ).strip()

    output_file = (
        Path(output_path).expanduser()
        if output_path
        else default_output
    )

    if output_file.resolve() == input_file.resolve():
        err("Error: Input and output files cannot be the same.")
        return

    if output_file.exists():
        err("Error: Output file already exists.")
        return

    # Ask for passphrase
    passphrase = getpass.getpass(
        "Enter passphrase (leave empty for public-key decryption): "
    )

    # Build GPG command
    command = [
        "gpg",
        "--batch",
        "--yes",
        "--output", str(output_file),
    ]

    if passphrase:
        command.extend([
            "--pinentry-mode", "loopback",
            "--passphrase-fd", "0"
        ])

    command.extend([
        "--decrypt",
        str(input_file)
    ])

    try:

        result = subprocess.run(
            command,
            input=passphrase + "\n" if passphrase else None,
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode == 0 and output_file.is_file():

            ok("\nFile decrypted successfully!")
            warn(f"Output: {output_file}")

        else:

            err("\nDecryption failed.")

            # Remove incomplete output
            if output_file.exists():
                output_file.unlink()

            if result.stderr:
                err(result.stderr.strip())

    except FileNotFoundError:
        err("Error: GPG is not installed.")

    except OSError as error:
        err(f"System error: {error}")

class CertificateInspector:
    def __init__(self,certificate_path):
        
        self.certificate_path = Path(certificate_path)
        self.certificate = None
        
    def load_certificate(self):
        if not self.certificate_path.is_file():
            err(f"File not found in {str(self.certificate_path)}")
            return
            
        data = self.certificate_path.read_bytes()
        
        try: 
            self.certificate = x509.load_pem_x509_certificate(data)
            
        except ValueError:
            self.certificate = x509.load_der_x509_certificate(data)
            
        return self.certificate
    
    def get_subject(self):
        if self.certificate is None:
            err("Certificate not loaded")
            
        subject = self.certificate.subject
        
        return {
            attribute.oid._name: attribute.value
            for attribute in subject
        }
        
    def get_issuer(self):
        if self.certificate is None:
            err("Certificate has not been loaded.")

        issuer = self.certificate.issuer

        return {
            attribute.oid._name: attribute.value
            for attribute in issuer
        }
        
    def get_serial_number(self):
        if self.certificate is None:
            err("Certificate has not been loaded.")

        return self.certificate.serial_number
    
    def get_version(self):
        if self.certificate is None:
            err("Certificate has not been loaded.")

        return self.certificate.version.name
    
    def get_validity(self):
        if self.certificate is None:
            err("Certificate has not been loaded.")

        return {
            "valid_from": self.certificate.not_valid_before_utc,
            "valid_until": self.certificate.not_valid_after_utc
        }
        
    def get_status(self):
        if self.certificate is None:
            err("Certificate has not been loaded.")

        now = datetime.now(timezone.utc)

        valid_from = self.certificate.not_valid_before_utc
        valid_until = self.certificate.not_valid_after_utc

        if now < valid_from:
            return "NOT_YET_VALID"

        elif now > valid_until:
            return "EXPIRED"

        return "VALID"
    
    def get_signature_algorithm(self):
        if self.certificate is None:
            err("Certificate has not been loaded.")

        return self.certificate.signature_hash_algorithm.name
    
    def get_public_key_info(self):
        if self.certificate is None:
            err("Certificate has not been loaded.")

        public_key = self.certificate.public_key()

        if isinstance(public_key, rsa.RSAPublicKey):
            key_type = "RSA"
            key_size = public_key.key_size

        elif isinstance(public_key, ec.EllipticCurvePublicKey):
            key_type = "Elliptic Curve"
            key_size = public_key.key_size

        elif isinstance(public_key, dsa.DSAPublicKey):
            key_type = "DSA"
            key_size = public_key.key_size

        elif isinstance(public_key, ed25519.Ed25519PublicKey):
            key_type = "Ed25519"
            key_size = 256

        elif isinstance(public_key, ed448.Ed448PublicKey):
            key_type = "Ed448"
            key_size = 448

        else:
            key_type = type(public_key).__name__
            key_size = getattr(public_key, "key_size", None)

        return {
            "key_type": key_type,
            "key_size": key_size
        }
        

    def get_fingerprint(self):
        if self.certificate is None:
            err("Certificate has not been loaded.")

        fingerprint = self.certificate.fingerprint(hashes.SHA256())

        return fingerprint.hex(":").upper()

    def get_subject_alternative_names(self):
        if self.certificate is None:
            err("Certificate has not been loaded.")

        try:
            extension = self.certificate.extensions.get_extension_for_class(
                x509.SubjectAlternativeName
            )

            return {
                "DNS": extension.value.get_values_for_type(x509.DNSName),
                "IP": [
                    str(ip)
                    for ip in extension.value.get_values_for_type(x509.IPAddress)
                ]
            }

        except x509.ExtensionNotFound:
            return {
                "DNS": [],
                "IP": []
            }
            
    def display_info(self):
        if self.certificate is None:
            err("Certificate has not been loaded.")

        data = {
            "Subject": self.get_subject(),
            "Issuer": self.get_issuer(),
            "Serial Number": self.get_serial_number(),
            "Version": self.get_version(),
            "Validity": self.get_validity(),
            "Status": self.get_status(),
            "Signature Algorithm": self.get_signature_algorithm(),
            "Public Key": self.get_public_key_info(),
            "SHA-256 Fingerprint": self.get_fingerprint(),
            "Subject Alternative Names": self.get_subject_alternative_names()
        }

        for title, value in data.items():
            section(title)

            if isinstance(value, (dict, list, tuple)):
                if isinstance(value, dict):
                    for key, item in value.items():
                        field(key, item)
                else:
                    for item in value:
                        print(f"  {Fore.GREEN}• {item}")

            else:
                field("Value", value)

        print(f"\n{COLORS['border']}{'━' * 70}")
        ok("Certificate inspection completed.")

        return data

    def get_signature_algorithm(self):
        if self.certificate is None:
            err("Certificate has not been loaded.")

        return {
            "algorithm": self.certificate.signature_algorithm_oid._name,
            "hash_algorithm": (
                self.certificate.signature_hash_algorithm.name
                if self.certificate.signature_hash_algorithm
                else None
            )
        }


class Integrity():
    def __init__(self):
        pass
    
    def hash(self, input_text, algorithms):
        algorithms = algorithms.lower()

        text_algorithms = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha224": hashlib.sha224,
            "sha256": hashlib.sha256,
            "sha384": hashlib.sha384,
            "sha512": hashlib.sha512,
        }

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
            
        return digest

    def check(self,input_file,hash,algorithm):
        
        input_file_hash = self.hash(input_file,algorithm)
        
        ok("File has been checked successfully")
        info(40 * "━")
        status = f"{Fore.CYAN + Style.BRIGHT + Style.RESET_ALL}STATUS : "

        if input_file_hash == hash:
            status += f"{Fore.GREEN} SAME{Style.RESET_ALL}"
            
        else:
            status += f"{Fore.RED} DIFFERENT{Style.RESET_ALL}"
            
        print(status)
        
    def chuncked_hash(self, file_path, algorithm="sha256"):
        hash_function = hashlib.new(algorithm)

        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_function.update(chunk)

        return hash_function.hexdigest()
        
    def create_baseline(self,input_directory,output_path = "../../../saved_data/securekit/integrity/",algorithm="sha256"):
        #If baseline.json is checked inside the directory, it may be inserted into the scan itself.
        #If a permission error occurs while reading one of the files, the operation may remain half-finished.

        input_directory = Path(input_directory)
        output_path = Path(output_path)

        if not input_directory.is_dir():
            err("Directory does not exist.")
        
        baseline = {
            "algorithm" : algorithm,
            "directory" : str(input_directory.resolve()),
            "files" : {}
        }
        
        for file_path in input_directory.rglob("*"):
            if not file_path.is_file():
                    continue

            relative_path = str(file_path.relative_to(input_directory))

            file_hash = self.chuncked_hash(file_path,algorithm)

            baseline["files"][relative_path] = file_hash

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(baseline, file, indent=4)

        ok(f"File sucessfully checked and json is on {str(output_path.resolve())}")

        info("Do you want to see the json file?")
        print(f"[1] Yes \n[2] No")
        user_input = input(">>>")
        if user_input == "1":
            pprint(baseline)

    def verify_baseline(self,input_dir, baseline_path):

        input_dir = Path(input_dir)
        baseline_path = Path(baseline_path)

        if not baseline_path.is_file():
            err("Baseline file not found.")

        if not input_dir.is_dir():
            err("Directory does not exist.")

        with baseline_path.open("r", encoding="utf-8") as file:
            baseline = json.load(file)

        algorithm = baseline["algorithm"]
        original_files = baseline["files"]

        current_files = {}

        for file_path in input_dir.rglob("*"):

            if file_path.is_symlink() or not file_path.is_file():
                continue

            relative_path = str(
                file_path.relative_to(input_dir)
            )

            current_files[relative_path] = self.chuncked_hash(
                file_path,
                algorithm
            )

        changes = {
            "added": [],
            "modified": [],
            "deleted": [],
            "unchanged": []
        }

        for file_path, file_hash in current_files.items():

            if file_path not in original_files:
                changes["added"].append(file_path)

            elif file_hash != original_files[file_path]:
                changes["modified"].append(file_path)

            else:
                changes["unchanged"].append(file_path)

        for file_path in original_files:

            if file_path not in current_files:
                changes["deleted"].append(file_path)

        ok("Files has been successfuuly checked")
        info("Changes : ")
        print(f"{Fore.CYAN}{40 * "━"}{Style.RESET_ALL}")
        # pprint(changes)
        
        for key , item in changes.items():
            if key == "added":
                print(f"{Fore.GREEN}Aded{Style.RESET_ALL}")
                
                for i in item:
                    print(f"    {Fore.YELLOW}{i}")
                    
                print(f"{Fore.CYAN}{40 * "━"}{Style.RESET_ALL}")

            if key == "deleted":
                print(f"{Fore.RED}Deleted{Style.RESET_ALL}")
                
                for i in item:
                    print(f"    {Fore.YELLOW}{i}")
                    
                print(f"{Fore.WHITE}{40 * "━"}{Style.RESET_ALL}")
                    
            if key == "modified":
                print(f"{Fore.MAGENTA}Modified{Style.RESET_ALL}")
                
                for i in item:
                    print(f"    {Fore.YELLOW}{i}")
                    
                print(f"{Fore.CYAN}{40 * "━"}{Style.RESET_ALL}")
                    
            if key == "unchanged":
                print(f"{Fore.WHITE}Unchanged{Style.RESET_ALL}")
                
                for i in item:
                    print(f"    {Fore.YELLOW}{i}")
                    
                print(f"{Fore.CYAN}{40 * "━"}{Style.RESET_ALL}")


class PermissionsChecker:

    def __init__(self, path):
        self.path = Path(path)

    def _get_stat(self):
        """Return file metadata after checking that the path exists."""
        if not self.path.exists():
            err(f"Path does not exist: {self.path}")

        return self.path.stat()

    def get_permissions(self):
        """Return the complete file mode."""
        return self._get_stat().st_mode

    def get_octal_permissions(self):
        """Return permissions in octal format, e.g. 0o755."""
        permissions = stat.S_IMODE(self.get_permissions())
        return oct(permissions)

    def get_symbolic_permissions(self):
        """Return permissions in symbolic format, e.g. rwxr-xr-x."""
        permissions = stat.S_IMODE(self.get_permissions())

        result = []

        permission_map = [
            (stat.S_IRUSR, "r"),
            (stat.S_IWUSR, "w"),
            (stat.S_IXUSR, "x"),
            (stat.S_IRGRP, "r"),
            (stat.S_IWGRP, "w"),
            (stat.S_IXGRP, "x"),
            (stat.S_IROTH, "r"),
            (stat.S_IWOTH, "w"),
            (stat.S_IXOTH, "x"),
        ]

        for bit, character in permission_map:
            result.append(character if permissions & bit else "-")

        # Handle special permission bits.
        if permissions & stat.S_ISUID:
            result[2] = "s" if permissions & stat.S_IXUSR else "S"

        if permissions & stat.S_ISGID:
            result[5] = "s" if permissions & stat.S_IXGRP else "S"

        if permissions & stat.S_ISVTX:
            result[8] = "t" if permissions & stat.S_IXOTH else "T"

        return "".join(result)

    def get_owner(self):
        """Return the owner username."""
        uid = self._get_stat().st_uid

        try:
            return pwd.getpwuid(uid).pw_name
        except KeyError:
            return str(uid)

    def get_group(self):
        """Return the group name."""
        gid = self._get_stat().st_gid

        try:
            return grp.getgrgid(gid).gr_name
        except KeyError:
            return str(gid)

    def check_read_access(self):
        """Check whether the current process can read the path."""
        return os.access(self.path, os.R_OK)

    def check_write_access(self):
        """Check whether the current process can write to the path."""
        return os.access(self.path, os.W_OK)

    def check_execute_access(self):
        """Check whether the current process can execute or traverse the path."""
        return os.access(self.path, os.X_OK)

    def display_info(self):
        """Display all collected permission information."""
        self._get_stat()
        permissions = stat.S_IMODE(self.get_permissions())

        data = {
            "Path": str(self.path.resolve()),
            "Type": "Directory" if self.path.is_dir() else "File",
            "Owner": self.get_owner(),
            "Group": self.get_group(),
            "Octal Permissions": self.get_octal_permissions(),
            "Symbolic Permissions": self.get_symbolic_permissions(),
            "Read Access": self.check_read_access(),
            "Write Access": self.check_write_access(),
            "Execute Access": self.check_execute_access(),
            "setuid": bool(permissions & stat.S_ISUID),
            "setgid": bool(permissions & stat.S_ISGID),
            "sticky": bool(permissions & stat.S_ISVTX),
        }
        
        ok_2("╭─────────────Permissions Inspector────────────────────────────────────────╮\n│")
        
        for key , value in data.items():
            print(f"{Fore.GREEN}│{Style.RESET_ALL}   {Fore.YELLOW}{key:<24}{Style.RESET_ALL}{Fore.RED}: {Style.RESET_ALL}{Fore.CYAN}{value}{Style.RESET_ALL}")
            
        ok_2("│\n╰──────────────────────────────────────────────────────────────────────────╯")
