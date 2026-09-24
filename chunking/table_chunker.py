"""
table_chunker.py

Hybrid Table Chunker

Features
--------
✓ Removes duplicate tables
✓ Skips empty tables
✓ Skips tiny tables
✓ Converts tables into readable text
✓ Preserves metadata
"""

MIN_TABLE_WORDS = 15


def table_to_text(rows):
    """
    Convert table rows into readable text.
    """

    lines = []

    for row in rows:

        clean = []

        for cell in row:

            cell = str(cell).strip()

            if cell:
                clean.append(cell)

        if clean:
            lines.append(" | ".join(clean))

    return "\n".join(lines)


def chunk_tables(sections):

    table_chunks = []

    seen_tables = set()

    chunk_no = 1

    for section in sections:

        heading = section.get("title", "General")

        page_start = section.get("page_start", 1)
        page_end = section.get("page_end", page_start)

        for table_index, table in enumerate(section.get("tables", []), start=1):

            table_id = table.get(
                "table_id",
                f"TBL_{chunk_no:05d}"
            )

            if table_id in seen_tables:
                continue

            seen_tables.add(table_id)

            rows = table.get("rows", [])

            # -----------------------------
            # Skip empty tables
            # -----------------------------

            if not rows:
                continue

            # -----------------------------
            # Skip single-row tables
            # -----------------------------

            if len(rows) < 2:
                continue

            # -----------------------------
            # Skip single-column tables
            # -----------------------------

            max_cols = max(len(r) for r in rows)

            if max_cols < 2:
                continue

            # -----------------------------
            # Convert table to text
            # -----------------------------

            table_text = table_to_text(rows)

            # Fallback
            if not table_text.strip():
                table_text = table.get("text", "").strip()

            words = len(table_text.split())

            # -----------------------------
            # Skip tiny tables
            # -----------------------------

            if words < MIN_TABLE_WORDS:
                continue

            caption = table.get("caption", "")

            table_chunks.append({

                "chunk_id": f"TABLE_{chunk_no:05d}",

                "chunk_type": "table",

                "heading": heading,

                "page_start": page_start,

                "page_end": page_end,

                "table_id": table_id,

                "table_index": table_index,

                "caption": caption,

                "text": table_text,

                "word_count": words,

                "row_count": len(rows),

                "column_count": max_cols,

                "table_count": 1,

                "image_count": 0,

                "tables": [table],

                "images": [],

                "keywords": []

            })

            chunk_no += 1

    return table_chunks