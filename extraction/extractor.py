# import os
# import json
# import fitz

# from metadata import extract_metadata
# from text_extractor import extract_text
# from table_extractor import extract_tables
# from image_extractor import extract_images
# from cleaner import clean_content

# PDF_FOLDER = "downloads/pdfs"
# OUTPUT_FOLDER = "output/documents"
# IMAGE_FOLDER = "output/images"

# os.makedirs(OUTPUT_FOLDER, exist_ok=True)
# os.makedirs(IMAGE_FOLDER, exist_ok=True)


# def extract_pdf(pdf_path):

#     doc = fitz.open(pdf_path)

#     metadata = extract_metadata(
#         doc,
#         pdf_path
#     )

#     pages = []

#     for page_no in range(len(doc)):

#         print(f"\n========== PAGE {page_no + 1} ==========")

#         page = doc.load_page(page_no)

#         # -----------------------------
#         # Extract Text
#         # -----------------------------
#         content = extract_text(page)

#         print(f"Extracted {len(content)} content blocks")

#         if len(content) > 0:
#             print("First content block:")
#             print(content[0])

#         # -----------------------------
#         # Clean Text
#         # -----------------------------
#         content = clean_content(content)

#         print(f"After cleaning: {len(content)} content blocks")

#         if len(content) > 0:
#             print("First cleaned block:")
#             print(content[0])

#         # -----------------------------
#         # Extract Tables
#         # -----------------------------
#         tables = extract_tables(
#             pdf_path,
#             page_no
#         )

#         print(f"Tables found: {len(tables)}")

#         # -----------------------------
#         # Extract Images
#         # -----------------------------
#         images = extract_images(
#             doc,
#             page_no,
#             metadata["document_name"],
#             IMAGE_FOLDER
#         )

#         print(f"Images found: {len(images)}")

#         pages.append({

#             "page_number": page_no + 1,

#             "content": content,

#             "tables": tables,

#             "images": images

#         })

#     doc.close()

#     return {

#         "metadata": metadata,

#         "pages": pages

#     }


# def extract_all_pdfs():

#     pdfs = [

#         f for f in os.listdir(PDF_FOLDER)

#         if f.lower().endswith(".pdf")

#     ]

#     print(f"\nFound {len(pdfs)} PDFs\n")

#     for pdf in pdfs:

#         try:

#             print("\n===================================================")
#             print(f"Extracting : {pdf}")
#             print("===================================================")

#             pdf_path = os.path.join(
#                 PDF_FOLDER,
#                 pdf
#             )

#             data = extract_pdf(pdf_path)

#             outfile = os.path.join(

#                 OUTPUT_FOLDER,

#                 pdf.replace(".pdf", ".json")

#             )

#             with open(

#                 outfile,

#                 "w",

#                 encoding="utf-8"

#             ) as f:

#                 json.dump(

#                     data,

#                     f,

#                     indent=4,

#                     ensure_ascii=False

#                 )

#             print("JSON Saved Successfully")

#         except Exception as e:

#             print(f"Failed : {pdf}")

#             print(e)

#     print("\nExtraction Finished.")


# if __name__ == "__main__":
#     extract_all_pdfs()

import fitz

from metadata import extract_metadata
from text_extractor import extract_text
from table_extractor import extract_tables
from image_extractor import extract_images
from cleaner import clean_content


def extract_pdf(pdf_path, image_output_folder):
    """
    Extract all information from a single PDF.

    Returns:
        Dictionary containing metadata and page-wise extracted content.
    """

    doc = fitz.open(pdf_path)

    metadata = extract_metadata(doc, pdf_path)

    pages = []

    for page_no in range(len(doc)):

        page = doc.load_page(page_no)

        # Extract text
        content = extract_text(page)

        # Clean text
        content = clean_content(content)

        # Extract tables
        tables = extract_tables(pdf_path, page_no)

        # Extract images
        images = extract_images(
            doc,
            page_no,
            metadata["document_name"],
            image_output_folder
        )

        pages.append({

            "page_number": page_no + 1,

            "content": content,

            "tables": tables,

            "images": images

        })

    doc.close()

    return {

        "metadata": metadata,

        "pages": pages

    }