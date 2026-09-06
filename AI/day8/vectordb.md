# Vector Database

## 3 Problems a Vector DB Solves

1. **No memory** — an LLM cannot remember past conversations across sessions.
2. **No private data access** — an LLM cannot search your private/internal data (it only knows what it was trained on).
3. **No retrieval** — an LLM cannot retrieve the right document on its own from a large corpus.

## How It Solves These Problems

A vector DB stores data as **embeddings** — mathematical (numerical vector) representations of the *meaning* of text, not the raw keywords.

- A query is converted into an embedding using the same embedding model.
- The DB compares that embedding against stored embeddings and returns the **nearest** ones using **semantic similarity** (e.g. cosine similarity), not exact string matching.
- This lets retrieval work even when the query and the document use different words but mean the same thing.

## Typical Flow (RAG)

1. Split documents into chunks.
2. Embed each chunk → vector.
3. Store vectors + metadata in the vector DB.
4. Embed the incoming query the same way.
5. Search for the top-k nearest vectors (similarity search).
6. Feed the retrieved chunks back to the LLM as context.

## How to Choose a Vector DB

| Option | Type | Notes |
|---|---|---|
| **pgvector** | Postgres extension | Good if already using Postgres; combines relational + vector data |
| **ChromaDB** | Lightweight/embedded | Easy local setup, great for prototyping |
| **Pinecone** | Managed/hosted | Fully managed, scales well, no infra to maintain |
| **Weaviate** | Managed/self-hosted | Built-in hybrid search (keyword + vector) |
| **FAISS** | Library (in-process) | Fast, no server, good for small/medium scale, no persistence built-in |

Things to consider when choosing:
- Scale (number of vectors, query volume)
- Need for hosted vs self-managed
- Hybrid search support (keyword + semantic)
- Metadata filtering capabilities
- Existing infra (e.g. already on Postgres → pgvector is simplest)

