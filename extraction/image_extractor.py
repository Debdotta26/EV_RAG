# import fitz
# import os


# def extract_images(doc, page_number, document_name, output_folder):
#     """
#     Extract all images from a page.

#     Parameters:
#         doc             : PyMuPDF document
#         page_number     : Page index (0-based)
#         document_name   : PDF file name
#         output_folder   : output/images

#     Returns:
#         List containing image information.
#     """

#     images = []

#     page = doc.load_page(page_number)

#     image_list = page.get_images(full=True)

#     if len(image_list) == 0:
#         return images

#     # Folder for this document
#     document_folder = os.path.join(
#         output_folder,
#         os.path.splitext(document_name)[0]
#     )

#     os.makedirs(document_folder, exist_ok=True)

#     image_count = 1

#     for img in image_list:

#         try:

#             xref = img[0]

#             pix = fitz.Pixmap(doc, xref)

#             if pix.alpha:
#                 pix = fitz.Pixmap(fitz.csRGB, pix)

#             image_name = f"page_{page_number+1}_image_{image_count}.png"

#             image_path = os.path.join(
#                 document_folder,
#                 image_name
#             )

#             pix.save(image_path)

#             images.append({

#                 "image_id": image_count,

#                 "image_name": image_name,

#                 "image_path": image_path

#             })

#             pix = None

#             image_count += 1

#         except Exception as e:

#             print(
#                 f"Image extraction failed "
#                 f"(Page {page_number+1}) : {e}"
#             )

#     return images

import fitz
import os


def extract_images(doc, page_number, document_name, output_folder):
    """
    Extract all images from a page.

    Parameters:
        doc             : PyMuPDF document
        page_number     : Page index (0-based)
        document_name   : PDF file name
        output_folder   : Output folder for extracted images

    Returns:
        List of extracted image information.
    """

    images = []

    page = doc.load_page(page_number)
    image_list = page.get_images(full=True)

    if not image_list:
        return images

    # Create document-specific folder
    document_folder = os.path.join(
        output_folder,
        os.path.splitext(document_name)[0]
    )

    os.makedirs(document_folder, exist_ok=True)

    for image_count, img in enumerate(image_list, start=1):

        try:

            xref = img[0]

            pix = fitz.Pixmap(doc, xref)

            if pix.alpha:
                pix = fitz.Pixmap(fitz.csRGB, pix)

            image_name = f"page_{page_number + 1}_image_{image_count}.png"

            image_path = os.path.join(
                document_folder,
                image_name
            )

            pix.save(image_path)

            images.append({

                "image_id": image_count,

                "page": page_number + 1,

                "xref": xref,

                "image_name": image_name,

                "image_path": image_path,

                "width": pix.width,

                "height": pix.height,

                "format": "PNG",

                "extraction_tool": "PyMuPDF"

            })

            pix = None

        except Exception as e:

            print(
                f"Image extraction failed "
                f"(Page {page_number + 1}): {e}"
            )

    return images