import os
# from google.cloud import documentai_v1beta3 as documentai
# from google.cloud.documentai_v1beta3 import types
from google.cloud import documentai
from pydotenv import Environment
from google.api_core.client_options import ClientOptions

# 서비스 계정 키 파일 경로 설정
env = Environment()
GCP_CREDENTIAL_PATH = env.get('gcp_credential_path')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCP_CREDENTIAL_PATH

# Document AI 클라이언트 초기화
client = documentai.DocumentProcessorServiceClient()


def process_document(project_id, location, processor_id, file_path):
    # 파일 읽기
    with open(file_path, "rb") as document_file:
        document_content = document_file.read()

    # Google Cloud Processor 정보 설정
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    # 문서 유형 및 파일 설정
    raw_document = documentai.RawDocument(content=document_content, mime_type="application/pdf")

    # 요청 생성
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    # Document AI로 요청 전송
    result = client.process_document(request=request)

    # 결과 처리
    document = result.document
    print("Document processing complete.\n")

    # 각 페이지에서 추출된 텍스트를 출력
    for page in document.pages:
        for form_field in page.form_fields:
            field_name = get_text(form_field.field_name, document)
            field_value = get_text(form_field.field_value, document)
            print(f"Field name: {field_name}, Field value: {field_value}")


def get_text(doc_element, document):
    """Helper function to extract text from a Document element."""
    response = ''
    for segment in doc_element.text_anchor.text_segments:
        start_index = int(segment.start_index) if segment.start_index else 0
        end_index = int(segment.end_index)
        response += document.text[start_index:end_index]

    return response


def list_processors_sample(project_id: str, location: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location
    parent = client.common_location_path(project_id, location)

    # Make ListProcessors request
    processor_list = client.list_processors(parent=parent)

    # Print the processor information
    for processor in processor_list:
        print(f"Processor Name: {processor.name}")
        print(f"Processor Display Name: {processor.display_name}")
        print(f"Processor Type: {processor.type_}")
        print("")


def main():
    # 프로젝트 및 프로세서 정보 설정
    project_id = 'amore-marketing-tech'
    location = 'us'  # 예: 'us' 또는 'eu'
    processor_id = '4c791e6a10d26877'  # Document AI의 프로세서 ID

    # 계약서 파일 경로
    file_path = './images/contract1.pdf'

    # Document AI 프로세서 리스트 조회
    # list_processors_sample(project_id, location)

    # 문서 처리 시작
    process_document(project_id, location, processor_id, file_path)


if __name__ == '__main__':
    main()
