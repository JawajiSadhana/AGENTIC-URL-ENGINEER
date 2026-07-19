from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from fastapi import Request
from app import models
import secrets, string

def generate_slug(n=6):
    return ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(n))

def create_url(db: Session, original_url: str):
    short = generate_slug()
    while db.query(models.URL).filter(models.URL.short_code == short).first():
        short = generate_slug()
    db_url = models.URL(short_code=short, original_url=original_url)
    db.add(db_url); db.commit(); db.refresh(db_url)
    return db_url

def get_url_by_code(db: Session, short_code: str):
    return db.query(models.URL).filter(models.URL.short_code == short_code).first()

def log_click(db: Session, url: models.URL, request: Request):
    click = models.Click(url_id=url.id, ip_address=request.client.host)
    db.add(click)
    url.clicks += 1
    db.commit()

def get_analytics_by_code(db: Session, short_code: str):
    url = get_url_by_code(db, short_code)
    if not url: return None
    total_clicks = url.clicks
    unique_visitors = db.query(func.count(distinct(models.Click.ip_address))).filter(models.Click.url_id == url.id).scalar() or 0
    return {
        "short_code": short_code, 
        "total_clicks": total_clicks, 
        "unique_visitors": unique_visitors
    }

def get_analytics(db: Session):
    total_urls = db.query(models.URL).count()
    total_clicks = db.query(func.sum(models.URL.clicks)).scalar() or 0
    recent_links = db.query(models.URL).order_by(models.URL.id.desc()).limit(10).all()
    return {
        "total_urls": total_urls,
        "total_clicks": total_clicks,
        "recent_links": recent_links
    }