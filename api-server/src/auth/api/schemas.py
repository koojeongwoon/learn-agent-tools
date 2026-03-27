from pydantic import BaseModel, Field
from common_util import UserProfile


class LoginRequest(BaseModel):
    """로그인 요청"""
    username: str = Field(..., description="사용자 이름")
    password: str = Field(..., description="비밀번호")


class UserResponse(BaseModel):
    """인증 후 반환할 사용자 정보"""
    username: str
    profile: UserProfile


class TokenData(BaseModel):
    """JWT Payload 데이터 구조"""
    sub: str = Field(..., description="사용자 ID (username)")
    jti: str = Field(..., description="Token ID (RTR 추적용)")
    exp: int = Field(..., description="만료 시간")
