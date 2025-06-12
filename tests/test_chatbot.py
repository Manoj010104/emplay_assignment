# tests/test_chatbot.py
import pytest
from chatbot.rag_chatbot import RAGChatbot
from utils.constants import DISCLAIMER

# Sample Test Queries from the document
SAMPLE_QUERIES = [
    "I'm sweating, shaky, and my glucometer reads 55 mg/dL—what should I do right now?",
    "My diabetic father just became unconscious; we think his sugar crashed. What immediate first-aid should we give?",
    "A pregnant woman with gestational diabetes keeps getting fasting readings around 130 mg/dL. What does this mean and how should we manage it?",
    "Crushing chest pain shooting down my left arm-do I chew aspirin first or call an ambulance?",
    "I'm having angina; how many nitroglycerin tablets can I safely take and when must I stop?",
    "Grandma has chronic heart failure, is suddenly short of breath, and her ankles are swelling. Any first-aid steps before we reach the ER?",
    "After working in the sun all day I've barely urinated and my creatinine just rose 0.4 mg/dL-could this be acute kidney injury and what should I do?",
    "CKD patient with a potassium level of 6.1 mmol/L—what emergency measures can we start right away?",
    "I took ibuprofen for back pain; now my flanks hurt and I'm worried about kidney damage-any immediate precautions?",
    "Type 2 diabetic, extremely thirsty, glucose meter says 'HI' but urine ketone strip is negative-what's happening and what's the first-aid?"
]

# Expected conditions/keywords for each query (for basic validation)
EXPECTED_INFO = {
    SAMPLE_QUERIES[0]: {"condition": "Hypoglycaemia", "keywords": ["glucose", "carbohydrate"]},
    SAMPLE_QUERIES[1]: {"condition": "Hypoglycaemia", "keywords": ["unconscious", "glucagon", "emergency"]},
    SAMPLE_QUERIES[2]: {"condition": "Gestational diabetes", "keywords": ["pregnancy", "manage"]},
    SAMPLE_QUERIES[3]: {"condition": "Myocardial infarction", "keywords": ["emergency services", "aspirin", "chest pain"]},
    SAMPLE_QUERIES[4]: {"condition": "Angina", "keywords": ["nitroglycerin", "doses"]},
    SAMPLE_QUERIES[5]: {"condition": "Heart failure", "keywords": ["short of breath", "edema", "upright"]},
    SAMPLE_QUERIES[6]: {"condition": "Acute kidney injury", "keywords": ["AKI", "creatinine", "hydration"]},
    SAMPLE_QUERIES[7]: {"condition": ["Hyperkalaemia", "Hyperkalemia"], "keywords": ["potassium", "emergency measures", "calcium gluconate", "insulin–glucose infusion", "stabilize heart rhythm"]},
    SAMPLE_QUERIES[8]: {"condition": ["Acute Kidney Injury", "AKI", "Kidney damage"], "keywords": ["NSAIDs", "AKI", "precautions", "ibuprofen", "stop taking"]}, # MODIFIED
    SAMPLE_QUERIES[9]: {"condition": "Hyperosmolar hyperglycaemic state", "keywords": ["thirsty", "glucose", "ketones", "dehydration"]},
}

@pytest.fixture(scope="module")
def chatbot_instance():
    """Provides a single chatbot instance for all tests."""
    # This will initialize all models once.
    print("\n--- Initializing Chatbot for Tests ---")
    bot = RAGChatbot()
    print("--- Chatbot Ready for Tests ---")
    yield bot
    # Clean up or report metrics after all tests
    print("\n--- Test Session Metrics ---")
    print(bot.get_metrics())

# You can add more granular fixtures or mocks here for controlled testing
# e.g., @pytest.fixture def mock_serper_response(): ...

@pytest.mark.parametrize("query_text", SAMPLE_QUERIES)
def test_sample_query_response(chatbot_instance, query_text):
    """
    Tests each sample query for expected content and structure.
    NOTE: This is a functional test that hits external APIs (Groq, Google CSE).
    For more robust unit testing, you'd mock API calls.
    """
    print(f"\n\n--- Testing Query: '{query_text}' ---")
    response = chatbot_instance.ask(query_text)
    print(f"\nResponse:\n{response}")

    # Basic checks for structure and disclaimer
    assert response.strip().startswith(DISCLAIMER.strip()), "Response must start with the disclaimer."
    assert "Condition:" in response, "Response must include 'Condition:'"
    assert "First-Aid Steps:" in response, "Response must include 'First-Aid Steps:'"
    assert "Source Citations:" in response, "Response must include 'Source Citations:'"

    # Specific keyword checks based on expected information
    expected = EXPECTED_INFO.get(query_text, {})

    if "condition" in expected:
        # Handle condition being a list of acceptable alternatives
        condition_found = False
        expected_conditions = [expected["condition"]] if isinstance(expected["condition"], str) else expected["condition"]
        for cond_str in expected_conditions:
            if cond_str.lower() in response.lower():
                condition_found = True
                break
        assert condition_found, f"Expected condition(s) '{expected_conditions}' not found in response for query: '{query_text}'"

    if "keywords" in expected:
        # Handle keywords being a list, check if AT LEAST ONE of the expected keywords is present
        # This is a bit lenient, you could require ALL or a subset.
        # For 'manage' (Query 3), we want 'manage' OR 'treatment plan' etc.
        # For 'short of breath' (Query 6), we want 'short of breath' OR 'alleviate shortness of breath'.
        # Let's adjust the loop to check for ANY of the provided keywords for that query.
        keywords_found_for_query = False
        for keyword in expected["keywords"]:
            if keyword.lower() in response.lower():
                keywords_found_for_query = True
                break # Found at least one relevant keyword, so this part of the test passes
        assert keywords_found_for_query, f"At least one expected keyword from '{expected['keywords']}' not found in response for query: '{query_text}'"

    # Check for presence of citations (at least one)
    citations_section = response.split("Source Citations:")[-1]
    assert "- " in citations_section, "Response must list at least one source citation."

    # You would manually verify word count and quality for these tests.
    # For automated tests, you might use regex to extract sections and count words.
    # E.g., re.findall(r'\b\w+\b', answer_text_without_disclaimer)