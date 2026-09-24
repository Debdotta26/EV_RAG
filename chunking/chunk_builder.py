from page_normalizer import normalize_document
from section_detector import detect_sections
from semantic_merger import merge_sections
from adaptive_splitter import adaptive_split
from keyword_generator import extract_keywords
from multimodal_linker import link_multimodal


MIN_CHUNK_WORDS = 50


def remove_duplicate_tables(tables):

    unique = []
    seen = set()

    for table in tables:

        key = str(table)

        if key not in seen:
            unique.append(table)
            seen.add(key)

    return unique


def remove_duplicate_images(images):

    unique = []
    seen = set()

    for image in images:

        key = image.get("image_path", "")

        if key not in seen:
            unique.append(image)
            seen.add(key)

    return unique


def merge_small_chunks(chunks):
    """
    Merge chunks smaller than MIN_CHUNK_WORDS
    into the previous chunk.
    """

    if not chunks:
        return chunks

    merged = []

    for chunk in chunks:

        if merged and chunk["word_count"] < MIN_CHUNK_WORDS:

            prev = merged[-1]

            prev["text"] += "\n\n" + chunk["text"]

            prev["page_end"] = chunk["page_end"]

            prev["tables"].extend(chunk["tables"])
            prev["images"].extend(chunk["images"])

            prev["tables"] = remove_duplicate_tables(prev["tables"])
            prev["images"] = remove_duplicate_images(prev["images"])

            prev["word_count"] = len(prev["text"].split())
            prev["char_count"] = len(prev["text"])

        else:

            merged.append(chunk)

    # Renumber chunk IDs
    for i, chunk in enumerate(merged, start=1):

        chunk["chunk_id"] = f"CWWG_{i:05d}"

    return merged


def build_chunks(document):

    metadata = document["metadata"]

    # ---------------------------------
    # Normalize document
    # ---------------------------------

    pages = normalize_document(document)

    print("Pages normalized :", len(pages))

    # ---------------------------------
    # Detect Sections
    # ---------------------------------

    sections = detect_sections(pages)

    print("Sections detected :", len(sections))

    # ---------------------------------
    # Merge Small Sections
    # ---------------------------------

    sections = merge_sections(sections)

    print("Sections after merge :", len(sections))

    chunks = []

    chunk_no = 1

    # ---------------------------------
    # Build Chunks
    # ---------------------------------

    for section in sections:

        split_chunks = adaptive_split(section["text"])

        tables = remove_duplicate_tables(
            section.get("tables", [])
        )

        images = remove_duplicate_images(
            section.get("images", [])
        )

        keywords = extract_keywords(section["text"])

        for piece in split_chunks:

            chunk = {

                "chunk_id": f"CWWG_{chunk_no:05d}",

                "document_name": metadata["document_name"],

                "heading": section.get(
                    "title",
                    "Unknown"
                ),

                "page_start": section["page_start"],

                "page_end": section["page_end"],

                "keywords": keywords,

                "word_count": len(piece.split()),

                "char_count": len(piece),

                "tables": tables,

                "images": images,

                "text": piece.strip()

            }

            chunk = link_multimodal(chunk)

            chunks.append(chunk)

            chunk_no += 1

    # ---------------------------------
    # Merge Tiny Chunks
    # ---------------------------------

    chunks = merge_small_chunks(chunks)

    # ---------------------------------
    # Calculate Statistics
    # ---------------------------------

    total_words = sum(chunk["word_count"] for chunk in chunks)

    average_words = round(
        total_words / len(chunks),
        2
    ) if chunks else 0

    smallest_chunk = min(
        chunk["word_count"] for chunk in chunks
    ) if chunks else 0

    largest_chunk = max(
        chunk["word_count"] for chunk in chunks
    ) if chunks else 0

    print("Final chunks :", len(chunks))
    print("Average words/chunk :", average_words)
    print("Smallest chunk :", smallest_chunk)
    print("Largest chunk :", largest_chunk)

    return {

        "metadata": metadata,

        "total_chunks": len(chunks),

        "average_chunk_words": average_words,

        "largest_chunk": largest_chunk,

        "smallest_chunk": smallest_chunk,

        "chunks": chunks

    }