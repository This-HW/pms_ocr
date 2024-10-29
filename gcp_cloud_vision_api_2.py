import io
import os
from google.cloud import vision
from dotenv import load_dotenv

load_dotenv()
GCP_CREDENTIAL_PATH = os.getenv('gcp_credential_path')

# 서비스 계정 키 파일 경로 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCP_CREDENTIAL_PATH

# Google Cloud Vision 클라이언트 초기화
client = vision.ImageAnnotatorClient()

# 이미지 파일을 열어 Vision API에 전달할 준비
def detect_text(image_path):
    """Detects text in the file."""
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # OCR을 수행하여 텍스트 추출
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # 추출된 텍스트 출력
    print('Texts:')
    for text in texts:
        print(f'\n"{text.description}"')

    if response.error.message:
        raise Exception(f'{response.error.message}')

# 이미지 파일 경로 지정
image_path = './images/contract1.jpeg'

# 텍스트 추출 함수 호출
detect_text(image_path)