from typing import Optional, Set, Dict
from ..domain import User, IUserRepository
from common_util import UserProfile
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# [MOCK DATABASE]
MOCK_USERS_DATA = {
    "testuser": {
        "password_hash": pwd_context.hash("test1234"),
        "profile": UserProfile(
            user_id="user_001",
            region="서울특별시",
            district="강남구",
            life_cycle="청년",
            interests=["주거", "고용"]
        )
    }
}

# [MOCK REFRESH TOKEN STORE]
_active_refresh_tokens: Dict[str, Set[str]] = {}


class MockUserRepository(IUserRepository):
    """메모리 기반의 Mock 사용자 저장소 구현"""

    def find_by_username(self, username: str) -> Optional[User]:
        data = MOCK_USERS_DATA.get(username)
        if not data:
            return None
        return User(
            username=username,
            password_hash=data["password_hash"],
            profile=data["profile"]
        )

    def get_active_jtis(self, username: str) -> Set[str]:
        return _active_refresh_tokens.get(username, set())

    def update_active_jtis(self, username: str, jtis: Set[str]) -> None:
        _active_refresh_tokens[username] = jtis

    def invalidate_all_jtis(self, username: str) -> None:
        if username in _active_refresh_tokens:
            _active_refresh_tokens[username] = set()
