from pydantic import BaseModel, Field
from typing import Optional, Literal

from .base import AgentResponse


class InternalEnvelope(BaseModel):
    """
    Agent ↔ API 서버 내부 통신 래퍼.
    실제 페이로드(AgentResponse)를 감싸고, 요청 추적(trace_id)과
    에러 핸들링을 위한 메타 정보를 제공한다.
    """
    trace_id: str = Field(..., description="요청 추적용 고유 ID (UUID)")
    status: Literal["ok", "error", "partial"] = Field(
        ..., description="처리 결과 상태"
    )
    payload: Optional[AgentResponse] = Field(
        None, description="에이전트 응답 본문 (에러 시 None)"
    )
    error_detail: Optional[str] = Field(
        None, description="에러 발생 시 상세 내용"
    )
    timestamp: str = Field(..., description="응답 생성 시각 (ISO 8601)")
