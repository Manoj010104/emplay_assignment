# retrieval/re_ranker.py

from sentence_transformers import CrossEncoder

class ReRanker:
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self._load_model()

    def _load_model(self):
        """Loads the cross-encoder model."""
        try:
            self.model = CrossEncoder(self.model_name)
            print(f"Loaded re-ranker model: {self.model_name}")
        except Exception as e:
            print(f"Error loading re-ranker model {self.model_name}: {e}")
            self.model = None

    def re_rank(self, query: str, documents: list[dict]):
        """
        Re-ranks a list of documents based on their relevance to the query.
        Documents should be a list of dicts with a 'content' key.
        Adds a 're_rank_score' to each document.
        """
        if not documents:
            return []
        if self.model is None:
            print("Re-ranker model not loaded, returning original order.")
            # Assign a dummy score if re-ranker fails
            for doc in documents:
                doc['re_rank_score'] = 0.0 # Or some default
            return documents

        sentence_pairs = [[query, doc["content"]] for doc in documents]
        scores = self.model.predict(sentence_pairs)

        for i, score in enumerate(scores):
            documents[i]['re_rank_score'] = float(score) # Convert numpy float to native float

        # Sort documents by re-rank score in descending order
        ranked_documents = sorted(documents, key=lambda x: x.get('re_rank_score', -float('inf')), reverse=True)
        return ranked_documents

if __name__ == "__main__":
    # Example usage:
    reranker = ReRanker()
    query = "blood sugar low"
    docs = [
        {"content": "Hypoglycaemia is defined as blood glucose < 70 mg/dL and needs rapid glucose intake."},
        {"content": "A fasting plasma glucose ≥ 126 mg/dL on two occasions confirms diabetes."},
        {"content": "First-aid for mild hypoglycaemia: give 15 g of fast-acting carbohydrate such as glucose tablets."},
        {"content": "Sudden chest pain radiating to the left arm may indicate myocardial infarction."},
        {"content": "For severe hypoglycaemia with unconsciousness, give intramuscular glucagon 1 mg if available."}
    ]

    ranked_docs = reranker.re_rank(query, docs)
    print(f"Re-ranked documents for '{query}':")
    for doc in ranked_docs:
        print(f"- [Score: {doc['re_rank_score']:.4f}] {doc['content']}")