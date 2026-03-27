import os


class Settings:
    """환경변수 기반 설정. 모든 모듈이 공유하는 단일 설정 객체."""

    # Agent 서버
    AGENTS_URL: str = os.environ.get("AGENTS_URL", "http://localhost:8080/chat")
    AGENT_TIMEOUT: float = float(os.environ.get("AGENT_TIMEOUT", "60.0"))

    # 서버
    APP_TITLE: str = "User Client API"
    API_PREFIX: str = "/api"

    # 인증 (JWT & Cookies)
    JWT_SECRET: str = os.environ.get("JWT_SECRET", "super-secret-key-change-it")
    JWT_ALGORITHM: str = "HS256"
    
    # Access Token: 30분
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Refresh Token: 7일
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Cookie 설정
    ACCESS_TOKEN_COOKIE_NAME: str = "access_token"
    REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"
    COOKIE_SECURE: bool = os.environ.get("COOKIE_SECURE", "False").lower() == "true"
    COOKIE_SAMESITE: str = "lax"


settings = Settings()
