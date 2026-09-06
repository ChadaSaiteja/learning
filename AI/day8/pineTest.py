import os
from dotenv import load_dotenv
from google import genai
from pinecone import Pinecone
load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


pc = Pinecone(
    api_key="pclocal", 
    host="http://localhost:5080" 
) 


query="refund policy of purchase."


query_embedding = client.models.embed_content(
        model="gemini-embedding-2",contents=query
    ).embeddings[0].values



print("Pinecone client indexes:", pc.list_indexes())
index = pc.Index(
    host="http://localhost:5081"
)
result= index.query(
    vector=query_embedding,
    top_k=3
)
print("Query result:", result)


for match in result["matches"]:
    print("Match:",match    )
    print("Match ID:", match["id"])
    print("Match Score:", match["score"])
    # print("Match Metadata:", match["metadata"])
    
    
stats = index.describe_index_stats()

print("Total vectors:", stats["total_vector_count"])