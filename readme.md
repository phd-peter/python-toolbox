# 🧰 Python Toolbox

파이썬 개발에서 자주 사용되는 재사용 가능한 코드 스니펫들을 체계적으로 정리한 도구상자입니다. 각 폴더는 완전히 독립적으로 작동하며, 다른 프로젝트에서 복사하여 즉시 사용할 수 있도록 설계되었습니다.

## 📋 프로젝트 목적

- **재사용성**: 검증된 코드 스니펫을 다른 프로젝트에서 바로 활용
- **독립성**: 각 모듈은 서로 의존하지 않고 독립적으로 작동
- **완결성**: 모든 폴더는 즉시 실행 가능한 완전한 패키지
- **문서화**: 명확한 사용법과 API 문서 제공

## 🏗️ 프로젝트 구조

```
python-toolbox/
├── llm-helper/              # OpenAI API 연결 및 LLM 상호작용 도구
├── pdf-data-extractor/      # PDF 파일에서 구조적 데이터 추출 도구
├── python-setting/          # Python 환경 설정 가이드
└── venv/                    # 가상환경 (Git에서 제외됨)
```

## 📦 모듈별 상세 설명

### 🤖 llm-helper
**OpenAI API 연결 모듈**

- **주요 기능**: OpenAI GPT 모델과의 상호작용, CSV 파일 처리, 파일 관리
- **핵심 파일**: `core.py`, `example.py`, `requirements.txt`
- **사용 예시**: 
  ```python
  from core import get_llm_response
  response = get_llm_response("Python의 장점을 알려줘")
  ```
- **의존성**: `openai`, `python-dotenv`, `pandas`, `httpx`

### 📄 pdf-data-extractor
**PDF 데이터 추출기**

- **주요 기능**: PDF 텍스트 추출, OpenAI를 통한 구조화, CSV 변환, OCR 지원
- **핵심 파일**: `demo.py`, `helper_functions.py`, `ocr-2column.py`
- **사용 예시**:
  ```python
  from demo import process_pdf_to_csv
  process_pdf_to_csv("document.pdf", pages_per_set=4)
  ```
- **의존성**: `openai`, `pdfplumber`, `PyPDF2`, `pandas`, `pdf2image`

### ⚙️ python-setting
**Python 환경 설정 가이드**

- **주요 기능**: 가상환경 설정, VS Code 연동, 패키지 관리 가이드
- **핵심 파일**: `venv설정.md`
- **내용**: 가상환경 생성/활성화, IDE 연동, 패키지 관리 모범 사례

## 🚀 빠른 시작

### 1. 특정 모듈 사용하기

원하는 모듈을 새 프로젝트로 복사:

```bash
# llm-helper 모듈 복사
cp -r python-toolbox/llm-helper ./my-project/

# pdf-data-extractor 모듈 복사
cp -r python-toolbox/pdf-data-extractor ./my-project/
```

### 2. 환경 설정

```bash
cd my-project/module-name
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 환경변수 설정 (필요시)

```bash
cp .env.template .env
# .env 파일을 편집하여 실제 값 입력
```

### 4. 즉시 사용 가능!

```python
# 각 모듈의 example.py나 demo.py 실행
python example.py
python demo.py
```

## 📚 폴더별 독립성 원칙

### ✅ 각 폴더가 포함해야 하는 필수 파일들

```
module-name/
├── requirements.txt      # 의존성 정의 (버전 고정)
├── README.md            # 상세한 사용법과 API 문서
├── core.py 또는 demo.py  # 핵심 기능 구현
├── example.py           # 실행 가능한 사용 예제
└── .env.template        # 환경변수 템플릿 (필요시)
```

### 🔒 독립성 보장 규칙

- **절대 경로 금지**: 상대 경로만 사용
- **폴더 간 의존성 금지**: 다른 폴더의 코드를 import하지 않음
- **자체 완결성**: 각 폴더는 모든 필요한 파일을 포함
- **환경 독립성**: 프로젝트 루트에 의존하지 않음

## 🛠️ 개발 가이드라인

### 새 모듈 추가 시

1. **폴더 생성**: 소문자와 하이픈 사용 (`new-module`)
2. **필수 파일 생성**: `requirements.txt`, `README.md`, 핵심 코드 파일
3. **문서화**: 모든 함수에 docstring과 타입 힌트 추가
4. **예제 제공**: 실행 가능한 example.py 파일 생성
5. **독립성 검증**: 다른 폴더 없이도 실행되는지 확인

### 코딩 스타일

```python
def function_name(param: type) -> return_type:
    """
    함수의 목적과 기능을 명확히 설명
    
    Args:
        param (type): 매개변수 설명
        
    Returns:
        return_type: 반환값 설명
        
    Example:
        >>> result = function_name("test")
        >>> print(result)
        "Expected output"
    """
    # 구현 코드
    pass
```

## 📋 현재 모듈 상태

| 모듈 | 상태 | 주요 기능 | 환경변수 필요 |
|------|------|-----------|---------------|
| `llm-helper` | ✅ 완료 | OpenAI API 연결, CSV 처리 | `OPENAI_API_KEY` |
| `pdf-data-extractor` | ✅ 완료 | PDF → CSV 변환, OCR | `OPENAI_API_KEY` |
| `python-setting` | ✅ 완료 | 환경 설정 가이드 | 없음 |

## 🔄 사용 워크플로우

### 개발자 관점
1. 필요한 기능의 모듈 선택
2. 해당 폴더를 새 프로젝트로 복사
3. 가상환경 설정 및 의존성 설치
4. 환경변수 설정 (필요시)
5. 바로 사용 시작

### 기여자 관점
1. 새로운 유용한 코드 스니펫 발견
2. 독립적인 모듈로 패키징
3. 완전한 문서화 및 예제 제공
4. 독립성 검증 후 추가

## ⚠️ 주의사항

- **API 키 보안**: `.env` 파일은 절대 Git에 커밋하지 않기
- **의존성 관리**: 각 모듈마다 별도의 `requirements.txt` 사용
- **버전 호환성**: 의존성 버전을 명시하여 호환성 보장
- **테스트**: 새 환경에서 모듈이 정상 작동하는지 확인

## 📞 문의 및 기여

이 프로젝트는 실용적인 Python 개발을 위한 도구상자입니다. 새로운 모듈 제안이나 기존 모듈 개선사항이 있다면 언제든지 기여해주세요!

### 기여하기
1. 독립성 원칙 준수
2. 완전한 문서화
3. 실행 가능한 예제 제공
4. 타입 힌트 및 에러 처리 포함

---

**🎯 목표**: 파이썬 개발 시 "바퀴를 다시 발명하지 않고" 검증된 코드를 즉시 활용할 수 있는 실용적인 도구상자 구축 