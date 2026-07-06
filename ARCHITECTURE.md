# RAG Architecture

## Offline Pipeline

1.  Load knowledge.txt
2.  Split into chunks using RecursiveCharacterTextSplitter
3.  Generate OpenAI embeddings
4.  Store embeddings in FAISS
5.  Save FAISS index locally

## Online Pipeline

User Question → Generate embedding → Search FAISS → Retrieve Top-K
chunks → Build custom prompt → Send prompt to ChatOpenAI → Return answer

## Responsibilities

### config.py

Environment variables and model configuration.

### ingest.py

Loads documents, chunks text, creates embeddings, builds FAISS index.

### retrieve.py

Loads FAISS index and retrieves relevant chunks.

### prompt.py

Contains prompt template that forces answers to rely only on retrieved
context.

### app.py

Coordinates the complete RAG workflow.

## Concepts Claude Should Teach

-   RAG
-   Chunking
-   Chunk overlap
-   Embeddings
-   Vector databases
-   FAISS
-   Cosine similarity
-   Top-K retrieval
-   Prompt engineering
-   Hallucination reduction
-   LangChain architecture

## Future Extensions

-   PDF support
-   DOCX support
-   Metadata filtering
-   Hybrid search (BM25 + Vector)
-   Re-ranking
-   Conversation memory
-   FastAPI backend
-   Streamlit/React frontend
