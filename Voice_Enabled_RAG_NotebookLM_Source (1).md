# Voice-Enabled AI RAG Assistant – Technical Design Document
## NotebookLM Source Document

---

# 1. Executive Summary

This project proposes a voice-enabled Retrieval-Augmented Generation (RAG) assistant that allows users to interact with an organization's knowledge base through natural speech. Instead of typing questions, users speak into the system, which converts speech into text, retrieves relevant organizational information, generates an accurate response using a Large Language Model (LLM), converts that response back into speech, and presents it through a real-time talking AI avatar.

The primary engineering objectives are:

- Low end-to-end latency
- Natural conversational experience
- Streaming architecture
- High-quality English and Hindi support
- Cost-effective deployment
- Modular architecture

---

# 2. Problem Statement

Traditional chatbots require users to type queries and often provide generic responses without grounding in organizational knowledge.

The proposed solution combines:
- Speech Recognition
- Retrieval-Augmented Generation
- Large Language Models
- Speech Synthesis
- Live AI Avatars

to create a more natural and informative interaction experience.

---

# 3. System Goals

## Functional Goals

- Accept voice input.
- Retrieve relevant information from a private knowledge base.
- Generate context-aware answers.
- Speak responses naturally.
- Display a synchronized AI avatar.

## Non-Functional Goals

- Low latency
- High response accuracy
- Streaming communication
- Modular components
- Easy model replacement

---

# 4. End-to-End Pipeline

User Speech

↓

Sarvam Saaras v3 (Streaming Speech-to-Text)

↓

RAG Retrieval Pipeline

↓

GPT-4o Mini

↓

Sarvam Bulbul v3 (Streaming Text-to-Speech)

↓

Simli Live Avatar (Planned)

↓

User receives spoken response with lip-synced avatar.

---

# 5. Component Breakdown

## A. Speech-to-Text (STT)

### Selected Model
**Sarvam Saaras v3**

### Reasons

- Optimized for Indian English and Hindi.
- Streaming support.
- Low latency.
- Competitive pricing.
- High transcription quality.

### Alternatives Evaluated

| Model | Decision |
|--------|----------|
| Whisper Streaming | Good accuracy but more implementation effort. |
| ElevenLabs Scribe Realtime | Excellent quality but higher pricing. |
| Deepgram | Strong streaming, less optimized for Indian languages. |
| AssemblyAI | Good APIs but less attractive cost/performance balance. |
| Gladia | Evaluated as an alternative. |

Conclusion: Sarvam Saaras v3 offered the best balance of latency, language support, and cost.

---

## B. Retrieval-Augmented Generation (RAG)

The RAG pipeline grounds every answer in the organization's knowledge base rather than relying only on the LLM's internal knowledge.

Typical flow:

1. User query
2. Embedding generation
3. Similarity search
4. Retrieval of relevant documents
5. Context injection
6. GPT-4o Mini response generation

Benefits:

- Reduced hallucinations
- Organization-specific answers
- Easier knowledge updates
- Improved reliability

---

## C. Vector Database

### Current Prototype

FAISS

### Still Under Evaluation

- ChromaDB
- Qdrant
- Pinecone (enterprise option)

### FAISS

Advantages
- Extremely fast
- Lightweight
- Excellent for local prototypes

Limitations
- Fewer management features

### ChromaDB

Advantages
- Better developer experience
- Persistent storage
- Rich metadata handling

Trade-off
- Slightly heavier than FAISS

Final selection will be based on scalability, maintainability, and retrieval performance.

---

## D. Large Language Model

### Selected Model

GPT-4o Mini

Reasons

- Strong reasoning capability
- Good response quality
- Cost-effective
- Well suited for RAG applications

The LLM never answers directly from memory alone. Retrieved organizational context is injected into every prompt before response generation.

---

## E. Text-to-Speech

### Selected Model

Sarvam Bulbul v3

Reasons

- Natural speech synthesis
- Indian language support
- Streaming capability
- Competitive pricing

Alternatives Evaluated

- ElevenLabs Flash
- ElevenLabs Multilingual
- OpenAI TTS
- Cartesia

Bulbul v3 was selected because it provides the best balance between quality, latency, and support for Indian voices.

---

## F. AI Avatar

### Planned Model

Simli Live Avatar

### Initially Considered

HeyGen Streaming Avatar

Reason for Change

HeyGen delivers an excellent experience but its pricing is significantly higher for continuous streaming applications.

Simli offers:

- Real-time streaming
- Lower operational cost
- Good lip synchronization
- Suitable for conversational assistants

---

# 6. Streaming Architecture

The system is designed so that every stage supports streaming whenever possible.

Streaming reduces perceived latency by allowing downstream components to begin processing before upstream components have completely finished.

Benefits include:

- Faster response times
- More natural conversations
- Reduced waiting time
- Better user experience

---

# 7. Latency Considerations

Major latency contributors:

- Speech recognition
- Retrieval
- LLM generation
- Speech synthesis
- Avatar rendering

Optimization strategies:

- Streaming STT
- Efficient retrieval
- Lightweight LLM
- Streaming TTS
- Streaming avatar pipeline

---

# 8. Cost Considerations

Cost optimization was a major design factor.

Key decisions:

