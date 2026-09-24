"""
entity_postprocessor.py

Hybrid Entity Post Processor

Features
--------
✓ Remove duplicate entities
✓ Normalize entity text
✓ Keep highest confidence entity
✓ Remove overlapping entities
✓ Sort by confidence
"""

import re


# -------------------------------------------------
# Normalize Entity Text
# -------------------------------------------------

def normalize_text(text):

    text = text.strip()

    text = re.sub(r"\s+", " ", text)

    return text


# -------------------------------------------------
# Remove Duplicate Entities
# -------------------------------------------------

def remove_duplicates(entities):

    unique = {}

    for entity in entities:

        text = normalize_text(entity["text"])

        label = entity["label"]

        score = entity["score"]

        key = (text.lower(), label.lower())

        if key not in unique:

            unique[key] = {

                "text": text,

                "label": label,

                "score": score

            }

        else:

            if score > unique[key]["score"]:

                unique[key] = {

                    "text": text,

                    "label": label,

                    "score": score

                }

    return list(unique.values())


# -------------------------------------------------
# Remove Overlapping Entities
# -------------------------------------------------

def remove_overlapping(entities):

    entities = sorted(

        entities,

        key=lambda x: (

            -len(x["text"]),

            -x["score"]

        )

    )

    final = []

    used = set()

    for entity in entities:

        lower = entity["text"].lower()

        if lower in used:

            continue

        overlap = False

        for previous in used:

            if lower in previous or previous in lower:

                overlap = True

                break

        if not overlap:

            final.append(entity)

            used.add(lower)

    return final


# -------------------------------------------------
# Sort by Confidence
# -------------------------------------------------

def sort_entities(entities):

    return sorted(

        entities,

        key=lambda x: x["score"],

        reverse=True

    )


# -------------------------------------------------
# Main Pipeline
# -------------------------------------------------

def postprocess_entities(entities):

    entities = remove_duplicates(entities)

    entities = remove_overlapping(entities)

    entities = sort_entities(entities)

    return entities