import sys
import argparse
from app.models.database import SessionLocal, init_db
from app.services.nlp_engine import load_model, load_intents, predict_intent
from app.services.file_indexer import search_files

def setup():
    init_db()
    load_model()
    load_intents()

def chat():
    print("Offline Chatbot CLI initialized. Type 'quit' to exit.")
    db = SessionLocal()
    try:
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['quit', 'exit']:
                break
                
            # Check edge gallery search heuristic
            lower_msg = user_input.lower()
            file_keywords = ["show", "search", "find", "file", "notes", "gallery", "document"]
            
            if any(keyword in lower_msg for keyword in file_keywords):
                print("Bot: Searching Edge Gallery...")
                results = search_files(db, user_input, top_k=1)
                if results and results[0]["score"] > 0.3:
                    best = results[0]
                    print(f"Bot: Found in {best['filename']} (Score: {best['score']:.2f}):\n{best['snippet']}")
                    continue
            
            intent, response = predict_intent(user_input)
            print(f"Bot: {response} [Intent: {intent}]")
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Offline Chatbot Backend CLI")
    parser.add_argument("--mode", type=str, choices=["chat", "setup"], default="chat", help="Mode to run the CLI in")
    
    args = parser.parse_args()
    
    if args.mode == "setup":
        print("Setting up database and downloading models if not present...")
        setup()
        print("Setup complete.")
    elif args.mode == "chat":
        setup()
        chat()
