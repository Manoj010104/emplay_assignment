# generation/llm_generator.py

from groq import Groq # New import for Groq
from utils.constants import GROQ_API_KEY, LLM_MODEL_NAME, DISCLAIMER, SYSTEM_PROMPT_TEMPLATE, USER_PROMPT_TEMPLATE

class LLMGenerator:
    def __init__(self, api_key=GROQ_API_KEY, model_name=LLM_MODEL_NAME):
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables.")
        self.client = Groq(api_key=api_key) # Initialize Groq client
        self.model_name = model_name
        print(f"LLM initialized with Groq model: {self.model_name}")

    def _format_context(self, context_snippets: list[dict]) -> str:
        """Formats the retrieved context for the LLM prompt."""
        formatted_context = []
        for i, snippet in enumerate(context_snippets):
            source_info = ""
            if snippet['source'] == 'local':
                source_info = f"Local Snippet {i+1}"
            elif snippet['source'] == 'web':
                source_info = f"Web Source {i+1} (Title: {snippet.get('title', 'N/A')}, URL: {snippet.get('link', 'N/A')})"
            
            # Clean content for LLM input
            content = snippet['content'].replace("\n", " ").strip()
            formatted_context.append(f"[{source_info}]\n{content}")
        return "\n\n".join(formatted_context)

    def generate_answer(self, query: str, context_snippets: list[dict]) -> dict:
        """
        Generates an answer using the LLM based on the query and retrieved context.
        Returns a dict containing the answer, token usage, and relevant sources.
        """
        formatted_context = self._format_context(context_snippets)
        
        system_message_content = SYSTEM_PROMPT_TEMPLATE.format(disclaimer=DISCLAIMER)
        user_message_content = USER_PROMPT_TEMPLATE.format(query=query, context=formatted_context)

        messages = [
            {"role": "system", "content": system_message_content},
            {"role": "user", "content": user_message_content},
        ]

        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                temperature=0.2, # Keep low for factual consistency
                max_tokens=400 # Sufficient for ~250 words + structure
            )

            answer = chat_completion.choices[0].message.content
            
            # Groq API returns token usage directly
            total_tokens = chat_completion.usage.total_tokens

            # Extract citation information from context_snippets for clear output
            citations = []
            for i, snippet in enumerate(context_snippets):
                if snippet['source'] == 'local':
                    citations.append(f"Local Snippet: \"{snippet['content'].strip()[:80]}...\"")
                elif snippet['source'] == 'web':
                    citations.append(f"Web: {snippet.get('title', 'N/A')} ({snippet.get('link', 'N/A')})")
            
            return {
                "answer": answer,
                "token_usage": total_tokens,
                "sources_used": citations
            }

        except Exception as e: # Catch broader exceptions for API calls
            print(f"An error occurred during Groq API call: {e}")
            return {
                "answer": f"{DISCLAIMER}\n\nI apologize, but I encountered an issue connecting to the AI. Please ensure your GROQ_API_KEY is correct and try again later.",
                "token_usage": 0,
                "sources_used": []
            }

if __name__ == "__main__":
    # Example usage:
    # Ensure your .env has GROQ_API_KEY set
    llm_generator = LLMGenerator()
    query = "my blood sugar is very low and I'm unconscious"
    
    # Dummy context for testing LLM directly
    dummy_context = [
        {"content": "For severe hypoglycaemia with unconsciousness, give intramuscular glucagon 1 mg if available.", "source": "local"},
        {"content": "Hypoglycaemia is defined as blood glucose < 70 mg/dL and needs rapid glucose intake.", "source": "local"},
        {"content": "Always call emergency services for unconsciousness.", "source": "web", "title": "First Aid Guide", "link": "https://example.com/first-aid"}
    ]
    
    response = llm_generator.generate_answer(query, dummy_context)
    print("\n--- LLM Generated Answer ---")
    print(response["answer"])
    print(f"\nToken Usage: {response['token_usage']}")
    print("\nSources Used:")
    for src in response["sources_used"]:
        print(f"- {src}")