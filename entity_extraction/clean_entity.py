"""
clean_entities.py

Cleans merged entity JSON.

Pipeline
--------
1. Remove duplicate entities
2. Normalize entity names
3. Remove invalid entities
4. Keep only valid agricultural entities
5. Generate statistics
"""

import os
import json
from collections import Counter


# =====================================================
# INPUT / OUTPUT
# =====================================================

INPUT_FILE = os.path.join(
    "output",
    "entities",
    "merged_entities.json"
)

OUTPUT_FILE = os.path.join(
    "output",
    "entities",
    "clean_entities.json"
)

REPORT_FILE = os.path.join(
    "output",
    "reports",
    "entity_cleaning_report.json"
)

os.makedirs(
    os.path.dirname(REPORT_FILE),
    exist_ok=True
)
# =====================================================
# INVALID VALUES
# =====================================================

INVALID_VALUES = {

    "",
    " ",
    "-",
    "--",
    "---",
    "na",
    "n/a",
    "none",
    "null",
    "unknown",
    "not mentioned",
    "nil",
    "others"

}


# =====================================================
# CROP NORMALIZATION
# =====================================================

CROP_MAP = {

    "paddy": "Rice",
    "paddy crop": "Rice",
    "rice crop": "Rice",

    "soyabean": "Soybean",
    "soy bean": "Soybean",

    "ground nut": "Groundnut",
    "ground nuts": "Groundnut",

    "maize crop": "Maize",

    "cotton crop": "Cotton",

    "gram crop": "Gram",

    "red gram": "Pigeon Pea",

    "tur": "Pigeon Pea",

    "green gram": "Moong",

    "black gram": "Urad"

}


# =====================================================
# VALID CROPS
# =====================================================

VALID_CROPS = {

    "Rice",
    "Wheat",
    "Maize",
    "Cotton",
    "Groundnut",
    "Soybean",
    "Mustard",
    "Gram",
    "Moong",
    "Urad",
    "Pigeon Pea",
    "Sugarcane",
    "Bajra",
    "Jowar",
    "Sesame",
    "Sunflower",
    "Castor",
    "Linseed",
    "Safflower",
    "Ragi",
    "Barley",
    "Potato",
    "Onion",
    "Tomato",
    "Chilli",
    "Turmeric",
    "Ginger",
    "Tea",
    "Coffee",
    "Rubber",
    "Coconut",
    "Arecanut",
    "Banana",
    "Mango",
    "Apple",
    "Orange",
    "Grapes",
    "Peas",
    "Lentil",
    "Cowpea",
    "Chickpea"

}


# =====================================================
# STATE NORMALIZATION
# =====================================================

STATE_MAP = {

    "u.p.": "Uttar Pradesh",
    "up": "Uttar Pradesh",

    "uttaranchal": "Uttarakhand",

    "nct delhi": "Delhi",

    "andaman & nicobar": "Andaman and Nicobar Islands",

    "j & k": "Jammu and Kashmir",

    "odissa": "Odisha"

}


# =====================================================
# VALID STATES
# =====================================================

VALID_STATES = {

    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",

    "Delhi",
    "Jammu and Kashmir",
    "Ladakh",
    "Puducherry",
    "Chandigarh",
    "Andaman and Nicobar Islands",
    "Dadra and Nagar Haveli and Daman and Diu",
    "Lakshadweep"

}


# =====================================================
# SEASON NORMALIZATION
# =====================================================

SEASON_MAP = {

    "rabi season": "Rabi",
    "rabi 2024-25": "Rabi",
    "rabi 2025": "Rabi",

    "kharif season": "Kharif",
    "kharif 2025": "Kharif",

    "zaid season": "Zaid",

    "summer season": "Summer"

}


VALID_SEASONS = {

    "Kharif",
    "Rabi",
    "Zaid",
    "Summer"

}


# =====================================================
# WEATHER NORMALIZATION
# =====================================================

WEATHER_MAP = {

    "heavy rainfall": "Heavy Rain",

    "heavy rain": "Heavy Rain",

    "light rain": "Light Rain",

    "very heavy rainfall": "Very Heavy Rain",

    "heatwave": "Heat Wave",

    "coldwave": "Cold Wave",

    "thunderstorm": "Thunderstorm"

}
# =====================================================
# HELPER FUNCTIONS
# =====================================================

def normalize_text(text):
    """
    Normalize text for comparison.
    """

    if text is None:
        return ""

    text = str(text).strip()

    text = " ".join(text.split())

    return text


def is_invalid(text):
    """
    Check whether an entity value is invalid.
    """

    if text is None:
        return True

    value = normalize_text(text).lower()

    return value in INVALID_VALUES


def normalize_crop(crop):
    """
    Normalize crop names.
    """

    crop = normalize_text(crop)

    key = crop.lower()

    if key in CROP_MAP:
        crop = CROP_MAP[key]

    return crop


def normalize_state(state):
    """
    Normalize state names.
    """

    state = normalize_text(state)

    key = state.lower()

    if key in STATE_MAP:
        state = STATE_MAP[key]

    return state


