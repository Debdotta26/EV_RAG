"""
chunk_validator.py

Hybrid Adaptive Chunk Validator

Features
--------
✓ Remove empty chunks
✓ Remove tiny chunks (<20 words)
✓ Remove duplicate text
✓ Remove duplicate tables
✓ Remove duplicate images
✓ Remove invalid multimodal objects
✓ Calculate quality metrics
"""

MIN_WORDS = 20
MAX_WORDS = 350


def normalize_text(text):
    return " ".join(text.lower().split())


def remove_duplicate_tables(tables):

    unique = []
    seen = set()

    for table in tables:

        table_id = table.get("table_id")

        if not table_id:
            continue

        if table_id in seen:
            continue

        rows = table.get("rows", [])

        # Skip empty tables
        if len(rows) == 0:
            continue

        seen.add(table_id)
        unique.append(table)

    return unique


def remove_duplicate_images(images):

    unique = []
    seen = set()

    for image in images:

        image_id = image.get("image_id")

        if not image_id:
            continue

        if image_id in seen:
            continue

        width = image.get("width", 0)
        height = image.get("height", 0)

        # Ignore tiny decorative images
        if width < 150 or height < 150:
            continue

        seen.add(image_id)
        unique.append(image)

    return unique


def validate_chunks(chunks):

    valid_chunks = []

    seen_text = set()

    duplicate_tables_removed = 0
    duplicate_images_removed = 0
    duplicate_chunks_removed = 0
    tiny_chunks_removed = 0

    for chunk in chunks:

        text = chunk.get("text", "").strip()

        # ------------------------
        # Remove empty chunks
        # ------------------------

        if not text:
            continue

        words = len(text.split())

        # ------------------------
        # Remove tiny chunks
        # ------------------------

        if words < MIN_WORDS:
            tiny_chunks_removed += 1
            continue

        # ------------------------
        # Normalize text
        # ------------------------

        normalized = normalize_text(text)

        if normalized in seen_text:
            duplicate_chunks_removed += 1
            continue

        seen_text.add(normalized)

        # ------------------------
        # Default heading
        # ------------------------

        chunk["heading"] = chunk.get(
            "heading",
            "General"
        )

        # ------------------------
        # Word Count
        # ------------------------

        chunk["word_count"] = words

        # ------------------------
        # Quality Label
        # ------------------------

        if words <= 80:
            quality = "small"

        elif words <= 250:
            quality = "good"

        elif words <= MAX_WORDS:
            quality = "excellent"

        else:
            quality = "large"

        chunk["quality"] = quality

        # ------------------------
        # Clean Tables
        # ------------------------

        old_tables = len(
            chunk.get("tables", [])
        )

        chunk["tables"] = remove_duplicate_tables(
            chunk.get("tables", [])
        )

        duplicate_tables_removed += (
            old_tables - len(chunk["tables"])
        )

        # ------------------------
        # Clean Images
        # ------------------------

        old_images = len(
            chunk.get("images", [])
        )

        chunk["images"] = remove_duplicate_images(
            chunk.get("images", [])
        )

        duplicate_images_removed += (
            old_images - len(chunk["images"])
        )

        # ------------------------
        # Counts
        # ------------------------

        chunk["table_count"] = len(chunk["tables"])

        chunk["image_count"] = len(chunk["images"])

        chunk["multimodal_score"] = (
            chunk["table_count"] * 2
            +
            chunk["image_count"]
        )

        valid_chunks.append(chunk)

    stats = {

        "valid_chunks": len(valid_chunks),

        "duplicate_chunks_removed": duplicate_chunks_removed,

        "tiny_chunks_removed": tiny_chunks_removed,

        "duplicate_tables_removed": duplicate_tables_removed,

        "duplicate_images_removed": duplicate_images_removed

    }

    return valid_chunks, stats