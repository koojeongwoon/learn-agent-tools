from common_util import AgentResponse, UserProfile
from ...core import AgentClient, AgentException
from ..api.schemas import ApiResponse
from ..domain.error_codes import ChatErrorCode
from ..domain.exceptions import ChatError


class ChatService:
    """채팅 도메인 서비스. 에이전트 통신과 응답 변환을 담당."""

    def __init__(self, agent_client: AgentClient):
        self.agent = agent_client

    async def handle_message(self, message: str, profile: UserProfile = None) -> ApiResponse:
        """
        사용자 메시지를 에이전트에 전달하고 응답을 가공한다.
        """
        try:
            agent_resp = await self.agent.send(message, user_profile=profile)
            return self._to_api_response(agent_resp)
        
        except AgentException as e:
            # 에이전트 관련 에러인 경우 CHAT 코드로 재포장하여 ChatError로 던짐
            if "CORE-002" in str(e.error_code):
                raise ChatError(ChatErrorCode.AGENT_RESPONSE_TIMEOUT)
            raise ChatError(ChatErrorCode.AGENT_CONNECTION_ERROR, message_override=str(e))
        except Exception as e:
            raise ChatError(ChatErrorCode.AGENT_CONNECTION_ERROR, message_override=str(e))

    @staticmethod
    def _to_api_response(agent_resp: AgentResponse) -> ApiResponse:
        """AgentResponse의 Full Payload에서 프론트에 필요한 필드만 추출."""
        return ApiResponse(
            status="success",
            message=agent_resp.content,
            needs_input=agent_resp.needs_clarification,
            input_prompt=agent_resp.clarification_question,
        )
