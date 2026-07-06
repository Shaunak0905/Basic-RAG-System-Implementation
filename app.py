"""
app.py

Coordinates the complete RAG workflow:
load vectorstore once -> loop: question -> retrieve -> build prompt
-> call ChatOpenAI -> print answer.

Run with:
    python app.py
"""

from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

from config import settings
from retrieve import load_vectorstore, retrieve_top_k
from prompt import build_prompt

def _extract_text(content: str | list) -> str:
    """
    Normalize ChatOpenAI's response.content into a plain string.

    Why this is needed: AIMessage.content is typed as
    str | list[str | dict[Any, Any]] because some providers can
    return multi-part content (tool calls, image blocks, etc).
    For a plain ChatOpenAI text completion this will always be a
    str in practice, but the type checker doesn't know that - so we
    narrow it explicitly here instead of casting/ignoring the error.
    """
    if isinstance(content, str):
        return content

    # Defensive fallback: join any string parts, skip non-string
    # parts (e.g. dicts representing tool calls) rather than crashing.
    parts = [part for part in content if isinstance(part, str)]
    return "\n".join(parts)

def get_answer(
    question: str,
    vectorstore,
    llm: ChatOpenAI,
) -> tuple[str, list[Document]]:
    chunks = retrieve_top_k(vectorstore, question, settings.top_k)
    messages = build_prompt(question, chunks)
    response = llm.invoke(messages)
    answer = _extract_text(response.content)
    return answer, chunks


def run_repl() -> None:
    """
    Simple command-line loop: load resources once, then answer
    questions until the user quits.
    """
    print(f"Loading vectorstore from: {settings.vectorstore_dir}")
    vectorstore = load_vectorstore(settings.vectorstore_dir, settings.embedding_model)

    llm = ChatOpenAI(
        model=settings.chat_model,
        temperature=settings.chat_temperature,
    )

    print("RAG system ready. Type a question, or 'quit' to exit.\n")

    while True:
        question = input("Question: ").strip()
        if question.lower() in {"quit", "exit"}:
            print("Goodbye.")
            break
        if not question:
            continue

        answer, chunks = get_answer(question, vectorstore, llm)

        print(f"\nAnswer: {answer}\n")
        print(f"(Retrieved {len(chunks)} chunks)")
        for i, chunk in enumerate(chunks, 1):
            preview = chunk.page_content[:80].replace("\n", " ")
            print(f"  [{i}] {preview}...")
        print()


if __name__ == "__main__":
    run_repl()