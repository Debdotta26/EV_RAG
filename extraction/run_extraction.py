# from extractor import extract_all_pdfs


# if __name__ == "__main__":

#     extract_all_pdfs()

import os
import json

from extractor import extract_pdf

# -----------------------------
# Base Directory
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# Paths
# -----------------------------
PDF_FOLDER = os.path.join(BASE_DIR, "..", "downloads", "pdfs")

PYMUPDF_OUTPUT = os.path.join(BASE_DIR, "output", "pymupdf")

IMAGE_FOLDER = os.path.join(BASE_DIR, "output", "images")

os.makedirs(PYMUPDF_OUTPUT, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)


def extract_all_pdfs():

    pdf_files = [

        f for f in os.listdir(PDF_FOLDER)

        if f.lower().endswith(".pdf")

    ]

    print(f"\nFound {len(pdf_files)} PDF(s).\n")

    for pdf in pdf_files:

        pdf_path = os.path.join(PDF_FOLDER, pdf)

        print(f"Extracting: {pdf}")

        try:

            data = extract_pdf(

                pdf_path,

                IMAGE_FOLDER

            )

            output_file = os.path.join(

                PYMUPDF_OUTPUT,

                pdf.replace(".pdf", ".json")

            )

            with open(

                output_file,

                "w",

                encoding="utf-8"

            ) as f:

                json.dump(

                    data,

                    f,

                    indent=4,

                    ensure_ascii=False

                )

            print("✔ Extraction completed.")

        except Exception as e:

            print(f"✖ Failed: {pdf}")

            print(e)

    print("\nAll PDFs processed successfully.")


if __name__ == "__main__":

    extract_all_pdfs()