Agentic-URL-Engineer

An AI-powered Agentic system that can auto-generate, test, and extend a production-grade URL Shortener using FastAPI.

Built for demonstrating: Code Generation, Brownfield Feature Addition, Testing, Security, and Observability.

## Features

### 1. Core App: URL Shortener Pro
- **URL Shortening**: Generate 6-char short codes for long URLs
- **SSRF Protection**: Blocks `ftp://`, `file://`, `localhost`, `127.0.0.1`, private IPs
- **Redirect Tracking**: Click count + IP logging for analytics
- **Rate Limiting**: `slowapi` - 10/min for shorten, 100/min for redirect
- **Request ID**: Every request gets `X-Request-ID` header
- **Admin Dashboard**: `/admin` - See total URLs, clicks, recent links
- **Analytics API**: `/api/v1/analytics/{code}` - Get clicks + unique visitors
- **Health Check**: `/health`

### 2. Agentic System
The agent in `/agent` folder can:
1.  **Greenfield**: Generate full URL Shortener from "url shortener" prompt
2.  **Brownfield**: Add features to existing app like "Add analytics to existing app"
3.  **Testing**: Auto-generate `pytest` test files
4.  **Validation**: Blocks dangerous commands like `rm -rf`, `DROP TABLE`
5.  **Tracing**: Logs every step to `logs/traces.jsonl`

### 3. Tech Stack
`FastAPI` + `SQLAlchemy` + `SQLite` + `Pydantic` + `SlowAPI` + `Pytest`

## Setup and Installation

1.  **Clone the repo**
    ```bash
    git clone https://github.com/your-username/Agentic-URL-Engineer.git
    
    cd Agentic-URL-EngineerInstall
    dependencies
    bash    pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings slowapi python-multipart pytest httpx
    Run the Appbash    uvicorn app.main:app --reload --port 8001
    Open: http://localhost:8001
    Run Tests
    bash    pytest -v
    How to Use the Agent

Go to /agent folder and run:bash
cd agent
python run.py

Example 1: Generate Full Appjavascript
Enter requirement: 
Build a url shortener with analytics
Approve this plan? [y/n]: yIt will generate all files in /app

Example 2: Add Feature to Existing App - Brownfieldjavascript
Enter requirement: Add tests to existing app
Approve this plan? [y/n]: y]
It will create tests/test_api.py and pytest.ini

Example 3: Add Analyticsjavascript
Enter requirement: Add analytics to existing app
Approve this plan? [y/n]: y
API EndpointsMethodEndpointDescription

Agentic-URL-Engineer/
├── agent/                  # The AI Agent
│   ├── planner.py
│   ├── executor.py
│   ├── orchestrator.py
│   └── run.py
├── app/                    # The Generated FastAPI App
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── routers/
│   ├── services/
│   ├── repositories/
│   └── middleware/
├── tests/                  # Pytest Tests
├── urls.db                 # SQLite DB
├── logs/traces.jsonl       # Agent Execution Logs
└── README.md

Security Features
SSRF Block: Only allows http and https public URLs
Rate Limit: Prevents abuse
Input Validation: Pydantic + Custom validators
Agent Guardrails: validator.py blocks dangerous commands
