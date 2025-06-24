"""
OpenAI API 연결 및 유틸리티 함수들

이 모듈은 OpenAI API와의 상호작용을 위한 핵심 함수들을 제공합니다.
CSV 파일 읽기, LLM 응답 생성, 파일 목록 조회 등의 기능을 포함합니다.
"""

import os
import csv
from typing import Dict, List, Optional, Any
from openai import OpenAI
from dotenv import load_dotenv

# 환경변수 로드 - 현재 스크립트 파일과 같은 디렉토리에서 .env 파일 찾기
script_dir = os.path.dirname(os.path.abspath(__file__)) # 현재 실행되는 파일의 절대경로 중 dirname 추출
env_path = os.path.join(script_dir, '.env') # 위에서 찾은 절대경로안에 있는 .env 파일 경로 제작
load_dotenv(env_path, override=True) # 환경변수 로드


def setup_openai_client() -> OpenAI:
    """
    OpenAI 클라이언트를 설정하고 반환합니다.
    
    Returns:
        OpenAI: 설정된 OpenAI 클라이언트 객체
        
    Raises:
        ValueError: API 키가 설정되지 않은 경우
        
    Example:
        >>> client = setup_openai_client()
        >>> # 클라이언트 사용 가능
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY가 .env 파일에 설정되지 않았습니다.")
    
    return OpenAI(api_key=api_key)


def read_csv_as_dict(csv_file_path: str) -> Dict[int, Dict[str, Any]]:
    """
    CSV 파일을 읽어서 딕셔너리 형태로 반환합니다.
    
    Args:
        csv_file_path (str): 읽을 CSV 파일의 경로
        
    Returns:
        Dict[int, Dict[str, Any]]: 행 번호를 키로 하는 딕셔너리
        
    Raises:
        FileNotFoundError: 파일이 존재하지 않는 경우
        csv.Error: CSV 파일 형식이 잘못된 경우
        
    Example:
        >>> data = read_csv_as_dict("data.csv")
        >>> print(data[0])  # 첫 번째 행 출력
        {'name': 'John', 'age': '25'}
    """
    try:
        data_list = []
        
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data_list.append(row)
        
        return {i: data_list[i] for i in range(len(data_list))}
    
    except FileNotFoundError:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {csv_file_path}")
    except csv.Error as e:
        raise csv.Error(f"CSV 파일 읽기 오류: {e}")


def get_llm_response(prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.0) -> str:
    """
    OpenAI LLM에서 응답을 받아와 문자열로 반환합니다.
    
    Args:
        prompt (str): LLM에 보낼 프롬프트
        model (str): 사용할 모델명 (기본값: "gpt-4o-mini")
        temperature (float): 응답의 창의성 정도 (0.0-1.0, 기본값: 0.0)
        
    Returns:
        str: LLM의 응답 텍스트
        
    Raises:
        ValueError: 프롬프트가 문자열이 아닌 경우
        Exception: OpenAI API 호출 실패 시
        
    Example:
        >>> response = get_llm_response("Python에 대해 간단히 설명해줘")
        >>> print(response)
        "Python은 간단하고 읽기 쉬운 프로그래밍 언어입니다..."
    """
    if not isinstance(prompt, str):
        raise ValueError("프롬프트는 문자열이어야 합니다.")
    
    try:
        client = setup_openai_client()
        
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "당신은 도움이 되지만 간결한 AI 어시스턴트로, 핵심만 간단명료하게 답변합니다.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        
        return completion.choices[0].message.content
    
    except Exception as e:
        raise Exception(f"OpenAI API 호출 중 오류 발생: {e}")


def print_llm_response(prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.0) -> None:
    """
    OpenAI LLM에서 응답을 받아와 즉시 출력합니다.
    
    Args:
        prompt (str): LLM에 보낼 프롬프트
        model (str): 사용할 모델명 (기본값: "gpt-4o-mini")
        temperature (float): 응답의 창의성 정도 (0.0-1.0, 기본값: 0.0)
        
    Example:
        >>> print_llm_response("안녕하세요, 누구세요?")
        저는 도움이 되는 AI 어시스턴트입니다.
    """
    try:
        response = get_llm_response(prompt, model, temperature)
        print(response)
    except Exception as e:
        print(f"오류: {e}")


def list_files_in_directory(directory: str = '.', show_hidden: bool = False) -> List[str]:
    """
    지정된 디렉토리의 파일 목록을 반환합니다.
    
    Args:
        directory (str): 파일을 나열할 디렉토리 경로 (기본값: 현재 디렉토리)
        show_hidden (bool): 숨김 파일 포함 여부 (기본값: False)
        
    Returns:
        List[str]: 파일명 목록
        
    Raises:
        FileNotFoundError: 디렉토리가 존재하지 않는 경우
        PermissionError: 디렉토리 접근 권한이 없는 경우
        
    Example:
        >>> files = list_files_in_directory("./data")
        >>> print(files)
        ['file1.txt', 'file2.csv', 'image.png']
    """
    try:
        all_items = os.listdir(directory)
        
        if show_hidden:
            files = [f for f in all_items if os.path.isfile(os.path.join(directory, f))]
        else:
            files = [f for f in all_items 
                    if (not f.startswith('.') and not f.startswith('_') 
                        and os.path.isfile(os.path.join(directory, f)))]
        
        return files
    
    except FileNotFoundError:
        raise FileNotFoundError(f"디렉토리를 찾을 수 없습니다: {directory}")
    except PermissionError:
        raise PermissionError(f"디렉토리 접근 권한이 없습니다: {directory}")


def print_files_in_directory(directory: str = '.', show_hidden: bool = False) -> None:
    """
    지정된 디렉토리의 파일 목록을 출력합니다.
    
    Args:
        directory (str): 파일을 나열할 디렉토리 경로 (기본값: 현재 디렉토리)
        show_hidden (bool): 숨김 파일 포함 여부 (기본값: False)
        
    Example:
        >>> print_files_in_directory("./data")
        file1.txt
        file2.csv
        image.png
    """
    try:
        files = list_files_in_directory(directory, show_hidden)
        for file in files:
            print(file)
    except Exception as e:
        print(f"오류: {e}") 