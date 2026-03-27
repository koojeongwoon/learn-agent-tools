from ...infrastructure.mcp import mcp_manager, extract_tools
from ...infrastructure import get_logger

logger = get_logger(__name__)

async def document_worker(task_description: str) -> str:
    logger.info("[Document Agent] 📄 문서 작업 임무 시작...")
    
    # 이 에이전트는 무기 창고 중에 'tools_mcp'에 있는 무기만 가져옵니다!
    client = await mcp_manager.get_client("tools_mcp")
    tools = await extract_tools(client)
    
    logger.info(f"[Document Agent] 사용할 수 있는 도구 목록: {tools}")
    
    # TODO: 여기서 LangChain / LlamaIndex 등의 AgentExecutor를 사용하여
    # LLM이 직접 tools 목록을 보고 판단해 `merge_pdfs` 등을 호출하도록 구현합니다.
    
    # 가상의 응답 반환
    return "문서 병합과 워드 생성을 완료했습니다! (더미 응답)"
