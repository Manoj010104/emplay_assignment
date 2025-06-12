# main.py

from chatbot.rag_chatbot import RAGChatbot

def main():
    chatbot = RAGChatbot()
    print("\n--- Welcome to the RAG-Powered First-Aid Chatbot ---")
    print("Focus areas: Diabetes, Cardiac, Renal Emergencies.")
    print("Always remember: This bot provides educational first-aid guidance only. It is not a substitute for professional medical advice.")
    print("In case of a medical emergency, call emergency services immediately.")
    print("\nType your medical symptoms or questions. Type 'exit' to quit.")

    while True:
        user_query = input("\nYour symptoms: ").strip()
        if user_query.lower() == 'exit':
            break
        if not user_query:
            print("Please enter some symptoms.")
            continue

        print("\nProcessing your request...")
        response = chatbot.ask(user_query)
        print("\n--- Chatbot's First-Aid Guidance ---")
        print(response)

    print("\n--- End of Session Metrics ---")
    print(chatbot.get_metrics())
    print("Thank you for using the chatbot. Stay safe!")

if __name__ == "__main__":
    main()