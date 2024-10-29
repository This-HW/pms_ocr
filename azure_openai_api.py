from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials


# Azure Computer Vision 리소스 키와 엔드포인트
subscription_key = "YOUR_COMPUTER_VISION_SUBSCRIPTION_KEY"
endpoint = "YOUR_COMPUTER_VISION_ENDPOINT"

# Computer Vision 클라이언트 생성
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# 이미지 파일 경로 또는 URL
image_path = "local_path_to_image.jpg"


# 로컬 이미지 파일을 열고 텍스트 추출
def extract_text_from_image(image_path):
    # 이미지 열기
    with open(image_path, "rb") as image_stream:
        # OCR 텍스트 추출
        ocr_result = computervision_client.recognize_printed_text_in_stream(image_stream)

    # 결과 출력
    for region in ocr_result.regions:
        for line in region.lines:
            print(" ".join([word.text for word in line.words]))


# 이미지에서 텍스트 추출 실행
extract_text_from_image(image_path)