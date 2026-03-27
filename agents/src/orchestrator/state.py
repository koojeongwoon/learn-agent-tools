"""
[state.py]
LangGraph의 핵심: 그래프 노드 간에 공유되는 상태(State) 정의.
각 노드는 이 TypedDict의 일부 필드를 읽고, 업데이트할 필드만 딕셔너리로 반환합니다.

research_results는 Annotated[list, operator.add]를 사용하여
병렬로 실행되는 여러 리서치 노드(RAG, Web)의 결과를 자동으로 합칩니다.
"""

import operator
from typing import Annotated, TypedDict

class AgentState(TypedDict):
    # ── 입력 가드레일 ──
    is_blocked: bool        # 가드레일에 의해 차단 여부
    block_reason: str       # 차단 사유 (로깅/응답용)

    # ── 입력 ──
    user_message: str       # 사용자의 원본 메시지
    user_profile: dict      # 사용자 컨텍스트 (지역, 생애주기, 관심사 등)

    # ── 의도 파악 ──
    intent: str             # 파악된 의도 (welfare_recommendation, document, direct_chat 등)

    # ── 정보 수집 (Clarification) ──
    needs_clarification: bool   # 추가 정보가 필요한지 여부
    clarification_question: str # 사용자에게 되물을 질문

    # ── 계획 ──
    plan: str               # 검색/답변 전략 계획

    # ── 조사 (병렬 Fan-out) ──
    # 여러 리서치 노드(RAG, Web 등)가 동시에 실행되어 결과를 이 리스트에 합침
    research_results: Annotated[list[str], operator.add]

    # ── 실행 ──
    draft_response: str     # 실행 에이전트가 작성한 답변 초안

    # ── 검토 ──
    review_passed: bool     # 검토 통과 여부
    review_feedback: str    # 검토 에이전트의 피드백
    review_scores: dict     # 항목별 점수 (예: {"relevance": 4, "faithfulness": 5, ...})

    # ── 최종 출력 ──
    final_response: str     # 최종 확정 답변

    # ── 제어 ──
    revision_count: int     # 무한 루프 방지 (최대 재시도 횟수)
