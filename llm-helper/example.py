"""
OpenAI API 연결 모듈 사용 예제

이 파일은 core.py의 함수들을 실제로 사용하는 방법을 보여줍니다.
실행하기 전에 .env 파일에 OPENAI_API_KEY를 설정해야 합니다.
"""

from core import (
    get_llm_response, 
    print_llm_response,
    list_files_in_directory,
    print_files_in_directory,
    read_csv_as_dict
)


def main():
    """메인 실행 함수"""
    
    print("=== OpenAI API 연결 모듈 사용 예제 ===\n")
    
    # 예제 1: 간단한 질문과 답변
    print("1. 간단한 LLM 응답 출력:")
    try:
        print_llm_response("Python의 주요 특징 3가지를 간단히 알려줘")
    except Exception as e:
        print(f"오류: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 예제 2: 응답을 변수에 저장
    print("2. LLM 응답을 변수에 저장:")
    try:
        response = get_llm_response("데이터 과학에서 가장 중요한 것은?")
        print(f"LLM 응답: {response}")
    except Exception as e:
        print(f"오류: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 예제 3: 변수를 활용한 프롬프트 (f-string 사용)
    print("3. 변수를 활용한 프롬프트 예제:")
    try:
        topic = "머신러닝"
        level = "초보자"
        prompt = f"""{topic}에 대해 {level}가 이해할 수 있도록 
        핵심 개념 3가지를 간단히 설명해줘"""
        
        print(f"사용된 프롬프트: {prompt}")
        print("="*30)
        print_llm_response(prompt)
    except Exception as e:
        print(f"오류: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 예제 4: 다양한 모델과 temperature 사용
    print("4. 다른 설정으로 LLM 호출:")
    try:
        creative_response = get_llm_response(
            "창의적인 아이디어를 하나 제안해줘", 
            temperature=0.7
        )
        print(f"창의적인 응답 (temperature=0.7): {creative_response}")
    except Exception as e:
        print(f"오류: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 예제 5: 현재 디렉토리 파일 목록
    print("5. 현재 디렉토리의 파일 목록:")
    try:
        files = list_files_in_directory()
        print(f"파일 개수: {len(files)}")
        print("파일 목록:")
        for file in files:
            print(f"  - {file}")
    except Exception as e:
        print(f"오류: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 예제 6: CSV 파일 읽기 (파일이 있는 경우)
    print("6. CSV 파일 읽기 예제:")
    csv_file = "sample_data.csv"
    try:
        # 실제 CSV 파일이 있다면 읽어서 출력
        data = read_csv_as_dict(csv_file)
        print(f"CSV 데이터 읽기 성공: {len(data)}행")
        if data:
            print("첫 번째 행 데이터:")
            print(data[0])
    except FileNotFoundError:
        print(f"'{csv_file}' 파일이 없습니다. CSV 예제를 건너뜁니다.")
    except Exception as e:
        print(f"CSV 읽기 오류: {e}")
    
    print("\n=== 예제 실행 완료 ===")


def interactive_mode():
    """대화형 모드 - 사용자 입력을 받아 LLM에 질문"""
    
    print("\n=== 대화형 모드 ===")
    print("질문을 입력하세요 ('quit' 입력시 종료):")
    
    while True:
        try:
            user_input = input("\n질문: ").strip()
            
            if user_input.lower() in ['quit', '종료', 'exit']:
                print("대화형 모드를 종료합니다.")
                break
            
            if not user_input:
                print("질문을 입력해주세요.")
                continue
            
            print("\nLLM 응답:")
            print_llm_response(user_input)
            
        except KeyboardInterrupt:
            print("\n\n대화형 모드를 종료합니다.")
            break
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")


if __name__ == "__main__":
    # 기본 예제 실행
    main()
    
    # 대화형 모드 실행 여부 묻기
    try:
        response = input("\n대화형 모드를 실행하시겠습니까? (y/n): ").strip().lower()
        if response in ['y', 'yes', '예', 'ㅇ']:
            interactive_mode()
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.") 