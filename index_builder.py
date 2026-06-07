from database import DatabaseManager
from embeddings import EmbeddingService
from vector_store import VectorStore

import pickle


db = DatabaseManager()

embedder = EmbeddingService()

store = VectorStore()

chunk_map = {}

chunks = db.get_all_chunks()

embeddings = []

for position, (chunk_id, text) in enumerate(chunks):

    embedding = embedder.create_embedding(text)

    embeddings.append(embedding)

    chunk_map[position] = chunk_id

store.add_embeddings(embeddings)

store.save_index(
    "data/index.faiss"
)

with open(
    "data/chunk_map.pkl",
    "wb"
) as f:

    pickle.dump(
        chunk_map,
        f
    )

print("Index Built Successfully")