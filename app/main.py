from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.database import engine, Base
from app.middleware.rate_limit import limiter
from app.middleware.request_id import RequestIDMiddleware
from app.routers import shorten, redirect, admin, health, analytics
from app.models import URL  # duplicate engine,Base hata diya


Base.metadata.create_all(bind=engine)

app = FastAPI(title="AgenticURL Pro")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(RequestIDMiddleware)

app.include_router(health.router)
app.include_router(shorten.router)
app.include_router(admin.router)  # <-- admin pehle
app.include_router(analytics.router) # NAYA
app.include_router(redirect.router) # last me hi rahe