import os
from validator import validate # <-- 1. IMPORT ADD KAR

CODE_TEMPLATES = {
    "app/database.py": "from sqlalchemy import create_engine\nfrom sqlalchemy.orm import sessionmaker, declarative_base\nDATABASE_URL = 'sqlite:///./urls.db'\n\nengine = create_engine(\n DATABASE_URL,\n connect_args={'check_same_thread': False},\n pool_size=5,\n max_overflow=10,\n pool_recycle=300\n)\n\nSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)\nBase = declarative_base()\n\ndef get_db():\n db = SessionLocal()\n try: yield db\n finally: db.close()\n",

    "app/models.py": "from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey\nfrom sqlalchemy.orm import relationship\nfrom app.database import Base\nclass URL(Base):\n __tablename__ = 'urls'\n id = Column(Integer, primary_key=True, index=True)\n short_code = Column(String, unique=True, index=True, nullable=False)\n original_url = Column(String, nullable=False)\n clicks = Column(Integer, default=0)\n created_at = Column(DateTime, default=func.now())\n click_logs = relationship('Click', back_populates='url')\n\nclass Click(Base):\n __tablename__ = 'clicks'\n id = Column(Integer, primary_key=True, index=True)\n url_id = Column(Integer, ForeignKey('urls.id'))\n clicked_at = Column(DateTime, default=func.now())\n ip_address = Column(String, nullable=True)\n url = relationship('URL', back_populates='click_logs')\n",

    "app/services/analytics_service.py": "from sqlalchemy.orm import Session\nfrom app.repositories import url_repo\ndef get_analytics(db: Session):\n return url_repo.get_analytics(db)\n\ndef get_analytics_by_code(db: Session, short_code: str):\n return url_repo.get_analytics_by_code(db, short_code)\n",

    "app/routers/analytics.py": "from fastapi import APIRouter, Depends\nfrom sqlalchemy.orm import Session\nfrom app.database import get_db\nfrom app.services import analytics_service\nrouter = APIRouter(prefix='/api/v1', tags=['analytics'])\n\n@router.get('/analytics/{code}')\ndef get_analytics(code: str, db: Session = Depends(get_db)):\n data = analytics_service.get_analytics_by_code(db, code)\n if not data: return {'error': 'not found'}\n return data\n",

    "tests/test_api.py": "from fastapi.testclient import TestClient\nfrom app.main import app\nclient = TestClient(app)\n\ndef test_health():\n response = client.get('/health')\n assert response.status_code == 200\n assert response.json() == {'status': 'ok'}\n\ndef test_shorten_valid_url():\n response = client.post('/shorten', data={'url': 'https://google.com'})\n assert response.status_code == 200\n assert 'Success' in response.text\ndef test_shorten_invalid_url():\n response = client.post('/shorten', data={'url': 'ftp://hack.com'})\n assert response.status_code == 200\n assert 'SSRF Blocked' in response.text\ndef test_analytics_not_found():\n response = client.get('/api/v1/analytics/abcdef')\n assert response.json() == {'error': 'not found'}\n",

    "pytest.ini": "[pytest]\npython_files = test_*.py\ntestpaths = tests\n"
}

def execute_task(task_str: str):
    validate(task_str) # <-- 2. SABSE PEHLE VALIDATE KAR

    parts = task_str.split(": ", 1)
    action = parts[0]
    target = parts[1].split(" -> ")[0]

    # FIX: Agar folder hai tabhi banayega, warna skip
    dir_name = os.path.dirname(target)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    os.makedirs("logs", exist_ok=True)

    if action == "file_write":
        content = CODE_TEMPLATES.get(target, f"# Generated file for {target}")
        with open(target, "w", encoding="utf-8") as f: f.write(content) # encoding add kar di
        return f"Wrote {target}"

    elif action == "file_patch":
        with open(target, "a", encoding="utf-8") as f: f.write(f"\n# PATCHED BY AGENT: {parts[1]}\n")
        return f"Patched {target}"

    return "Unknown action"