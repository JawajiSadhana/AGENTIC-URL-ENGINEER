def create_plan(req: str):
    req = req.lower()
    tasks = []
    risks = []
    is_ambiguous = False
    questions = []

    # 1. BROWNFIELD: Existing code me feature add
def create_plan(req: str):
    req = req.lower()
    tasks = []
    risks = []
    is_ambiguous = False
    questions = []

    # 1. BROWNFIELD: Existing code me feature add
    if "add" in req and "to" in req and "existing" in req:
        print("Detected: Brownfield Feature Add")
        from codebase_reader import read_existing_codebase
        codebase = read_existing_codebase()

        # YE NAYA BLOCK ADD KAR
        if "test" in req or "pytest" in req:
            tasks = [
                "file_write: tests/test_api.py",
                "file_write: pytest.ini"
            ]
            risks = ["Need to install pytest and httpx"]

        elif "expiry" in req and "app/models.py" in codebase["files"]:
            tasks = [
                "file_patch: app/models.py -> add expires_at column to URL",
                "file_patch: app/services/url_service.py -> check expiry in get_original_url",
                "file_write: app/tasks/cleanup.py"
            ]
            risks = ["Will require DB migration", "Existing URLs will have no expiry"]

        elif "click" in req or "analytics" in req and "app/models.py" in codebase["files"]:
            tasks = [
                "file_patch: app/models.py -> add Click table with FK to URL",
                "file_patch: app/repositories/url_repo.py -> add log_click and get_analytics_by_code",
                "file_patch: app/services/url_service.py -> add get_analytics_by_code wrapper",
                "file_patch: app/routers/redirect.py -> pass request to get_original_url",
                "file_write: app/routers/analytics.py"
            ]
            risks = ["DB migration required, delete urls.db"]

        else:
            tasks = ["file_write: app/README_BROWNFIELD.md"]
            risks = ["Could not detect where to add feature"]
        is_ambiguous = False

    # 2. GREENFIELD: URL Shortener
    elif "url" in req or "shorten" in req:
        print("Detected: URL Shortener")
        tasks = [
            "file_write: app/database.py", "file_write: app/models.py", "file_write: app/schemas.py",
            "file_write: app/middleware/rate_limit.py", "file_write: app/middleware/request_id.py", "file_write: app/middleware/auth.py",
            "file_write: app/repositories/url_repo.py", "file_write: app/services/url_service.py", "file_write: app/services/analytics_service.py",
            "file_write: app/main.py", "file_write: app/routers/shorten.py", "file_write: app/routers/redirect.py",
            "file_write: app/routers/admin.py", "file_write: app/routers/health.py",
            "file_write: app/routers/analytics.py",
            "file_write: app/templates/home.html", "file_write: app/templates/admin.html",
            "file_write: tests/test_api.py", # <-- NAYA
            "file_write: pytest.ini", # <-- NAYA
        ]
        risks = ["SSRF possible in redirect"]
        is_ambiguous = False

    # 3. GREENFIELD: Todo
    elif "todo" in req or "task" in req:
        print("Detected: Todo App")
        tasks = ["file_write: app/database.py", "file_write: app/models.py", "file_write: app/routers/todo.py"]
        risks = ["No auth"]
        is_ambiguous = False

    # 4. AMBIGUOUS
    else:
        print("Ambiguous requirement")
        tasks = []
        risks = ["Could not detect app type"]
        is_ambiguous = True
        questions = ["Do you want URL Shortener, Todo App, or add feature to existing app?"]

    return {"tasks": tasks, "risks": risks, "is_ambiguous": is_ambiguous, "questions": questions}