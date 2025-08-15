import chromadb
import uuid
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import os
 
texts = [
    "Vector database",
    "I love U",
    "Good Morning"
]


# chroma_client = chromadb.Client()
chroma_client = chromadb.PersistentClient("./chroma_db")

ef = OpenAIEmbeddingFunction(
    model_name="nomic-embed-text",
    api_base=os.getenv("OLLAMA_ENDPOINT"),
    api_key="ollama",
)

collection = chroma_client.create_collection(
    name="my-collection",
    embedding_function=ef,
    configuration={
        "hnsw": {
            "space": "cosine"
        }
    }
)

collection.add(
    documents=texts,
    ids=[str(uuid.uuid4()) for _ in texts],
    # metadatas=[{"language": "en"} for _ in texts]
    metadatas=[{"label" : "A"}, {"label" : "A"}, {"label" : "B"}]
)

# result = collection.peek()
# print(result)

result = collection.query(
    query_texts="heart",
    n_results=5,
    where={"label": "A"}
)

print(result["documents"])
print(result["distances"])

