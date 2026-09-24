import os
from docling.document_converter import DocumentConverter

PDF_FOLDER = "downloads/pdfs"

pdf_files = [
    f for f in os.listdir(PDF_FOLDER)
    if f.lower().endswith(".pdf")
]

if not pdf_files:
    raise FileNotFoundError("No PDF files found!")

pdf_path = os.path.join(PDF_FOLDER, pdf_files[0])

print("Testing:", pdf_path)

converter = DocumentConverter()

result = converter.convert(pdf_path)

document = result.document

print(document.export_to_markdown())