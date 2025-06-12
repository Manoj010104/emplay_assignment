# data/corpus_manager.py

import faiss
import numpy as np
import os
from data.medical_snippets import MEDICAL_SNIPPETS
from retrieval.embedding_model import EmbeddingModel
from utils.constants import EMBEDDING_MODEL_NAME

class CorpusManager:
    def __init__(self, model_name=EMBEDDING_MODEL_NAME):
        self.snippets = MEDICAL_SNIPPETS
        self.embedding_model = EmbeddingModel(model_name)
        self.index = None
        self.snippet_embeddings = None
        self._build_index()

    def _build_index(self):
        """Builds the FAISS index for the medical snippets."""
        print(f"Building FAISS index for {len(self.snippets)} snippets...")
        self.snippet_embeddings = self.embedding_model.get_embeddings(self.snippets)
        d = self.snippet_embeddings.shape[1] # Dimension of embeddings
        self.index = faiss.IndexFlatL2(d) # L2 distance for similarity
        self.index.add(self.snippet_embeddings)
        print("FAISS index built successfully.")

    def search(self, query_embedding, k=5):
        """
        Searches the FAISS index for the top k most similar snippets.
        Returns a list of (snippet_text, similarity_score) tuples.
        """
        if self.index is None:
            raise ValueError("FAISS index not built. Call _build_index() first.")

        D, I = self.index.search(np.array([query_embedding]), k)
        
        results = []
        for i, score in zip(I[0], D[0]):
            results.append({
                "content": self.snippets[i],
                "score": score,
                "source": "local"
            })
        return results

    def get_all_snippets(self):
        """Returns all medical snippets."""
        return self.snippets

if __name__ == "__main__":
    # Example usage:
    corpus_manager = CorpusManager()
    query = "sweating, shaky, and glucometer reads 55 mg/dL"
    query_embedding = corpus_manager.embedding_model.get_embeddings([query])[0]
    
    results = corpus_manager.search(query_embedding, k=3)
    print(f"\nTop 3 local results for '{query}':")
    for res in results:
        print(f"- [Score: {res['score']:.4f}] {res['content']}")