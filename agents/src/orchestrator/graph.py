"""
[graph.py]
LangGraph StateGraph를 초기화하고 에이전트 노드를 연결하는 핵심 배선(Wiring) 모듈입니다.

플로우:
  START -> intent -> (조건부) -> clarification -> (조건부: 추가 정보 필요 시 END로 반환)
                                               -> planning -> [rag_research + web_research 병렬] -> execution -> review
                                                                                                       ↑            |
                                                                                                       └── (반려) ──┘
                                                                                                            (승인) -> END
"""

from typing import Literal
from langgraph.graph import StateGraph, START, END

from .state import AgentState
from ..workers import (
    input_guard_node,
    intent_node,
    clarification_node,
    planning_node,
    research_node,
    web_search_node,
    execution_node,
    review_node,
)
from ..infrastructure import get_logger

logger = get_logger(__name__)


# ── 조건부 라우팅 함수들 ──

def route_after_guard(state: AgentState) -> Literal["intent", "__end__"]:
    """가드레일 통과 여부에 따라 라우팅: 안전하면 intent로, 차단이면 즉시 종료."""
    if state.get("is_blocked", False):
        return END
    return "intent"


def route_after_intent(state: AgentState) -> Literal["clarification", "__end__"]:
    """의도 파악 후 라우팅: 복지 추천이면 clarification으로, 그 외(direct_chat 등)는 즉시 종료."""
    intent = state.get("intent", "")
    if intent == "welfare_recommendation":
        return "clarification"
    return END


def route_after_clarification(state: AgentState) -> Literal["planning", "__end__"]:
    """추가 정보가 필요하면 END(사용자에게 질문 반환), 충분하면 planning으로 진행."""
    if state.get("needs_clarification", False):
        return END
    return "planning"


def route_after_review(state: AgentState) -> Literal["execution", "__end__"]:
    """검토 통과 시 END, 반려 시 재작업(execution)으로 복귀."""
    if state.get("review_passed", False):
        return END
    return "execution"


# ── clarification END 전처리: 질문을 final_response로 매핑 ──

async def clarification_finalize(state: dict) -> dict:
    """clarification 결과가 END로 향할 때, 질문을 final_response로 세팅."""
    if state.get("needs_clarification", False):
        return {"final_response": state.get("clarification_question", "")}
    return {}


# ── 그래프 정의 ──

def build_welfare_graph() -> StateGraph:
    """복지 정책 추천 에이전틱 플로우 그래프를 생성하고 컴파일합니다."""
    builder = StateGraph(AgentState)

    # 1. 노드 등록
    builder.add_node("input_guard", input_guard_node)
    builder.add_node("intent", intent_node)
    builder.add_node("clarification", clarification_node)
    builder.add_node("clarification_finalize", clarification_finalize)
    builder.add_node("planning", planning_node)
    builder.add_node("rag_research", research_node)
    builder.add_node("web_research", web_search_node)
    builder.add_node("execution", execution_node)
    builder.add_node("review", review_node)

    # 2. 엣지 연결
    # START -> input_guard -> (조건부) intent 또는 END
    builder.add_edge(START, "input_guard")
    builder.add_conditional_edges("input_guard", route_after_guard, {
        "intent": "intent",
        END: END,
    })


    # intent -> (조건부) clarification 또는 END
    builder.add_conditional_edges("intent", route_after_intent, {
        "clarification": "clarification",
        END: END,
    })

    # clarification -> clarification_finalize
    builder.add_edge("clarification", "clarification_finalize")

    # clarification_finalize -> (조건부) planning 또는 END
    builder.add_conditional_edges("clarification_finalize", route_after_clarification, {
        "planning": "planning",
        END: END,
    })

    # planning -> [rag_research, web_research] 병렬 실행 (Fan-out)
    builder.add_edge("planning", "rag_research")
    builder.add_edge("planning", "web_research")

    # [rag_research, web_research] -> execution (Fan-in: research_results가 operator.add로 자동 병합)
    builder.add_edge("rag_research", "execution")
    builder.add_edge("web_research", "execution")

    # execution -> review
    builder.add_edge("execution", "review")

    # review -> (조건부) END 또는 execution(재작업)
    builder.add_conditional_edges("review", route_after_review, {
        END: END,
        "execution": "execution",
    })

    logger.info("[Graph] 🔗 복지 정책 추천 플로우 그래프 빌드 완료 (병렬 리서치 포함)")
    return builder.compile()


# 컴파일된 그래프 (싱글톤)
welfare_graph = build_welfare_graph()
