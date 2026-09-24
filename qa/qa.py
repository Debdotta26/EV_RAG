"""
qa.py

Simple non-LLM question answering system
for EV manuals.

Pipeline:

Question
   ↓
BM25 retrieval
   ↓
Keyword matching
   ↓
Entity matching
   ↓
Relevant chunks
   ↓
Sentence extraction
   ↓
Exact text from manual
"""

from pathlib import Path

from retriever import create_retriever
from answerer import get_answer


# ============================================================
# CONFIGURATION
# ============================================================

# CHANGE THIS PATH
CHUNKS_FILE = Path(
    "output\\entities\\EV9-Owners-Manual_chunks.json"
)

TOP_K = 5


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("        EV MANUAL QUESTION ANSWERING SYSTEM")
    print("=" * 60)

    print("\nLoading manual chunks...")

    retriever = create_retriever(
        CHUNKS_FILE
    )

    print("\nSystem ready.")
    print("Ask a question about the EV manual.")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("Question: ").strip()

        if question.lower() == "exit":
            print("\nExiting...")
            break

        if not question:
            continue

        # ----------------------------------------------------
        # RETRIEVE
        # ----------------------------------------------------

        results = retriever.search(
            question,
            top_k=TOP_K
        )

        if not results:

            print(
                "\nNo relevant information found "
                "in the manuals.\n"
            )

            continue

        # ----------------------------------------------------
        # EXTRACT ANSWER
        # ----------------------------------------------------

        answer = get_answer(
            question,
            results
        )

        if answer is None:

            print(
                "\nI could not find a relevant answer "
                "in the available EV manuals.\n"
            )

            continue

        # ----------------------------------------------------
        # DISPLAY ANSWER
        # ----------------------------------------------------

        chunk = answer["chunk"]

        print("\n" + "-" * 60)

        print("ANSWER:")
        print(answer["answer"])

        print("\nSOURCE:")

        # Try different possible metadata names
        document = (
            chunk.get("document")
            or chunk.get("filename")
            or chunk.get("file_name")
            or chunk.get("source")
            or "EV Manual"
        )

        page_start = (
            chunk.get("page_start")
            or chunk.get("page")
        )

        page_end = chunk.get("page_end")

        print(f"Manual: {document}")

        if page_start and page_end:
            print(
                f"Pages: {page_start}-{page_end}"
            )

        elif page_start:
            print(
                f"Page: {page_start}"
            )

        print("-" * 60 + "\n")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()