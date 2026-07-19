from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import analytics_service 

router = APIRouter(prefix="/api/v1", tags=["analytics"])

@router.get("/analytics/{code}")
def get_analytics(code: str, db: Session = Depends(get_db)):
    data = analytics_service.get_analytics_by_code(db, code)
    if not data: return {"error": "not found"}
    return data