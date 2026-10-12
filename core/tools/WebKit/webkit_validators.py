"""
webkit_validators.py - Validation utilities for WebKit.
"""
from urllib.parse import urlparse
import re

def validate_url(url: str) -> tuple[bool, str]:
    if not url or not url.strip():
        return False, "URL is empty."
    url = url.strip()
    if not re.match(r'^https?://', url):
        url = "https://" + url
        
    parsed = urlparse(url)
    if not parsed.netloc or not parsed.scheme:
        return False, f"Invalid URL format: {url}"
    return True, url