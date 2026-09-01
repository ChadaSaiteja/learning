# Day 7 — Context Window

## Why Context Windows Have Limits

### 1. Quadratic Self-Attention Cost
In a Transformer, every token attends to every other token (self-attention).  
With 10,000 tokens, that's **10,000 × 10,000 = 100M comparisons** — quadratic in sequence length.

### 2. KV Cache Memory
For each generated token the model stores **Key** and **Value** vectors in GPU memory.  
Very long contexts require hundreds of GBs of VRAM, making them impractical.

### 3. Training Data Length Limit
Models are trained on sequences up to a fixed length.  
Quality **degrades** beyond the length seen during training.

---

## Solutions

### Sparse Attention
Instead of attending to all tokens, each token attends to a **sparse subset**.

#### BigBird Attention (quadratic → linear)
Combines three connection types:
| Type | Description |
|------|-------------|
| **Sliding window** | Each token attends to its local neighbors |
| **Global tokens** | A few special tokens attend to the entire sequence |
| **Random connections** | Each token attends to a few random tokens |

---

### Sliding Window Attention
An efficient Transformer mechanism where each token attends only to a **fixed-size local neighborhood** instead of the entire sequence.

- Reduces complexity from O(n²) to O(n × w), where `w` is the window size.
- Used in models like **Longformer** and **Mistral**.

---

### KV Cache Compression
When a Transformer generates a token, it computes **Q, K, V** vectors and caches K/V for all previous tokens.  
For a new query, it attends over all cached K, V — memory grows with sequence length.

**KV cache compression** reduces this by:
- Evicting less important K/V pairs
- Quantizing cached vectors
- Merging similar entries

Reduces cost from **O(n²)** → **O(n)** without full recomputation.

---

### Summary-Based Memory
> *Compressing conversation without losing intent*

A **continuously updated textual summary** of the conversation so far.  
Instead of keeping every message, it retains only what matters:

- User intent
- Constraints
- Key decisions

The summary evolves based on the purpose of the chat.

**LangChain** provides `ConversationSummaryMemory` for this pattern.

> *Summarized memory allows agents to remember **what matters**, not **everything that happened**.*


