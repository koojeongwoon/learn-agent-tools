import time
from fastapi import Request
from common_util.logger import logger, trace_id_var

async def trace_id_middleware(request: Request, call_next):
    """
    요청으로부터 trace_id를 추출하여 로거 컨텍스트에 심습니다.
    에이전트는 주로 호출받는 입장이므로 쿼리나 헤더에서 추출을 우선합니다.
    """
    trace_id = request.headers.get("X-Trace-ID") or request.query_params.get("trace_id")
    
    token = trace_id_var.set(trace_id)
    try:
        start_time = time.time()
        logger.info(f"Incoming request: {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        logger.info(f"Request completed: {response.status_code} (took {duration:.3f}s)")
        return response
    finally:
        trace_id_var.reset(token)
