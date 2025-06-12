# retrieval/hybrid_retriever.py

from retrieval.local_retriever import LocalRetriever
from retrieval.web_retriever import WebRetriever
from retrieval.re_ranker import ReRanker
from utils.constants import LOCAL_K, WEB_K, FINAL_CONTEXT_N

class HybridRetriever:
    def __init__(self):
        self.local_retriever = LocalRetriever()
        self.web_retriever = WebRetriever()
        self.re_ranker = ReRanker()

    def retrieve(self, query: str) -> list[dict]:
        """
        Performs hybrid retrieval (local + web) and re-ranks the results.
        Returns a list of top N relevant documents.
        Each document dict will have at least 'content', 'source', and 're_rank_score'.
        Web results will also have 'title' and 'link'.
        """
        print(f"Performing local search for '{query}'...")
        local_results = self.local_retriever.retrieve(query, k=LOCAL_K)
        print(f"Found {len(local_results)} local results.")

        print(f"Performing web search for '{query}'...")
        web_results = self.web_retriever.retrieve(query, k=WEB_K)
        print(f"Found {len(web_results)} web results.")

        all_results = local_results + web_results
        
        if not all_results:
            print("No results from either local or web search.")
            return []

        print(f"Re-ranking {len(all_results)} combined results...")
        re_ranked_results = self.re_ranker.re_rank(query, all_results)
        
        # Select the top N for the final context
        final_context = re_ranked_results[:FINAL_CONTEXT_N]
        print(f"Selected top {len(final_context)} results for context.")
        
        return final_context

if __name__ == "__main__":
    # Example usage:
    hybrid_retriever = HybridRetriever()
    query = "CKD patient with a potassium level of 6.1 mmol/L—what emergency measures can we start right away?"
    context = hybrid_retriever.retrieve(query)

    print("\n--- Final Context for LLM ---")
    for i, doc in enumerate(context):
        print(f"{i+1}. [Score: {doc.get('re_rank_score', 'N/A'):.4f}] [Source: {doc['source']}] {doc['content']}")
        if doc['source'] == 'web':
            print(f"   (Link: {doc['link']})")