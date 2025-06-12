# chatbot/rag_chatbot.py

from retrieval.hybrid_retriever import HybridRetriever
from generation.llm_generator import LLMGenerator
from utils.metrics import MetricsTracker
from utils.constants import DISCLAIMER

class RAGChatbot:
    def __init__(self):
        self.retriever = HybridRetriever()
        self.generator = LLMGenerator()
        self.metrics_tracker = MetricsTracker()
        print("RAGChatbot initialized.")

    def ask(self, query: str) -> str:
        """
        Processes a user query through the RAG pipeline.
        Returns the generated first-aid answer.
        """
        self.metrics_tracker.start_timer()
        
        # 1. Hybrid Retrieval
        retrieved_context = self.retriever.retrieve(query)
        
        # 2. Answer Generation
        llm_response = self.generator.generate_answer(query, retrieved_context)
        
        self.metrics_tracker.stop_timer()
        self.metrics_tracker.add_token_usage(llm_response["token_usage"])
        self.metrics_tracker.increment_query_count()

        full_answer = llm_response["answer"]
        # Ensure the disclaimer is always present at the beginning (primary requirement)
        # And at the end, just in case (as a fallback safety measure).
        if not full_answer.strip().startswith(DISCLAIMER.strip()):
            full_answer = f"{DISCLAIMER}\n\n" + full_answer
        if not full_answer.strip().endswith(DISCLAIMER.strip()):
            full_answer += f"\n\n{DISCLAIMER}" # Add if not already there

        return full_answer

    def get_metrics(self) -> MetricsTracker:
        return self.metrics_tracker

    def reset_metrics(self):
        self.metrics_tracker.reset()

if __name__ == "__main__":
    chatbot = RAGChatbot()
    print("Type your medical emergency symptoms (e.g., 'I'm sweating, shaky, and my glucometer reads 55 mg/dL'). Type 'exit' to quit.")

    while True:
        user_query = input("\n> ").strip()
        if user_query.lower() == 'exit':
            break
        if not user_query:
            continue

        response = chatbot.ask(user_query)
        print("\n--- Chatbot Response ---")
        print(response)

    print("\n--- Session Metrics ---")
    print(chatbot.get_metrics())
    print("Exiting chatbot.")