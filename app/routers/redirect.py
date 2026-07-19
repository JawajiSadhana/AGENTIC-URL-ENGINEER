from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import url_service
from app.middleware.rate_limit import limiter
from config import settings

router = APIRouter()

@router.get("/{short}")
@limiter.limit(settings.rate_limit_redirect)
def redirect(request: Request, short: str, db: Session = Depends(get_db)):
    url = url_service.get_original_url(db, short, request) # request pass
    if url: return RedirectResponse(url.original_url)
    return {"error": "not found"}