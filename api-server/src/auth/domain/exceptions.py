from ...core.exceptions import BaseAppException

class AuthError(BaseAppException):
    """인증 도메인의 통합 예외 클래스. AuthErrorCode를 인자로 받습니다."""
    pass
