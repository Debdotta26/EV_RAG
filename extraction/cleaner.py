import re


def clean_content(content):
    """
    Clean extracted PDF text blocks.

    Removes:
    - excessive whitespace
    - empty blocks
    - repeated line breaks
    - unnecessary spaces

    Keeps:
    - headings
    - warnings
    - safety instructions
    - important technical information
    """

    cleaned = []

    for block in content:

        # -------------------------------------------------
        # Handle dictionary-style content blocks
        # -------------------------------------------------
        if isinstance(block, dict):

            block_copy = block.copy()

            if "text" in block_copy and isinstance(block_copy["text"], str):

                text = block_copy["text"]

                # Normalize whitespace
                text = re.sub(r"[ \t]+", " ", text)

                # Normalize excessive newlines
                text = re.sub(r"\n{3,}", "\n\n", text)

                # Remove leading/trailing whitespace
                text = text.strip()

                # Keep non-empty blocks
                if text:
                    block_copy["text"] = text
                    cleaned.append(block_copy)

            else:
                cleaned.append(block_copy)

        # -------------------------------------------------
        # Handle plain string blocks
        # -------------------------------------------------
        elif isinstance(block, str):

            text = re.sub(r"[ \t]+", " ", block)

            text = re.sub(r"\n{3,}", "\n\n", text)

            text = text.strip()

            if text:
                cleaned.append(text)

        # -------------------------------------------------
        # Keep other structures unchanged
        # -------------------------------------------------
        else:

            cleaned.append(block)

    return cleaned