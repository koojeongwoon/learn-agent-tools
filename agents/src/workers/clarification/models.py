from pydantic import BaseModel, Field

class ClarificationDecision(BaseModel):
    needs_clarification: bool = Field(
        description="추가 정보가 필요하면 true, 충분하면 false"
    )
    question: str = Field(
        description="needs_clarification이 true일 때 사용자에게 되물을 자연스러운 질문. false이면 빈 문자열."
    )
