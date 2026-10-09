from pinecone import Pinecone

pc = Pinecone(
    api_key="pclocal", 
    host="http://localhost:5080" 
)
index = pc.Index(
    host="http://localhost:5081"
)

result = index.fetch(ids=["doc-1"])
# record = result["vectors"]
print("Fetch result:", result)