from typing import Optional

class ToolError(Exception):
    """
    MCP 도구(Skill) 실행 중 발생하는 비즈니스 논리 예외.
    이 예외는 오케스트레이터가 인지하고 에러 응답으로 변환할 수 있습니다.
    """
    def __init__(self, message: str, tool_name: Optional[str] = None):
        self.message = message
        self.tool_name = tool_name
        super().__init__(self.message)

class ToolTimeoutError(ToolError):
    """도구 실행 시간 초과"""
    pass

class ToolInvalidInputError(ToolError):
    """도구 입력 인자 부적합"""
    pass
