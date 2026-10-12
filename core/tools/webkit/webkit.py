"""
webkit.py - Core logic of WebKit.
"""
import os
import ssl
import socket
import datetime
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print(f"{Fore.RED}Missing dependencies. Run: pip install requests beautifulsoup4{Style.RESET_ALL}")
    exit(1)

# ── Path Configuration ──
TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(TOOL_DIR, "..", "..", ".."))
SAVE_BASE_DIR = os.path.join(PROJECT_ROOT, "saved_data", "WebKit")

def info(msg):  print(f"{Fore.CYAN}{msg}{Style.RESET_ALL}")
def ok(msg):    print(f"{Fore.GREEN}✔ {msg}{Style.RESET_ALL}")
def warn(msg):  print(f"{Fore.YELLOW}⚡ {msg}{Style.RESET_ALL}")
def err(msg):   print(f"{Fore.RED}✘ {msg}{Style.RESET_ALL}")

def _get_save_dir(url: str) -> str:
    """Creates and returns the save directory for a specific domain."""
    domain = urlparse(url).netloc
    save_dir = os.path.join(SAVE_BASE_DIR, domain)
    os.makedirs(save_dir, exist_ok=True)
    return save_dir

def _fetch(url: str):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/91.0.4472.114 Safari/537.36'}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        return res
    except requests.RequestException as e:
        err(f"Failed to fetch {url}: {e}")
        return None

def check_status(url: str):
    info(f"Checking status for {url}...")
    res = _fetch(url)
    if res:
        print(f"  {Fore.GREEN}Status:{Style.RESET_ALL} {res.status_code} {res.reason}")
        print(f"  {Fore.GREEN}Server:{Style.RESET_ALL} {res.headers.get('Server', 'Unknown')}")
        print(f"  {Fore.GREEN}Content-Type:{Style.RESET_ALL} {res.headers.get('Content-Type', 'Unknown')}")

def download_website(url: str):
    info(f"Downloading HTML from {url}...")
    res = _fetch(url)
    if res:
        save_dir = _get_save_dir(url)
        domain = urlparse(url).netloc
        filepath = os.path.join(save_dir, f"{domain}.html")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(res.text)
        ok(f"Website HTML saved to {filepath}")

def extract_links(url: str):
    info(f"Extracting links from {url}...")
    res = _fetch(url)
    if res:
        soup = BeautifulSoup(res.text, "html.parser")
        links = set()
        for a in soup.find_all("a", href=True):
            full_link = urljoin(url, a["href"])
            links.add(full_link)
        
        print(f"\n{Fore.YELLOW}╭─ Found {len(links)} Links ──────────────────────╮{Style.RESET_ALL}")
        for i, link in enumerate(links, 1):
            print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.CYAN}{i}.{Style.RESET_ALL} {link}")
        print(f"{Fore.YELLOW}╰────────────────────────────────────────────────╯{Style.RESET_ALL}\n")

def download_images(url: str):
    info(f"Downloading images from {url}...")
    res = _fetch(url)
    if res:
        soup = BeautifulSoup(res.text, "html.parser")
        img_tags = soup.find_all("img", src=True)
        
        if not img_tags:
            warn("No images found.")
            return
            
        save_dir = _get_save_dir(url)
        img_dir = os.path.join(save_dir, "images")
        os.makedirs(img_dir, exist_ok=True)
        
        count = 0
        for img in img_tags:
            img_url = urljoin(url, img["src"])
            try:
                img_data = requests.get(img_url, stream=True, timeout=5).content
                img_name = os.path.basename(urlparse(img_url).path)
                if not img_name:
                    img_name = f"image_{count}.jpg"
                with open(os.path.join(img_dir, img_name), "wb") as f:
                    f.write(img_data)
                count += 1
            except Exception:
                continue
        ok(f"Downloaded {count} images to {img_dir}")

