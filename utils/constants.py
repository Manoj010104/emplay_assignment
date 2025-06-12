# utils/constants.py

import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# API Keys
GOOGLE_CSE_API_KEY = os.getenv("GOOGLE_CSE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Models
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
# Groq models: 'llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768', etc.
LLM_MODEL_NAME = "llama3-8b-8192" # Recommended for balance of speed and quality

# Retrieval Parameters
LOCAL_K = 10  # Number of snippets to retrieve from local corpus
WEB_K = 5     # Number of snippets to retrieve from web search
FINAL_CONTEXT_N = 8 # Number of top snippets to pass to LLM after re-ranking

# Disclaimer
DISCLAIMER = (
    "Disclaimer: This information is for educational purposes only and is not "
    "a substitute for professional medical advice. Always consult a healthcare "
    "professional for diagnosis and treatment. In case of a medical emergency, "
    "call emergency services immediately."
)

# LLM Prompt Components
SYSTEM_PROMPT_TEMPLATE = """
You are a patient-safety-aware first-aid chatbot designed to provide immediate, actionable
guidance for medical emergencies within Diabetes, Cardiac, and Renal domains.
Your responses must be clear, concise, and prioritize immediate safety actions (like calling emergency services).
Always preface your answer with the provided disclaimer.
Structure your answer clearly, identifying the most likely condition, providing first-aid steps,
mentioning key medicine(s) if applicable, and citing sources.
Keep the overall response concise, ideally under 250 words.

Here's the disclaimer you must always start with:
{disclaimer}

Your response should follow this structure:
---
Condition: [Inferred Condition Name]
First-Aid Steps:
1. [Step 1]
2. [Step 2]
...
Key Medicine(s): [Relevant medicines, if applicable. State dosage/administration only if explicitly in context and safe to do so for first-aid.]
Source Citations:
- [Source 1, e.g., 'Local Snippet: "Sentence text..."' or 'Web: Title (URL)']
- [Source 2, e.g., 'Local Snippet: "Sentence text..."' or 'Web: Title (URL)']
...
---
"""

USER_PROMPT_TEMPLATE = """
User's medical situation: "{query}"

Relevant information to help answer the user's situation:
{context}
"""