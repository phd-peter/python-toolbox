# PDF 데이터 추출기 (PDF Data Extractor)

PDF 파일에서 구조적 데이터를 추출하여 CSV 형식으로 변환하는 도구입니다. OpenAI GPT 모델을 사용하여 PDF 텍스트를 구조화된 데이터로 변환하며, 영어/한글 문서와 1단/2단 레이아웃을 지원합니다.

## 📋 기능 설명

- **PDF 텍스트 추출**: pdfplumber와 PyPDF2를 사용한 안정적인 텍스트 추출
- **구조화된 데이터 변환**: OpenAI GPT 모델을 통한 지능적 데이터 구조화
- **다중 레이아웃 지원**: 1단/2단 문서, 영어/한글 문서 처리
- **배치 처리**: 여러 페이지를 세트별로 자동 처리
- **CSV 병합**: 여러 CSV 파일을 하나로 자동 병합
- **OCR 지원**: 이미지 기반 PDF를 위한 GPT-4 Vision 활용

## 🚀 설치 방법

1. 의존성 설치:
```bash
pip install -r requirements.txt
```

2. 환경변수 설정:
```bash
cp .env.template .env
# .env 파일을 편집하여 실제 OpenAI API 키 입력
```

## 💻 사용법

### 기본 사용법
```bash
python demo.py
```

메뉴에서 다음 옵션을 선택할 수 있습니다:
1. PDF 처리하여 CSV 생성 (세트 2~10)
2. 모든 CSV 파일 병합  
3. 종료

### 프로그래밍 방식 사용법

```python
from helper_functions import get_llm_response, setup_openai_client
from demo import extract_text_from_pdf_pages, create_csv_from_llm_response

# PDF에서 텍스트 추출
text = extract_text_from_pdf_pages("document.pdf", 0, 3)

# OpenAI를 사용하여 CSV 형식으로 변환
csv_data = create_csv_from_llm_response(text, 1, "reference.csv")

# 결과 저장
with open("output.csv", "w", encoding="utf-8") as f:
    f.write(csv_data)
```

### 2단 문서 처리 (한글)
```python
# OCR을 사용한 2단 문서 처리
python ocr-2column.py
```

## 🔧 주요 함수/클래스

### helper_functions.py

#### `setup_openai_client() -> OpenAI`
OpenAI 클라이언트를 설정하고 반환합니다.

**Returns:**
- `OpenAI`: 설정된 OpenAI 클라이언트 객체

**Example:**
```python
client = setup_openai_client()
```

#### `get_llm_response(prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.0) -> str`
OpenAI LLM에서 응답을 받아와 문자열로 반환합니다.

**Args:**
- `prompt (str)`: LLM에 보낼 프롬프트
- `model (str)`: 사용할 모델명 (기본값: "gpt-4o-mini")
- `temperature (float)`: 응답의 창의성 정도 (0.0-1.0, 기본값: 0.0)

**Returns:**
- `str`: LLM의 응답 텍스트

**Example:**
```python
response = get_llm_response("이 데이터를 CSV로 변환해줘")
```

#### `read_csv_as_dict(csv_file_path: str) -> Dict[int, Dict[str, Any]]`
CSV 파일을 읽어서 딕셔너리 형태로 반환합니다.

**Args:**
- `csv_file_path (str)`: 읽을 CSV 파일의 경로

**Returns:**
- `Dict[int, Dict[str, Any]]`: 행 번호를 키로 하는 딕셔너리

#### `list_files_in_directory(directory: str = '.', show_hidden: bool = False) -> List[str]`
지정된 디렉토리의 파일 목록을 반환합니다.

### demo.py

#### `extract_text_from_pdf_pages(pdf_path: str, start_page: int, end_page: int) -> str`
PDF에서 지정된 페이지 범위의 텍스트를 추출합니다.

