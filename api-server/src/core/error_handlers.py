from fastapi import Request
from fastapi.responses import JSONResponse
from .exceptions import BaseAppException
from common_util.logger import trace_id_var

async def domain_exception_handler(request: Request, exc: BaseAppException):
    """
    도메인/비즈니스 예외를 표준화된 JSON 응답으로 변환합니다.
    Trace ID가 있는 경우 데이터에 포함시켜 프론트에서 추적 가능하게 합니다.
    """
    trace_id = trace_id_var.get()
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error_code": exc.error_code,
            "message": exc.message,
            "trace_id": trace_id,
            "data": exc.data
        }
    )
