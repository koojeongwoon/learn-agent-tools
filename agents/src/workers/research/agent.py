from common_util.logger import logger, trace_id_var
from ..common.exceptions import ToolError

async def research_node(_state: dict) -> dict:
    """RAG를 통해 복지 정책을 검색하는 LangGraph 노드."""
    # 현재 컨텍스트의 trace_id 가져오기
    trace_id = trace_id_var.get()
    logger.info("🔍 Researching welfare policies via RAG...")

    # TODO: 실제 MCP 도구 호출 로직
    # client = await mcp_manager.get_client("rag_mcp")
    # result = await client.call_tool("search_knowledge_base", {
    #     "query": _state["user_message"],
    #     "trace_id": trace_id # <-- 여기서 전파!
    # })
    
    success = True
    if not success:
        logger.error("Failed to connect to RAG MCP server")
        raise ToolError("RAG 검색 서버와 통신할 수 없습니다.", tool_name="rag_mcp")

    dummy_policies = """
1. [서울 청년 월세 지원] ...
2. [국민취업지원제도] ...
"""

    logger.info("🔍 Research completed successfully.")
    return {"research_results": [dummy_policies]}
