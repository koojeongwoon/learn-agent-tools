from pydantic import BaseModel, Field

class GuardDecision(BaseModel):
    is_safe: bool = Field(
        description="사용자 입력이 안전한지 여부. True=안전, False=위험"
    )
    reason: str = Field(
        description="판단 근거를 한 줄로 간결하게 설명"
    )
