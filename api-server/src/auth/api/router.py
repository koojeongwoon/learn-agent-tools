from fastapi import APIRouter, Response, Cookie, Depends
from .schemas import LoginRequest, UserResponse
from ..application.service import AuthService
from ...core.config import settings

router = APIRouter(prefix="/api/auth", tags=["Auth"])
_auth_service = AuthService()


def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    """보안 쿠키 설정 (HttpOnly, Secure, SameSite)"""
    response.set_cookie(
        key=settings.ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )


@router.post("/login", response_model=UserResponse)
async def login(request: LoginRequest, response: Response):
    """로그인 및 쿠키 설정. 에러는 글로벌 핸들러에서 처리됨."""
    profile, at, rt = _auth_service.login(request.username, request.password)

    # 쿠키 굽기
    set_auth_cookies(response, at, rt)

    return UserResponse(username=request.username, profile=profile)


@router.post("/refresh")
async def refresh(
    response: Response, refresh_token: str = Cookie(None, alias=settings.REFRESH_TOKEN_COOKIE_NAME)
):
    """Refresh Token Rotation (RTR). 에러는 글로벌 핸들러에서 처리됨."""
    new_at, new_rt = _auth_service.rotate_tokens(refresh_token)
    set_auth_cookies(response, new_at, new_rt)
    return {"status": "success", "message": "Tokens rotated"}


@router.post("/logout")
async def logout(response: Response):
    """로그아웃 및 쿠키 제거"""
    response.delete_cookie(settings.ACCESS_TOKEN_COOKIE_NAME)
    response.delete_cookie(settings.REFRESH_TOKEN_COOKIE_NAME)
    return {"status": "success", "message": "Logged out"}
