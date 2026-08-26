import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()
from google import genai

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
sentences = [
    "I love playing football.",
    "I really enjoy playing soccer.",
    "Football is my favorite sport.",
    "I like eating pizza.",
    "The weather is very cold today."
]

# result = client.models.embed_content(
#         model="gemini-embedding-2",
#         content="I love playing football."
# )

def cosine_similarity(a,b):
    return np.dot(a,b)/np.linalg.norm(a)/np.linalg.norm(b)
    

embedding_list=[
    client.models.embed_content(
        model="gemini-embedding-2",contents=sentence
    ).embeddings[0].values
    for sentence in sentences
]

print("Total number of embeddings generated:", len(embedding_list))
# print("Embedding for the first sentence:", embedding_list)
print(type(embedding_list[0]))


for i in range(len(embedding_list)):
    
    for j in range(i+1, len(embedding_list)):
        similarity = cosine_similarity(np.array(embedding_list[i]), np.array(embedding_list[j]))
        print(f" {sentences[i]} and {sentences[j]} have similarity of {similarity:.4f}")
        # print(f"Cosine similarity between sentence {i+1} and sentence {j+1}: {similarity:.4f}")         