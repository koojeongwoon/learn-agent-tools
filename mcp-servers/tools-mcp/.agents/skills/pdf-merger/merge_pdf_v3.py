# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "PyPDF2",
#     "reportlab",
# ]
# ///

import os
import argparse
import json
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- [설정 부분] ---
FONT_PATH = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
FONT_NAME = "AppleGothic"

if os.path.exists(FONT_PATH):
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))
else:
    FONT_NAME = "Helvetica-Bold"

def create_overlay_page(text, is_title_page=False):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    if is_title_page:
        can.setFont(FONT_NAME, 30)
        can.drawCentredString(297.5, 500, text)
        
    can.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

def create_cover_page(title, subtitle=None):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont(FONT_NAME, 40)
    # 제목 렌더링
    can.drawCentredString(297.5, 460, title)
    # 부제목(이름)이 있으면 렌더링
    if subtitle:
        can.setFont(FONT_NAME, 20)
        can.drawCentredString(297.5, 400, subtitle)
    can.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

def create_toc_page(titles_with_pages):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont(FONT_NAME, 25)
    can.drawCentredString(297.5, 750, "< 전체 목차 >")
    
    can.setFont(FONT_NAME, 14)
    y_position = 680
    for title, page_num in titles_with_pages:
        can.drawString(100, y_position, title)
        can.drawRightString(500, y_position, f"{page_num} page")
        y_position -= 30
    
    can.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

def merge_pdfs_v3(config):
    pdf_list = config.get("items", [])
    output_filename = config.get("output", "merged_output.pdf")
    cover_title = config.get("cover_title")
    cover_subtitle = config.get("cover_subtitle")

    temp_writer = PdfWriter()
    toc_data = []
    
    # Calculate initial page numbers
    has_cover = bool(cover_title)
    current_page_num = 1
    if has_cover:
        current_page_num += 1  # Cover
    if pdf_list:
        current_page_num += 1  # TOC is 1 page minimum

    for item in pdf_list:
        display_title = item.get('title', 'Unknown Section')
        files = item.get('files', [])

        # 1. 항목별 소제목 페이지 (섹션 시작)
        toc_data.append((display_title, current_page_num))
        title_pg = create_overlay_page(display_title, is_title_page=True)
        temp_writer.add_page(title_pg)
        current_page_num += 1

        # 2. 해당 항목에 속한 모든 파일 병합
        for file_path in files:
            if not os.path.exists(file_path):
                print(f"파일 없음 건너뜀: {file_path}")
                continue
            
            try:
                reader = PdfReader(file_path)
                for page in reader.pages:
                    temp_writer.add_page(page)
                    current_page_num += 1
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        
        print(f"병합 완료: [{display_title}] - {len(files)}개 파일")

    # 최종 병합
    final_writer = PdfWriter()
    
    # 맨 앞에 표지 추가
    if has_cover:
        cover_page = create_cover_page(cover_title, subtitle=cover_subtitle)
        final_writer.add_page(cover_page)
    
    # 목차 추가
    if toc_data:
        toc_page = create_toc_page(toc_data)
        final_writer.add_page(toc_page)
    
    for page in temp_writer.pages:
        final_writer.add_page(page)

    # 북마크 추가 (0-indexed)
    for title, page_num in toc_data:
        final_writer.add_outline_item(title, page_num - 1)

    # 출력 폴더 확인 및 저장
    os.makedirs(os.path.dirname(output_filename) or ".", exist_ok=True)
    with open(output_filename, "wb") as f:
        final_writer.write(f)
    print(f"\\n최종 파일 생성 완료: {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge PDFs based on JSON configuration.")
    parser.add_argument("--data", type=str, required=True, help="JSON string containing the configuration")
    
    args = parser.parse_args()
    try:
        config = json.loads(args.data)
        merge_pdfs_v3(config)
    except Exception as e:
        print(f"Error executing pdf merge: {e}")
        exit(1)