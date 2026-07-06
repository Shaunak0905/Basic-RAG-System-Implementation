from retrieve import get_relevant_chunks

chunks = get_relevant_chunks("What is this knowledge base about?")
for i, chunk in enumerate(chunks, 1):
    print(f"--- Chunk {i} ---")
    print(chunk.page_content)
    print()