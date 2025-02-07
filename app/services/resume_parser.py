import fitz
from io import BytesIO


def extract_text_from_pdf(file_content):
    file_stream = BytesIO(file_content)
    resume_text = ""

    pdf_document = fitz.open(stream=file_stream.read(), filetype="pdf")
    for page in pdf_document:
        resume_text += page.get_text()

    return resume_text.strip()