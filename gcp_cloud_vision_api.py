"""
    구글 Vision API 사용
    글자 추출 가장 잘 되지만, 원하는 항목의 수치를 가져오는 방법 확인 필요
"""
import os
from google.cloud import vision
from dotenv import load_dotenv

load_dotenv()
GCP_CREDENTIAL_PATH = os.getenv('gcp_credential_path')

# 환경 변수 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCP_CREDENTIAL_PATH

def extract_text_from_image(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # 전체 텍스트 추출
    full_text = texts[0].description
    print('Full Text:', full_text)

    # 항목별로 파싱 (예: 계약서 항목)
    # 아래 예제는 특정 패턴을 기반으로 간단히 나눈 예시
    lines = full_text.split('\n')
    contract_data = {}
    for line in lines:
        if '소재지' in line:
            contract_data['소재지'] = line.split(':')[-1].strip()
        elif '면적' in line:
            contract_data['면적'] = line.split(':')[-1].strip()
        elif '중도금' in line:
            contract_data['중도금'] = line.split(':')[-1].strip()
        elif '잔금' in line:
            contract_data['잔금'] = line.split(':')[-1].strip()
        # 필요에 따라 추가 항목을 처리

    return contract_data

# 예제 실행
image_path = './images/contract1.jpeg'
data = extract_text_from_image(image_path)
print('Extracted Data:', data)