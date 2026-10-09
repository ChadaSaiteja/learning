import os
from dotenv import load_dotenv
from google import genai
from pinecone import Pinecone,ServerlessSpec
load_dotenv()


pc = Pinecone(
    api_key="pclocal", 
    host="http://localhost:5080" 
) 


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

documents = [
    {
        "id": "doc-1",
        "text": "Customers can request a refund within 30 days of purchase.",
        "category": "refund"
    },
    {
        "id": "doc-2",
        "text": "Installation appointments can be rescheduled up to 24 hours before the appointment.",
        "category": "installation"
    },
    {
        "id": "doc-3",
        "text": "Technical support is available Monday through Friday from 9 AM to 6 PM.",
        "category": "support"
    },
    {
        "id": "doc-4",
        "text": "Customers can reset their password using the Forgot Password option.",
        "category": "account"
    },
    {
        "id": "doc-5",
        "text": "Fiber internet installation usually takes between two and four hours.",
        "category": "installation"
    },
    {
        "id": "doc-6",
        "text": "Customers can update their billing address from their account settings.",
        "category": "billing"
    }
]

embedding_list=[
    client.models.embed_content(
        model="gemini-embedding-2",contents=sentence
    ).embeddings[0].values
    for sentence in [doc["text"] for doc in documents]
]

print("Total documents:", len(documents))
print("Total embeddings:", len(embedding_list))
print("Embedding dimensions:", len(embedding_list[0]))


# if "order" not in pc.list_indexes():
#     pc.create_index(
#         name="order",
#         dimension=len(embedding_list[0]),
#         metric="cosine",
#         spec=ServerlessSpec(
#             cloud="aws",
#             region="us-east-1"
#         )
#     )
index = pc.Index(
    host="http://localhost:5081"
)
vectors = [
    {
        "id": doc["id"],
        "values": embedding_list[i],
        "metadata": {"category": doc["category"], "text": doc["text"]}
    }
    for i, doc in enumerate(documents)
]
print("Total vectors:", len(vectors))

index.upsert(
    vectors=vectors
)
print("Vectors upserted to Pinecone.")
print("Index stats:", index.describe_index_stats())