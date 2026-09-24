# import fitz
# import os
# import json
# import re

# PDF_FOLDER = "downloads/pdfs"
# OUTPUT_FOLDER = "output/json"

# os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# # ------------------------------------
# # Extract Metadata
# # ------------------------------------
# def extract_metadata(doc, filename):

#     metadata = doc.metadata

#     return {
#         "document_name": filename,
#         "title": metadata.get("title", ""),
#         "author": metadata.get("author", ""),
#         "creator": metadata.get("creator", ""),
#         "producer": metadata.get("producer", ""),
#         "total_pages": len(doc)
#     }


# # ------------------------------------
# # Clean Text
# # ------------------------------------
# def clean_line(text):

#     text = text.replace("\n", " ")
#     text = re.sub(r"\s+", " ", text)

#     return text.strip()


# # ------------------------------------
# # Extract Text
# # ------------------------------------
# def extract_text(page):

#     blocks = page.get_text("dict")["blocks"]

#     content = []

#     paragraph = ""

#     for block in blocks:

#         if "lines" not in block:
#             continue

#         block_text = ""

#         max_font = 0

#         for line in block["lines"]:

#             line_text = ""

#             for span in line["spans"]:

#                 line_text += span["text"]

#                 if span["size"] > max_font:
#                     max_font = span["size"]

#             line_text = clean_line(line_text)

#             if line_text:
#                 block_text += " " + line_text

#         block_text = clean_line(block_text)

#         if not block_text:
#             continue

#         # Detect Heading
#         if max_font >= 14:

#             # Save previous paragraph
#             if paragraph.strip():

#                 content.append({

#                     "type": "paragraph",

#                     "text": paragraph.strip()

#                 })

#                 paragraph = ""

#             # Save heading
#             content.append({

#                 "type": "heading",

#                 "text": block_text

#             })

#         else:

#             # Merge all normal text into one paragraph
#             paragraph += " " + block_text

#     # Save last paragraph

#     if paragraph.strip():

#         content.append({

#             "type": "paragraph",

#             "text": paragraph.strip()

#         })

#     return content


# # ------------------------------------
# # Extract One PDF
# # ------------------------------------
# def extract_pdf(pdf_path):

#     doc = fitz.open(pdf_path)

#     pages = []

#     for page_no in range(len(doc)):

#         page = doc.load_page(page_no)

#         content = extract_text(page)

#         pages.append({

#             "page_number": page_no + 1,

#             "content": content,

#             "tables": [],

#             "images": []

#         })

#     metadata = extract_metadata(

#         doc,

#         os.path.basename(pdf_path)

#     )

#     doc.close()

#     return metadata, pages


# # ------------------------------------
# # Extract All PDFs
# # ------------------------------------
# def extract_all_pdfs():

#     pdf_files = [

#         f for f in os.listdir(PDF_FOLDER)

#         if f.lower().endswith(".pdf")

#     ]

#     print(f"\nTotal PDFs : {len(pdf_files)}\n")

#     for pdf in pdf_files:

#         pdf_path = os.path.join(PDF_FOLDER, pdf)

#         print("Extracting :", pdf)

#         try:

#             metadata, pages = extract_pdf(pdf_path)

#             data = {

#                 "metadata": metadata,

#                 "pages": pages

#             }

#             json_name = pdf.replace(".pdf", ".json")

#             with open(

#                 os.path.join(OUTPUT_FOLDER, json_name),

#                 "w",

#                 encoding="utf-8"

#             ) as f:

#                 json.dump(

#                     data,

#                     f,

#                     indent=4,

#                     ensure_ascii=False

#                 )

#             print("Saved")

#         except Exception as e:

#             print("Skipped :", pdf)
#             print(e)

#     print("\nExtraction Completed.")


# # ------------------------------------
# # Main
# # ------------------------------------
# if __name__ == "__main__":

#     extract_all_pdfs()

import re


def clean_line(text):
    """
    Clean extracted text by removing extra spaces and newlines.
    """
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_text(page):
    """
    Extract headings and paragraphs from a PDF page while preserving
    page structure, reading order, and layout information.
    """

    blocks = page.get_text("dict")["blocks"]

    content = []
    paragraph = ""

    order = 1

    for block_id, block in enumerate(blocks):

        if "lines" not in block:
            continue

        block_text = ""
        max_font = 0

        for line in block["lines"]:

            line_text = ""

            for span in line["spans"]:

                line_text += span["text"]

                if span["size"] > max_font:
                    max_font = span["size"]

            line_text = clean_line(line_text)

            if line_text:
                block_text += " " + line_text

        block_text = clean_line(block_text)

        if not block_text:
            continue

        # -------------------------------
        # Heading Detection
        # -------------------------------
        if max_font >= 14:

            # Save previous paragraph
            if paragraph.strip():

                content.append({

                    "order": order,
                    "page": page.number + 1,
                    "block": block_id,
                    "type": "paragraph",
                    "text": paragraph.strip()

                })

                order += 1
                paragraph = ""

            # Save heading
            content.append({

                "order": order,
                "page": page.number + 1,
                "block": block_id,
                "type": "heading",
                "font_size": round(max_font, 2),
                "text": block_text

            })

            order += 1

        else:

            # Merge normal text into paragraph
            paragraph += " " + block_text

    # Save last paragraph
    if paragraph.strip():

        content.append({

            "order": order,
            "page": page.number + 1,
            "block": len(blocks),
            "type": "paragraph",
            "text": paragraph.strip()

        })

    return content