"""
entity_statistics.py

Hybrid Entity Statistics

Generates:
-----------
✓ Total Documents
✓ Total Chunks
✓ Total Entities
✓ Entity Type Distribution
✓ Average Entities per Chunk
✓ Most Frequent Entities
✓ Processing Statistics
"""

from collections import Counter
import json
import os


# -------------------------------------------------
# Generate Statistics
# -------------------------------------------------

def generate_statistics(all_documents):

    """
    all_documents

    List of processed chunk JSONs
    """

    stats = {

        "documents_processed": 0,

        "chunks_processed": 0,

        "total_entities": 0,

        "average_entities_per_chunk": 0,

        "entity_type_distribution": {},

        "top_entities": [],

        "empty_chunks": 0

    }

    entity_types = Counter()

    entity_frequency = Counter()

    total_chunks = 0

    total_entities = 0

    empty_chunks = 0

    for document in all_documents:

        stats["documents_processed"] += 1

        chunks = document.get("chunks", [])

        total_chunks += len(chunks)

        for chunk in chunks:

            entities = chunk.get("entities", [])

            if not entities:

                empty_chunks += 1
                continue

            total_entities += len(entities)

            for entity in entities:

                label = entity.get("label", "Unknown")

                text = entity.get("text", "").strip()

                entity_types[label] += 1

                entity_frequency[text] += 1

    stats["chunks_processed"] = total_chunks

    stats["total_entities"] = total_entities

    stats["empty_chunks"] = empty_chunks

    if total_chunks > 0:

        stats["average_entities_per_chunk"] = round(

            total_entities / total_chunks,

            2

        )

    stats["entity_type_distribution"] = dict(

        sorted(

            entity_types.items(),

            key=lambda x: x[1],

            reverse=True

        )

    )

    stats["top_entities"] = [

        {

            "entity": entity,

            "count": count

        }

        for entity, count in entity_frequency.most_common(20)

    ]

    return stats


# -------------------------------------------------
# Save Report
# -------------------------------------------------

def save_statistics(stats, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    report_path = os.path.join(

        output_folder,

        "entity_statistics.json"

    )

    with open(

        report_path,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            stats,

            f,

            indent=4,

            ensure_ascii=False

        )

    return report_path


# -------------------------------------------------
# Console Report
# -------------------------------------------------

def print_statistics(stats):

    print("\n")

    print("=" * 70)

    print(" HYBRID ENTITY EXTRACTION REPORT ")

    print("=" * 70)

    print(f"Documents Processed       : {stats['documents_processed']}")

    print(f"Chunks Processed          : {stats['chunks_processed']}")

    print(f"Total Entities            : {stats['total_entities']}")

    print(f"Average Entities/Chunk    : {stats['average_entities_per_chunk']}")

    print(f"Empty Chunks              : {stats['empty_chunks']}")

    print()

    print("Entity Distribution")

    print("-" * 70)

    for label, count in stats["entity_type_distribution"].items():

        print(f"{label:<25} {count}")

    print()

    print("Top 20 Entities")

    print("-" * 70)

    for item in stats["top_entities"]:

        print(f"{item['entity']:<30} {item['count']}")

    print("=" * 70)