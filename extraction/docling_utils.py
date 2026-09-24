import os


def create_output_folders(output_folder):

    markdown = os.path.join(output_folder, "markdown")
    text = os.path.join(output_folder, "text")
    json_folder = os.path.join(output_folder, "json")

    os.makedirs(markdown, exist_ok=True)
    os.makedirs(text, exist_ok=True)
    os.makedirs(json_folder, exist_ok=True)

    return markdown, text, json_folder