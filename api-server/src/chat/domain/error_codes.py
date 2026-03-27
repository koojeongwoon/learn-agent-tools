from enum import Enum

class ChatErrorCode(Enum):
    """채팅 도메인 고유 에러 코드 (Java Enum 스타일)"""
    AGENT_CONNECTION_ERROR = ("CHAT-001", "Failed to communicate with agent", 502)
    AGENT_RESPONSE_TIMEOUT = ("CHAT-002", "Agent responded too slowly", 504)

    def __init__(self, code: str, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code
