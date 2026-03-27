from ...infrastructure import llm, get_logger
from .prompts import EXECUTION_PROMPT

logger = get_logger(__name__)

async def execution_node(state: dict) -> dict:
    """맞춤형 복지 정책 답변 초안을 작성하는 LangGraph 노드."""
    logger.info("[Execution Agent] ✍️ 답변 초안 작성 중...")

    user_message = state.get("user_message", "")
    user_profile = state.get("user_profile", {})
    plan = state.get("plan", "")
    research_results = state.get("research_results", [])
    review_feedback = state.get("review_feedback", "")
    revision_count = state.get("revision_count", 0)

    # 병렬로 수집된 리서치 결과들을 하나로 합침
    combined_research = "\n---\n".join(research_results)

    context = f"""사용자 요청: {user_message}
사용자 프로필: {user_profile}
검색 전략: {plan}
검색된 정책 데이터 (RAG + 웹 통합):
{combined_research}"""

    if review_feedback:
        context += f"\n\n[이전 검토 피드백 - 반드시 반영할 것]\n{review_feedback}"

    draft = await llm.get_text_output(
        system_prompt=EXECUTION_PROMPT,
        user_message=context
    )

    logger.info(f"[Execution Agent] ✍️ 초안 작성 완료 (revision #{revision_count})")
    return {
        "draft_response": draft,
        "revision_count": revision_count + 1
    }
