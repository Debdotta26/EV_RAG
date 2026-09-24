import re

# Words commonly used as report headings
HEADING_KEYWORDS = [
    "Key Insights",
    "Introduction",
    "Weather Update",
    "Weather Forecast",
    "Inputs Situation",
    "Pests & Diseases",
    "Market Prices",
    "Wholesale Prices",
    "Annexure",
    "Summary",
    "Recommendations",
    "Conclusion"
]


def is_heading(item):
    """
    Detect whether a content block is a heading.
    """

    if item.get("type") == "heading":
        return True

    text = item.get("text", "").strip()

    if not text:
        return False

    # Exact heading keywords
    for keyword in HEADING_KEYWORDS:
        if keyword.lower() == text.lower():
            return True

    # All uppercase headings
    if (
        len(text) < 80
        and text.isupper()
        and len(text.split()) <= 10
    ):
        return True

    # Ends with colon and short
    if (
        text.endswith(":")
        and len(text.split()) <= 8
    ):
        return True

    # Title Case headings
    if (
        len(text.split()) <= 8
        and text.istitle()
    ):
        return True

    return False


def detect_heading(page):

    for item in page["content"]:

        if is_heading(item):
            return item["text"]

    return "Introduction"