**Args:**
- `pdf_path (str)`: PDF 파일 경로
- `start_page (int)`: 시작 페이지 (0부터 시작)
- `end_page (int)`: 끝 페이지 (포함)

**Returns:**
- `str`: 추출된 텍스트

#### `create_csv_from_llm_response(text_data: str, set_number: int, reference_csv: str = "sorted_table.csv") -> str`
추출된 텍스트를 OpenAI API를 사용하여 CSV 형식으로 변환합니다.

**Args:**
- `text_data (str)`: PDF에서 추출된 텍스트
- `set_number (int)`: 세트 번호 (1~10)
- `reference_csv (str)`: 참조할 CSV 파일 경로

**Returns:**
- `str`: CSV 형식의 문자열

#### `process_pdf_to_csv(pdf_path: str = "design_results.pdf", pages_per_set: int = 4)`
PDF 파일을 처리하여 여러 개의 CSV 파일을 생성합니다.

#### `merge_all_csv_files()`
모든 생성된 CSV 파일을 하나로 병합합니다.

## 📦 의존성

### 필수 환경변수
- `OPENAI_API_KEY`: OpenAI API 키 (필수)

### Python 패키지
- `openai>=1.51.0`: OpenAI API 클라이언트
- `python-dotenv>=1.0.1`: 환경변수 관리
- `pandas>=2.2.0`: 데이터 처리
- `PyPDF2>=3.0.1`: PDF 처리 (백업용)
- `pdfplumber>=0.11.0`: PDF 텍스트 추출 (메인)
- `pdf2image>=1.17.0`: PDF를 이미지로 변환 (OCR용)

### 시스템 요구사항
- Python 3.8 이상
- OpenAI API 액세스

## 📁 파일 구조

```
pdf-data-extractor/
├── requirements.txt          # 의존성 정의
├── .env.template            # 환경변수 템플릿
├── README.md                # 이 파일
├── helper_functions.py      # 핵심 유틸리티 함수들
├── demo.py                  # 메인 실행 파일 및 예제
├── ocr-2column.py          # 2단 문서용 OCR 처리
├── demo-pdfplumber.py      # pdfplumber 단순 테스트
├── design_results.pdf      # 샘플 PDF 파일
├── sorted_table.csv        # 참조 CSV 파일 (세트 1)
├── sorted_table_set_*.csv  # 생성된 CSV 파일들
└── merged_sorted_table.csv # 병합된 최종 파일
```

## 🔍 문서 유형별 처리 방법

### 영어 1단 문서
- **방법**: pdfplumber로 충분히 처리 가능
- **파일**: `demo.py` 사용

### 영어 2단 문서  
- **방법**: 좌우 열 구분 코딩 필요
- **파일**: `demo.py`에 추가 로직 구현 필요

### 한글 2단 문서
- **방법**: GPT-4 Vision을 사용한 OCR 처리
- **파일**: `ocr-2column.py` 사용
- **처리 과정**: PDF → 이미지 → GPT-4 Vision → 좌우 열 구분

## ⚠️ 주의사항

- OpenAI API 사용량에 따라 비용이 발생할 수 있습니다
- 첫 번째 세트(`sorted_table.csv`)는 수동으로 작성된 참조 파일로 가정합니다
- PDF 파일의 텍스트 추출이 어려운 경우 수동 검토가 필요할 수 있습니다
- 대용량 PDF 처리 시 메모리 사용량에 주의하세요
- API 응답 시간에 따라 처리 시간이 길어질 수 있습니다

## 🚀 빠른 시작 예제

```python
# 1. 환경 설정
from dotenv import load_dotenv
load_dotenv()

# 2. PDF 처리
from demo import process_pdf_to_csv
process_pdf_to_csv("your_document.pdf", pages_per_set=4)

# 3. 결과 병합
from demo import merge_all_csv_files
merge_all_csv_files()

print("처리 완료! merged_sorted_table.csv 파일을 확인하세요.")
```