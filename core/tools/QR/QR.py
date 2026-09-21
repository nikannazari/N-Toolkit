"""
qr.py - Core logic of QR tool.
"""
import os
import json
import datetime
import subprocess
import sys

# Dynamic loading helpers
TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(TOOL_DIR, "..", "..", ".."))
CONFIG_DIR = os.path.join(PROJECT_ROOT, "saved_data", "QR")
CONFIG_FILE = os.path.join(CONFIG_DIR, "history.json")

def _import_modules():
    """Import external libraries and handle missing errors."""
    try:
        import qrcode
        from PIL import Image
        return qrcode, Image
    except ImportError:
        return None, None

def _import_decoder():
    try:
        from pyzbar.pyzbar import decode
        import cv2
        import numpy as np
        return decode, cv2, np
    except ImportError:
        return None, None, None

qrcode, Image = _import_modules()
decode, cv2, np = _import_decoder()

# ── Persistence ──
def ensure_config():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump([], f)

def load_history() -> list:
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_history(data: list):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_to_history(text: str, source: str):
    history = load_history()
    history.append({
        "text": text,
        "source": source,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_history(history)

# ── Color Helpers ──
def info(msg):  print(f"{Fore.CYAN}{msg}{Style.RESET_ALL}")
def ok(msg):    print(f"{Fore.GREEN}✔ {msg}{Style.RESET_ALL}")
def warn(msg):  print(f"{Fore.YELLOW}⚡ {msg}{Style.RESET_ALL}")
def err(msg):   print(f"{Fore.RED}✘ {msg}{Style.RESET_ALL}")

# Fix missing imports in this scope
from colorama import Fore, Style

# ── Actions ──
def generate_qr(text: str, filename: str = "qr_code.png"):
    if not qrcode or not Image:
        err("Missing dependencies. Run: pip install qrcode[pil]")
        return
        
    save_path = os.path.join(os.getcwd(), filename)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(save_path)
    ok(f"QR Code generated and saved to: {save_path}")

def decode_image(filepath: str):
    if not decode:
        err("Missing dependencies. Run: pip install pyzbar opencv-python")
        return
    try:
        img = Image.open(filepath)
        results = decode(img)
        if not results:
            warn(f"No QR code found in {filepath}.")
            return
            
        for res in results:
            text = res.data.decode('utf-8')
            ok(f"Decoded: {text}")
            add_to_history(text, f"File: {filepath}")
    except Exception as e:
        err(f"Failed to read image: {e}")

def batch_decode(directory: str):
    if not decode:
        err("Missing dependencies.")
        return
        
    valid_exts = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
    found_any = False
    
    for filename in os.listdir(directory):
        if any(filename.lower().endswith(ext) for ext in valid_exts):
            filepath = os.path.join(directory, filename)
            img = Image.open(filepath)
            results = decode(img)
            for res in results:
                text = res.data.decode('utf-8')
                ok(f"[{filename}] -> {text}")
                add_to_history(text, f"Batch: {filepath}")
                found_any = True
                
    if not found_any:
        warn("No QR codes found in the specified directory.")

def decode_webcam():
    if not cv2 or not decode:
        err("Missing dependencies. Run: pip install opencv-python pyzbar")
        return

    info("Starting webcam. Press 'q' in the webcam window to quit.")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        err("Cannot access webcam.")
        return

    found = False
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                err("Failed to grab frame.")
                break
                
            # Convert to grayscale for pyzbar
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            results = decode(gray)
            
            for res in results:
                text = res.data.decode('utf-8')
                points = res.polygon
                
                # Draw bounding box
                if len(points) > 0:
                    pts = [(p.x, p.y) for p in points]
                    cv2.polylines(frame, [np.array(pts, np.int32)], True, (0, 255, 0), 3)
                    
                cv2.putText(frame, text, (points[0].x, points[0].y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                            
                ok(f"Decoded from webcam: {text}")
                add_to_history(text, "Webcam")
                found = True
                break  # Exit after first detection
                
            cv2.imshow('QR Scanner - Press Q to Exit', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or found:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if not found:
            warn("No QR code detected before closing.")

def decode_screen():
    if not cv2 or not decode:
        err("Missing dependencies. Run: pip install opencv-python pyzbar mss")
        return
        
    try:
        import mss
    except ImportError:
        err("Missing dependency: pip install mss")
        return
        
    info("Scanning screen...")
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        
        # Convert to numpy array for cv2
        img = np.array(screenshot)
        # mss returns BGRA, convert to BGR for cv2/pyzbar
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        results = decode(img)
        if not results:
            warn("No QR code found on screen.")
            return
            
        for res in results:
            text = res.data.decode('utf-8')
            ok(f"Decoded from screen: {text}")
            add_to_history(text, "Screen Capture")

def show_history():
    history = load_history()
    if not history:
        warn("History is empty.")
        return
        
    print(f"\n{Fore.YELLOW}╭─ QR History ───────────────────────────────────╮{Style.RESET_ALL}")
    for i, entry in enumerate(history, 1):
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.MAGENTA}{i}.{Style.RESET_ALL} {Fore.CYAN}{entry['text']}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}│{Style.RESET_ALL}    {Style.DIM}Src: {entry['source']} | Time: {entry['time']}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}╰────────────────────────────────────────────────╯{Style.RESET_ALL}\n")

def clear_history():
    save_history([])
    ok("History cleared.")