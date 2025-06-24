import os
import pandas as pd
import PyPDF2
import pdfplumber
from helper_functions import get_llm_response
from dotenv import load_dotenv
import csv
import base64
from openai import OpenAI

# Load environment variables
load_dotenv('.env', override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

def extract_text_from_pdf_pages(pdf_path, start_page, end_page):
    """
    PDF에서 지정된 페이지 범위의 텍스트를 추출합니다.
    
    Args:
        pdf_path (str): PDF 파일 경로
        start_page (int): 시작 페이지 (0부터 시작)
        end_page (int): 끝 페이지 (포함)
    
    Returns:
        str: 추출된 텍스트
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num in range(start_page, min(end_page + 1, len(pdf.pages))):
                page = pdf.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += f"=== 페이지 {page_num + 1} ===\n"
                    text += page_text + "\n\n"
    except Exception as e:
        print(f"PDF 텍스트 추출 중 오류 발생: {e}")
        # PyPDF2로 백업 시도
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(start_page, min(end_page + 1, len(pdf_reader.pages))):
                    page = pdf_reader.pages[page_num]
                    text += f"=== 페이지 {page_num + 1} ===\n"
                    text += page.extract_text() + "\n\n"
        except Exception as e2:
            print(f"PyPDF2로도 텍스트 추출 실패: {e2}")
    
    return text

def create_csv_from_llm_response(text_data, set_number, reference_csv="sorted_table.csv"):
    """
    추출된 텍스트를 OpenAI API를 사용하여 CSV 형식으로 변환합니다.
    
    Args:
        text_data (str): PDF에서 추출된 텍스트
        set_number (int): 세트 번호 (1~10)
        reference_csv (str): 참조할 CSV 파일 경로
    
    Returns:
        str: CSV 형식의 문자열
    """
    # 참조 CSV 파일 읽기
    with open(reference_csv, 'r', encoding='utf-8') as f:
        reference_csv_content = f.read()
    
    prompt = f"""
다음은 PDF에서 추출한 구조적 설계 데이터입니다:

{text_data}

위 데이터를 아래 참조 CSV 파일과 동일한 형식으로 변환해주세요:

참조 CSV 형식:
{reference_csv_content}

요구사항:
1. 참조 CSV와 정확히 동일한 컬럼 구조를 유지해주세요
2. 데이터가 없는 경우 빈 문자열로 처리해주세요
3. 숫자 데이터는 소수점 2자리까지 표시해주세요
4. CSV 헤더는 포함하지 말고 데이터 행만 반환해주세요
5. 각 행은 새로운 라인으로 구분해주세요

CSV 데이터만 반환해주세요 (설명이나 다른 텍스트 없이):
"""
    
    try:
        response = get_llm_response(prompt)
        return response.strip()
    except Exception as e:
        print(f"OpenAI API 호출 중 오류 발생: {e}")
        return ""

def process_pdf_to_csv(pdf_path="design_results.pdf", pages_per_set=4):
    """
    PDF 파일을 처리하여 여러 개의 CSV 파일을 생성합니다.
    
    Args:
        pdf_path (str): 처리할 PDF 파일 경로
        pages_per_set (int): 세트당 페이지 수
    """
    try:
        # PDF 총 페이지 수 확인
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
        
        print(f"총 페이지 수: {total_pages}")
        total_sets = total_pages // pages_per_set
        print(f"총 세트 수: {total_sets}")
        
        # 첫 번째 세트는 이미 처리되었다고 가정하고 2번째부터 처리
        for set_num in range(2, total_sets + 1):
            start_page = (set_num - 1) * pages_per_set
            end_page = start_page + pages_per_set - 1
            
            print(f"\n세트 {set_num} 처리 중 (페이지 {start_page + 1}-{end_page + 1})...")
            
            # PDF에서 텍스트 추출
            extracted_text = extract_text_from_pdf_pages(pdf_path, start_page, end_page)
            
            if not extracted_text.strip():
                print(f"세트 {set_num}에서 텍스트를 추출할 수 없습니다.")
                continue
            
            # OpenAI를 사용하여 CSV 데이터 생성
            csv_data = create_csv_from_llm_response(extracted_text, set_num)
            
            if csv_data:
                # CSV 파일로 저장
                output_filename = f"sorted_table_set_{set_num}.csv"
                
                # 헤더를 원본 파일에서 가져오기
                with open("sorted_table.csv", 'r', encoding='utf-8') as f:
                    header = f.readline().strip()
                
                with open(output_filename, 'w', encoding='utf-8', newline='') as f:
                    f.write(header + '\n')
                    f.write(csv_data)
                
                print(f"세트 {set_num} 완료: {output_filename} 생성됨")
            else:
                print(f"세트 {set_num} 처리 실패")
        
        print("\n모든 세트 처리 완료!")
        
    except Exception as e:
        print(f"오류 발생: {e}")

def merge_all_csv_files():
    """
    모든 생성된 CSV 파일을 하나로 병합합니다.
    """
    try:
        # 모든 CSV 파일 찾기
        csv_files = ["sorted_table.csv"]  # 첫 번째 세트
        
        for i in range(2, 11):  # 2~10번 세트
            filename = f"sorted_table_set_{i}.csv"
            if os.path.exists(filename):
                csv_files.append(filename)
        
        if len(csv_files) == 1:
            print("병합할 추가 CSV 파일이 없습니다.")
            return
        
        # 모든 CSV 파일 병합
        all_data = []
        header = None
        
        for csv_file in csv_files:
            with open(csv_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if header is None:
                    header = lines[0].strip()
                    all_data.append(header)
                # 헤더를 제외한 데이터 추가
                for line in lines[1:]:
                    if line.strip():  # 빈 줄이 아닌 경우만
                        all_data.append(line.strip())
        
        # 병합된 파일 저장
        with open("merged_sorted_table.csv", 'w', encoding='utf-8') as f:
            for line in all_data:
                f.write(line + '\n')
        
        print(f"병합 완료: merged_sorted_table.csv ({len(csv_files)}개 파일 병합)")
        
    except Exception as e:
        print(f"병합 중 오류 발생: {e}")

if __name__ == "__main__":
    print("PDF to CSV 변환 프로그램")
    print("=" * 50)
    
    # PDF 파일 존재 확인
    if not os.path.exists("design_results.pdf"):
        print("design_results.pdf 파일을 찾을 수 없습니다.")
        exit(1)
    
    # 환경 변수 확인
    if not openai_api_key:
        print("OpenAI API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
        exit(1)
    
    # 메뉴
    while True:
        print("\n선택하세요:")
        print("1. PDF 처리하여 CSV 생성 (세트 2~10)")
        print("2. 모든 CSV 파일 병합")
        print("3. 종료")
        
        choice = input("선택 (1-3): ").strip()
        
        if choice == "1":
            process_pdf_to_csv()
        elif choice == "2":
            merge_all_csv_files()
        elif choice == "3":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 선택해주세요.")
