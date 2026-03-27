from fastapi import FastAPI

from .core.config import settings
from .core.exceptions import BaseAppException
from .core.error_handlers import domain_exception_handler
from .core.middleware import trace_id_middleware

from .chat import router as chat_router
from .auth import router as auth_router

app = FastAPI(title=settings.APP_TITLE)

# ── Middleware Registration ──
app.middleware("http")(trace_id_middleware)

# ── Global Exception Handler Registration ──
app.add_exception_handler(BaseAppException, domain_exception_handler)

# ── Module Router Registration ──
app.include_router(chat_router)
app.include_router(auth_router)

@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트."""
    return {"status": "ok"}
