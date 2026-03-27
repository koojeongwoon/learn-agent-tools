from enum import Enum
from typing import Optional, Any

class CoreErrorCode(Enum):
    """Core/Infrastructure 수준의 고유 에러 코드"""
    AGENT_ERROR = ("CORE-001", "Agent server error", 502)
    AGENT_TIMEOUT = ("CORE-002", "Agent server timeout", 504)

    def __init__(self, code: str, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code

class BaseAppException(Exception):
    """모든 도메인 예외의 조상. Enum 또는 직접 값을 입력받아 표준화된 에러 정보를 구성함."""
    def __init__(self, error_code: Any, message_override: Optional[str] = None, data: Optional[Any] = None):
        self.error_code = error_code.code
        self.message = message_override or error_code.message
        self.status_code = error_code.status_code
        self.data = data
        super().__init__(self.message)

class AgentException(BaseAppException):
    """에이전트 통신 관련 통합 예외 클래스. CoreErrorCode를 인자로 받습니다."""
    pass
