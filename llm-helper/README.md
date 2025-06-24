# OpenAI API 연결 모듈

OpenAI API와의 상호작용을 위한 유틸리티 함수들을 제공하는 모듈입니다. LLM 응답 생성, CSV 파일 읽기, 파일 목록 조회 등의 기능을 포함합니다.

## 🚀 주요 기능

- **LLM 응답 생성**: OpenAI GPT 모델을 사용한 텍스트 생성
- **CSV 데이터 처리**: CSV 파일을 딕셔너리 형태로 읽기
- **파일 관리**: 디렉토리 내 파일 목록 조회
- **환경변수 관리**: .env 파일을 통한 API 키 관리

## 📦 설치 방법

1. 필요한 의존성 설치:
```bash
pip install -r requirements.txt
```

2. 환경변수 설정:
```bash
cp .env.template .env
# .env 파일을 편집하여 실제 OpenAI API 키를 입력
```

## 🔧 사용법

### 기본 사용 예제

```python
from core import get_llm_response, print_llm_response

# LLM 응답을 바로 출력
print_llm_response("Python의 장점을 알려줘")

# LLM 응답을 변수에 저장
response = get_llm_response("데이터 분석에 대해 설명해줘")
print(response)
```

### CSV 파일 읽기

```python
from core import read_csv_as_dict

# CSV 파일을 딕셔너리로 읽기
data = read_csv_as_dict("sample.csv")
print(data[0])  # 첫 번째 행 출력
```

### 파일 목록 조회

```python
from core import list_files_in_directory

# 현재 디렉토리의 파일 목록
files = list_files_in_directory()
for file in files:
    print(file)
```

## 🎯 주요 함수

### `get_llm_response(prompt, model="gpt-4o-mini", temperature=0.0)`
- OpenAI LLM에서 응답을 받아와 문자열로 반환
- **매개변수**:
  - `prompt`: LLM에 보낼 질문/지시사항
  - `model`: 사용할 OpenAI 모델 (기본값: "gpt-4o-mini")
  - `temperature`: 창의성 정도 (0.0-1.0, 기본값: 0.0)

### `print_llm_response(prompt, model="gpt-4o-mini", temperature=0.0)`
- LLM 응답을 즉시 출력
- 매개변수는 `get_llm_response()`와 동일

### `read_csv_as_dict(csv_file_path)`
- CSV 파일을 행 번호를 키로 하는 딕셔너리로 변환
- **매개변수**: `csv_file_path` - 읽을 CSV 파일 경로

### `list_files_in_directory(directory=".", show_hidden=False)`
- 지정된 디렉토리의 파일 목록을 반환
- **매개변수**:
  - `directory`: 조회할 디렉토리 경로 (기본값: 현재 디렉토리)
  - `show_hidden`: 숨김 파일 포함 여부 (기본값: False)

## 🏃‍♂️ 실행 예제

완전한 사용 예제를 보려면:
```bash
python example.py
```

대화형 모드로 실행하여 직접 질문해볼 수 있습니다.

## 🔒 환경변수

`.env` 파일에 다음 항목이 필요합니다:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## 📋 의존성

- `openai==1.51.0`: OpenAI API 클라이언트
- `python-dotenv==1.0.0`: 환경변수 관리
- `pandas>=2.0.0`: 데이터 처리 (확장 기능용)
- `httpx==0.24.1`: HTTP 클라이언트 (OpenAI 호환성 보장)

## 🚨 주의사항

- OpenAI API 키가 필요합니다 (.env 파일에 설정)
- API 호출은 비용이 발생할 수 있습니다
- 네트워크 연결이 필요합니다
- CSV 파일은 UTF-8 인코딩을 사용해야 합니다

## 🔄 다른 프로젝트에서 사용

이 폴더를 다른 프로젝트로 복사하여 사용:

1. 폴더 전체 복사:
```bash
cp -r openai-api-connect /path/to/your/project/
```

2. 의존성 설치:
```bash
cd /path/to/your/project/openai-api-connect
pip install -r requirements.txt
```

3. 환경변수 설정 후 바로 사용 가능 