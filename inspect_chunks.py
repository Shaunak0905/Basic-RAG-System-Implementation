"""
inspect_chunks.py

Debug utility: runs only the chunking step (no embeddings, no FAISS,
no API calls) and prints the resulting chunks for inspection.

Run with:
    python inspect_chunks.py
"""

from config import settings
from ingest import load_knowledge_text, chunk_text


def main() -> None:
    raw_text = load_knowledge_text(settings.data_path)
    documents = chunk_text(raw_text)

    print(f"Produced {len(documents)} chunks.\n")
    for i, doc in enumerate(documents, 1):
        print(f"--- Chunk {i} ({len(doc.page_content)} chars) ---")
        print(doc.page_content)
        print()


if __name__ == "__main__":
    main()