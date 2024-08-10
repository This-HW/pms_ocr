"""
    오픈소스를 통해 글자 추출
    글자 추출이 되는 편이지만 서비스로 사용하기에는 쉽지 않을 것으로 파악됨
"""
import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageOps
import re

# Tesseract 경로 설정 (필요한 경우)
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'  # 필요에 따라 경로 조정

# 이미지 로드
image_path = './images/contract1.jpeg'
image = Image.open(image_path)

# 이미지 크기 조정 (2배로 확대)
image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)

# 그레이스케일 변환
image = image.convert('L')

# # 이진화 (Thresholding)
# image = image.point(lambda x: 0 if x < 128 else 255, '1')

# 이미지 노이즈 제거 (Gaussian 블러 사용)
# 이미지를 OpenCV 형식으로 변환 (이미 그레이스케일이므로 2차원 배열로 변환됨)
open_cv_image = np.array(image)

# 이진화된 이미지의 타입을 uint8로 변환
open_cv_image = open_cv_image.astype(np.uint8)

# Gaussian 블러 적용
open_cv_image = cv2.GaussianBlur(open_cv_image, (5, 5), 0)

# 다시 PIL 이미지로 변환 (그레이스케일이므로 바로 변환 가능)
image = Image.fromarray(open_cv_image)

# Tesseract 설정 (화이트리스트 옵션 제거)
custom_config = r'--oem 3 --psm 6'

# OCR 수행
text = pytesseract.image_to_string(image, lang='kor', config=custom_config)

# 결과 출력
# print(text)



# 추출된 텍스트 (위 코드의 결과를 text 변수로 저장)
# text = """
# (여기에 위에서 추출된 텍스트를 넣으세요)
# """

# 정규 표현식을 사용하여 필요한 정보 파싱
sojaeji = re.search(r'소재지[^\n]*\n[^\n]*', text)
imdae_myeonjeok = re.search(r'임대 면적[^\n]*\n[^\n]*', text)
bojeonggeum = re.search(r'보증금[^\n]*\n[^\n]*', text)
gyeyakgeum = re.search(r'계약금[^\n]*\n[^\n]*', text)
janggeum = re.search(r'잔금[^\n]*\n[^\n]*', text)
wolse = re.search(r'월세[^\n]*\n[^\n]*', text)

# 추출된 정보를 깔끔하게 출력
print(f"소재지: {sojaeji.group() if sojaeji else '정보 없음'}")
print(f"임대 면적: {imdae_myeonjeok.group() if imdae_myeonjeok else '정보 없음'}")
print(f"보증금: {bojeonggeum.group() if bojeonggeum else '정보 없음'}")
print(f"계약금: {gyeyakgeum.group() if gyeyakgeum else '정보 없음'}")
print(f"잔금: {janggeum.group() if janggeum else '정보 없음'}")
print(f"월세: {wolse.group() if wolse else '정보 없음'}")