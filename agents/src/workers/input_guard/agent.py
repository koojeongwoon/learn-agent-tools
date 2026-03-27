import os
from ...infrastructure import llm, get_logger
from .models import GuardDecision
from .prompts import GUARD_PROMPT

logger = get_logger(__name__)

async def input_guard_node(state: dict) -> dict:
    """사용자 입력의 안전성을 검사하는 LangGraph 노드."""
    logger.info("[Input Guard] 🛡️ 입력 안전성 검사 시작...")

    user_message = state.get("user_message", "")

    # API 키 없으면 개발 편의를 위해 통과
    if not os.environ.get("OPENAI_API_KEY"):
        logger.warning("[Input Guard] ⚠️ OPENAI_API_KEY 미설정 — 가드레일 건너뜀")
        return {"is_blocked": False, "block_reason": ""}

    try:
        decision = await llm.get_structured_output(
            system_prompt=GUARD_PROMPT,
            user_message=user_message,
            response_model=GuardDecision,
        )

        if decision.is_safe:
            logger.info(f"[Input Guard] ✅ 안전 판정: {decision.reason}")
            return {"is_blocked": False, "block_reason": ""}
        else:
            logger.warning(f"[Input Guard] 🚫 차단: {decision.reason}")
            return {
                "is_blocked": True,
                "block_reason": decision.reason,
                "final_response": "죄송합니다. 해당 요청은 서비스 정책에 의해 처리할 수 없습니다.",
            }

    except Exception as e:
        # 가드레일 실패 시에도 서비스는 계속 동작 (fail-open)
        logger.error(f"[Input Guard] ❌ 검사 실패, 통과 처리: {e}")
        return {"is_blocked": False, "block_reason": ""}
