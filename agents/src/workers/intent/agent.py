import os
from ...infrastructure import llm, get_logger
from .models import RouteDecision
from .prompts import ROUTING_PROMPT, AGENT_DESCRIPTIONS

logger = get_logger(__name__)

async def intent_node(state: dict) -> dict:
    """사용자 메시지를 분석하여 의도를 State에 기록하는 LangGraph 노드."""
    logger.info("[Intent Agent] 🧠 사용자 의도 분석 시작...")

    user_message = state.get("user_message", "")

    if not os.environ.get("OPENAI_API_KEY"):
        logger.warning("[Intent Agent] ⚠️ OPENAI_API_KEY가 설정되지 않아 임시 패턴 매칭(Fallback)을 수행합니다.")
        if "문서" in user_message or "합쳐" in user_message:
            return {"intent": "document_agent", "final_response": ""}
        return {"intent": "welfare_recommendation", "final_response": ""}

    system_content = ROUTING_PROMPT.format(agent_descriptions=AGENT_DESCRIPTIONS)
    
    parsed = await llm.get_structured_output(
        system_prompt=system_content,
        user_message=user_message,
        response_model=RouteDecision
    )

    logger.info(f"[Intent Agent] 🎯 의도 판별 완료: [{parsed.agent_name}]")

    # direct_chat인 경우 바로 최종 응답 세팅
    if parsed.agent_name == "direct_chat":
        return {
            "intent": "direct_chat",
            "final_response": parsed.direct_message
        }

    return {"intent": parsed.agent_name}
