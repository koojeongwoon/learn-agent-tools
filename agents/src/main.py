from fastapi import FastAPI
from .infrastructure.error_handlers import global_exception_handler
from .infrastructure.middleware import trace_id_middleware
from .orchestrator import run_orchestrator

app = FastAPI(title="엔터프라이즈 AI 오케스트레이터")

# ── Middleware Registration ──
app.middleware("http")(trace_id_middleware)

# ── Global Exception Handler Registration ──
app.add_exception_handler(Exception, global_exception_handler)

@app.post("/chat")
async def chat_endpoint(user_message: str, trace_id: str = None):
    """
    API 서버로부터 요청을 받아 오케스트레이터에게 위임합니다.
    """
    envelope = await run_orchestrator(user_message)
    return envelope

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)
