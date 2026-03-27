"""
[llm_client.py]
LangChain을 대체하여 OpenAI API 호출을 공통화하는 유틸리티 서비스입니다.
여러 에이전트에서 LLM을 호출할 때 발생하는 AsyncOpenAI의 중복된 보일러플레이트 코드를 줄여줍니다.
"""

import os
from typing import Type, TypeVar, Any
from pydantic import BaseModel
from openai import AsyncOpenAI

T = TypeVar('T', bound=BaseModel)

class LLMClient:
    def __init__(self):
        # API 키가 환경 변수에 있을 때만 클라이언트를 초기화 (에러 방지용)
        self.api_key_exists = bool(os.environ.get("OPENAI_API_KEY"))
        self._client = None
        self.default_model = "gpt-4o-mini"
        self.temperature = 0
        
    @property
    def client(self) -> AsyncOpenAI:
        if not self._client:
            self._client = AsyncOpenAI()
        return self._client

    async def get_structured_output(
        self, 
        system_prompt: str, 
        user_message: str, 
        response_model: Type[T],
        model: str = None
    ) -> T:
        """Pydantic 모델(response_model)을 기반으로 구조화된 JSON 출력을 객체화하여 반환합니다."""
        response = await self.client.beta.chat.completions.parse(
            model=model or self.default_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format=response_model,
            temperature=self.temperature
        )
        return response.choices[0].message.parsed

    async def get_text_output(
        self,
        system_prompt: str,
        user_message: str,
        model: str = None
    ) -> str:
        """구조화되지 않은 일반 텍스트 문자열 응답을 반환합니다."""
        response = await self.client.chat.completions.create(
            model=model or self.default_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=self.temperature
        )
        return response.choices[0].message.content

# 전역 싱글톤 인스턴스로 제공
llm = LLMClient()
