---
name: pdf-merger
description: "JSON 데이터를 기반으로 여러 PDF 파일을 하나로 병합하고, 목차와 표지를 자동 생성합니다."
# 에이전트가 이 스킬을 실행하기 위해 필요한 권한 (2026 표준)
allowed_tools: ["bash", "python"]
---

# PDF 병합 스킬 (PDF Merger)

이 스킬은 사용자의 요청을 분석하여 같은 위치의 `merge_pdf_v3.py`를 실행하고 병합된 결과물(PDF)을 만듭니다.

## 사용 가능한 도구 (Tools)

### `merge_document`

구조화된 파일 목록과 내용을 바탕으로 하나의 병합된 PDF 파일을 생성합니다. 결과물에는 표지와 전체 목차가 포함되며, 각 병합 항목 시작 시 간지(Overlay page)가 추가됩니다.

```json
{
  "command": "uv run .agents/skills/pdf-merger/merge_pdf_v3.py",
  "args": ["--data", "{{payload}}"],
  "parameters": {
    "type": "object",
    "properties": {
      "payload": {
        "type": "string",
        "description": "병합할 PDF 파일 목록과 문서 정보를 담은 JSON 문자열. 'output', 'cover_title', 'cover_subtitle', 'items' 객체 구조여야 합니다. (각 item은 'title'과 'files' 문자열 배열을 포함해야 함)"
      }
    },
    "required": ["payload"]
  }
}
```

### JSON 구조(payload) 예시
```json
{
  "output": "output/merged_portfolio.pdf",
  "cover_title": "[PwC컨설팅] 서류 제출",
  "cover_subtitle": "지원자: 구정운",
  "items": [
    {
      "title": "이력서",
      "files": ["resume.pdf"]
    },
    {
      "title": "포트폴리오",
      "files": ["portfolio1.pdf", "portfolio2.pdf"]
    }
  ]
}
```
