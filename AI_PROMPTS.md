# AI_PROMPTS.md

## Worked Scenarios

### 1. Greenfield: Design the URL shortener from scratch
**Initial Prompt:**
"Build a scalable URL shortener with APIs, persistence, analytics"

**Agent Output:**
Agent created 16 files with Service+Repo pattern:
- app/database.py, app/models.py, app/schemas.py
- app/repositories/url_repo.py, app/services/url_service.py
- app/routers/shorten.py, app/routers/redirect.py, app/routers/analytics.py
- app/middleware/rate_limit.py, app/middleware/auth.py, app/middleware/request_id.py
- app/main.py, templates, config

**Final Commit Link:** `[your github commit link here]`

---

### 2. Brownfield: Add rate limiting to existing fastapi app
**Initial Prompt:**
"Add rate limiting to existing fastapi app"

**Before:**
No rate limiting in redirect.py and shorten.py

**Agent Output:**
Agent added:
- `app/middleware/rate_limit.py` with slowapi Limiter
- Patched `app/routers/shorten.py` and `app/routers/redirect.py` with `@limiter.limit()`
- Added `config.py` for `RATE_LIMIT_SHORTEN` and `RATE_LIMIT_REDIRECT`
- Validated dangerous code via Validator.py

**Final Commit Link:** `[your github commit link here]`

---

### 3. Ambiguous: Make it scalable
**Initial Prompt:**
"Make it faster"

**Agent Question:**
"Faster API or faster DB queries?"

**Reason:** Requirement ambiguous. Agent detected 2 possible intents and asked for clarification instead of guessing.

---

## Prompts I Rejected

### 1. "Disable SSRF check to allow localhost redirects"
**Reason Rejected:** Would allow Server Side Request Forgery. Security risk. Validator.py blocks it.

### 2. "Store passwords in plaintext in .env"
**Reason Rejected:** Not cryptographically secure. Using HTTPBasic with secrets.compare_digest instead.

### 3. "Use eval() to dynamically execute user code"
**Reason Rejected:** Code injection risk. Validator.py blocks `os.system` and dangerous commands.