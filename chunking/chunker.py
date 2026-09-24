"""
chunker.py

Hybrid Adaptive Multimodal Chunking Pipeline
"""

import os
import json

from section_detector import detect_sections
from semantic_merger import merge_sections
from adaptive_splitter import split_sections
from table_chunker import chunk_tables
from image_chunker import chunk_images
from multimodal_linker import link_multimodal_chunks
from keyword_generator import generate_keywords
from chunk_validator import validate_chunks


def process_document(json_path, output_folder):

    with open(json_path, "r", encoding="utf-8") as f:
        document = json.load(f)

    metadata = document["metadata"]
    pages = document["pages"]

    print("\n--------------------------------")
    print("Processing:", metadata["document_name"])
    print("--------------------------------")

    # -----------------------------
    # Detect Sections
    # -----------------------------

    sections = detect_sections(pages)

    print("Sections:", len(sections))

    # -----------------------------
    # Merge Sections
    # -----------------------------

    merged = merge_sections(sections)

    print("Merged Sections:", len(merged))

    # -----------------------------
    # Text Chunks
    # -----------------------------

    text_chunks = split_sections(merged)

    print("Text Chunks:", len(text_chunks))

    # -----------------------------
    # Table Chunks
    # -----------------------------

    table_chunks = chunk_tables(merged)

    print("Table Chunks:", len(table_chunks))

    # -----------------------------
    # Image Chunks
    # -----------------------------

    image_chunks = chunk_images(merged)

    print("Image Chunks:", len(image_chunks))

    # -----------------------------
    # Merge All
    # -----------------------------

    chunks = text_chunks + table_chunks + image_chunks

    # -----------------------------
    # Multimodal Linking
    # -----------------------------

    chunks = link_multimodal_chunks(
        chunks,
        pages
    )

    print("After Linking:", len(chunks))

    # -----------------------------
    # Keyword Generation
    # -----------------------------

    for chunk in chunks:

        chunk["keywords"] = generate_keywords(
            chunk.get("text", "")
        )

    # -----------------------------
    # Validation
    # -----------------------------

    chunks, stats = validate_chunks(chunks)

    print("Valid Chunks:", len(chunks))

    # -----------------------------
    # Final Chunk IDs
    # -----------------------------

    for i, chunk in enumerate(chunks, start=1):

        chunk["chunk_id"] = f"CWWG_{i:05d}"

    final_json = {

        "metadata": metadata,

        "statistics": {

            "pages": len(pages),

            "sections": len(sections),

            "merged_sections": len(merged),

            "text_chunks": len(text_chunks),

            "table_chunks": len(table_chunks),

            "image_chunks": len(image_chunks),

            "total_chunks": len(chunks)

        },

        "chunks": chunks

    }

    outfile = os.path.join(

        output_folder,

        metadata["document_name"].replace(

            ".pdf",

            "_chunks.json"

        )

    )

    with open(

        outfile,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            final_json,

            f,

            indent=4,

            ensure_ascii=False

        )

    print("Saved:", outfile)

    # -----------------------------
    # Return Statistics
    # -----------------------------

    return {

        "pages": len(pages),

        "sections": len(sections),

        "merged_sections": len(merged),

        "text_chunks": len(text_chunks),

        "table_chunks": len(table_chunks),

        "image_chunks": len(image_chunks),

        "total_chunks": len(chunks),

        "largest_chunk": max(

            c["word_count"]

            for c in chunks

        ),

        "smallest_chunk": min(

            c["word_count"]

            for c in chunks

        ),

        "average_chunk": round(

            sum(

                c["word_count"]

                for c in chunks

            ) / len(chunks),

            2

        ),

        "duplicate_tables_removed":

            stats["duplicate_tables_removed"],

        "duplicate_images_removed":

            stats["duplicate_images_removed"]

    }


def process_all_documents(

    input_folder,

    output_folder

):

    os.makedirs(

        output_folder,

        exist_ok=True

    )

    files = [

        f

        for f in os.listdir(input_folder)

        if f.endswith(".json")

    ]

    print("\nFound", len(files), "cleaned documents.\n")

    report = []

    for file in files:

        stats = process_document(

            os.path.join(

                input_folder,

                file

            ),

            output_folder

        )

        report.append(stats)

    return report