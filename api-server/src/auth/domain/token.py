import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional, Set, Dict
from ...core.config import settings

@dataclass(frozen=True)
class TokenInfo:
    """토큰의 데이터와 만료 시간을 담은 Value Object"""
    sub: str
    exp: datetime
    jti: Optional[str] = None
    type: str = "access"

    def to_dict(self) -> Dict:
        data = {"sub": self.sub, "exp": self.exp, "type": self.type}
        if self.jti:
            data["jti"] = self.jti
        return data

class AccessToken(TokenInfo):
    @classmethod
    def create(cls, username: str) -> "AccessToken":
        """AccessToken 생성 정책"""
        return cls(
            sub=username,
            exp=datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            type="access"
        )

class RefreshToken(TokenInfo):
    @classmethod
    def create(cls, username: str) -> "RefreshToken":
        """RefreshToken 생성 정책"""
        return cls(
            sub=username,
            exp=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            jti=str(uuid.uuid4()),
            type="refresh"
        )

    def validate_rotation(self, active_jtis: Set[str]) -> bool:
        """RTR 규칙 검증"""
        return self.jti in active_jtis
