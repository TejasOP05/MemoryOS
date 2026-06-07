from database import DatabaseManager
from embeddings import EmbeddingService
from vector_store import VectorStore
import pickle


class SemanticSearch:
    def __init__(self):
        self.db = DatabaseManager()
        self.embedder = EmbeddingService()
        self.store = VectorStore()
        self.load_existing_index()
        
    def load_existing_index(self):
        self.store.load_index("data/index.faiss")
        with open("data/chunk_map.pkl", "rb") as f:
            self.chunk_map = pickle.load(f)
        # print(
    "Chunk Map Size:",
    len(self.chunk_map)
)
        # print(
    "Total Vectors:",
    self.store.index.ntotal
)
        
    def build_index(self):
        chunks = self.db.get_all_chunks()
        embeddings = []
        for position, (chunk_id, text) in enumerate(chunks):
            embedding = self.embedder.create_embedding(text)
            embeddings.append(embedding)
            self.chunk_map[position] = chunk_id
        self.store.add_embeddings(embeddings)
        
    def search(self, query, k=3):
        
        keyword_results = self.db.keyword_search(query)
        # print("Keyword Matches:", len(keyword_results))
        
        if keyword_results:
            results = []
            seen_files = set()
            for chunk_id, text, filename, path in keyword_results:
                if filename in seen_files:
                    continue
                seen_files.add(filename)
                results.append((filename, path, text, 0.0))
            return results

        query_embedding = self.embedder.create_embedding(query)
        distance, indices = self.store.search(query_embedding, k)
        results = []
        seen_files = set()
        
        for distance, position in zip(distance[0], indices[0]):
            if position == -1:
                continue
            if distance > 1.4:
                continue
            chunk_id = self.chunk_map[position]
            filename, path, text = self.db.get_file_info_from_chunk(chunk_id)
            if filename in seen_files:
                continue

            seen_files.add(filename)
            results.append((filename, path, text, float(distance)))
        return results
    