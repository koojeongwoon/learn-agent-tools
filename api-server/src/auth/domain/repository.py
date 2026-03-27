from abc import ABC, abstractmethod
from typing import Optional, Set
from .user import User

class IUserRepository(ABC):
    """사용자 저장소 추상 인터페이스"""
    
    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_active_jtis(self, username: str) -> Set[str]:
        pass

    @abstractmethod
    def update_active_jtis(self, username: str, jtis: Set[str]) -> None:
        pass

    @abstractmethod
    def invalidate_all_jtis(self, username: str) -> None:
        pass
