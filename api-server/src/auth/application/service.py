from typing import Optional
from common_util import UserProfile

from ..domain import RefreshToken, AccessToken, IUserRepository
from ..domain.error_codes import AuthErrorCode
from ..domain.exceptions import AuthError
from ..infrastructure.mock_repository import MockUserRepository
from ..infrastructure.token_provider import TokenProvider


class AuthService:
    """애플리케이션 서비스. 도메인 정책을 조달하고 인프라와 협력하여 유스케이스를 조율한다."""

    def __init__(self, repository: IUserRepository = None):
        self.repo = repository or MockUserRepository()
        self.tp = TokenProvider()

    def login(self, username: str, password: str) -> tuple[UserProfile, str, str]:
        """로그인 유스케이스: 도메인 전용 예외(AuthError)에 Enum을 담아 던짐"""
        user = self.repo.find_by_username(username)
        if not user or not user.verify_password(password):
            # 도메인 이름(AuthError) + 이넘(AuthErrorCode) 조합
            raise AuthError(AuthErrorCode.INVALID_CREDENTIALS)

        at_vo, rt_vo = user.issue_tokens()
        self.repo.update_active_jtis(username, {rt_vo.jti})
        
        return user.profile, self.tp.sign(at_vo), self.tp.sign(rt_vo)

    def rotate_tokens(self, refresh_token_str: str) -> tuple[str, str]:
        """토큰 갱신 유스케이스 (RTR)"""
        try:
            payload = self.tp.decode(refresh_token_str)
            username = payload.get("sub")
            jti = payload.get("jti")
            
            active_jtis = self.repo.get_active_jtis(username)
            rt_vo = RefreshToken(jti=jti, sub=username, exp=None)

            if not rt_vo.validate_rotation(active_jtis):
                self.repo.invalidate_all_jtis(username)
                raise AuthError(AuthErrorCode.TOKEN_REUSED)

            user = self.repo.find_by_username(username)
            if not user:
                raise AuthError(AuthErrorCode.USER_NOT_FOUND)

            new_at_vo, new_rt_vo = user.issue_tokens()
            self.repo.update_active_jtis(username, {new_rt_vo.jti})
            
            return self.tp.sign(new_at_vo), self.tp.sign(new_rt_vo)

        except AuthError as e:
            raise e
        except Exception:
            raise AuthError(AuthErrorCode.INVALID_CREDENTIALS, message_override="Could not validate refresh token")

    def get_user_profile(self, username: str) -> Optional[UserProfile]:
        user = self.repo.find_by_username(username)
        return user.profile if user else None

    def logout(self, username: str):
        self.repo.invalidate_all_jtis(username)
