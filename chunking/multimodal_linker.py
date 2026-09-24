"""
multimodal_linker.py

Hybrid Multimodal Linker

Features
--------
✓ Removes duplicate tables
✓ Removes duplicate images
✓ Links only nearby multimodal objects
✓ Calculates multimodal score
"""

from copy import deepcopy


def remove_duplicate_tables(tables):

    unique = []
    seen = set()

    for table in tables:

        table_id = table.get("table_id")

        if table_id not in seen:

            seen.add(table_id)
            unique.append(table)

    return unique


def remove_duplicate_images(images):

    unique = []
    seen = set()

    for image in images:

        image_id = image.get("image_id")

        if image_id not in seen:

            seen.add(image_id)
            unique.append(image)

    return unique


def link_multimodal_chunks(chunks, pages):

    for chunk in chunks:

        page_start = chunk.get("page_start", 1)
        page_end = chunk.get("page_end", page_start)

        linked_tables = []
        linked_images = []

        # Search only within the chunk's page range
        for page in pages:

            page_no = page.get("page_number")

            if page_no < page_start or page_no > page_end:
                continue

            linked_tables.extend(
                deepcopy(page.get("tables", []))
            )

            linked_images.extend(
                deepcopy(page.get("images", []))
            )

        # Remove duplicates
        linked_tables = remove_duplicate_tables(linked_tables)
        linked_images = remove_duplicate_images(linked_images)

        chunk["tables"] = linked_tables
        chunk["images"] = linked_images

        # Metadata
        chunk["table_count"] = len(linked_tables)
        chunk["image_count"] = len(linked_images)

        chunk["multimodal_score"] = (
            chunk["table_count"]
            +
            chunk["image_count"]
        )

    return chunks