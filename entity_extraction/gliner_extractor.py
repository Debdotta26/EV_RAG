"""
gliner_extractor.py

EV Manual GLiNER Entity Extractor

Features
--------
✓ Loads GLiNER only once
✓ Uses custom EV-manual labels
✓ Confidence threshold
✓ Removes duplicate entities
✓ Returns structured entities
"""

from gliner import GLiNER


# -------------------------------------------------
# Load Model (only once)
# -------------------------------------------------

MODEL_NAME = "urchade/gliner_medium-v2.1"

print("Loading GLiNER model...")

model = GLiNER.from_pretrained(MODEL_NAME)

print("GLiNER loaded successfully.\n")


# -------------------------------------------------
# EV Domain Labels
# -------------------------------------------------

EV_ENTITY_LABELS = [
    "Vehicle Model",
    "Vehicle",
    "Battery",
    "Charging",
    "Charger",
    "Charging Port",
    "Charging Station",
    "Charging Time",
    "Charging Power",
    "Charging Voltage",
    "Charging Current",
    "Range",
    "Driving Mode",
    "Regenerative Braking",
    "Brake",
    "Tyre",
    "Tyre Pressure",
    "Motor",
    "Warning",
    "Safety",
    "Maintenance",
    "Service",
    "Fault",
    "Error",
    "Dashboard",
    "Display",
    "Infotainment",
    "Navigation",
    "Bluetooth",
    "V2L",
    "ADAS",
    "Temperature",
    "Location",
    "Button",
    "Indicator"
]


# -------------------------------------------------
# Confidence Threshold
# -------------------------------------------------

THRESHOLD = 0.50


# -------------------------------------------------
# Entity Extraction
# -------------------------------------------------

def extract_entities(text):
    """
    Extract EV-related entities from a text chunk.
    """

    if not text or not text.strip():
        return []

    predictions = model.predict_entities(
        text,
        EV_ENTITY_LABELS,
        threshold=THRESHOLD
    )

    entities = []
    seen = set()

    for entity in predictions:

        entity_text = entity["text"].strip()
        label = entity["label"]
        score = round(entity["score"], 4)

        key = (
            entity_text.lower(),
            label.lower()
        )

        if key in seen:
            continue

        seen.add(key)

        entities.append({
            "text": entity_text,
            "label": label,
            "score": score
        })

    return entities