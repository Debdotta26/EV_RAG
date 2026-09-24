"""
bm25_retriever.py

BM25-assisted retrieval for EV manual entity extraction.

BM25 is used to identify the relevance of each chunk
to different EV-related entity categories before GLiNER
performs the actual entity extraction.
"""

import re

from rank_bm25 import BM25Okapi


# =====================================================
# EV DOMAIN QUERY TERMS
# =====================================================

ENTITY_QUERIES = {

    "Vehicle Model": """
        vehicle model car model automobile vehicle name
        model variant trim version
    """,

    "Vehicle": """
        vehicle car automobile EV electric vehicle
        passenger vehicle
    """,

    "Battery": """
        battery high voltage battery HV battery
        lithium ion battery battery pack battery capacity
        state of charge SOC battery level
    """,

    "Charging": """
        charge charging EV charging electric charging
        charging procedure charging process charge level
    """,

    "Charger": """
        charger charging equipment charging device
        portable charger wall charger home charger
    """,

    "Charging Port": """
        charging port charge port charging connector
        inlet connector socket charging socket
    """,

    "Charging Station": """
        charging station charging point public charger
        charging infrastructure EV station
    """,

    "Charging Time": """
        charging time charging duration charge time
        charging period minutes hours
    """,

    "Charging Power": """
        charging power power output kW kilowatt
        charging capacity power rating
    """,

    "Charging Voltage": """
        charging voltage voltage volts V AC voltage DC voltage
        electrical voltage
    """,

    "Charging Current": """
        charging current current ampere amps A
        electrical current amperage
    """,

    "Range": """
        driving range vehicle range electric range
        distance range remaining range
        estimated range
    """,

    "Driving Mode": """
        driving mode drive mode mode ECO SPORT NORMAL
        comfort snow terrain mode
    """,

    "Regenerative Braking": """
        regenerative braking regeneration regen
        regenerative brake energy recovery
        regenerative braking level
    """,

    "Brake": """
        brake braking brake pedal braking system
        brake fluid parking brake emergency brake
    """,

    "Tyre": """
        tyre tire tires tyres wheel wheel assembly
        tire size tire condition
    """,

    "Tyre Pressure": """
        tyre pressure tire pressure tire inflation
        pressure psi kPa bar recommended pressure
    """,

    "Motor": """
        electric motor motor drive motor propulsion
        motor power motor speed torque
    """,

    "Warning": """
        warning warning message warning light
        caution notice warning indicator
    """,

    "Safety": """
        safety safe danger hazard precaution
        safety instructions emergency protective
    """,

    "Maintenance": """
        maintenance service inspection replacement
        maintenance schedule periodic maintenance
        check cleaning lubrication
    """,

    "Service": """
        service dealer authorized dealer service center
        repair workshop technician
    """,

    "Fault": """
        fault fault condition malfunction problem
        failure system fault vehicle fault
    """,

    "Error": """
        error error message error code diagnostic
        fault code warning message
    """,

    "Dashboard": """
        dashboard instrument cluster instrument panel
        driver information display cluster
    """,

    "Display": """
        display screen information screen LCD
        touchscreen message indicator
    """,

    "Infotainment": """
        infotainment audio multimedia media system
        radio music speaker entertainment
    """,

    "Navigation": """
        navigation map route destination GPS
        navigation system location route guidance
    """,

    "Bluetooth": """
        bluetooth pairing wireless phone smartphone
        bluetooth connection device connection
    """,

    "V2L": """
        V2L vehicle to load vehicle-to-load
        external power power supply electrical appliance
    """,

    "ADAS": """
        ADAS advanced driver assistance driver assistance
        lane keeping lane departure blind spot
        adaptive cruise collision avoidance
    """,

    "Temperature": """
        temperature thermal hot cold overheating
        degrees Celsius battery temperature
        motor temperature ambient temperature
    """,

    "Location": """
        location position place destination address
        charging location vehicle location
    """,

    "Button": """
        button switch control knob lever press
        push button steering wheel button
    """,

    "Indicator": """
        indicator warning lamp light signal
        turn indicator status indicator
        dashboard indicator
    """
}


# =====================================================
# TOKENIZER
# =====================================================

def tokenize(text):
    """
    Convert text into lowercase alphanumeric tokens.
    """

    return re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )


# =====================================================
# BUILD BM25 INDEX
# =====================================================

def build_bm25_index(chunks):
    """
    Build a BM25 index from chunk text.
    """

    corpus = [
        tokenize(chunk.get("text", ""))
        for chunk in chunks
    ]

    # Prevent empty documents from causing problems.
    corpus = [
        tokens if tokens else ["empty"]
        for tokens in corpus
    ]

    bm25 = BM25Okapi(corpus)

    return bm25


# =====================================================
# GET CATEGORY SCORES
# =====================================================

def get_category_scores(chunks):
    """
    Calculate BM25 relevance scores for every EV category
    for every chunk.

    Returns:

    [
        {
            "chunk_index": 0,
            "bm25_scores": {
                "Battery": 12.42,
                "Charging": 8.31,
                ...
            }
        }
    ]
    """

    if not chunks:
        return []

    bm25 = build_bm25_index(chunks)

    results = []

    # Tokenize each category query only once.
    tokenized_queries = {
        label: tokenize(query)
        for label, query in ENTITY_QUERIES.items()
    }

    # Calculate BM25 scores for each category.
    category_scores = {}

    for label, query_tokens in tokenized_queries.items():

        all_scores = bm25.get_scores(query_tokens)

        category_scores[label] = all_scores

    # Convert scores into chunk-wise results.
    for index, chunk in enumerate(chunks):

        scores = {}

        for label in ENTITY_QUERIES:

            scores[label] = round(
                float(category_scores[label][index]),
                4
            )

        results.append({
            "chunk_index": index,
            "bm25_scores": scores
        })

    return results


# =====================================================
# GET TOP CATEGORIES FOR A CHUNK
# =====================================================

def get_top_categories(
    bm25_scores,
    top_k=5
):
    """
    Return the most relevant EV categories for a chunk.
    """

    sorted_categories = sorted(
        bm25_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        category
        for category, score in sorted_categories[:top_k]
        if score > 0
    ]