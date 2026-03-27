import time
import uuid
from fastapi import Request
from common_util.logger import trace_id_var

async def trace_id_middleware(request: Request, call_next):
    """
    모든 API 요청에 대해 trace_id를 생성하거나 추출합니다.
    """
    # 1. 헤더에서 찾거나 없으면 새로 생성 (API 서버는 Originator이므로)
    trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())
    
    token = trace_id_var.set(trace_id)
    try:
        start_time = time.time()
        response = await call_next(request)
        
        # 응답 헤더에도 trace_id를 실어서 보냄
        response.headers["X-Trace-ID"] = trace_id
        return response
    finally:
        trace_id_var.reset(token)
