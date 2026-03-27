import logging
import sys
import os
from contextvars import ContextVar
from typing import Optional

# 전역적으로 유지될 요청 추적 ID 컨텍스트
trace_id_var: ContextVar[Optional[str]] = ContextVar("trace_id", default=None)

class TraceIdFormatter(logging.Formatter):
    """로그 출력 시 trace_id를 자동으로 삽입하는 포맷터"""
    def format(self, record):
        trace_id = trace_id_var.get()
        # [TRACE-ID] 형태가 로그 메시지 앞에 붙도록 설정
        record.trace_id = f"[{trace_id}] " if trace_id else ""
        return super().format(record)

def setup_logger(name: str):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(log_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # %(trace_id)s 가 포맷터에서 삽입됨
    formatter = TraceIdFormatter(
        '%(asctime)s [%(levelname)s] %(trace_id)s[%(name)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False
    
    return logger

def get_logger(name: str):
    return setup_logger(name)

logger = get_logger("shared-utility")
