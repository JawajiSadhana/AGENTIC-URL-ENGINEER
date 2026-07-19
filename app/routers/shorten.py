from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import url_service
from app.middleware.rate_limit import limiter
from config import settings

router = APIRouter()

BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AgenticURL Pro</title>
    <style>
        body {{ font-family: Arial; max-width: 700px; margin: 50px auto; padding: 20px; }}
        input {{ width: 400px; padding: 8px; }}
        button {{ padding: 8px 15px; }}
        .error {{ color: red; margin-top: 10px; }}
        .success {{ color: green; margin-top: 10px; }}
    </style>
</head>
<body>
    <h1>AgenticURL Pro - SSRF Protected</h1>
    <form action="/shorten" method="post">
        <input type="text" name="url" placeholder="Enter http:// or https:// URL" required>
        <button type="submit">Shorten</button>
    </form>
    {message}
    <br><a href="/admin">Admin Dashboard</a>
</body>
</html>
"""

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return HTMLResponse(BASE_HTML.format(message=""))

@router.post("/shorten", response_class=HTMLResponse)
@limiter.limit(settings.rate_limit_shorten)
def shorten_url(request: Request, url: str = Form(...), db: Session = Depends(get_db)):
    try:
        db_url = url_service.create_short_url(db, url)
        short_code = db_url.short_code
        full_url = f"http://localhost:8001/{short_code}"
        msg = f'<div class="success"><b>Success:</b> <a href="{full_url}">{full_url}</a></div>'
        return HTMLResponse(BASE_HTML.format(message=msg))
    except ValueError as e:
        msg = f'<div class="error"><b>Error:</b> {str(e)}</div>'
        return HTMLResponse(BASE_HTML.format(message=msg))
