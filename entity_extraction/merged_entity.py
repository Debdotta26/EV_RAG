"""
merge_entities.py

Merge all entity JSON files into a single
master entity knowledge base.
"""

import os
import json

# ---------------------------------------------------
# INPUT / OUTPUT
# ---------------------------------------------------

INPUT_FOLDER = os.path.join(
    "output",
    "entities"
)

OUTPUT_FILE = os.path.join(
    "output",
    "entities",
    "merged_entities.json"
)


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

def main():

    files = sorted([

        f

        for f in os.listdir(INPUT_FOLDER)

        if f.endswith(".json")

        and f != "merged_entities.json"

        and f != "clean_entities.json"

    ])

    merged = {

        "metadata": {

            "documents": len(files),

            "source_folder": INPUT_FOLDER

        },

        "chunks": []

    }

    total_chunks = 0

    total_entities = 0

    for file in files:

        path = os.path.join(INPUT_FOLDER, file)

        print(f"Merging: {file}")

        with open(path, "r", encoding="utf-8") as f:

            document = json.load(f)

        metadata = document.get("metadata", {})

        chunks = document.get("chunks", [])

        for chunk in chunks:

            chunk["source_document"] = metadata.get(
                "document_name",
                file
            )

            total_entities += len(
                chunk.get("entities", [])
            )

        merged["chunks"].extend(chunks)

        total_chunks += len(chunks)

    merged["metadata"]["total_chunks"] = total_chunks

    merged["metadata"]["total_entities"] = total_entities

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            merged,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 60)

    print("ENTITY MERGE REPORT")

    print("=" * 60)

    print(f"Documents Merged : {len(files)}")

    print(f"Total Chunks     : {total_chunks}")

    print(f"Total Entities   : {total_entities}")

    print(f"Output File      : {OUTPUT_FILE}")

    print("=" * 60)


if __name__ == "__main__":

    main()