import os
from tavily import AsyncTavilyClient

from ...infrastructure import get_logger
from .utils import build_search_query, format_results

logger = get_logger(__name__)

async def web_search_node(state: dict) -> dict:
    """웹 검색을 통해 복지 정책 정보를 수집하는 LangGraph 노드."""
    logger.info("[Web Search Agent] 🌐 웹 검색 시작...")

    # API 키 확인
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        logger.warning("[Web Search Agent] ⚠️ TAVILY_API_KEY가 설정되지 않았습니다. 웹 검색을 건너뜁니다.")
        return {"research_results": ["[웹 검색 건너뜀: API 키 미설정]"]}

    query = build_search_query(state)
    logger.info(f"[Web Search Agent] 🔎 검색 쿼리: {query}")

    try:
        client = AsyncTavilyClient(api_key=api_key)
        response = await client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=False,
        )

        results = response.get("results", [])
        formatted = format_results(results)

        logger.info(f"[Web Search Agent] 🌐 웹 검색 완료 — {len(results)}건 수집")
        return {"research_results": [formatted]}

    except Exception as e:
        logger.error(f"[Web Search Agent] ❌ 웹 검색 실패: {e}")
        return {"research_results": [f"[웹 검색 실패: {e}]"]}
