FROM python:3.12-slim

# 빠른 패키지 매니저인 uv를 컨테이너에 설치합니다.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# 1. 환경 변수와 의존성 파일 복사
COPY pyproject.toml .envrc* ./

# 2. 의존성 설치
RUN uv sync --frozen --no-dev

# 3. 소스 코드 복사 (src 폴더)
COPY src/ ./src/

# 4. 내부용 API 서버 실행 (Orchestrator 진입점)
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
