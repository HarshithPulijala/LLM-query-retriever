from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

class EmbeddingStore:
    def __init__(self, model_name='all-MiniLM-L6-v2', chunk_size=1000, overlap=200):
        self.model = SentenceTransformer(model_name)
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunks = []
        self.embeddings = None
        self.index = None

    def chunk_text(self, text):
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunks.append(text[start:end])
            start += self.chunk_size - self.overlap
        return chunks

    def add_document(self, text):
        self.chunks = self.chunk_text(text)
        self.embeddings = self.model.encode(self.chunks, show_progress_bar=False)
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(self.embeddings).astype('float32'))

    def search(self, query, top_k=5):
        if self.index is None:
            return []
        query_emb = self.model.encode([query])
        D, I = self.index.search(np.array(query_emb).astype('float32'), top_k)
        results = [(self.chunks[i], float(D[0][idx])) for idx, i in enumerate(I[0])]
        return results

    def clear(self):
        self.chunks = []
        self.embeddings = None
        self.index = None 