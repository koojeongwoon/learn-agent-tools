"""
[connection_manager.py]
여러 MCP 서버(tools-mcp, rag-mcp 등)와의 연결(SSE 방식)을 관리하는 브릿지입니다.
"""

import asyncio
from contextlib import AsyncExitStack
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession
from .. import logger

class MCPConnectionManager:
    def __init__(self):
        self.sessions = {}
        self.exit_stack = AsyncExitStack()

    async def connect_to_tools_mcp(self):
        """
        문서 병합, 워드 생성 도구가 있는 tools-mcp 서버와 SSE로 연결합니다.
        """
        try:
            import os
            url = os.environ.get("TOOLS_MCP_URL", "http://localhost:8000/sse")
            sse_transport = await self.exit_stack.enter_async_context(sse_client(url))
            session = await self.exit_stack.enter_async_context(ClientSession(sse_transport[0], sse_transport[1]))
            await session.initialize()
            self.sessions["tools"] = session
            logger.info(f"[System] tools-mcp (SSE) 접속 완료! ({url})")
        except Exception as e:
            logger.error(f"[Error] tools-mcp 접속 실패: {e}")

    async def connect_to_rag_mcp(self):
        """
        RAG 서버와 SSE 방식으로 연결합니다.
        """
        try:
            import os
            url = os.environ.get("RAG_MCP_URL", "http://localhost:8001/sse")
            sse_transport = await self.exit_stack.enter_async_context(sse_client(url))
            session = await self.exit_stack.enter_async_context(ClientSession(sse_transport[0], sse_transport[1]))
            await session.initialize()
            self.sessions["rag"] = session
            logger.info(f"[System] rag-mcp (SSE) 접속 완료! ({url})")
        except Exception as e:
            logger.error(f"[Error] rag-mcp 접속 실패: {e}")

    async def get_client(self, server_name: str):
        return self.sessions.get(server_name)

    async def close_all(self):
        """모든 MCP 세션을 종료합니다."""
        await self.exit_stack.aclose()
        self.sessions.clear()

# 싱글톤 인스턴스
mcp_manager = MCPConnectionManager()
