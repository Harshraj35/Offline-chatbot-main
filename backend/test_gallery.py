import sys
import os

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_dir)

from app.services.nlp_engine import load_model, load_intents, predict_intent

def test_gallery_intents():
    print("Loading model and intents...")
    load_model()
    load_intents()

    queries = [
        "What AI skills do you have?",
        "Which models are supported?",
        "Tell me about your skills",
        "List all models"
    ]

    print("\nTesting queries:")
    for query in queries:
        tag, response = predict_intent(query)
        print(f"\nQuery: {query}")
        print(f"Predicted Tag: {tag}")
        print(f"Response: {response}")

if __name__ == "__main__":
    test_gallery_intents()
