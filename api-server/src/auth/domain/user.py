from dataclasses import dataclass
from common_util import UserProfile
from passlib.context import CryptContext
from .token import AccessToken, RefreshToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@dataclass
class User:
    """사용자 엔티티 (핵심 비즈니스 규칙 소유)"""
    username: str
    password_hash: str
    profile: UserProfile

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password_hash)

    def issue_tokens(self) -> tuple[AccessToken, RefreshToken]:
        """인증 성공 후 토큰 쌍 발행 정책"""
        return AccessToken.create(self.username), RefreshToken.create(self.username)

    @classmethod
    def create(cls, username: str, plain_password: str, profile: UserProfile) -> "User":
        return cls(
            username=username,
            password_hash=pwd_context.hash(plain_password),
            profile=profile
        )
