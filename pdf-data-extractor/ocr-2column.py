# ocr_2column_pdf_openai.py

import base64
import openai
from pdf2image import convert_from_path
import os
from dotenv import load_dotenv


# 1. PDF를 이미지로 변환
pdf_path = "test-pdf3.pdf"
pages = convert_from_path(pdf_path, dpi=300)

# 2. 첫 페이지만 예시로 처리 (여러 페이지면 for문 사용)
page_image = pages[1]
image_path = "page2.png"
page_image.save(image_path, "PNG")

# 3. 이미지 파일을 base64로 인코딩
with open(image_path, "rb") as img_file:
    b64_image = base64.b64encode(img_file.read()).decode("utf-8")
    image_data_url = f"data:image/png;base64,{b64_image}"

# 4. OpenAI Vision API 호출
script_dir = os.path.dirname(os.path.abspath(__file__)) # 현재 실행되는 파일의 절대경로 중 dirname 추출
env_path = os.path.join(script_dir, '.env') # 위에서 찾은 절대경로안에 있는 .env 파일 경로 제작
load_dotenv(env_path, override=True) # 환경변수 로드

prompt = (
    "이 이미지는 2단(2-column)으로 되어 있습니다. "
    "왼쪽 열부터 오른쪽 열 순서로 모든 텍스트를 정확하게 추출해 주세요. "
    "표, 각주 등도 모두 포함해 주세요."
)

response = openai.chat.completions.create(
    model="gpt-4.1",  # 또는 "gpt-4-vision-preview"
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_data_url}}
            ]
        }
    ],
    max_tokens=4096
)

print(response.choices[0].message.content)
