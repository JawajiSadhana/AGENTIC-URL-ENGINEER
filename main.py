from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
import sqlite3
from datetime import datetime
import hashlib

app = FastAPI()
DB = "app.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS urls (short_code TEXT PRIMARY KEY, long_url TEXT, created_at TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS clicks (id INTEGER PRIMARY KEY AUTOINCREMENT, short_code TEXT, timestamp TEXT, ip TEXT, ua TEXT)')
    conn.commit()
    conn.close()

init_db()

def make_code(url):
    return hashlib.sha256(url.encode()).hexdigest()[:6]

@app.get("/", response_class=HTMLResponse)
def home():
    return '<h1>Agentic URL Shortener</h1><form action="/shorten" method="post"><input name="url" placeholder="Paste URL" style="width:300px"><button>Shorten</button></form><br><a href="/admin">Admin Dashboard</a>'

@app.post("/shorten")
async def shorten(request: Request):
    form = await request.form()
    url = form.get("url")
    code = make_code(url)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO urls VALUES (?,?,?)", (code, url, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return JSONResponse({"short_url": f"http://localhost:8001/{code}"})

@app.get("/admin", response_class=HTMLResponse)
def admin():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Saari URLs nikalo
    c.execute("SELECT * FROM urls")
    urls = c.fetchall()

    # Har URL ke clicks count karo
    c.execute("SELECT short_code, COUNT(*) FROM clicks GROUP BY short_code")
    click_counts = dict(c.fetchall())

    # Total clicks
    c.execute("SELECT COUNT(*) FROM clicks")
    total_clicks = c.fetchone()[0]

    conn.close()

    # Table rows banao
    rows = ""
    for u in urls:
        code = u[0]
        clicks = click_counts.get(code, 0)
        rows += f"<tr><td>{code}</td><td>{u[1]}</td><td>{clicks}</td></tr>"

    # HTML return karo
    html = f"""
    <h1>Admin Dashboard - Analytics</h1>
    <h3>Total URLs: {len(urls)} | Total Clicks: {total_clicks}</h3>
    <table border=1 cellpadding=8>
        <tr><th>Code</th><th>URL</th><th>Clicks</th></tr>
        {rows}
    </table>
    <br><a href="/">Back to Home</a>
    """
    return HTMLResponse(html)

@app.get("/{code}")
def redirect(code: str, request: Request):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT long_url FROM urls WHERE short_code=?", (code,))
    row = c.fetchone()
    if not row:
        raise HTTPException(404)
    c.execute("INSERT INTO clicks VALUES (NULL,?,?,?,?)", (code, datetime.now().isoformat(), request.client.host, request.headers.get("user-agent")))
    conn.commit()
    conn.close()
    return RedirectResponse(row[0])