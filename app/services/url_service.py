import ipaddress
from urllib.parse import urlparse
from sqlalchemy.orm import Session
from fastapi import Request
from app.repositories import url_repo
from app.models import URL

BLOCKED_SCHEMES = {"ftp", "file", "gopher", "ldap", "dict"}

def is_private_or_loopback(hostname: str) -> bool:
    try:
        ip = ipaddress.ip_address(hostname)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        return False

def create_short_url(db: Session, original_url: str) -> URL:
    parsed = urlparse(original_url)
    if parsed.scheme not in ["http", "https"]:
        raise ValueError("SSRF Blocked: Only http/https public URLs allowed")
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Invalid URL")
    if is_private_or_loopback(hostname):
        raise ValueError("SSRF Blocked: Private/Localhost IPs not allowed")
    return url_repo.create_url(db, original_url)

def get_original_url(db: Session, short_code: str, request: Request) -> URL | None:
    url = url_repo.get_url_by_code(db, short_code)
    if url:
        url_repo.log_click(db, url, request)
    return url

# YE 2 HATA DE
# def get_analytics(db: Session):
#     return url_repo.get_analytics(db)

# def get_analytics_by_code(db: Session, short_code: str):
#     return url_repo.get_analytics_by_code(db, short_code)