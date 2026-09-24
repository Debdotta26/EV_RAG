"""
section_detector.py

Hybrid Section Detector
Detects:
- Main headings
- Numbered sections
- Roman numeral headings
- Uppercase headings
- Weather Outlook
- Annex
"""

import re


MAIN_HEADING = re.compile(
    r'^(\d+\.\s+.+|[IVXLCDM]+\.\s+.+)$'
)

UPPERCASE = re.compile(
    r'^[A-Z][A-Z\s&()/,-]{5,}$'
)

TITLE_CASE = re.compile(
    r'^[A-Z][A-Za-z0-9\s()/,&-]{3,80}:?$'
)


def is_heading(text):

    text = text.strip()

    if not text:
        return False

    if MAIN_HEADING.match(text):
        return True

    if UPPERCASE.match(text):
        return True

    if TITLE_CASE.match(text):

        if len(text.split()) <= 10:
            return True

    return False


def detect_sections(pages):

    sections = []

    current = None

    for page in pages:

        page_no = page["page_number"]

        content = page.get("content", [])

        tables = page.get("tables", [])

        images = page.get("images", [])

        for block in content:

            block_type = block.get("type", "paragraph")

            text = block.get("text", "").strip()

            if not text:
                continue

            heading = False

            if block_type == "heading":
                heading = True

            elif is_heading(text):
                heading = True

            if heading:

                if current:

                    sections.append(current)

                current = {

                    "title": text,

                    "text": "",

                    "page_start": page_no,

                    "page_end": page_no,

                    "tables": [],

                    "images": []

                }

                continue

            if current is None:

                current = {

                    "title": "Introduction",

                    "text": "",

                    "page_start": page_no,

                    "page_end": page_no,

                    "tables": [],

                    "images": []

                }

            current["text"] += text + "\n"

            current["page_end"] = page_no

        # Attach page tables/images to current section
        if current:

            current["tables"].extend(tables)

            current["images"].extend(images)

    if current:

        sections.append(current)

    return sections