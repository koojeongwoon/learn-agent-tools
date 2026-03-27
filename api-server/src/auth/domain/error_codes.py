from enum import Enum

class AuthErrorCode(Enum):
    """인증 도메인 고유 에러 코드 (Java Enum 스타일)"""
    # (에러코드, 메시지, HTTP 상태코드)
    INVALID_CREDENTIALS = ("AUTH-001", "Incorrect username or password", 401)
    TOKEN_EXPIRED = ("AUTH-002", "Token has expired", 401)
    TOKEN_REUSED = ("AUTH-003", "Refresh token reuse detected", 401)
    USER_NOT_FOUND = ("AUTH-004", "User not found", 401)

    def __init__(self, code: str, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code
