from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class UserProfile(BaseModel):
    """사용자의 기본 인적 사항 및 거주 정보를 공통으로 관리하는 모델"""
    user_id: Optional[str] = Field(None, description="사용자 고유 ID")
    region: str = Field(..., description="거주 지역 (예: 서울특별시, 경기도 등)")
    district: Optional[str] = Field(None, description="상세 지역 (예: 강남구, 수원시 등)")
    life_cycle: str = Field(..., description="생애주기 (예: 청년, 중장년, 노년 등)")
    income_level: Optional[str] = Field(None, description="소득 수준 (예: 기초생활수급자, 차상위계층 등)")
    interests: List[str] = Field(default_factory=list, description="관심 분야 (예: 주거, 금융, 고용)")


class AgentResponse(BaseModel):
    """
    에이전트 → API 서버 내부 통신 규격.
    에이전트가 생산하는 '모든' 산출물을 담는 Full Payload.
    API 서버는 이 중 필요한 필드만 골라서 외부에 전달한다.
    """
    success: bool = True
    intent: str = Field(..., description="분류된 의도 (welfare_recommendation, document, direct_chat 등)")
    content: str = Field(..., description="최종 답변 본문")

    # ── 근거 데이터 ──
    referenced_policies: List[str] = Field(
        default_factory=list, description="답변에 인용된 정책 ID 목록"
    )
    search_results: List[Dict[str, Any]] = Field(
        default_factory=list, description="RAG/Web 검색 원본 결과"
    )

    # ── 품질 메트릭 ──
    review_scores: Dict[str, Any] = Field(
        default_factory=dict, description="검토 에이전트의 항목별 점수"
    )
    confidence_score: Optional[float] = Field(
        None, description="답변 신뢰도 (0.0~1.0)"
    )

    # ── 대화 흐름 제어 ──
    needs_clarification: bool = Field(
        False, description="사용자에게 추가 질문이 필요한지 여부"
    )
    clarification_question: Optional[str] = Field(
        None, description="사용자에게 되물을 질문"
    )

    # ── 디버깅 / 모니터링 ──
    node_path: List[str] = Field(
        default_factory=list, description="LangGraph 노드 실행 경로"
    )
    execution_time_ms: Optional[int] = Field(
        None, description="전체 처리 소요 시간 (ms)"
    )

    # ── 기타 ──
    meta_data: Dict[str, Any] = Field(
        default_factory=dict, description="확장용 부가 정보"
    )
