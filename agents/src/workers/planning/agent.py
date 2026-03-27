from ...infrastructure import llm, get_logger
from .prompts import PLANNING_PROMPT

logger = get_logger(__name__)

async def planning_node(state: dict) -> dict:
    """검색 및 답변 전략을 수립하는 LangGraph 노드."""
    logger.info("[Planning Agent] 📋 검색 전략 수립 중...")

    user_message = state.get("user_message", "")
    user_profile = state.get("user_profile", {})

    context = f"사용자 요청: {user_message}\n사용자 프로필: {user_profile}"

    plan = await llm.get_text_output(
        system_prompt=PLANNING_PROMPT,
        user_message=context
    )

    logger.info("[Planning Agent] 📋 계획 수립 완료")
    return {"plan": plan}
