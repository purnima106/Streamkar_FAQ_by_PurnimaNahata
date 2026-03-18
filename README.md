# Streamkar FAQ RAG API

## Problem Statement

Users frequently have questions about the Streamkar app (like how to buy beans, level up, etc.). Searching through standard FAQ pages is tedious. This intelligent FAQ Bot allows users to securely query product information using plain natural language and receive accurate, context-aware responses, fully backed by an AI Large Language Model.

## Architecture

This service acts as a complete Retrieval-Augmented Generation (RAG) backend:

1. **Ingestion Flow**: Raw FAQs → sentence-transformers Embeddings → Qdrant Vector DB
2. **Retrieval Flow**: User Query → Embedding → Similarity Search → Retrieved Context
3. **Generation Flow**: Context + Query → Prompt Engineering → TinyLlama/TinyLlama-1.1B-Chat-v1.0 → Filtered Answer

**Guardrails Implemented**: 
- Responses restricted to verified contexts.
- Configurable confidence thresholds to prevent arbitrary low-quality answers.
- "I don't know" catch handlers for unsupported queries.

## Setup Instructions

**Option 1: Local Environment (Recommended)**

Because Qdrant Vector DB is configured to run fully locally relying on a local disk `local_qdrant` directory, you don't even need Docker.

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the ingestion script to populate knowledge base
python scripts/ingest.py

# 3. Start the API
uvicorn app.main:app
```

**Option 2: Dockerized API**

If you want to run the API process itself within a container:

```bash
docker build -t streamkar-bot .
docker run -p 8000:8000 streamkar-bot
```

## API Endpoints

- `POST /add_faq` - Add a single question-answer pair.
- `POST /bulk_upload` - Send an array of FAQs to ingest multiple data points simultaneously.
- `POST /ask` - Issue a question and retrieve an LLM-assisted answer from the context.

## Sample Queries

**1. Good Query (Matches FAQ context)**
```json
// POST /ask
{
  "query": "How do I buy beans?"
}
```
*Response*: "You can purchase beans directly from the top-up page inside the app."

**2. Out-of-Bounds Query (Triggering Guardrails)**
```json
// POST /ask
{
  "query": "How to cook pasta?"
}
```
*Response*: "I don't have enough information to answer that."

## Future Improvements

- Use asynchronous LLM serving models for high-concurrency (e.g. vLLM or OpenAI).
- Advanced reranking for context extraction (Cross-Encoders).
- Session tracking and contextual multi-turn conversation support.


