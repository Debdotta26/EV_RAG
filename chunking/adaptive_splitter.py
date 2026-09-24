"""
adaptive_splitter.py

Hybrid Structure-Aware Adaptive Splitter
"""

import re

TARGET_WORDS = 220
MIN_WORDS = 120
MAX_WORDS = 320


def word_count(text):
    return len(text.split())


def split_sentences(text):
    """
    Split using sentence boundaries.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    return [s.strip() for s in sentences if s.strip()]


def force_split(sentence):
    """
    Force split long sentences using commas,
    semicolons or fixed-size word windows.
    """

    words = sentence.split()

    if len(words) <= MAX_WORDS:
        return [sentence]

    # Try commas first
    parts = re.split(r'(?<=,)\s+', sentence)

    if len(parts) > 1:

        output = []

        current = ""

        count = 0

        for part in parts:

            wc = word_count(part)

            if count + wc <= TARGET_WORDS:

                current += part + " "

                count += wc

            else:

                output.append(current.strip())

                current = part + " "

                count = wc

        if current.strip():
            output.append(current.strip())

        return output

    # Final fallback → split by words

    chunks = []

    for i in range(0, len(words), TARGET_WORDS):

        chunks.append(
            " ".join(words[i:i + TARGET_WORDS])
        )

    return chunks


def split_large_text(text):

    sentences = split_sentences(text)

    chunks = []

    current = ""

    current_words = 0

    for sentence in sentences:

        pieces = force_split(sentence)

        for piece in pieces:

            piece_words = word_count(piece)

            if current_words + piece_words <= TARGET_WORDS:

                current += piece + " "

                current_words += piece_words

            else:

                if current.strip():

                    chunks.append(current.strip())

                current = piece + " "

                current_words = piece_words

    if current.strip():

        chunks.append(current.strip())

    return chunks


def split_sections(sections):

    chunks = []

    pending = None

    chunk_no = 1

    for section in sections:

        heading = section.get("title", "General")

        text = section.get("text", "").strip()

        if not text:
            continue

        words = word_count(text)

        page_start = section.get("page_start", 1)

        page_end = section.get("page_end", page_start)

        tables = section.get("tables", [])

        images = section.get("images", [])

        # --------------------------
        # Merge small sections
        # --------------------------

        if words < MIN_WORDS:

            if pending is None:

                pending = section

                continue

            else:

                pending["text"] += "\n\n" + text

                pending["tables"].extend(tables)

                pending["images"].extend(images)

                pending["page_end"] = page_end

                continue

        # --------------------------
        # Flush pending
        # --------------------------

        if pending is not None:

            chunks.append({

                "chunk_id": f"TEMP_{chunk_no}",

                "chunk_type": "text",

                "heading": pending["title"],

                "page_start": pending["page_start"],

                "page_end": pending["page_end"],

                "text": pending["text"],

                "word_count": word_count(pending["text"]),

                "tables": pending["tables"],

                "images": pending["images"]

            })

            chunk_no += 1

            pending = None

        # --------------------------
        # Normal section
        # --------------------------

        if words <= MAX_WORDS:

            chunks.append({

                "chunk_id": f"TEMP_{chunk_no}",

                "chunk_type": "text",

                "heading": heading,

                "page_start": page_start,

                "page_end": page_end,

                "text": text,

                "word_count": words,

                "tables": tables,

                "images": images

            })

            chunk_no += 1

        else:

            pieces = split_large_text(text)

            for piece in pieces:

                chunks.append({

                    "chunk_id": f"TEMP_{chunk_no}",

                    "chunk_type": "text",

                    "heading": heading,

                    "page_start": page_start,

                    "page_end": page_end,

                    "text": piece,

                    "word_count": word_count(piece),

                    "tables": tables,

                    "images": images

                })

                chunk_no += 1

    # Flush final pending section

    if pending is not None:

        chunks.append({

            "chunk_id": f"TEMP_{chunk_no}",

            "chunk_type": "text",

            "heading": pending["title"],

            "page_start": pending["page_start"],

            "page_end": pending["page_end"],

            "text": pending["text"],

            "word_count": word_count(pending["text"]),

            "tables": pending["tables"],

            "images": pending["images"]

        })

    return chunks