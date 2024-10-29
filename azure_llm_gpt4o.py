import os
import requests
import base64
from dotenv import load_dotenv
import os


# Configuration
load_dotenv()  # .env 파일 로드
API_KEY = os.getenv('AZURE_API_KEY')

IMAGE_PATH = "./images/"  # POC Path
IMAGE_1 = IMAGE_PATH+"상가건물 임대차 표준계약서_1_page-0001.jpg"  # POC Image
IMAGE_2 = IMAGE_PATH+"상가건물 임대차 표준계약서_1_page-0002.jpg"  # POC Image
encoded_image_1 = base64.b64encode(open(IMAGE_1, 'rb').read()).decode('ascii')
encoded_image_2 = base64.b64encode(open(IMAGE_2, 'rb').read()).decode('ascii')
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}
ENDPOINT = os.getenv('AZURE_ENDPOINT')


# Payload for the request
# Payload for the request
payload = {
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "너는 한국의 부동산과 관련된 문서들의 글자들을 추출하는 역할을 수행할거야.\n이번에는 임대차 계약서와 관련된 글자를 추출해줘.\n임대차계약서는 테이블과 글자가 혼합되어 있는 형태로 한국어와 숫자 등으로 이루어진 문서야.\n그 문서에서 각 항목 및 기준에 맞춰 텍스트, 숫자, 날짜와 같은 값들을 추출해줘.\n\n추출해야하는 주요 지표들은 아래와 같아.\n['소재지','임대차시작일','임대차종료일','계약체결일','계약적용일', '총보증금액','계약금','중도금','잔금','임대료(월세)','임대료납부주기','임대료납부일']\n만약 주요 지표들이 숫자가 아니라 한글로 적혀있다면 그 한글을 숫자로 변환해서 적어주고 숫자와 한글이 동시에 있다면 같은 의미를 나타내고 있는지 확인하고 같다면 그 숫자를 표기하고 다르다면 숫자를 추출해줘.\n금액과 관련된 지표들은 '원' 단위는 필요없고 딱 숫자만 추출해줘.\n날짜와 관련된 지표들은 'yyyy-mm-dd' 형식으로 추출해줘.\n임대료 납부 주기는 '월 납부','분기별 납부', '반기별 납부', '연별 납부' 이 중에서 동일하거나 가장 비슷한 의미의 값으로 추출해줘.\n임대료 납부일은 매달 몇일에 납부하는지 일자만 숫자로 추출해줘.\n만약 구하기로 한 수치들 중에서 정확히 구하기 어려운 수치가 있다면 공란으로 비워줘.\n\n최종 답변의 형식은 json이야."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "\n"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{encoded_image_1}"
          }
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{encoded_image_2}"
          }
        }
      ]
    }
  ],
  "temperature": 0.5,
  "top_p": 0.95,
  "max_tokens": 800,
  "response_format": {
    "type": "json_object"
  }
}

# Send request
try:
    response = requests.post(ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
except requests.RequestException as e:
    raise SystemExit(f"Failed to make the request. Error: {e}")

# JSON 문자열 추출 및 파싱
if response is not None:
    response_json = response.json()
    message_content = response_json['choices'][0]['message']['content']
    # message_content = json.loads(message_content_str)  # JSON 문자열을 Python 딕셔너리로 변환

    # message_content 출력 (확인용)
    print("수집된 데이터:\n",message_content)

else:
    print("수집된 데이터가 없습니다.")