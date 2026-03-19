# AI Agent Document Generator

이 프로젝트는 Claude Code 또는 Gemini CLI와 연동하여, 사용자의 자연어 요청을 분석하고 구조화된 Word(.docx) 문서를 자동으로 생성하는 AI 에이전트 스킬 세트입니다.

## Tech Stack

Runtime: Python 3.12+

Package Manager: uv (Extremely fast Rust-based manager)

Agent Framework: Claude Code / Gemini CLI (Agent Skills Standard)

Template Engine: python-docx-template (Jinja2 based docx rendering)

## Prerequisites (사전 준비)

Python 3.12+ 설치

uv 설치:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

direnv 설치 (선택 사항, 환경 자동 로드용)

## Setup Guide (세팅 순서)

1. 프로젝트 초기화 및 의존성 설치
   uv를 사용하여 가상환경을 생성하고 필요한 라이브러리를 한 번에 설치합니다.

```bash
# 의존성 동기화 및 가상환경(.venv) 자동 생성
uv sync
```

2. 환경 변수 및 활성화
   direnv를 사용 중이라면 아래 명령어로 환경을 승인하세요.

```bash
direnv allow
```

(사용하지 않는다면 source .venv/bin/activate를 수동으로 입력하세요.)

3. 디렉토리 구조 확인
   프로젝트가 정상적으로 작동하려면 아래 폴더 구조가 유지되어야 합니다.

templates/: .docx 템플릿 파일 저장소 (예: proposal_v1.docx)

output/: 생성된 문서가 저장되는 폴더

scripts/: 핵심 비즈니스 로직 (generate_docx.py)

.agents/skills/: AI 에이전트 스킬 정의서 (SKILL.md)

## AI 에이전트 연동 (Skill Registration)

별도의 설정 없이 .agents/skills/ 폴더를 자동으로 인식합니다. 터미널에서 llm 실행 후 바로 명령하세요.

"(특정양식을 선택한 후) ~~로 문서 만들어줘"

## 테스트 (Local Test)

AI 없이 로직만 테스트하고 싶을 때 아래 명령어를 사용합니다.

```bash
uv run scripts/generate_docx.py --template "proposal_v1" --data '{"name": "구정운", "achievements": ["테스트 성공"]}'
```

## 주의사항 (Fact Check)

템플릿 문법: 워드 파일 내에 {{ variable }} 또는 {% for ... %}와 같은 Jinja2 문법이 정확히 기입되어 있어야 합니다.

에이전트 권한: 에이전트가 스크립트를 실행할 때 터미널에서 요청하는 **승인(Y/N)**에 동의해야 파일이 생성됩니다.

파일 경로: 모든 명령어는 반드시 프로젝트 루트 디렉토리에서 실행해야 경로 에러가 발생하지 않습니다.
