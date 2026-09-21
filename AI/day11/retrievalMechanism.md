 # Day 11 — Retrieval Mechanics

Retrieval is the process of finding the most relevant pieces of information from a knowledge store, given a user query.

## 1. Query Processing

Steps:

1. **Tokenization** — splitting text into smaller units (tokens/words).
2. **Lowercasing** — converting text to lower case for consistent matching.
3. **Stop word removal** — eliminating common words that carry little meaning, such as "the", "a", "is", etc.
4. **Stemming** (for sparse retrieval) — reducing words to their root form to improve matching (e.g., `running` → `run`).
5. **Embedding generation** (for dense retrieval) — transforming the processed query into a vector embedding that captures its semantic meaning.

## 2. Knowledge Base Representation

- **Chunking** — splitting documents into small units that retain rich, self-contained context.
- **Indexing** — a data structure used for fast searching; the type depends on the retrieval method:
  - **Inverted index** — maps keywords to the documents/chunks that contain them (used in sparse retrieval).
  - **Vector index** — stores vector embeddings and supports Approximate Nearest Neighbor (ANN) search (used in dense retrieval).
  - **Graph structure** (for graph-based retrieval) — represents entities and relationships as nodes and edges.

## 3. Matching / Scoring

- **Sparse retrieval** — matching is based on the overlap of terms between the processed query and chunks. Scoring functions like **TF-IDF** or **BM25** are used to assign a relevance score.
- **Dense retrieval** — the embedded query is compared against stored embeddings using **cosine similarity** or **dot product** to measure similarity between them.
- **Graph-based retrieval** — matching involves traversing the graph to identify related, connected nodes. Scoring depends on node similarity, path length, and relation types.

## 4. Ranking and Selection

- After matching/scoring, each stored chunk has a relevance score relative to the input query.
- Stored chunks are ranked based on this score.
- The **top-k** highest-scoring chunks are retrieved.

## Hybrid Retrieval

Combines two or more retrieval techniques — the most common combination is **sparse + dense** retrieval.

The query is processed by both dense and sparse techniques in parallel; the results are combined and reranked using a fusion technique (e.g., Reciprocal Rank Fusion).

## Multi-Vector Retrieval

Represents a single document/chunk with multiple embeddings (e.g., one per sentence or one per semantic aspect) instead of a single vector, allowing more fine-grained matching against the query.

## Choosing a Retrieval Method

The choice of retrieval method impacts the performance of the RAG pipeline:

- **Sparse** offers efficiency and strong keyword-matching capabilities.
- **Dense** excels at semantic understanding.
- **Hybrid** provides the best balance by combining the strengths of both.
- **Graph-based** and **multi-vector** retrieval represent more specialized and evolving approaches.



