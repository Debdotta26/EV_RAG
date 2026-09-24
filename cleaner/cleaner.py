import re
import html
from copy import deepcopy


# --------------------------------------------------
# Repeated headers
# --------------------------------------------------

HEADER_PATTERNS = [

    r"Agricultural Statistics Division.*?Farmers Welfare",
    r"Department of Agriculture.*?Farmers Welfare",
    r"Ministry of Agriculture.*?Farmers Welfare",

]


# --------------------------------------------------
# Remove only page numbers
# --------------------------------------------------

def remove_page_number(text):

    if not text:
        return ""

    lines = text.splitlines()

    cleaned = []

    for line in lines:

        s = line.strip()

        # Remove only if the entire line is a page number
        if re.fullmatch(r"\d{1,3}", s):
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


# --------------------------------------------------
# Clean text
# --------------------------------------------------

def clean_text(text):

    if not text:
        return ""

    text = html.unescape(text)

    text = remove_page_number(text)

    for pattern in HEADER_PATTERNS:

        text = re.sub(

            pattern,

            "",

            text,

            flags=re.IGNORECASE

        )

    # Normalize bullets

    text = (

        text.replace("", "-")

            .replace("•", "-")

            .replace("●", "-")

    )

    # Fix ordinals

    text = re.sub(r"(\d+)\s+st", r"\1st", text)

    text = re.sub(r"(\d+)\s+nd", r"\1nd", text)

    text = re.sub(r"(\d+)\s+rd", r"\1rd", text)

    text = re.sub(r"(\d+)\s+th", r"\1th", text)

    # Remove duplicate image markers

    text = re.sub(

        r"(<!-- image -->\s*){2,}",

        "<!-- image -->\n",

        text

    )

    # Remove extra spaces

    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# --------------------------------------------------
# Remove duplicate content
# --------------------------------------------------

def remove_duplicate_content(content):

    seen = set()

    cleaned = []

    for item in content:

        if "text" not in item:

            cleaned.append(item)

            continue

        txt = clean_text(item["text"])

        if txt == "":

            continue

        if txt in seen:

            continue

        seen.add(txt)

        item["text"] = txt

        cleaned.append(item)

    return cleaned


# --------------------------------------------------
# Clean pages
# --------------------------------------------------

def clean_pages(pages):

    for page in pages:

        if "content" in page:

            page["content"] = remove_duplicate_content(

                page["content"]

            )

        if "tables" in page:

            for table in page["tables"]:

                if "header" in table:

                    table["header"] = [

                        clean_text(x)

                        for x in table["header"]

                    ]

                if "rows" in table:

                    new_rows = []

                    for row in table["rows"]:

                        new_rows.append(

                            [

                                clean_text(str(cell))

                                for cell in row

                            ]

                        )

                    table["rows"] = new_rows

    return pages


# --------------------------------------------------
# Clean JSON
# --------------------------------------------------

def clean_json(data):

    data = deepcopy(data)

    # Markdown

    if "content" in data:

        if "markdown" in data["content"]:

            data["content"]["markdown"] = clean_text(

                data["content"]["markdown"]

            )

        if "text" in data["content"]:

            data["content"]["text"] = clean_text(

                data["content"]["text"]

            )

    # Pages

    if "pages" in data:

        data["pages"] = clean_pages(

            data["pages"]

        )

    return data