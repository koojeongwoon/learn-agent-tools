from pydantic import BaseModel, Field

class RouteDecision(BaseModel):
    agent_name: str = Field(
        description="선택된 에이전트의 이름 (예: welfare_recommendation, document_agent, direct_chat)"
    )
    direct_message: str = Field(
        description="agent_name이 direct_chat일 경우, 사용자에게 건네는 AI의 자연스러운 답변. 그 외의 에이전트일 경우 빈 문자열."
    )
