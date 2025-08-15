# from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os
import sqlite3
import sqlite_vec
import numpy as np

texts = [
    "Vector database",
    "I love U",
    "Good Morning"
]

# model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# embeddings = model.encode(texts)
# print(embeddings[0])
# print(len(embeddings[0])) # 384

### Ollama nomic-embed-text
ai_client = OpenAI(
    base_url=os.getenv("OLLAMA_ENDPOINT"),
    api_key="ollama",
)

model = "nomic-embed-text"
dimension = 768



### Azure OpenAi
# ai_client = OpenAI(
#     base_url=os.getenv("AZURE_OPENAI_ENDPOINT") + "/openai/v1",
#     api_key=os.getenv("AZURE_OPENAI_KEY"),
#     default_query={"api-version": "preview"}
# )
# model = "text-embedding-3-small"
# dimension = 1536


# response = ai_client.embeddings.create(
#     model=model,
#     input=texts
# )

# print(response.data[0].embedding)

conn = sqlite3.connect(":memory:")
conn.enable_load_extension(True)
sqlite_vec.load(conn)

cursor = conn.cursor()
cursor.execute(f"""
    CREATE VIRTUAL TABLE documents USING vec0(
        vector FLOAT[{dimension}]
    )
""")

response = ai_client.embeddings.create(
    model=model,
    input=texts
)

embeddings = [(np.array(item.embedding, dtype=np.float32).tobytes(),) for item in response.data]
cursor.executemany("INSERT INTO documents (vector) VALUES (?)", embeddings)

query_response = ai_client.embeddings.create(
    input="heart",
    model=model,
)

query_embeddings = (np.array(query_response.data[0].embedding, dtype=np.float32).tobytes(),)

cursor.execute("""
    SELECT 
        rowid, distance
    FROM documents 
    WHERE vector MATCH ?
    ORDER BY distance
    LIMIT 5
""", query_embeddings)

rows = cursor.fetchall()
for id, distance in rows:
    print(f"ID: {id} - Distance: {distance}")