from pydantic import BaseModel, Field
from typing import Optional, List


class ChatRequest(BaseModel):
    """프론트엔드 → API 서버: 채팅 요청"""
    message: str = Field(..., description="사용자 메시지")


class PolicySummary(BaseModel):
    """프론트엔드 카드 UI에 렌더링될 정책 요약"""
    policy_id: str = Field(..., description="정책 고유 ID")
    title: str = Field(..., description="정책 제목")
    summary: Optional[str] = Field(None, description="정책 요약 설명")


class ApiResponse(BaseModel):
    """
    API 서버 → 프론트엔드: 사용자에게 보여줄 응답.
    AgentResponse의 Full Payload에서 필요한 필드만 투영.
    """
    status: str = Field("success", description="응답 상태 (success | error)")
    message: str = Field(..., description="사용자에게 보여줄 답변")
    policies: List[PolicySummary] = Field(
        default_factory=list, description="추천된 정책 카드 목록"
    )
    needs_input: bool = Field(
        False, description="사용자 추가 입력 필요 여부"
    )
    input_prompt: Optional[str] = Field(
        None, description="추가 입력 요청 프롬프트"
    )
    suggestions: List[str] = Field(
        default_factory=list, description="후속 질문 추천 목록"
    )
