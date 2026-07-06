# RAG Project

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system
using: - Python 3.11+ - LangChain - OpenAI - FAISS - TXT knowledge base

## Objectives

-   Learn RAG from first principles.
-   Build a modular, production-style codebase.
-   Avoid high-level helper chains that hide the retrieval pipeline.
-   Keep the system easy to extend.

## Tech Stack

-   LangChain
-   langchain-openai
-   langchain-community
-   FAISS
-   OpenAI
-   python-dotenv
-   tiktoken

## Project Structure

``` text
rag_project/
├── README.md
├── CLAUDE.md
├── ARCHITECTURE.md
├── requirements.txt
├── .env
├── data/
│   └── knowledge.txt
├── vectorstore/
├── config.py
├── ingest.py
├── retrieve.py
├── prompt.py
└── app.py
```

## End Goal

Answer user questions using only retrieved context from the TXT
knowledge base.
