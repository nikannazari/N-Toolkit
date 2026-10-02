"""
status.py - Core logic of Status tool.
"""
import os
import time
import subprocess
import shutil
from colorama import Fore, Style

try:
    import psutil
except ImportError:
    print(f"{Fore.RED}Missing dependency: psutil. Run: pip install psutil{Style.RESET_ALL}")
    exit(1)

def info(msg):  print(f"{Fore.CYAN}{msg}{Style.RESET_ALL}")
def ok(msg):    print(f"{Fore.GREEN}✔ {msg}{Style.RESET_ALL}")
def warn(msg):  print(f"{Fore.YELLOW}⚡ {msg}{Style.RESET_ALL}")
def err(msg):   print(f"{Fore.RED}✘ {msg}{Style.RESET_ALL}")

def make_bar(percent: float, length: int = 20) -> str:
    """Generates a colored ASCII progress bar."""
    filled = int((percent / 100) * length)
    empty = length - filled
    
    if percent < 50:
        color = Fore.GREEN
    elif percent < 80:
        color = Fore.YELLOW
    else:
        color = Fore.RED
        
    return f"{color}{'█' * filled}{'░' * empty}{Style.RESET_ALL}"

def fmt_bytes(b: int) -> str:
    """Formats bytes into human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if b < 1024:
            return f"{b:.1f}{unit}"
        b /= 1024

def show_cpu():
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}── CPU ───────────────────────────────{Style.RESET_ALL}")
    usage = psutil.cpu_percent(interval=0.5)
    print(f"  Usage:    [{make_bar(usage)}] {usage}%")
    
    freq = psutil.cpu_freq()
    if freq:
        print(f"  Freq:     {freq.current:.0f}MHz / {freq.max:.0f}MHz")
        
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    print(f"  Cores:    {cores} Physical / {threads} Logical")

def show_ram():
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}── Memory (RAM) ─────────────────────{Style.RESET_ALL}")
    mem = psutil.virtual_memory()
    print(f"  Usage:    [{make_bar(mem.percent)}] {mem.percent}%")
    print(f"  Used:     {fmt_bytes(mem.used)} / {fmt_bytes(mem.total)}")
    print(f"  Available:{fmt_bytes(mem.available)}")

def show_disk():
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}── Disk ─────────────────────────────{Style.RESET_ALL}")
    partitions = psutil.disk_partitions()
    for p in partitions:
        if 'cdrom' in p.opts or p.fstype == '':
            continue
        try:
            usage = psutil.disk_usage(p.mountpoint)
            print(f"  [{p.device}] mounted at {p.mountpoint}")
            print(f"    [{make_bar(usage.percent)}] {usage.percent}%")
            print(f"    Used: {fmt_bytes(usage.used)} / {fmt_bytes(usage.total)}")
        except PermissionError:
            continue

def show_network():
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}── Network ──────────────────────────{Style.RESET_ALL}")
    io = psutil.net_io_counters()
    print(f"  Sent:     {fmt_bytes(io.bytes_sent)} ({io.packets_sent} packets)")
    print(f"  Received: {fmt_bytes(io.bytes_recv)} ({io.packets_recv} packets)")

def show_battery():
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}── Battery ──────────────────────────{Style.RESET_ALL}")
    bat = psutil.sensors_battery()
    if not bat:
        warn("No battery detected.")
        return
        
    print(f"  Charge:   [{make_bar(bat.percent)}] {bat.percent}%")
    if bat.power_plugged:
        print(f"  Status:   Plugged in (Charging)")
    else:
        print(f"  Status:   Discharging")
        if bat.secsleft != psutil.POWER_TIME_UNLIMITED and bat.secsleft != psutil.POWER_TIME_UNKNOWN:
            mins, secs = divmod(bat.secsleft, 60)
            hrs, mins = divmod(mins, 60)
            print(f"  Time left:{hrs}h {mins}m {secs}s")

def show_fans():
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}── Fans ─────────────────────────────{Style.RESET_ALL}")
    try:
        fans = psutil.sensors_fans()
        if not fans:
            warn("No fans detected.")
            return
            
        for name, entries in fans.items():
            print(f"  [{name}]")
            for entry in entries:
                print(f"    {entry.label or 'Fan'}: {entry.current} RPM")
    except AttributeError:
        warn("Fans not supported on this OS.")

def show_temp():
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}── Temperatures ─────────────────────{Style.RESET_ALL}")
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            warn("No temperature sensors detected.")
            return
            
        for name, entries in temps.items():
            print(f"  [{name}]")
            for entry in entries:
                print(f"    {entry.label or 'Temp'}: {entry.current}°C (High: {entry.high or 'N/A'}°C)")
    except AttributeError:
        warn("Temperatures not supported on this OS.")

def show_gpu():
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}── GPU ──────────────────────────────{Style.RESET_ALL}")
    if not shutil.which("nvidia-smi"):
        warn("GPU monitoring requires 'nvidia-smi' (NVIDIA cards only).")
        return
        
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            data = result.stdout.strip().split(", ")
            util, mem_used, mem_total = int(data[0]), int(data[1]), int(data[2])
            mem_percent = (mem_used / mem_total) * 100 if mem_total > 0 else 0
            
            print(f"  Usage:    [{make_bar(util)}] {util}%")
            print(f"  VRAM:     [{make_bar(mem_percent)}] {mem_percent:.1f}%")
            print(f"  Memory:   {mem_used}MB / {mem_total}MB")
        else:
            err("Failed to read nvidia-smi data.")
    except Exception as e:
        err(f"Error reading GPU: {e}")

def show_procs(limit=5):
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}── Top Processes (CPU) ──────────────{Style.RESET_ALL}")
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    # Sort by CPU usage
    procs.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
    
    print(f"  {'PID':<8} {'CPU%':<8} {'MEM%':<8} {'Name'}")
    print(f"  {'─'*8} {'─'*8} {'─'*8} {'─'*20}")
    for p in procs[:limit]:
        pid = p.get('pid', 'N/A')
        cpu = p.get('cpu_percent', 0)
        mem = p.get('memory_percent', 0)
        name = p.get('name', 'Unknown')[:20]
        print(f"  {str(pid):<8} {cpu:<8.1f} {mem:<8.1f} {name}")

def show_all():
    show_cpu()
    show_ram()
    show_gpu()
    show_disk()
    show_network()
    show_battery()
    show_fans()
    show_temp()
    show_procs()
    print()