"""
image_chunker.py

Hybrid Image Chunker

Features
--------
✓ Removes duplicate images
✓ Skips tiny/decorative images
✓ Skips invalid images
✓ Preserves metadata
✓ Creates rich image descriptions
"""

MIN_WIDTH = 150
MIN_HEIGHT = 150


def build_description(heading, caption, image_name):

    description = heading

    if caption:
        description += f" | {caption}"

    elif image_name:
        description += f" | {image_name}"

    return description.strip()


def chunk_images(sections):

    image_chunks = []

    seen_images = set()

    chunk_no = 1

    for section in sections:

        heading = section.get("title", "General")

        page_start = section.get("page_start", 1)
        page_end = section.get("page_end", page_start)

        for image_index, image in enumerate(section.get("images", []), start=1):

            image_id = image.get(
                "image_id",
                f"IMG_{chunk_no:05d}"
            )

            if image_id in seen_images:
                continue

            seen_images.add(image_id)

            width = image.get("width", 0)
            height = image.get("height", 0)

            # ---------------------------------
            # Skip tiny decorative images
            # ---------------------------------

            if width < MIN_WIDTH or height < MIN_HEIGHT:
                continue

            image_path = image.get("image_path", "").strip()

            # ---------------------------------
            # Skip invalid images
            # ---------------------------------

            if not image_path:
                continue

            image_name = image.get("image_name", "")

            caption = image.get("caption", "")

            image_format = image.get("format", "")

            description = build_description(
                heading,
                caption,
                image_name
            )

            words = len(description.split())

            image_chunks.append({

                "chunk_id": f"IMAGE_{chunk_no:05d}",

                "chunk_type": "image",

                "heading": heading,

                "page_start": page_start,

                "page_end": page_end,

                "image_id": image_id,

                "image_index": image_index,

                "image_name": image_name,

                "image_path": image_path,

                "width": width,

                "height": height,

                "format": image_format,

                "caption": caption,

                "text": description,

                "word_count": words,

                "table_count": 0,

                "image_count": 1,

                "tables": [],

                "images": [image],

                "keywords": []

            })

            chunk_no += 1

    return image_chunks