from mcp.server.fastmcp import FastMCP
from handlers.search import search_knowledge_base

# 1. RAG용 MCP 서버 인스턴스 생성
mcp = FastMCP("RAG 팩토리 서버")

# 2. 도구(Tools) 등록: 각 파일에 분리된 함수들
mcp.tool()(search_knowledge_base)

if __name__ == "__main__":
    import sys
    print("MCP 서버(RAG 팩토리)를 SSE 모드로 시작합니다 (포트: 8001)...", file=sys.stderr)
    mcp.run(transport='sse', port=8001)
