"""
entity_validator.py

Hybrid Entity Validator

Features
--------
✓ Remove low confidence entities
✓ Remove empty entities
✓ Remove numeric-only entities
✓ Remove stopwords
✓ Remove duplicate entities
✓ Generate validation statistics
"""

import re

# -------------------------------------------------
# Configuration
# -------------------------------------------------

MIN_CONFIDENCE = 0.50

MIN_LENGTH = 2

STOPWORDS = {

    "the","a","an","and","or","of","to","for","in",
    "on","at","by","with","from","into","during",
    "before","after","between","over","under","is",
    "are","was","were","be","been","being","this",
    "that","these","those"

}


# -------------------------------------------------
# Helper Functions
# -------------------------------------------------

def is_numeric(text):

    return bool(re.fullmatch(r"[\d.,/-]+", text))


def is_valid_text(text):

    text = text.strip()

    if len(text) < MIN_LENGTH:
        return False

    if text.lower() in STOPWORDS:
        return False

    if is_numeric(text):
        return False

    return True


# -------------------------------------------------
# Validation
# -------------------------------------------------

def validate_entities(entities):

    valid_entities = []

    seen = set()

    stats = {

        "total_entities": len(entities),

        "valid_entities": 0,

        "duplicates_removed": 0,

        "low_confidence_removed": 0,

        "invalid_removed": 0

    }

    for entity in entities:

        text = entity.get("text", "").strip()

        label = entity.get("label", "").strip()

        score = entity.get("score", 0)

        # -----------------------------
        # Confidence Check
        # -----------------------------

        if score < MIN_CONFIDENCE:

            stats["low_confidence_removed"] += 1
            continue

        # -----------------------------
        # Text Validation
        # -----------------------------

        if not is_valid_text(text):

            stats["invalid_removed"] += 1
            continue

        # -----------------------------
        # Duplicate Check
        # -----------------------------

        key = (

            text.lower(),

            label.lower()

        )

        if key in seen:

            stats["duplicates_removed"] += 1
            continue

        seen.add(key)

        valid_entities.append({

            "text": text,

            "label": label,

            "score": round(score, 4)

        })

    stats["valid_entities"] = len(valid_entities)

    return valid_entities, stats