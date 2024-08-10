"""
    opencv를 사용해서 사각형을 검출하고 그 안의 글자 추출 테스트
    너무 작은 사각형만 인식되는 문제 확인
"""

import cv2
import numpy as np
import pytesseract

# 이미지 불러오기
image_path = 'images/contract1.jpeg'
img = cv2.imread(image_path)

# # 그레이스케일로 변환
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 블러링을 적용하여 노이즈 제거
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# blurred = cv2.GaussianBlur(img, (1, 1), 0)

# 엣지 검출 (Canny Edge Detection)
# edged = cv2.Canny(blurred, 50, 200)
edged = cv2.Canny(img, 50, 200)

# 엣지 이미지를 확인해보고 싶다면 주석을 해제하세요
# cv2.imshow("Edged Image", edged)
# cv2.waitKey(0)


# 윤곽선 찾기
contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 윤곽선을 사각형으로 근사화하여 네모칸 찾기
rects = []
for contour in contours:
    # 각 윤곽선을 사각형으로 근사화
    approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

    # 네모칸인지 확인 (4개의 꼭지점이 있는 경우)
    if len(approx) == 4:
        rects.append(approx)

# 감지된 네모칸 확인
print(f"Detected {len(rects)} rectangular contours.")

for rect in rects:
    # 사각형의 좌표를 찾음
    x, y, w, h = cv2.boundingRect(rect)

    # 이미지에서 사각형 영역을 잘라냄
    cropped_img = img[y:y + h, x:x + w]

    # 잘라낸 이미지에서 텍스트 추출
    text = pytesseract.image_to_string(cropped_img, lang='kor')

    print(f"Extracted text from a rectangle:\n{text}")

# 사각형을 이미지에 그려서 확인 (디버깅용)
for rect in rects:
    cv2.drawContours(img, [rect], -1, (0, 255, 0), 2)

# 결과 이미지 표시
cv2.imshow("Detected Rectangles", img)
cv2.waitKey(0)
cv2.destroyAllWindows()