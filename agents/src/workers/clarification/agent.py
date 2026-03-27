from ...infrastructure import llm, get_logger
from .models import ClarificationDecision
from .prompts import CLARIFICATION_PROMPT

logger = get_logger(__name__)

async def clarification_node(state: dict) -> dict:
    """사용자에게 추가 정보가 필요한지 판단하는 LangGraph 노드."""
    logger.info("[Clarification Agent] 🔎 추가 정보 필요 여부 판단 중...")

    user_message = state.get("user_message", "")
    user_profile = state.get("user_profile", {})

    context = f"사용자 메시지: {user_message}\n현재 프로필 정보: {user_profile}"
    
    decision = await llm.get_structured_output(
        system_prompt=CLARIFICATION_PROMPT,
        user_message=context,
        response_model=ClarificationDecision
    )

    if decision.needs_clarification:
        logger.info(f"[Clarification Agent] ❓ 추가 정보 요청: {decision.question}")
    else:
        logger.info("[Clarification Agent] ✅ 충분한 정보 확보, 계획 단계로 진행")

    return {
        "needs_clarification": decision.needs_clarification,
        "clarification_question": decision.question if decision.needs_clarification else ""
    }