def website_screenshot(url: str):
    info(f"Taking screenshot of {url}...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        err("Missing dependencies. Run: pip install selenium webdriver-manager")
        return

    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        
        save_dir = _get_save_dir(url)
        domain = urlparse(url).netloc
        filepath = os.path.join(save_dir, f"{domain}_screenshot.png")
        
        driver.save_screenshot(filepath)
        driver.quit()
        ok(f"Screenshot saved to {filepath}")
    except Exception as e:
        err(f"Failed to take screenshot: {e}")

def seo_info(url: str):
    info(f"Fetching SEO info for {url}...")
    res = _fetch(url)
    if res:
        soup = BeautifulSoup(res.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No title found"
        
        desc_tag = soup.find("meta", attrs={"name": "description"})
        desc = desc_tag["content"].strip() if desc_tag and desc_tag.has_attr("content") else "No description found"
        
        h1s = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]
        alts = [img.get("alt", "NO ALT") for img in soup.find_all("img", src=True)]
        
        print(f"\n{Fore.YELLOW}╭─ SEO Info ──────────────────────────────────────╮{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.GREEN}Title:{Style.RESET_ALL} {title}")
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.GREEN}Desc:{Style.RESET_ALL}  {desc}")
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.GREEN}H1s:{Style.RESET_ALL}   {h1s if h1s else 'None'}")
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.GREEN}Imgs:{Style.RESET_ALL}  {len(alts)} total. Missing alt: {alts.count('NO ALT')}")
        print(f"{Fore.YELLOW}╰────────────────────────────────────────────────╯{Style.RESET_ALL}\n")

def ssl_info(url: str):
    info(f"Checking SSL certificate for {url}...")
    parsed = urlparse(url)
    hostname = parsed.netloc
    if not hostname:
        err("Invalid URL for SSL check.")
        return

    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
        issuer = dict(x[0] for x in cert['issuer'])
        subject = dict(x[0] for x in cert['subject'])
        expiry_date = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
        days_left = (expiry_date - datetime.datetime.utcnow()).days
        
        print(f"\n{Fore.YELLOW}╭─ SSL Certificate ──────────────────────────────╮{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.GREEN}Subject:{Style.RESET_ALL} {subject.get('commonName', 'N/A')}")
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.GREEN}Issuer:{Style.RESET_ALL}  {issuer.get('organizationName', 'N/A')}")
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.GREEN}Expires:{Style.RESET_ALL} {expiry_date.strftime('%Y-%m-%d')} ({days_left} days left)")
        print(f"{Fore.YELLOW}╰────────────────────────────────────────────────╯{Style.RESET_ALL}\n")
    except Exception as e:
        err(f"Failed to retrieve SSL info: {e}")

def fetch_robots(url: str):
    info(f"Fetching robots.txt for {url}...")
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    res = _fetch(robots_url)
    if res:
        print(f"\n{Fore.YELLOW}╭─ robots.txt ───────────────────────────────────╮{Style.RESET_ALL}")
        for line in res.text.splitlines():
            print(f"{Fore.YELLOW}│{Style.RESET_ALL} {line}")
        print(f"{Fore.YELLOW}╰────────────────────────────────────────────────╯{Style.RESET_ALL}\n")

def fetch_sitemap(url: str):
    info(f"Fetching sitemap.xml for {url}...")
    parsed = urlparse(url)
    sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
    res = _fetch(sitemap_url)
    if res:
        soup = BeautifulSoup(res.text, "xml")
        urls = [loc.text for loc in soup.find_all("loc")]
        
        print(f"\n{Fore.YELLOW}╭─ sitemap.xml ({len(urls)} URLs) ─────────────────╮{Style.RESET_ALL}")
        for i, u in enumerate(urls[:20], 1): # Limit to first 20 for brevity
            print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.CYAN}{i}.{Style.RESET_ALL} {u}")
        if len(urls) > 20:
            print(f"{Fore.YELLOW}│{Style.RESET_ALL} ... and {len(urls)-20} more.")
        print(f"{Fore.YELLOW}╰────────────────────────────────────────────────╯{Style.RESET_ALL}\n")