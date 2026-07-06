"""
retrieve.py

Online pipeline (retrieval half): loads the previously saved FAISS
index from disk and exposes a function to fetch the Top-K most
relevant chunks for a given user question.
"""

from pathlib import Path

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from config import settings


def load_vectorstore(vectorstore_dir: str, embedding_model: str) -> FAISS:
    """
    Load a previously saved FAISS index from disk.

    Why we need to pass `embedding_model` again here, identical to
    ingestion: FAISS.load_local() needs an embeddings object to embed
    *future* queries (it doesn't need it to read the already-computed
    vectors from disk). If this model doesn't match the one used
    during ingest.py, query vectors and stored chunk vectors will
    live in different embedding spaces and similarity scores become
    meaningless.

    Why allow_dangerous_deserialization=True is required:
    FAISS's on-disk format uses Python's pickle for the docstore
    component. LangChain gates this behind an explicit flag because
    unpickling arbitrary files is a security risk *if the file came
    from an untrusted source*. Here it's safe because we generated
    this file ourselves in ingest.py.
    """
    path = Path(vectorstore_dir)
    if not path.exists():
        raise FileNotFoundError(
            f"No vectorstore found at '{vectorstore_dir}'. "
            f"Did you run ingest.py first?"
        )

    embeddings = OpenAIEmbeddings(model=embedding_model)
    return FAISS.load_local(
        folder_path=vectorstore_dir,
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )


def retrieve_top_k(vectorstore: FAISS, question: str, k: int) -> list[Document]:
    """
    Embed the question and return the k most similar chunks.

    Why similarity_search() and not similarity_search_with_score():
    app.py only needs the chunk content to build the prompt, not the
    raw similarity scores. If you later want to log/debug retrieval
    quality, similarity_search_with_score() is the one to swap in —
    isolating that choice to this single function keeps the change
    contained.
    """
    return vectorstore.similarity_search(query=question, k=k)


def get_relevant_chunks(question: str) -> list[Document]:
    """
    Convenience entry point used by app.py: loads the vectorstore and
    returns the Top-K relevant chunks for a question, using settings
    from config.py.

    Why not cache the loaded vectorstore at module level:
    Tempting for performance, but app.py will be the one deciding the
    lifecycle (e.g. loading it once at startup vs. per-request) — see
    that file for how this gets used so we don't reload the index on
    every single query.
    """
    vectorstore = load_vectorstore(settings.vectorstore_dir, settings.embedding_model)
    return retrieve_top_k(vectorstore, question, settings.top_k)