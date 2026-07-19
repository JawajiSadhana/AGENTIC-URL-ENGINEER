from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from app.repositories import url_repo

def get_analytics(db: Session):
    return url_repo.get_analytics(db)

def get_analytics_by_code(db: Session, short_code: str):
    return url_repo.get_analytics_by_code(db, short_code)