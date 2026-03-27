import time
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse
from common_util import InternalEnvelope
from common_util.logger import logger, trace_id_var

async def global_exception_handler(request: Request, exc: Exception):
    """
    에이전트 내부에서 발생하는 모든 예외를 잡아서
    InternalEnvelope(status='error') 규격으로 변환합니다.
    """
    error_msg = str(exc)
    stack_trace = traceback.format_exc()
    trace_id = trace_id_var.get()
    
    logger.error(f"Unhandled exception occurred: {error_msg}\n{stack_trace}")
    
    envelope = InternalEnvelope(
        trace_id=trace_id or "unknown",
        status="error",
        payload=None,
        error_detail=error_msg,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )
    
    return JSONResponse(
        status_code=500,
        content=envelope.model_dump()
    )
