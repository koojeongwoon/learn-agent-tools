"""
[tool_aggregator.py]
특정 MCP 클라이언트에서 도구(Tool) 목록을 가져와서,
OpenAI나 Anthropic 등 LLM이 이해할 수 있는 함수 호출(Function Calling) 포맷으로 변환해주는 유틸리티입니다.
"""

async def extract_tools(mcp_client):
    """
    (더미 함수) MCP 서버에서 노출된 도구 목록을 가져옵니다.
    실무에선 client.list_tools() 결과를 LangChain Tool 객체로 변환합니다.
    """
    if not mcp_client:
        return ["no_tools_available"]
        
    # 실제로는 await mcp_client.list_tools() 등을 호출
    return ["dummy_tool_1", "dummy_tool_2"]