def normalize_season(season):
    """
    Normalize season names.
    """

    season = normalize_text(season)

    key = season.lower()

    if key in SEASON_MAP:
        season = SEASON_MAP[key]

    return season


def normalize_weather(weather):
    """
    Normalize weather names.
    """

    weather = normalize_text(weather)

    key = weather.lower()

    if key in WEATHER_MAP:
        weather = WEATHER_MAP[key]

    return weather
# =====================================================
# CLEANING STATISTICS
# =====================================================

statistics = {

    "chunks_processed": 0,

    "entities_before": 0,

    "entities_after": 0,

    "duplicates_removed": 0,

    "invalid_removed": 0,

    "normalized": 0

}
# =====================================================
# ADVANCED NORMALIZATION
# =====================================================

def clean_crop(crop):
    """
    Advanced crop normalization.
    """
    crop = normalize_crop(crop)

    crop = crop.replace(" Crop", "")
    crop = crop.replace(" crop", "")

    return crop.strip()


def clean_state(state):
    """
    Advanced state normalization.
    """
    state = normalize_state(state)

    state = state.replace(" State", "")
    state = state.replace(" state", "")

    return state.strip()


def clean_season(season):
    """
    Advanced season normalization.
    """
    season = normalize_season(season)

    season = season.replace(" Season", "")
    season = season.replace(" season", "")

    return season.strip()
# =====================================================
# CLEAN A SINGLE CHUNK
# =====================================================

def clean_chunk(chunk):
    """
    Clean all entities in one chunk.
    """

    cleaned_entities = []

    seen = set()

    entities = chunk.get("entities", [])

    statistics["chunks_processed"] += 1

    statistics["entities_before"] += len(entities)

    for entity in entities:

        label = entity.get("label", "").strip()

        text = entity.get("text", "").strip()

        score = entity.get("score", 1.0)

        # -----------------------------------------
        # Skip invalid entity
        # -----------------------------------------

        if is_invalid(text):

            statistics["invalid_removed"] += 1

            continue

        # -----------------------------------------
        # Normalize based on label
        # -----------------------------------------

        original = text

        if label == "Crop":

            text = clean_crop(text)

            if text not in VALID_CROPS:

                statistics["invalid_removed"] += 1

                continue

        elif label == "State":

            text = clean_state(text)

            if text not in VALID_STATES:

                statistics["invalid_removed"] += 1

                continue

        elif label == "Season":

            text = clean_season(text)

            if text not in VALID_SEASONS:

                statistics["invalid_removed"] += 1

                continue

        elif label == "Weather Event":

            text = normalize_weather(text)

        # -----------------------------------------
        # Count normalization
        # -----------------------------------------

        if original != text:

            statistics["normalized"] += 1

        # -----------------------------------------
        # Remove duplicates
        # -----------------------------------------

        key = (

            label.lower(),

            text.lower()

        )

        if key in seen:

            statistics["duplicates_removed"] += 1

            continue

        seen.add(key)

        entity["text"] = text

        entity["score"] = round(score, 3)

        cleaned_entities.append(entity)

    statistics["entities_after"] += len(cleaned_entities)

    chunk["entities"] = cleaned_entities

    return chunk
# =====================================================
# MAIN
# =====================================================

def main():

    if not os.path.exists(INPUT_FILE):

        print("\nMerged entity file not found.")

        return

    with open(

        INPUT_FILE,

        "r",

        encoding="utf-8"

    ) as f:

        data = json.load(f)

    cleaned_chunks = []

    for chunk in data.get("chunks", []):

        cleaned_chunks.append(

            clean_chunk(chunk)

        )

    cleaned_data = {

        "metadata": data.get("metadata", {}),

        "chunks": cleaned_chunks

    }

    # ---------------------------------------------
    # Save Clean JSON
    # ---------------------------------------------

    with open(

        OUTPUT_FILE,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            cleaned_data,

            f,

            indent=4,

            ensure_ascii=False

        )

    # ---------------------------------------------
    # Save Cleaning Report
    # ---------------------------------------------

    with open(

        REPORT_FILE,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            statistics,

            f,

            indent=4,

            ensure_ascii=False

        )

    # ---------------------------------------------
    # Console Report
    # ---------------------------------------------

    print("\n")

    print("=" * 70)

    print(" ENTITY CLEANING REPORT ")

    print("=" * 70)

    print(f"Chunks Processed      : {statistics['chunks_processed']}")

    print(f"Entities Before       : {statistics['entities_before']}")

    print(f"Entities After        : {statistics['entities_after']}")

    print()

    print(f"Duplicates Removed    : {statistics['duplicates_removed']}")

    print(f"Invalid Removed       : {statistics['invalid_removed']}")

    print(f"Normalized Entities   : {statistics['normalized']}")

    print()

    print(f"Clean JSON Saved      : {OUTPUT_FILE}")

    print(f"Report Saved          : {REPORT_FILE}")

    print("=" * 70)

    print("\nEntity Cleaning Completed Successfully.")


# =====================================================

if __name__ == "__main__":

    main()