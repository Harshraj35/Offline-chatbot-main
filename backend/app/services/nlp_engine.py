import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Lightweight model suitable for offline CPU use
MODEL_NAME = "all-MiniLM-L6-v2"
model = None

intent_embeddings = []
intents_data = []

def load_model():
    global model
    logger.info(f"Loading NLP model: {MODEL_NAME}...")
    try:
        model = SentenceTransformer(MODEL_NAME)
        logger.info("Model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise e

def load_intents(filepath: str = "backend/data/intents.json"):
    global intent_embeddings, intents_data
    if not os.path.exists(filepath):
        logger.warning(f"Intents file not found at {filepath}. Skipping intent loading.")
        return
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        intents_data = data.get("intents", [])
        
        # Prepare phrases for embedding
        all_patterns = []
        pattern_to_intent = []
        
        for intent in intents_data:
            for pattern in intent.get("patterns", []):
                all_patterns.append(pattern)
                pattern_to_intent.append(intent)
                
        if all_patterns and model:
            logger.info(f"Encoding {len(all_patterns)} intent patterns...")
            embeddings = model.encode(all_patterns)
            
            intent_embeddings = {
                "embeddings": embeddings,
                "mappings": pattern_to_intent
            }
            logger.info("Intents loaded and encoded successfully.")
    except Exception as e:
        logger.error(f"Failed to load intents: {e}")

def get_embedding(text: str) -> np.ndarray:
    """Generate embedding for a single string."""
    if model is None:
        load_model()
    return model.encode([text])[0]

def predict_intent(text: str, threshold: float = 0.5):
    """Predict the intent of a given text using cosine similarity."""
    if not intent_embeddings or "embeddings" not in intent_embeddings:
        return None, "I'm sorry, I don't have any trained intents yet."
        
    try:
        query_emb = get_embedding(text).reshape(1, -1)
        db_embs = intent_embeddings["embeddings"]
        
        similarities = cosine_similarity(query_emb, db_embs)[0]
        best_match_idx = np.argmax(similarities)
        best_score = similarities[best_match_idx]
        
        if best_score >= threshold:
            matched_intent = intent_embeddings["mappings"][best_match_idx]
            import random
            response = random.choice(matched_intent.get("responses", ["I understood but have no response."]))
            return matched_intent.get("tag"), response
        else:
            return "unknown", "I'm not quite sure I understand. Could you rephrase?"
    except Exception as e:
        logger.error(f"Error predicting intent: {e}")
        return "error", "Sorry, I encountered an internal error while processing your request."
