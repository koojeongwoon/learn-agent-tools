from fastapi import APIRouter, Depends
from ...auth import get_current_user
from .schemas import ChatRequest, ApiResponse
from ..application.service import ChatService
from common_util import UserProfile

router = APIRouter(prefix="/api/chat", tags=["Chat"])

# 서비스 인프라 주입 (AgentClient는 Core에서 가져옴)
from ...core import AgentClient
_chat_service = ChatService(agent_client=AgentClient())


@router.post("", response_model=ApiResponse)
async def chat(
    request: ChatRequest, 
    current_user: UserProfile = Depends(get_current_user)
):
    """
    채팅 엔드포인트. 에러는 글로벌 핸들러에서 처리됨.
    """
    return await _chat_service.handle_message(request.message, profile=current_user)
