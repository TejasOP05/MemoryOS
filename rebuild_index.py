from database import DatabaseManager
from embeddings import EmbeddingService
from vector_store import VectorStore

import pickle


def rebuild_index():

    db = DatabaseManager()

    embedder = EmbeddingService()

    chunks = db.get_all_chunks()

    store = VectorStore()

    embeddings = []

    chunk_map = {}

    for position, (chunk_id, text) in enumerate(chunks):

        embedding = embedder.create_embedding(
            text
        )

        embeddings.append(
            embedding
        )

        chunk_map[position] = chunk_id

    if embeddings:

        store.add_embeddings(
            embeddings
        )

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

    db.close()

    print(
        f"Indexed {len(chunks)} chunks"
    )
    
if __name__ == "__main__":
    rebuild_index()