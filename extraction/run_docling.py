import os
import time

from docling_extractor import extract_docling

PDF_FOLDER = "downloads/pdfs"
OUTPUT_FOLDER = "extraction/output/docling"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

pdfs = sorted([
    f for f in os.listdir(PDF_FOLDER)
    if f.lower().endswith(".pdf")
])

total = len(pdfs)

print(f"\nFound {total} PDFs\n")

start = time.time()

for i, pdf in enumerate(pdfs, start=1):

    pdf_path = os.path.join(PDF_FOLDER, pdf)

    print(f"\n[{i}/{total}] Processing: {pdf}")

    t1 = time.time()

    extract_docling(
        pdf_path,
        OUTPUT_FOLDER
    )

    t2 = time.time()

    print(f"Completed in {(t2-t1):.2f} sec")

end = time.time()

print("\n===================================")
print(f"Finished {total} PDFs")
print(f"Total Time : {(end-start)/60:.2f} minutes")
print("===================================")