- GPT-4o Mini over larger premium models.
- Sarvam Saaras v3 for STT.
- Sarvam Bulbul v3 for TTS.
- Simli instead of HeyGen for live avatars.

The objective is to achieve high conversational quality while keeping operational costs practical.

---

# 9. Engineering Decisions

Each component was selected after considering:

- Accuracy
- Latency
- Streaming support
- Pricing
- Ease of integration
- Support for Indian users

The project emphasizes balanced engineering decisions rather than simply selecting the highest-performing models.

---

# 10. Current Status

Completed

- Voice pipeline design
- Model evaluation
- RAG prototype
- FAISS prototype
- GPT-4o Mini integration planning
- STT and TTS selection

In Progress

- Vector database evaluation
- Avatar integration
- End-to-end optimization

---

# 11. Future Roadmap

- Develop a modern web-based user interface.
- Deploy the system to the cloud for secure access from any device.
- Add authentication and user management.
- Continue optimizing latency.
- Evaluate additional vector databases.
- Expand multilingual support.
- Improve avatar realism and conversational experience.

---


---


# 11A. APIs, Services & Pricing

The following APIs and services are required to build the complete Voice-Enabled RAG system.

| Component | API / Service Name | Official Plan Name | Pricing Model | Pricing | Notes |
|-----------|--------------------|--------------------|---------------|---------|-------|
| **Large Language Model (LLM)** | GPT-4o Mini API | API (Pay-as-you-go) | Per 1M Input / Output Tokens | __________ | Used for RAG response generation. |
| **Embeddings** | text-embedding-3-small API | API (Pay-as-you-go) | Per 1M Input Tokens | __________ | Used for vector embeddings. |
| **Speech-to-Text (STT)** | Sarvam Saaras v3 API | __________________ | Per Hour / Per Minute of Audio | __________ | Streaming speech recognition with Indian language support. |
| **Text-to-Speech (TTS)** | Sarvam Bulbul v3 API | __________________ | Per Character / Per 1K Characters | __________ | Natural voice synthesis with streaming support. |
| **AI Avatar** | Simli Live Avatar API | __________________ | Monthly Subscription + Usage | __________ | Real-time streaming avatar with lip-sync. |
| **Vector Database** | FAISS | Open Source | Free | ₹0 | Current prototype implementation. |
| **RAG Framework** | LangChain | Open Source | Free | ₹0 | Workflow orchestration framework. |
| **Backend Framework** | FastAPI | Open Source | Free | ₹0 | Python backend framework. |

---

## APIs to Purchase

### 1. OpenAI

**API:** GPT-4o Mini

**Purpose:**
- Response generation
- Conversational reasoning

**Official Plan:**
> ___________________________

**Pricing:**
- Input Tokens:
- Output Tokens:
- Billing Unit:
- Free Tier:

---

### 2. OpenAI

**API:** text-embedding-3-small

**Purpose:**
- Document embeddings
- Semantic search

**Official Plan:**
> ___________________________

**Pricing:**
- Price:
- Billing Unit:

---

### 3. Sarvam AI

**API:** Saaras v3

**Purpose:**
- Streaming Speech-to-Text

**Official Plan:**
> ___________________________

**Pricing**
- Price:
- Billing Unit:
- Languages Supported:

---

### 4. Sarvam AI

**API:** Bulbul v3

**Purpose**
- Streaming Text-to-Speech

**Official Plan**
> ___________________________

**Pricing**
- Price:
- Billing Unit:
- Voice Support:

---

### 5. Simli

**API**
Live Avatar API

**Purpose**
- Real-time talking avatar
- Lip synchronization
- Avatar streaming

**Official Plan**
> ___________________________

**Pricing**
- Monthly Cost:
- Included Usage:
- Additional Usage Cost:

---

## Free/Open-Source Components

| Technology | Cost |
|------------|------|
| FAISS | Free |
| LangChain | Free |
| FastAPI | Free |
| Python | Free |

---

## Estimated Prototype Cost

### One-Time Cost

None (excluding optional setup).

### Monthly Subscription Costs

| Service | Estimated Cost |
|----------|----------------|
| Simli | __________ |
| OpenAI | Usage-Based |
| Sarvam STT | Usage-Based |
| Sarvam TTS | Usage-Based |

---

## Billing Model Summary

| Service | Billing Type |
|----------|--------------|
| OpenAI GPT-4o Mini | Usage-Based |
| OpenAI Embeddings | Usage-Based |
| Sarvam Saaras v3 | Usage-Based |
| Sarvam Bulbul v3 | Usage-Based |
| Simli Avatar | Monthly + Usage |
| FAISS | Free |
| LangChain | Free |
| FastAPI | Free |

---

### Why These APIs?

The selected APIs were chosen after evaluating:

- Latency
- Response Quality
- Streaming Support
- Cost Efficiency
- Ease of Integration
- Support for English and Hindi
- Suitability for real-time conversational AI

The architecture prioritizes production-ready, low-latency components while maintaining a cost-effective pricing model suitable for prototype and future deployment.


# 12. Conclusion

This project demonstrates a modular voice-enabled RAG architecture that combines streaming speech recognition, retrieval-augmented generation, large language models, speech synthesis, and live avatar technology into a single conversational system.

The design emphasizes technical soundness, modularity, low latency, cost efficiency, and future extensibility, making it a strong foundation for an AI-powered organizational assistant.
