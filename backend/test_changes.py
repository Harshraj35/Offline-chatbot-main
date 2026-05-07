import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.services.nlp_engine import predict_intent
from app.models.database import SessionLocal, GalleryFile
from app.services.file_indexer import search_files

def test_changes():
    print("--- Testing Intents ---")
    intents = [
        "Show me some coding examples or help me write some code.",
        "Explain an important concept to me.",
        "Help me with my homework or study materials."
    ]
    
    for query in intents:
        tag, response = predict_intent(query)
        print(f"Query: {query}")
        print(f"Tag: {tag}")
        print(f"Response: {response}\n")

    print("--- Testing Gallery Search ---")
    db = SessionLocal()
    search_queries = ["coding tips", "machine learning concept", "study strategies"]
    for query in search_queries:
        results = search_files(db, query, top_k=1)
        if results:
            print(f"Search: {query}")
            print(f"Found: {results[0]['filename']} (Score: {results[0]['score']:.4f})")
            print(f"Snippet: {results[0]['snippet']}\n")
    db.close()

if __name__ == "__main__":
    test_changes()
