---
name: docx-generator
description: "JSON 데이터를 기반으로 정해진 규격의 Word(.docx) 문서를 생성합니다."
# 에이전트가 이 스킬을 실행하기 위해 필요한 권한 (2026 표준)
allowed_tools: ["bash", "python"]
---

# 문서 생성 스킬 (Docx Generator)

이 스킬은 사용자의 요청을 분석하여 같은 폴더 내의 `generate_docx.py`를 실행하고 결과물을 만듭니다.

## 사용 가능한 도구 (Tools)

### `generate_document`

구조화된 데이터를 바탕으로 실제 파일을 생성합니다.

```json
{
  "command": "uv run .agents/skills/docx-generator/generate_docx.py",
  "args": ["--template", "{{template_id}}", "--data", "{{payload}}"],
  "parameters": {
    "type": "object",
    "properties": {
      "template_id": {
        "type": "string",
        "description": "사용할 양식 ID (예: 'proposal_v1', 'resume_v2')"
      },
      "payload": {
        "type": "string",
        "description": "문서에 들어갈 내용을 담은 JSON 문자열"
      }
    },
    "required": ["template_id", "payload"]
  }
}
```

### `--get-vars` 옵션
템플릿 파일 안에 어떤 변수가 필요한지 모를 때는 `--data` 인수 대신 이 플래그를 사용하여 변수 목록만 추출할 수 있습니다.
```bash
uv run .agents/skills/docx-generator/generate_docx.py --template {{template_id}} --get-vars
```
