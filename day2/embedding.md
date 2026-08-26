
# Embeddings

Embeddings are numerical representations of words that specify their meaning. Computers don't understand natural language but work efficiently with numbers. Every embedding is a vector representing a word or concept in multi-dimensional space.



## Process of Creating Vector Embeddings

1. Get the raw data
2. Clean the data - tokenization, removing noise, preprocessing
3. Break the data into small individual pieces (tokens)
4. Convert tokens into numerical vectors 



## Example

```
A = "I love football"
B = "I love soccer"
```

### Cosine Similarity Formula

```
cosine_similarity(A, B) = A·B / (||A|| × ||B||)
```



### Similarity Score Interpretation

- **1.0** → Very similar direction
- **0.8** → Strongly similar
- **0.5** → Somewhat related
- **0.0** → Little/no directional relationship
- **-1.0** → Opposite direction



## Semantic Relationships in Embeddings

```
        KING (●)
         ↑
         │ gender relationship
         │
        MAN (●)

  Replace "man" with "woman"
         ↓

        QUEEN (●)
```

Embeddings capture semantic relationships, allowing operations like: KING - MAN + WOMAN ≈ QUEEN
        

