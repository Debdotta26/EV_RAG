"""
semantic_merger.py

Hybrid Semantic Merger

Merge only if:
✓ Same heading
✓ Consecutive pages
✓ Small section
✓ Similar topic
"""

MIN_WORDS = 120


def word_count(text):
    return len(text.split())


def normalize(text):
    return text.lower().strip()


def merge_sections(sections):

    if not sections:
        return []

    merged = []

    current = sections[0]

    for nxt in sections[1:]:

        current_words = word_count(current["text"])
        next_words = word_count(nxt["text"])

        same_heading = (
            normalize(current["title"])
            ==
            normalize(nxt["title"])
        )

        nearby_pages = (
            nxt["page_start"]
            <=
            current["page_end"] + 1
        )

        # -----------------------
        # Merge Condition
        # -----------------------

        should_merge = (

            same_heading

            or

            (
                current_words < MIN_WORDS
                and
                nearby_pages
            )

        )

        if should_merge:

            current["text"] += "\n\n" + nxt["text"]

            current["page_end"] = nxt["page_end"]

            current["tables"].extend(
                nxt.get("tables", [])
            )

            current["images"].extend(
                nxt.get("images", [])
            )

        else:

            merged.append(current)

            current = nxt

    merged.append(current)

    return merged