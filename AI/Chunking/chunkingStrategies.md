# Chunking Strategies

Chunking is the process of breaking a large document into smaller segments.

The trick lies in finding chunks that are big enough to contain meaningful information, but small enough to stay focused. Finding the optimal chunk size for the documents in your corpus is crucial to ensuring that search results are accurate and relevant.

## Why do we need chunking?

LLMs have a context limit. Loading all the information into the context window will cause the LLM to hallucinate and lead to excessive token usage.

## What to think about when choosing a chunking strategy?

1. **What kind of data is being chunked?**

2. **What embedding model are you using?**
   Embedding models are domain-specific — choosing the correct embedding model will have an impact on chunking.

3. **What are the expectations for the length and complexity of user queries?**
   Will they be short or long? This gives us information on how to chunk content so that the relationship between the embedded query and the embedded chunks stays strong.

4. **How will the retrieved results be utilized within your specific application?**
   Will they be used for semantic search, RAG, or an agentic workflow? Based on this, the ideal amount of retrieved info will vary — humans typically need a smaller amount of info, while an LLM may need more context.

## Chunking Methods

### 1. Fixed-size chunking

Decide on a chunk size and break the document into fixed-size chunks.

### 2. Content-aware chunking

Strategies that adhere to the document's structure to help inform the meaning of the chunks.

- **Naive splitter**: Splits sentences based on identifiers like `,`, `.`, new lines, or whitespace.
- **NLTK** (Natural Language Toolkit): A popular Python library for working with natural language. It provides a trained sentence tokenizer that helps split text into sentences, giving each chunk more meaning.
- **spaCy**: A powerful Python library for NLP tasks.

### 3. Recursive character-level chunking

LangChain implements `RecursiveCharacterTextSplitter` (RCLC), which splits based on a list of separators in a given order — e.g. `["\n\n", "\n", "."]` — up to a given chunk size.

### 4. Document structure-based chunking

- **PDF docs**: Often contain many headings and subheadings that need to be processed before creating chunks. LangChain has utilities that help with this cleanup.
- **HTML pages**: Contain lots of tags — you can write your own parser or use LangChain's splitters to process them.
- **Markdown**: Chunked based on headers/sections.
- **LaTeX**: Chunked based on its own structural syntax.

### 5. Semantic chunking

1. Break the document into sentences.
2. Group each sentence with its surrounding sentences.
3. Create embeddings for each group.
4. Split into chunks based on the similarity between consecutive group embeddings.

### 6. Contextual chunking


