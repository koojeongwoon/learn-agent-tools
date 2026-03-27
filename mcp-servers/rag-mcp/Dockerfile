FROM python:3.12-slim

# 빠른 패키지 매니저인 uv를 컨테이너에 설치합니다.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# 1. 의존성 파일 먼저 복사
COPY pyproject.toml uv.lock ./

# 2. 의존성 설치
RUN uv sync --frozen --no-dev

# 3. 소스 코드 복사
COPY . .

EXPOSE 8001

# 4. 앱 실행
CMD ["uv", "run", "mcp_server.py"]
