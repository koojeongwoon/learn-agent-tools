from jose import jwt
from ...core.config import settings
from ..domain import TokenInfo

class TokenProvider:
    """토큰 서명 및 검증을 담당하는 Infrastructure 레이어"""

    @staticmethod
    def sign(token_info: TokenInfo) -> str:
        """도메인 객체(TokenInfo)를 받아 JWT로 서명한다."""
        return jwt.encode(
            token_info.to_dict(),
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def decode(token: str) -> dict:
        """JWT를 디코딩하여 페이로드를 반환한다."""
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
