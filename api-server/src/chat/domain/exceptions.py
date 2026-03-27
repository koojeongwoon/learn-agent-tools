from ...core.exceptions import BaseAppException

class ChatError(BaseAppException):
    """채팅 도메인의 통합 예외 클래스. ChatErrorCode를 인자로 받습니다."""
    pass
