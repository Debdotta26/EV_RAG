# import os


# def extract_metadata(doc, pdf_path):
#     """
#     Extract metadata from a PDF document.
#     """

#     info = doc.metadata

#     metadata = {
#         "document_name": os.path.basename(pdf_path),
#         "title": info.get("title", ""),
#         "author": info.get("author", ""),
#         "creator": info.get("creator", ""),
#         "producer": info.get("producer", ""),
#         "subject": info.get("subject", ""),
#         "keywords": info.get("keywords", ""),
#         "creation_date": info.get("creationDate", ""),
#         "modification_date": info.get("modDate", ""),
#         "total_pages": len(doc)
#     }

#     return metadata

import os
from datetime import datetime


def extract_metadata(doc, pdf_path):
    """
    Extract metadata from a PDF document.
    """

    info = doc.metadata

    metadata = {
        "document_name": os.path.basename(pdf_path),
        "document_path": pdf_path,

        "title": info.get("title", ""),
        "author": info.get("author", ""),
        "creator": info.get("creator", ""),
        "producer": info.get("producer", ""),
        "subject": info.get("subject", ""),
        "keywords": info.get("keywords", ""),

        "creation_date": info.get("creationDate", ""),
        "modification_date": info.get("modDate", ""),

        "total_pages": len(doc),
        "file_size_bytes": os.path.getsize(pdf_path),

        "extraction_tool": "PyMuPDF",
        "extraction_timestamp": datetime.now().isoformat()
    }

    return metadata