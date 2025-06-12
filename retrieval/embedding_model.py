# retrieval/embedding_model.py

from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name):
        self.model_name = model_name
        self._load_model()

    def _load_model(self):
        """Loads the sentence-transformers model."""
        try:
            self.model = SentenceTransformer(self.model_name)
            print(f"Loaded embedding model: {self.model_name}")
        except Exception as e:
            print(f"Error loading embedding model {self.model_name}: {e}")
            self.model = None

    def get_embeddings(self, texts):
        """Generates embeddings for a list of texts."""
        if self.model is None:
            raise RuntimeError("Embedding model not loaded.")
        # Ensure texts is a list
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts, convert_to_numpy=True)