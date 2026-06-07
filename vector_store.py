import faiss
import numpy as np
import pickle

class VectorStore:
    def __init__(self):
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        
    def add_embeddings(self, embeddings):
        vectors = np.array(embeddings, dtype=np.float32)
        self.index.add(vectors)
        
    def search(
        self,
        query_embedding,
        k=5
    ):

        query = np.array(
            query_embedding,
            dtype=np.float32
        ).reshape(1, -1)

        distances, indices = self.index.search(
            query,
            k
        )
        return distances, indices
    
    def save_index(self,path):
        faiss.write_index(self.index, path)
        
    def load_index(self, path):
        self.index = faiss.read_index(path)