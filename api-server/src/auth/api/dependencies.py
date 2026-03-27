from fastapi import Depends, HTTPException, status, Cookie
from jose import JWTError, jwt

from ...core.config import settings
from ..application.service import AuthService
from ..infrastructure.mock_repository import MockUserRepository
from common_util import UserProfile

# 의존성 주입 조리
_repo = MockUserRepository()
_auth_service = AuthService(repository=_repo)

async def get_current_user(
    access_token: str = Cookie(None, alias=settings.ACCESS_TOKEN_COOKIE_NAME)
) -> UserProfile:
    """
    쿠키에서 Access Token을 추출하여 검증하고 UserProfile을 반환합니다.
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = jwt.decode(
            access_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        profile = _auth_service.get_user_profile(username)
        if profile is None:
            raise HTTPException(status_code=401, detail="User not found")
        return profile

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
