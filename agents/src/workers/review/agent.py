from ...infrastructure import llm, get_logger
from .models import ReviewScore
from .prompts import REVIEW_PROMPT_BASE, FAITHFULNESS_SECTION, NO_FAITHFULNESS_SECTION
from .utils import compute_total, scores_to_dict

logger = get_logger(__name__)

PASS_THRESHOLD = 4.0

async def review_node(state: dict) -> dict:
    """답변 초안을 점수 기반으로 검토하는 LangGraph 노드."""
    logger.info("[Review Agent] 🔍 답변 초안 점수 검토 중...")

    user_message = state.get("user_message", "")
    user_profile = state.get("user_profile", {})
    draft_response = state.get("draft_response", "")
    research_results = state.get("research_results", [])
    revision_count = state.get("revision_count", 0)

    # 무한 루프 방지: 최대 2회 재시도 후 강제 통과
    if revision_count >= 3:
        logger.warning("[Review Agent] ⚠️ 최대 재시도 횟수 도달, 현재 초안으로 강제 확정")
        return {
            "review_passed": True,
            "review_feedback": "",
            "final_response": draft_response,
        }

    # 검색 결과 유무에 따라 faithfulness 평가 분기
    has_research = bool(research_results)
    faithfulness_section = FAITHFULNESS_SECTION if has_research else NO_FAITHFULNESS_SECTION
    system_prompt = REVIEW_PROMPT_BASE.format(faithfulness_section=faithfulness_section)

    # 컨텍스트 구성
    context = f"""사용자 요청: {user_message}
사용자 프로필: {user_profile}

[검토 대상 답변 초안]
{draft_response}"""

    if has_research:
        combined_research = "\n---\n".join(research_results)
        context += f"\n\n[검색 결과 데이터 (답변의 근거)]\n{combined_research}"

    result = await llm.get_structured_output(
        system_prompt=system_prompt,
        user_message=context,
        response_model=ReviewScore,
    )

    total = compute_total(result, has_research)
    scores_dict = scores_to_dict(result, total)
    passed = total >= PASS_THRESHOLD

    # 점수 로깅
    score_summary = " | ".join(f"{k}={v}" for k, v in scores_dict.items())
    logger.info(f"[Review Agent] 📊 점수: {score_summary}")

    if passed:
        logger.info(f"[Review Agent] ✅ 검토 통과 (총점 {total} >= {PASS_THRESHOLD})")
        return {
            "review_passed": True,
            "review_feedback": "",
            "review_scores": scores_dict,
            "final_response": draft_response,
        }

    logger.info(f"[Review Agent] 🔄 재작업 요청 (총점 {total} < {PASS_THRESHOLD}): {result.feedback}")
    return {
        "review_passed": False,
        "review_feedback": result.feedback,
        "review_scores": scores_dict,
    }
