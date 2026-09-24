import re


def clean_page_text(text):
    """
    Clean page text before chunking.
    """

    if not text:
        return ""

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Remove isolated page numbers
    text = re.sub(r"\b\d+\b(?=\s*$)", "", text)

    # Remove repeated headers
    text = text.replace(
        "Agricultural Statistics Division| Department of Agriculture & Farmers Welfare |Ministry of Agriculture & Farmers Welfare",
        ""
    )

    return text.strip()


def normalize_document(document):
    """
    Merge page content into a normalized document while
    preserving page references.
    """

    normalized = []

    for page in document["pages"]:

        page_text = []

        for item in page["content"]:

            if item["type"] == "paragraph":

                page_text.append(item["text"])

        normalized.append({

            "page_number": page["page_number"],

            "text": clean_page_text(
                " ".join(page_text)
            ),

            "tables": page["tables"],

            "images": page["images"]

        })

    return normalized