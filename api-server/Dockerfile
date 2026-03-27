FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml .envrc* ./
RUN uv sync --frozen --no-dev
COPY src/ ./src/

# 퍼블릭 사용자 API 8002포트로 오픈
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8002"]
