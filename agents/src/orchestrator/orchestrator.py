"""
[orchestrator.py]
사용자의 요청을 LangGraph 기반 에이전틱 플로우에 위임하는 진입점(Wrapper)입니다.
그래프 실행 결과(AgentState)를 AgentResponse → InternalEnvelope으로 변환하여 반환합니다.
"""

from common_util import AgentResponse, InternalEnvelope, now_kst, format_datetime
from common_util.logger import logger, trace_id_var
from .graph import welfare_graph


def _state_to_agent_response(state: dict) -> AgentResponse:
    """LangGraph 최종 상태(AgentState)를 AgentResponse로 변환합니다."""
    final = state.get("final_response", "")
    if not final:
        final = "죄송합니다. 요청을 처리하는 중 문제가 발생했습니다."

    return AgentResponse(
        success=True,
        intent=state.get("intent", "unknown"),
        content=final,
        referenced_policies=state.get("referenced_policies", []),
        search_results=state.get("search_results", []),
        review_scores=state.get("review_scores", {}),
        needs_clarification=state.get("needs_clarification", False),
        clarification_question=state.get("clarification_question"),
        node_path=state.get("node_path", []),
        meta_data=state.get("meta_data", {}),
    )


def _wrap_envelope(payload: AgentResponse, trace_id: str) -> dict:
    """AgentResponse를 InternalEnvelope로 래핑하여 dict로 반환합니다."""
    envelope = InternalEnvelope(
        trace_id=trace_id,
        status="ok",
        payload=payload,
        timestamp=format_datetime(now_kst()),
    )
    return envelope.model_dump()


async def run_orchestrator(user_message: str, user_profile: dict = None) -> dict:
    """LangGraph 에이전틱 플로우를 실행하고 InternalEnvelope을 반환합니다."""
    # 미들웨어에서 설정된 trace_id 사용
    trace_id = trace_id_var.get() or "unknown"
    logger.info(f"🤖 Orchestrator started. message_len={len(user_message)}")

    # 초기 상태 구성
    initial_state = {
        "user_message": user_message,
        "user_profile": user_profile or {},
        "intent": "",
        "needs_clarification": False,
        "clarification_question": "",
        "plan": "",
        "research_results": [],
        "draft_response": "",
        "review_passed": False,
        "review_feedback": "",
        "final_response": "",
        "revision_count": 0,
    }

    # LangGraph 그래프 실행 (예외는 main.py의 글로벌 핸들러가 처리함)
    result = await welfare_graph.ainvoke(initial_state)

    # AgentState → AgentResponse → InternalEnvelope
    agent_response = _state_to_agent_response(result)
    envelope = _wrap_envelope(agent_response, trace_id)

    logger.info(f"✅ Flow completed. intent={agent_response.intent}")
    return envelope
