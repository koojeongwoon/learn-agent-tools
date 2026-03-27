"""
에이전트 서버 통신 공통 클라이언트.
모든 도메인 모듈은 이 클라이언트를 통해 에이전트에 접근한다.
InternalEnvelope 파싱, 에러 핸들링, 타임아웃 처리를 여기서 끝낸다.
"""

import httpx
import uuid
from common_util import InternalEnvelope, AgentResponse
from common_util.logger import logger, trace_id_var
from .config import settings
from .exceptions import BaseAppException, CoreErrorCode, AgentException


class AgentClient:
    """에이전트 서버와의 HTTP 통신을 캡슐화하는 클라이언트."""

    def __init__(self, base_url: str = None, timeout: float = None):
        self.base_url = base_url or settings.AGENTS_URL
        self.timeout = timeout or settings.AGENT_TIMEOUT

    async def send(self, message: str, user_profile: dict = None) -> AgentResponse:
        """
        에이전트에 메시지를 보내고, InternalEnvelope을 파싱하여
        AgentResponse를 반환합니다.
        """
        # 1. 기존 추적 ID가 있으면 재사용, 없으면 생성
        trace_id = trace_id_var.get() or str(uuid.uuid4())
        token = trace_id_var.set(trace_id)
        
        logger.info(f"Sending request to agent. message_len={len(message)}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # 에이전트에 trace_id 전달
                params = {
                    "user_message": message,
                    "trace_id": trace_id
                }
                response = await client.post(self.base_url, params=params)
                response.raise_for_status()
                raw = response.json()

        except httpx.TimeoutException:
            logger.error(f"Agent request timed out after {self.timeout}s")
            raise AgentException(CoreErrorCode.AGENT_TIMEOUT)
        except httpx.HTTPError as e:
            logger.error(f"Agent HTTP error occurred: {e}")
            raise AgentException(CoreErrorCode.AGENT_ERROR, message_override=str(e))
        finally:
            # 컨텍스트 복구
            trace_id_var.reset(token)

        # InternalEnvelope 파싱
        try:
            envelope = InternalEnvelope(**raw)
        except Exception as e:
            logger.error(f"Failed to parse InternalEnvelope: {e}")
            raise AgentException(CoreErrorCode.AGENT_ERROR, message_override=f"Invalid envelope: {e}")

        # 에러 envelope 처리
        if envelope.status == "error":
            logger.error(f"Agent returned error envelope: {envelope.error_detail}")
            raise AgentException(CoreErrorCode.AGENT_ERROR, message_override=f"Agent error: {envelope.error_detail}")

        if envelope.payload is None:
            raise AgentException(CoreErrorCode.AGENT_ERROR, message_override="Agent returned empty payload")

        return envelope.payload
