"""
run_chunking.py

Runs Hybrid Adaptive Multimodal Chunking
for all cleaned documents.

Outputs:
--------
1. Chunk JSONs
2. Console Report
3. chunking_report.json
"""

import os
import json
import time

from chunker import process_all_documents


# -------------------------------------------------
# INPUT / OUTPUT
# -------------------------------------------------

INPUT_FOLDER = os.path.join(
    "extraction",
    "output",
    "pymupdf"
)

OUTPUT_FOLDER = os.path.join(
    "output",
    "chunks"
)

REPORT_FOLDER = os.path.join(
    "output",
    "reports"
)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


# -------------------------------------------------
# MAIN
# -------------------------------------------------

def main():

    start = time.time()

    report = process_all_documents(
        INPUT_FOLDER,
        OUTPUT_FOLDER
    )

    if len(report) == 0:

        print("\nNo documents found.")
        return

    # -----------------------------------------
    # Overall Statistics
    # -----------------------------------------

    documents = len(report)

    pages = sum(r["pages"] for r in report)

    sections = sum(r["sections"] for r in report)

    merged = sum(r["merged_sections"] for r in report)

    total_chunks = sum(r["total_chunks"] for r in report)

    text_chunks = sum(r["text_chunks"] for r in report)

    table_chunks = sum(r["table_chunks"] for r in report)

    image_chunks = sum(r["image_chunks"] for r in report)

    largest = max(r["largest_chunk"] for r in report)

    smallest = min(r["smallest_chunk"] for r in report)

    avg_chunk = round(

        sum(r["average_chunk"] for r in report)

        / documents,

        2

    )

    avg_chunks_doc = round(

        total_chunks / documents,

        2

    )

    duplicate_tables = sum(

        r["duplicate_tables_removed"]

        for r in report

    )

    duplicate_images = sum(

        r["duplicate_images_removed"]

        for r in report

    )

    runtime = round(

        time.time() - start,

        2

    )

    # -----------------------------------------
    # Chunk Quality Score
    # -----------------------------------------

    score = 10.0

    if avg_chunk < 120:
        score -= 1

    if avg_chunk > 350:
        score -= 1

    if duplicate_tables > 20:
        score -= 0.5

    if duplicate_images > 20:
        score -= 0.5

    score = round(max(score, 0), 2)

    # -----------------------------------------
    # Print Report
    # -----------------------------------------

    print("\n")

    print("=" * 70)

    print(" HYBRID ADAPTIVE MULTIMODAL CHUNKING REPORT ")

    print("=" * 70)

    print(f"Documents Processed      : {documents}")

    print(f"Pages Processed          : {pages}")

    print()

    print(f"Sections Detected        : {sections}")

    print(f"Merged Sections          : {merged}")

    print()

    print(f"Total Chunks            : {total_chunks}")

    print(f"Text Chunks             : {text_chunks}")

    print(f"Table Chunks            : {table_chunks}")

    print(f"Image Chunks            : {image_chunks}")

    print()

    print(f"Largest Chunk           : {largest} words")

    print(f"Smallest Chunk          : {smallest} words")

    print(f"Average Chunk Size      : {avg_chunk} words")

    print(f"Average Chunks/Document : {avg_chunks_doc}")

    print()

    print(f"Duplicate Tables Removed : {duplicate_tables}")

    print(f"Duplicate Images Removed : {duplicate_images}")

    print()

    print(f"Processing Time         : {runtime} sec")

    print()

    print(f"Chunk Quality Score     : {score}/10")

    print("=" * 70)

    # -----------------------------------------
    # Save Report
    # -----------------------------------------

    report_json = {

        "documents_processed": documents,

        "pages_processed": pages,

        "sections_detected": sections,

        "merged_sections": merged,

        "total_chunks": total_chunks,

        "text_chunks": text_chunks,

        "table_chunks": table_chunks,

        "image_chunks": image_chunks,

        "largest_chunk": largest,

        "smallest_chunk": smallest,

        "average_chunk": avg_chunk,

        "average_chunks_per_document": avg_chunks_doc,

        "duplicate_tables_removed": duplicate_tables,

        "duplicate_images_removed": duplicate_images,

        "processing_time_seconds": runtime,

        "chunk_quality_score": score

    }

    with open(

        os.path.join(

            REPORT_FOLDER,

            "chunking_report.json"

        ),

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            report_json,

            f,

            indent=4,

            ensure_ascii=False

        )

    print("\nReport Saved Successfully.")

    print(

        os.path.join(

            REPORT_FOLDER,

            "chunking_report.json"

        )

    )


# -------------------------------------------------

if __name__ == "__main__":

    main()