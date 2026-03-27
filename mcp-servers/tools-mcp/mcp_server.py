# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mcp",
# ]
# ///

from mcp.server.fastmcp import FastMCP
from handlers.docx import generate_docx
from handlers.pdf import merge_pdfs

# 1. MCP 서버 인스턴스 생성
mcp = FastMCP("Tools 팩토리 서버")

# 2. 도구(Tools) 등록: 각 파일에 분리된 함수들
mcp.tool()(generate_docx)
mcp.tool()(merge_pdfs)


if __name__ == "__main__":
    import sys
    
    # SSE 방식(네트워크)과 Stdio 방식 중 선택 실행이 가능합니다.
    # 로컬 에이전트 연동이 목적이라면 기본적으로 mcp가 stdio 모드로 켜집니다.
    print("MCP 서버(Tools 팩토리)를 SSE 모드로 시작합니다 (포트: 8000)...", file=sys.stderr)
    mcp.run(transport='sse', port=8000)
