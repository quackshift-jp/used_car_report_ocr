import os
from dotenv import load_dotenv
from google.cloud import documentai_v1 as documentai

load_dotenv(verbose=True)

PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION")
PROCESSOR_ID = os.environ.get("PROCESSOR_ID")


def process_document(
    project_id: str, location: str, processor_id: str, file_path: str, mime_type: str
) -> documentai.Document:
    documentai_client = documentai.DocumentProcessorServiceClient()
    resource_name = documentai_client.processor_path(project_id, location, processor_id)
    with open(file_path, "rb") as image:
        image_content = image.read()
        raw_document = documentai.RawDocument(
            content=image_content, mime_type=mime_type
        )
        request = documentai.ProcessRequest(
            name=resource_name, raw_document=raw_document
        )
        result = documentai_client.process_document(request=request)
        return result.document


response = process_document(
    project_id=PROJECT_ID,
    location=LOCATION,
    processor_id=PROCESSOR_ID,
    file_path="data/sample.pdf",
    mime_type="application/pdf",
)
