from typing import Optional
from pydantic import BaseModel, Field

class ReviewScore(BaseModel):
    relevance: int = Field(
        description="사용자의 질문과 답변의 관련성 (1~5). 5=완벽히 관련, 1=무관"
    )
    completeness: int = Field(
        description="정보 완결성 (1~5). 제목/대상/지원내용/신청방법/마감일 등 핵심 정보 포함 여부. 5=빠짐없음, 1=대부분 누락"
    )
    accuracy: int = Field(
        description="사실 정확도 (1~5). 사용자의 지역/생애주기에 맞지 않는 정책이 포함되었는지. 5=모두 정확, 1=잘못된 정보 다수"
    )
    tone: int = Field(
        description="톤과 가독성 (1~5). 친절하고 이해하기 쉬운 표현인지. 5=매우 친절, 1=딱딱하고 어려움"
    )
    faithfulness: Optional[int] = Field(
        default=None,
        description="검색 결과 근거 충실도 (1~5). 답변이 제공된 검색 데이터에 근거하는지. 5=완전 근거, 1=근거 없는 내용 다수. 검색 데이터가 없으면 null"
    )
    feedback: str = Field(
        description="가장 낮은 점수 항목에 대한 구체적 개선 방향. 모든 항목이 4점 이상이면 빈 문자열."
    )
