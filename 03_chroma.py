import chromadb
import uuid

texts = [
    "Vector database",
    "I love U",
    "Good Morning"
]


chroma_client = chromadb.Client()
collection = chroma_client.create_collection(
    name="my-collection",
)

collection.add(
    documents=texts,
    ids=[str(uuid.uuid4()) for _ in texts],
    metadatas=[{"language": "en"} for _ in texts]
)

# result = collection.peek()
# print(result)

result = collection.query(
    query_texts="heart",
    n_results=5
)

print(result["documents"])
print(result["distances"])