import subprocess
import os

from common_util.logger import logger, trace_id_var

def merge_pdfs(payload_json_string: str, trace_id: str = None) -> str:
    """
    JSON 데이터를 받아 지정된 여러 PDF 파일을 순서대로 병합하고 목차/표지를 생성합니다.
    (pdf-merger 스킬 실행)
    
    Args:
        payload_json_string: 병합할 PDF 파일 목록과 출력 정보를 담은 JSON 문자열.
                             'output', 'cover_title', 'items' 객체 구조여야 합니다.
    """
    if trace_id:
        trace_id_var.set(trace_id)
        
    logger.info(f"📑 Initiating PDF merge with payload: {payload_json_string[:100]}...") # Log first 100 chars of payload
    
    script_path = ".agents/skills/pdf-merger/merge_pdf_v3.py"
    
    if not os.path.exists(script_path):
        return f"오류: 스킬 스크립트를 찾을 수 없습니다. ({script_path})"
        
    try:
        # 하위 프로세스로 스킬 스크립트 실행
        result = subprocess.run(
            ["uv", "run", script_path, "--data", payload_json_string],
            capture_output=True,
            text=True,
            check=True
        )
        return f"성공적으로 문서 병합을 완료했습니다!\n출력결과:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"문서 병합 중 오류 발생:\n{e.stderr}"
