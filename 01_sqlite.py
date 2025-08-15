import sqlite3
import sqlite_vec
import numpy as np

conn = sqlite3.connect(":memory:")
conn.enable_load_extension(True)
sqlite_vec.load(conn)

cursor = conn.cursor()
cursor.execute("""
    CREATE VIRTUAL TABLE documents USING vec0(
        vector float[3]
    )
""")

# vector = np.array([1.0, 2.0, 3.0], dtype=np.float32).tobytes()
# cursor.execute("INSERT INTO documents (vector) VALUES (?)", (vector,))

### Insert vectors into the database
vectors = [
   (np.array([1.0, 2.0, 3.0], dtype=np.float32).tobytes(),),
   (np.array([4.0, 5.0, 6.0], dtype=np.float32).tobytes(),),
   (np.array([7.0, 8.0, 9.0], dtype=np.float32).tobytes(),),
   (np.array([10.0, 11.0, 12.0], dtype=np.float32).tobytes(),)
]
cursor.executemany("INSERT INTO documents (vector) VALUES (?)", vectors)

### Query the database
query_vector = (np.array([1.0, 1.0, 1.0], dtype=np.float32).tobytes(),)
cursor.execute("""
    SELECT 
        rowid, distance, vector
    FROM documents 
    WHERE vector MATCH ?
    ORDER BY distance
    LIMIT 5
""", query_vector)
rows = cursor.fetchall()

for id, distance, vector in rows:
    print(f"ID: {id} - {np.frombuffer(vector, dtype=np.float32)} - Distance: {distance}")