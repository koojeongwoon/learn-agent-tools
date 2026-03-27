#!/usr/bin/env python3
import argparse
import json
import os
import sys
from docxtpl import DocxTemplate

def generate_document(template_id, payload_str):
    """
    AI가 준 JSON 데이터를 받아 워드 템플릿에 렌더링합니다.
    """
    try:
        # 1. JSON 문자열 파싱 (AI가 준 데이터)
        try:
            payload = json.loads(payload_str)
        except json.JSONDecodeError as e:
            # 에러 메시지를 구체적으로 뱉어야 AI가 보고 재시도함 (2026 표준)
            sys.exit(f"Error: Invalid JSON data format. {str(e)}")

        # 2. 템플릿 파일 경로 설정
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir, "templates", f"{template_id}.docx")
        if not os.path.exists(template_path):
            sys.exit(f"Error: Template file not found at {template_path}")

        # 3. 템플릿 로드 및 데이터 바인딩
        doc = DocxTemplate(template_path)
        
        # 템플릿 내 필요한 변수 추출 및 알림
        expected_vars = doc.get_undeclared_template_variables()
        missing_vars = [var for var in expected_vars if var not in payload]
        if missing_vars:
            print(f"Warning: The following variables are expected by the template but missing from payload: {missing_vars}")
            
        # payload 자체가 Jinja2 컨텍스트로 들어갑니다.
        doc.render(payload)

        # 4. 결과 파일 저장 (파일명 규칙: template_id_timestamp.docx)
        import time
        timestamp = int(time.time())
        output_name = f"{template_id}_{timestamp}.docx"
        output_path = f"output/{output_name}"

        # 출력 폴더 생성
        os.makedirs("output", exist_ok=True)
        
        doc.save(output_path)
        
        # 5. 성공 메시지 출력 (AI가 이 메시지를 읽고 사용자에게 최종 답변함)
        print(f"SUCCESS: Document generated successfully at {output_path}")

    except Exception as e:
        sys.exit(f"Critical Error during document generation: {str(e)}")

if __name__ == "__main__":
    # 아규먼트 파싱 (SKILL.md의 args와 매핑됨)
    parser = argparse.ArgumentParser(description="Generate docx from JSON data and template.")
    parser.add_argument("--template", required=True, help="Template ID (filename without extension)")
    parser.add_argument("--data", required=False, help="JSON string containing document content")
    parser.add_argument("--get-vars", action="store_true", help="Print the undeclared variables in the template and exit")
    
    args = parser.parse_args()
    
    if args.get_vars:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir, "templates", f"{args.template}.docx")
        if not os.path.exists(template_path):
            sys.exit(f"Error: Template file not found at {template_path}")
        doc = DocxTemplate(template_path)
        print(f"Variables found in template '{args.template}': {list(doc.get_undeclared_template_variables())}")
        sys.exit(0)
        
    if not args.data:
        sys.exit("Error: the following arguments are required: --data (unless --get-vars is used)")
        
    generate_document(args.template, args.data)