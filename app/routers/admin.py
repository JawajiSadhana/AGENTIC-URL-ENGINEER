from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import analytics_service

router = APIRouter()

@router.get("/admin")
def admin_dashboard(db: Session = Depends(get_db)):
    data = analytics_service.get_analytics(db)

    rows = "".join([
        f"<tr><td>{i.short_code}</td><td>{i.original_url[:80]}</td><td>{i.clicks}</td></tr>" 
        for i in data["recent_links"]
    ])

    html = f"""
    <h1>Admin Dashboard</h1>
    <p><b>Total URLs:</b> {data['total_urls']}</p>
    <p><b>Total Clicks:</b> {data['total_clicks']}</p>
    <h3>Recent Links</h3>
    <table border=1 cellpadding=5>
        <tr><th>Short Code</th><th>Original URL</th><th>Clicks</th></tr>
        {rows}
    </table>
    """
    return HTMLResponse(html)