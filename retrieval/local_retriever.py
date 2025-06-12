# retrieval/local_retriever.py

from data.corpus_manager import CorpusManager
from utils.constants import EMBEDDING_MODEL_NAME

class LocalRetriever:
    def __init__(self, model_name=EMBEDDING_MODEL_NAME):
        self.corpus_manager = CorpusManager(model_name)

    def retrieve(self, query: str, k: int = 5):
        """
        Retrieves top k relevant snippets from the local corpus.
        Returns a list of dicts: {"content": str, "score": float, "source": "local"}
        """
        query_embedding = self.corpus_manager.embedding_model.get_embeddings([query])[0]
        results = self.corpus_manager.search(query_embedding, k=k)
        return results

if __name__ == "__main__":
    # Example usage:
    local_retriever = LocalRetriever()
    query = "I'm having angina; how many nitroglycerin tablets can I safely take and when must I stop?"
    results = local_retriever.retrieve(query, k=3)
    print(f"Local retrieval results for '{query}':")
    for res in results:
        print(f"- [Score: {res['score']:.4f}] {res['content']}")