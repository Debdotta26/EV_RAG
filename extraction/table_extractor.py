# import pdfplumber


# def extract_tables(pdf_path, page_number):
#     """
#     Extract all tables from a specific page.

#     Returns:
#         List of tables.
#         Each table is stored as a list of rows.
#     """

#     tables = []

#     try:

#         with pdfplumber.open(pdf_path) as pdf:

#             page = pdf.pages[page_number]

#             extracted_tables = page.extract_tables()

#             if extracted_tables:

#                 for table_id, table in enumerate(extracted_tables, start=1):

#                     cleaned_table = []

#                     for row in table:

#                         cleaned_row = []

#                         if row is None:
#                             continue

#                         for cell in row:

#                             if cell is None:
#                                 cleaned_row.append("")
#                             else:
#                                 cleaned_row.append(cell.strip())

#                         cleaned_table.append(cleaned_row)

#                     tables.append(
#                         {
#                             "table_id": table_id,
#                             "rows": cleaned_table
#                         }
#                     )

#     except Exception as e:

#         print(f"Error extracting tables from Page {page_number+1}: {e}")

#     return tables

import pdfplumber


def extract_tables(pdf_path, page_number):
    """
    Extract all tables from a specific page.

    Returns:
        List of structured tables.
    """

    tables = []

    try:

        with pdfplumber.open(pdf_path) as pdf:

            page = pdf.pages[page_number]

            extracted_tables = page.extract_tables()

            if extracted_tables:

                for table_id, table in enumerate(extracted_tables, start=1):

                    cleaned_table = []

                    if not table:
                        continue

                    for row in table:

                        if row is None:
                            continue

                        cleaned_row = []

                        for cell in row:

                            cleaned_row.append(
                                cell.strip() if cell else ""
                            )

                        cleaned_table.append(cleaned_row)

                    if not cleaned_table:
                        continue

                    tables.append({

                        "table_id": table_id,

                        "page": page_number + 1,

                        "rows_count": len(cleaned_table),

                        "columns_count": max(
                            (len(row) for row in cleaned_table),
                            default=0
                        ),

                        "header": cleaned_table[0] if cleaned_table else [],

                        "rows": cleaned_table,

                        "extraction_tool": "pdfplumber"

                    })

    except Exception as e:

        print(f"Error extracting tables from Page {page_number + 1}: {e}")

    return tables