"""
prompt.py

Defines the prompt template used to ground LLM answers strictly in
retrieved context, and a helper to assemble the final prompt string
from a question and a list of retrieved chunks.
"""

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

# The system instruction is the primary lever for hallucination
# reduction. Each numbered rule below addresses a specific failure
# mode we want to prevent:
#
# 1. "use ONLY the context" -> blocks the model from filling gaps
#    with outside/parametric knowledge.
# 2. "If the context does not contain enough information, say so" ->
#    gives the model an explicit, acceptable way to express
#    uncertainty instead of guessing.
# 3. "Do not make up information" -> redundant with #1 by design;
#    repetition in instructions does measurably reduce slip-through
#    in practice.
RAG_SYSTEM_INSTRUCTIONS = """You are a precise, careful AI designed to provide information about the company (Prescient Technologies). Answer questions using ONLY the information provided in the context below.

Rules you must follow:
1. Use ONLY the information in the context to answer. Do not use any outside knowledge.
2. If the context does not contain enough information to answer the question, respond exactly with: "I don't have enough information in the provided context to answer that."
3. Do not make up, infer, or guess information that is not explicitly present in the context.
4. Keep your answer concise and directly responsive to the question.
5. If the question is a greeting (e.g., "Hello", "Hi"), respond politely and briefly (e.g., "Hello! How can I help you with information about Prescient Technologies today?"). Do not attempt to answer it as a factual query.
6. If the user asks about a specific technology or project not present in the context, respond with: "I don't have specific information about [technology/project] in my current knowledge base."
7. If the question asks about Prescient Technologies in general (e.g., "Tell me about Prescient Technologies", "What does Prescient Technologies do?"), provide a comprehensive summary based on the context.
8. If the user asks about careers or jobs, politely redirect them to the official careers page: "You can find information about careers at Prescient Technologies on our official careers page."
9. If use asks you who YOU are, tell them you are an AI of Precient Technologies present to guide them about the information of the company.
"""

RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", RAG_SYSTEM_INSTRUCTIONS),
        (
            "human",
            "Context:\n{context}\n\nQuestion:\n{question}",
        ),
    ]
)


def format_context(chunks: list[Document]) -> str:
    """
    Join retrieved chunks into a single context string for the prompt.

    Why number each chunk ([Chunk 1], [Chunk 2], ...) instead of just
    concatenating raw text:
    It gives the model (and you, when debugging) a clear way to see
    where one retrieved chunk ends and another begins, which matters
    when chunks come from different, possibly contradictory, parts
    of the source document.
    """
    return "\n\n".join(
        f"[Chunk {i + 1}]\n{chunk.page_content}"
        for i, chunk in enumerate(chunks)
    )


def build_prompt(question: str, chunks: list[Document]) -> list:
    """
    Assemble the final list of chat messages to send to the LLM.

    Returns a list of LangChain message objects (not a raw string) -
    ChatOpenAI's .invoke() expects this format. Returning the
    formatted messages here (rather than just text) keeps the
    system/human role separation intact all the way to the API call.
    """
    context_str = format_context(chunks)
    return RAG_PROMPT.format_messages(context=context_str, question=question)