import subprocess
import os

from common_util.logger import logger, trace_id_var

def create_docx(data: dict, template_path: str = None, output_path: str = None, trace_id: str = None) -> str:
    """
    JSON 데이터를 기반으로 Word 문서를 생성합니다.
    (docx-generator 스킬 실행)
    
    Args:
        data: 문서에 들어갈 내용을 담은 JSON 데이터 (dict)
        template_path: 사용할 템플릿 파일 경로 (예: 'templates/proposal_v1.docx')
        output_path: 생성될 문서의 출력 경로 (예: 'output/generated_document.docx')
        trace_id: 요청 추적을 위한 ID
    """
    if trace_id:
        trace_id_var.set(trace_id)
        
    logger.info(f"📄 Creating Word document with template: {template_path}")

    script_path = ".agents/skills/docx-generator/generate_docx.py"
    
    if not os.path.exists(script_path):
        return f"오류: 스킬 스크립트를 찾을 수 없습니다. ({script_path})"
        
    try:
        # 하위 프로세스로 스킬 스크립트 실행 (에이전트가 하던 일을 서버가 대신함!)
        result = subprocess.run(
            ["uv", "run", script_path, "--template", template_id, "--data", payload_json_string],
            capture_output=True,
            text=True,
            check=True
        )
        return f"성공적으로 문서를 생성했습니다!\n출력결과:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"문서 생성 중 오류 발생:\n{e.stderr}"
