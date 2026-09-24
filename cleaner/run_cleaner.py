import os
import json

from cleaner import clean_json

# -----------------------------
# Paths
# -----------------------------

INPUT_FOLDER = os.path.join(
    "extraction",
    "output",
    "merged"
)

OUTPUT_FOLDER = os.path.join(
    "extraction",
    "output",
    "cleaned"
)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

files = [

    f

    for f in os.listdir(INPUT_FOLDER)

    if f.endswith(".json")

]

print(f"\nFound {len(files)} JSON files.\n")

for file in files:

    input_path = os.path.join(INPUT_FOLDER, file)

    with open(input_path, "r", encoding="utf-8") as f:

        data = json.load(f)

    cleaned = clean_json(data)

    output_path = os.path.join(OUTPUT_FOLDER, file)

    with open(output_path, "w", encoding="utf-8") as f:

        json.dump(
            cleaned,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"✔ Cleaned: {file}")

print("\nFinished cleaning all files.")