import re

# Detect:
# a)
# b)
# c)
# ...
SUBSECTION_PATTERN = re.compile(
    r'(?=(?:^|\s)([a-z])\)\s+[^:]{2,80}:)',
    re.IGNORECASE
)


def split_into_subsections(text):
    """
    Split a section into subsections.

    Example:

    a) Temperature:
    ...

    b) Rainfall:
    ...
    """

    text = text.strip()

    matches = list(SUBSECTION_PATTERN.finditer(text))

    if not matches:
        return [{
            "title": "",
            "text": text
        }]

    subsections = []

    for i, match in enumerate(matches):

        start = match.start()

        if i == len(matches) - 1:
            end = len(text)
        else:
            end = matches[i + 1].start()

        part = text[start:end].strip()

        title = part.split(":")[0].strip()

        subsections.append({

            "title": title,

            "text": part

        })

    return subsections


def detect_subsections(section):

    results = []

    parts = split_into_subsections(section["text"])

    for part in parts:

        results.append({

            "heading": section["heading"],

            "section": section["section"],

            "subsection": part["title"],

            "text": part["text"]

        })

    return results