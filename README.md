# Enterprise AI Agent Workspace

이 프로젝트는 MCP(Model Context Protocol) 기반의 **무기 창고(도구 서버)**와 이를 지휘하는 **멀티 에이전트 오케스트레이터(지휘자 봇)**가 완벽하게 분리된 엔터프라이즈급 AI 아키텍처 뼈대입니다.

## 🏗️ Architecture Overview

프로젝트는 두 가지 핵심 도메인으로 나뉘어 있습니다:

### 1. `mcp-servers/` (팔과 다리: 무기 창고)
비즈니스 로직(PDF 병합, Word 문서 생성 등)이 실제로 실행되는 독립된 환경입니다.
에이전트 클라이언트의 무거운 컨텍스트를 줄이기 위해, 서버들은 용도에 맞게 독립적으로 배포됩니다.
- **`tools-mcp/`**: 가벼운 유틸리티 문서 작업 전문 서버 (`mcp_server.py`)
  - `.agents/skills/pdf-merger`: PDF 문서 병합 로직 및 스킬
  - `.agents/skills/docx-generator`: Word 데이터 렌더링 로직 및 템플릿
- **`rag-mcp/`**: (추후 생성) 무거운 사내 지식 검색(Vector DB 커넥션 유지용) 전용 서버

### 2. `agent-backend/` (뇌: 에이전트 지휘 본부)
MCP 서버들로부터 도구 목록만 받아와서, 사용자의 대화를 분석하고 상황에 맞는 에이전트에게 업무를 배분하는 오케스트레이터입니다.
- **`orchestrator.py`**: 사용자의 질문을 가장 먼저 분석하는 라우터 (Supervisor)
- **`agents/`**: 전문 에이전트 군단 (예: `document_agent`, `research_agent`)
- **`mcp_clients/`**: 각 MCP 서버들과의 네트워크 연결(SSE 등)을 유지하고 도구를 긁어오는 통신 브릿지

---

## 🚀 How to Run

### 무기 창고(MCP 서버) 단독 테스트
`mcp-servers/tools-mcp/` 폴더 안으로 이동하여 기존에 만들어진 파이썬 스크립트 도구들을 실행할 수 있습니다.
```bash
cd mcp-servers/tools-mcp
uv run mcp_server.py
```
(또는 각 스킬 폴더 안에 있는 파이썬 스크립트를 `uv run`으로 직접 호출할 수 있습니다.)

### 에이전트 백엔드(뇌) 뼈대
`agent-backend/`에서 클라이언트 서버를 띄울 수 있도록 FastAPI 보일러플레이트가 작성되어 있습니다.
```bash
cd agent-backend
# 필요한 패키지 등을 설치 후:
uvicorn src.main:app --reload
```

## ⚠️ Notes
이 구조는 **관심사의 분리(Separation of Concerns)**가 적용되어 있습니다. 
만약 새로운 문서 작업(Excel 변환 등) 기능이 필요하다면 `agent-backend`의 코드는 1줄도 수정할 필요 없이, 오직 `mcp-servers/tools-mcp/.agents/skills/` 폴더 안에 새로운 폴더 하나만 추가하면 모든 것이 자동화됩니다!

---

## 💡 Developer Setup: 로컬 에이전트 연동 (Symlink)
Cursor나 로컬에 설치된 범용 AI 에이전트가 최상위 폴더(`/tools`)에서 스킬(`SKILL.md`)을 자동으로 인식하게 하려면, 프로젝트 루트에 **심볼릭 링크(소프트 링크)**를 생성해 두어야 합니다.

> **Note:** Git은 심볼릭 링크 자체를 커밋하고 체크아웃할 때 복원해 줍니다. 하지만 윈도우(Windows) 등 일부 환경에서 링크가 끊어질 경우 아래 명령어를 수동으로 실행하세요.

```bash
# 프로젝트 루트 디렉토리에서 실행
ln -s mcp-servers/tools-mcp/.agents .agents
```
이 꼼수(Trick) 덕분에, 물리적으로 아키텍처를 `mcp-servers/` 내부에 안전하게 격리하면서도 로컬 IDE 개발 경험을 100% 쾌적하게 유지할 수 있습니다.
