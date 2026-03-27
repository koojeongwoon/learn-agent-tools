def build_search_query(state: dict) -> str:
    """사용자 메시지, 프로필, 계획을 종합하여 검색 쿼리를 구성합니다."""
    user_message = state.get("user_message", "")
    user_profile = state.get("user_profile", {})
    plan = state.get("plan", "")

    # 지역 정보가 있으면 쿼리에 포함
    region = user_profile.get("region", "")
    life_cycle = user_profile.get("life_cycle", "")

    query_parts = [user_message]
    if region:
        query_parts.append(region)
    if life_cycle:
        query_parts.append(life_cycle)

    # planning 에이전트가 키워드를 줬으면 보강
    if plan:
        query_parts.append("복지 정책 지원")

    return " ".join(query_parts)


def format_results(results: list[dict]) -> str:
    """Tavily 검색 결과를 읽기 쉬운 텍스트로 포맷합니다."""
    if not results:
        return "[웹 검색 결과 없음]"

    formatted = ["[웹 검색 결과]"]
    for i, result in enumerate(results, 1):
        title = result.get("title", "제목 없음")
        url = result.get("url", "")
        content = result.get("content", "내용 없음")
        # 내용이 너무 길면 잘라냄
        if len(content) > 300:
            content = content[:300] + "..."
        formatted.append(f"\n{i}. [{title}]")
        formatted.append(f"   - {content}")
        formatted.append(f"   - 출처: {url}")

    return "\n".join(formatted)
