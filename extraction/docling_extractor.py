from docling.document_converter import DocumentConverter
import os
import json
import traceback

# Create the converter ONLY ONCE
converter = DocumentConverter()


def extract_docling(pdf_path, output_folder):
    """
    Extract PDF using Docling and save:
    1. Markdown
    2. Plain Text
    3. JSON
    """

    try:

        result = converter.convert(pdf_path)

        document = result.document

        name = os.path.splitext(os.path.basename(pdf_path))[0]

        markdown_dir = os.path.join(output_folder, "markdown")
        text_dir = os.path.join(output_folder, "text")
        json_dir = os.path.join(output_folder, "json")

        os.makedirs(markdown_dir, exist_ok=True)
        os.makedirs(text_dir, exist_ok=True)
        os.makedirs(json_dir, exist_ok=True)

        markdown = document.export_to_markdown()

        text = document.export_to_text()

        data = {
            "document_name": name,
            "markdown": markdown,
            "text": text
        }

        with open(
            os.path.join(markdown_dir, name + ".md"),
            "w",
            encoding="utf-8"
        ) as f:
            f.write(markdown)

        with open(
            os.path.join(text_dir, name + ".txt"),
            "w",
            encoding="utf-8"
        ) as f:
            f.write(text)

        with open(
            os.path.join(json_dir, name + ".json"),
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(f"✓ {name}")

    except Exception as e:

        print(f"✗ Failed : {pdf_path}")
        print(e)
        traceback.print_exc()