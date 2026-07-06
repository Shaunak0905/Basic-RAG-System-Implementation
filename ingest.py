"""
ingest.py

Offline pipeline: loads the raw knowledge base, splits it into chunks,
generates embeddings for each chunk, and persists a FAISS index to disk.

Run this script directly whenever data/knowledge.txt changes:
    python ingest.py
"""

from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from config import settings


def load_knowledge_text(data_path: str) -> str:
    """
    Read the raw knowledge base file from disk.

    Why a dedicated function instead of inlining open() in main():
    isolating I/O makes it trivial to swap in PDF/DOCX loaders later
    (see ARCHITECTURE.md "Future Extensions") without touching the
    chunking or embedding logic below.
    """
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Knowledge file not found at '{data_path}'. "
            f"Did you create data/knowledge.txt?"
        )
    return path.read_text(encoding="utf-8")


def chunk_text(raw_text: str) -> list[Document]:
    """
    Split raw text into one chunk per paragraph, using blank lines
    as the boundary.

    Why no chunk_size/chunk_overlap here, unlike the character-based
    approach: paragraph chunking doesn't size-cap chunks - each
    paragraph becomes exactly one chunk, whatever length it happens
    to be. This trades predictable chunk size for semantic coherence
    (each chunk = one author-intended idea), which is the right
    tradeoff IF your knowledge.txt has clean, well-formed paragraphs.
    """
    paragraphs = [p.strip() for p in raw_text.split("\n\n")]
    paragraphs = [p for p in paragraphs if p]  # drop empty strings from extra blank lines
    return [Document(page_content=p) for p in paragraphs]


def build_vectorstore(documents: list[Document], embedding_model: str) -> FAISS:
    """
    Generate embeddings for each document chunk and build a FAISS
    index in memory.

    Why FAISS.from_documents() and not a manual loop calling the
    embeddings API per chunk:
    from_documents batches the embedding calls internally, which is
    both faster and avoids hitting OpenAI's rate limits with one
    request per chunk on a large knowledge base.
    """
    embeddings = OpenAIEmbeddings(model=embedding_model)
    return FAISS.from_documents(documents=documents, embedding=embeddings)


def save_vectorstore(vectorstore: FAISS, save_dir: str) -> None:
    """
    Persist the FAISS index to disk so retrieve.py and app.py can
    load it later without re-embedding anything.
    """
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(save_dir)


def main() -> None:
    print(f"Loading knowledge base from: {settings.data_path}")
    raw_text = load_knowledge_text(settings.data_path)

    print("Chunking text by paragraph...")
    documents = chunk_text(raw_text)
    print(f"Produced {len(documents)} chunks.")

    print(f"Generating embeddings with model: {settings.embedding_model}...")
    vectorstore = build_vectorstore(documents, settings.embedding_model)

    print(f"Saving FAISS index to: {settings.vectorstore_dir}")
    save_vectorstore(vectorstore, settings.vectorstore_dir)

    print("Ingestion complete.")


if __name__ == "__main__":
    main()