import os
import json
import re

PYMUPDF_FOLDER = "output/pymupdf"
DOCLING_FOLDER = "output/docling/json"
OUTPUT_FOLDER = "output/hybrid"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ---------------------------------------
# Clean page text
# ---------------------------------------
def clean_text(text):

    if not text:
        return ""

    text = text.replace("\xa0", " ")

    # collapse spaces
    text = re.sub(r"[ \t]+", " ", text)

    # remove page numbers standing alone
    text = re.sub(r"\n?\s*\d+\s*\n?", "\n", text)

    return text.strip()


# ---------------------------------------
# Remove duplicate paragraphs
# ---------------------------------------
def remove_duplicates(content):

    seen = set()
    cleaned = []

    for item in content:

        txt = clean_text(item.get("text", ""))

        if txt not in seen:

            item["text"] = txt

            cleaned.append(item)

            seen.add(txt)

    return cleaned


# ---------------------------------------
# Extract topics from headings
# ---------------------------------------
def get_topics(pages):

    topics = []

    for page in pages:

        for item in page.get("content", []):

            if item.get("type") == "heading":

                heading = item["text"].strip()

                if heading not in topics:

                    topics.append(heading)

    return topics


# ---------------------------------------
# Merge one document
# ---------------------------------------
def merge_document(name):

    pymupdf_path = os.path.join(PYMUPDF_FOLDER, name + ".json")

    docling_path = os.path.join(DOCLING_FOLDER, name + ".json")

    if not os.path.exists(docling_path):

        print(f"Missing Docling file: {name}")

        return

    with open(pymupdf_path, encoding="utf-8") as f:

        pymu = json.load(f)

    with open(docling_path, encoding="utf-8") as f:

        doc = json.load(f)

    pages = pymu["pages"]

    total_tables = 0
    total_images = 0
    total_paragraphs = 0

    for page in pages:

        page["content"] = remove_duplicates(page["content"])

        total_paragraphs += len(page["content"])

        total_tables += len(page.get("tables", []))

        total_images += len(page.get("images", []))

    hybrid = {

        "metadata": pymu["metadata"],

        "pages": pages,

        # keep ONLY markdown from Docling
        "markdown": doc["markdown"],

        "summary": {

            "title": name,

            "topics": get_topics(pages)

        },

        "statistics": {

            "pages": len(pages),

            "paragraphs": total_paragraphs,

            "tables": total_tables,

            "images": total_images

        },

        "extraction": {

            "text": "PyMuPDF",

            "tables": "pdfplumber",

            "images": "PyMuPDF",

            "markdown": "Docling"

        }

    }

    out = os.path.join(OUTPUT_FOLDER, name + ".json")

    with open(out, "w", encoding="utf-8") as f:

        json.dump(hybrid, f, indent=4, ensure_ascii=False)

    print(f"✓ {name}")


# ---------------------------------------
# Merge all PDFs
# ---------------------------------------

files = [

    os.path.splitext(f)[0]

    for f in os.listdir(PYMUPDF_FOLDER)

    if f.endswith(".json")

]

for file in files:

    merge_document(file)

print("\nFinished.")