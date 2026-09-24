"""
run_entities.py

Runs Hybrid BM25 + GLiNER Entity Extraction
for all chunked documents.

Pipeline
--------
Chunks
   ↓
BM25 Relevance Scoring
   ↓
GLiNER Entity Extraction
   ↓
Post Processing
   ↓
Validation
   ↓
Save Updated Chunks
   ↓
Statistics Report

IMPORTANT
---------
BM25 is currently used in ASSIST MODE.

It does NOT remove or filter out chunks.
All chunks are still passed to GLiNER.

BM25 relevance information is stored inside
each chunk so it can later be used for:
- entity validation
- confidence improvement
- search
- traceability
- Streamlit retrieval
"""

import os
import json
import time

from gliner_extractor import extract_entities

from bm25_retriever import (
    get_category_scores,
    get_top_categories
)

from entity_postprocessor import (
    postprocess_entities
)

from entity_validator import (
    validate_entities
)

from entity_statistics import (
    generate_statistics,
    print_statistics,
    save_statistics
)


# =====================================================
# INPUT / OUTPUT
# =====================================================

INPUT_FOLDER = os.path.join(
    "output",
    "chunks"
)

OUTPUT_FOLDER = os.path.join(
    "output",
    "entities"
)

REPORT_FOLDER = os.path.join(
    "output",
    "reports"
)


# =====================================================
# CREATE OUTPUT DIRECTORIES
# =====================================================

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


# =====================================================
# PROCESS ONE DOCUMENT
# =====================================================

def process_document(filepath):

    # -------------------------------------------------
    # Load document
    # -------------------------------------------------

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:

        document = json.load(f)

    print("\n----------------------------------")

    print(
        "Processing:",
        document["metadata"]["document_name"]
    )

    print("----------------------------------")

    # -------------------------------------------------
    # Get chunks
    # -------------------------------------------------

    chunks = document.get(
        "chunks",
        []
    )

    if not chunks:

        print(
            "WARNING: No chunks found."
        )

        return document

    # -------------------------------------------------
    # BM25
    # -------------------------------------------------

    print(
        "Running BM25 relevance scoring..."
    )

    bm25_results = get_category_scores(
        chunks
    )

    print(
        "BM25 scoring completed."
    )

    # -------------------------------------------------
    # Entity Counter
    # -------------------------------------------------

    total_entities = 0

    # -------------------------------------------------
    # Process Every Chunk
    # -------------------------------------------------

    for index, chunk in enumerate(chunks):

        # ---------------------------------------------
        # Get chunk text
        # ---------------------------------------------

        text = chunk.get(
            "text",
            ""
        )

        # ---------------------------------------------
        # BM25 Information
        # ---------------------------------------------

        bm25_data = bm25_results[index]

        top_categories = get_top_categories(

            bm25_data.get(
                "bm25_scores",
                {}
            ),

            top_k=5

        )

        # ---------------------------------------------
        # Store BM25 information
        # ---------------------------------------------

        chunk["bm25"] = {

            "top_categories":
                top_categories,

            "scores":
                bm25_data.get(
                    "bm25_scores",
                    {}
                )

        }

        # ---------------------------------------------
        # GLiNER Entity Extraction
        # ---------------------------------------------

        entities = extract_entities(
            text
        )

        # ---------------------------------------------
        # Post Processing
        # ---------------------------------------------

        entities = postprocess_entities(
            entities
        )

        # ---------------------------------------------
        # Entity Validation
        # ---------------------------------------------

        entities, stats = validate_entities(
            entities
        )

        # ---------------------------------------------
        # Store Entities
        # ---------------------------------------------

        chunk["entities"] = entities

        total_entities += len(
            entities
        )

    # -------------------------------------------------
    # Document Summary
    # -------------------------------------------------

    print(
        "Chunks:",
        len(chunks)
    )

    print(
        "Entities:",
        total_entities
    )

    # -------------------------------------------------
    # Output File
    # -------------------------------------------------

    outfile = os.path.join(

        OUTPUT_FOLDER,

        os.path.basename(filepath)

    )

    # -------------------------------------------------
    # Save Updated Document
    # -------------------------------------------------

    with open(

        outfile,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            document,

            f,

            indent=4,

            ensure_ascii=False

        )

    print(
        "Saved:",
        outfile
    )

    return document


# =====================================================
# MAIN
# =====================================================

def main():

    # -------------------------------------------------
    # Start Timer
    # -------------------------------------------------

    start = time.time()

    print()
    print("=" * 60)
    print("BM25 + GLiNER ENTITY EXTRACTION")
    print("=" * 60)
    print()

    # -------------------------------------------------
    # Check Input Folder
    # -------------------------------------------------

    if not os.path.exists(
        INPUT_FOLDER
    ):

        print(
            "ERROR: Input folder does not exist:"
        )

        print(
            INPUT_FOLDER
        )

        return

    # -------------------------------------------------
    # Get JSON Chunk Files
    # -------------------------------------------------

    files = [

        f

        for f in os.listdir(
            INPUT_FOLDER
        )

        if f.endswith(".json")

    ]

    # -------------------------------------------------
    # No Files
    # -------------------------------------------------

    if not files:

        print(
            "No chunk files found."
        )

        print(
            "Expected folder:"
        )

        print(
            INPUT_FOLDER
        )

        return

    # -------------------------------------------------
    # Sort Files
    # -------------------------------------------------

    files.sort()

    print(
        "Chunk documents found:",
        len(files)
    )

    print()

    # -------------------------------------------------
    # Store All Documents
    # -------------------------------------------------

    all_documents = []

    # -------------------------------------------------
    # Process Every Document
    # -------------------------------------------------

    for file in files:

        filepath = os.path.join(

            INPUT_FOLDER,

            file

        )

        try:

            document = process_document(
                filepath
            )

            all_documents.append(
                document
            )

        except Exception as e:

            print()
            print(
                "ERROR processing:",
                file
            )

            print(
                "Error:",
                str(e)
            )

            print(
                "Skipping this document..."
            )

            continue

    # -------------------------------------------------
    # Generate Statistics
    # -------------------------------------------------

    if not all_documents:

        print()
        print(
            "No documents were processed successfully."
        )

        return

    print()
    print(
        "=" * 60
    )

    print(
        "Generating entity statistics..."
    )

    print(
        "=" * 60
    )

    stats = generate_statistics(
        all_documents
    )

    # -------------------------------------------------
    # Runtime
    # -------------------------------------------------

    runtime = round(

        time.time() - start,

        2

    )

    stats[
        "processing_time_seconds"
    ] = runtime

    # -------------------------------------------------
    # Print Statistics
    # -------------------------------------------------

    print_statistics(
        stats
    )

    # -------------------------------------------------
    # Save Statistics
    # -------------------------------------------------

    report_path = save_statistics(

        stats,

        REPORT_FOLDER

    )

    print()

    print(
        "Statistics Saved Successfully."
    )

    print(
        report_path
    )

    print()

    # -------------------------------------------------
    # Completion
    # -------------------------------------------------

    print(
        "=" * 60
    )

    print(
        "BM25 + GLiNER ENTITY EXTRACTION"
    )

    print(
        "COMPLETED SUCCESSFULLY"
    )

    print(
        "=" * 60
    )

    print()

    print(
        "Processing time:",
        runtime,
        "seconds"
    )


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":

    main()