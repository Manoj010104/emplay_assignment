# retrieval/web_retriever.py

from googleapiclient.discovery import build
import os
from utils.constants import GOOGLE_CSE_API_KEY, GOOGLE_CSE_ID

class WebRetriever:
    def __init__(self, api_key=GOOGLE_CSE_API_KEY, cse_id=GOOGLE_CSE_ID):
        if not api_key or not cse_id:
            raise ValueError("GOOGLE_CSE_API_KEY or GOOGLE_CSE_ID is not set in environment variables.")
        self.service = build("customsearch", "v1", developerKey=api_key)
        self.cse_id = cse_id

    def retrieve(self, query: str, k: int = 5):
        """
        Performs a web search using Google Custom Search Engine and returns top k relevant snippets.
        Returns a list of dicts: {"content": str, "title": str, "link": str, "source": "web"}
        """
        try:
            # max results per query is 10 for CSE API. Adjust 'num' accordingly.
            search_results = self.service.cse().list(
                q=query,
                cx=self.cse_id,
                num=min(k, 10) # Max 10 results per call for CSE
            ).execute()

            results = []
            if 'items' in search_results:
                for item in search_results['items']:
                    content = item.get('snippet', '')
                    title = item.get('title', 'No Title')
                    link = item.get('link', '#')
                    if content: # Only add if snippet content exists
                        results.append({
                            "content": content,
                            "title": title,
                            "link": link,
                            "source": "web"
                        })
            return results

        except Exception as e:
            print(f"Error during Google CSE web search: {e}")
            return []

if __name__ == "__main__":
    # Example usage:
    # Ensure your .env has GOOGLE_CSE_API_KEY and GOOGLE_CSE_ID set
    web_retriever = WebRetriever()
    query = "first aid for severe diabetic foot ulcer"
    results = web_retriever.retrieve(query, k=3)
    print(f"Web retrieval results for '{query}':")
    if results:
        for res in results:
            print(f"- [Web] {res['title']} ({res['link']}): {res['content']}")
    else:
        print("No web results found (check API keys, CSE ID, and internet connection).")