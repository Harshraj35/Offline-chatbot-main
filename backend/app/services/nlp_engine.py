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

def load_intents(filepath: str = None):
    global intent_embeddings, intents_data
    
    if filepath is None:
        # Get the path relative to this file: ../../data/intents.json
        # This is more robust than using a hardcoded relative path if run from different CWDs
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_file_dir, "..", "..", "data", "intents.json")
    
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
                
        if all_patterns:
            # Ensure model is loaded before encoding
            if model is None:
                load_model()
                
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
    global intent_embeddings
    
    # Auto-load intents if they haven't been loaded yet
    # Check if it's empty or doesn't have the expected keys
    if not intent_embeddings or not isinstance(intent_embeddings, dict) or "embeddings" not in intent_embeddings:
        logger.info("Intent embeddings not found. Attempting to load intents...")
        load_intents()
        
    # Final check after attempt to load
    if not intent_embeddings or not isinstance(intent_embeddings, dict) or "embeddings" not in intent_embeddings:
        return "error", "I'm sorry, I don't have any trained intents yet. Please ensure data/intents.json is present and valid."
        
    try:
        query_emb = get_embedding(text).reshape(1, -1)
        db_embs = intent_embeddings["embeddings"]
        
        similarities = cosine_similarity(query_emb, db_embs)[0]
        best_match_idx = np.argmax(similarities)
        best_score = similarities[best_match_idx]
        
        logger.info(f"Top intent match score: {best_score:.4f}")
        
        if best_score >= threshold:
            matched_intent = intent_embeddings["mappings"][best_match_idx]
            tag = matched_intent.get("tag")
            
            import random
            response = random.choice(matched_intent.get("responses", ["I understood but have no response."]))
            
            # Special handling for gallery intents
            try:
                from app.services.gallery_service import gallery_service
                if tag == "gallery_skills":
                    skills = gallery_service.get_all_skills()
                    if skills:
                        skill_names = ", ".join([s['name'] for s in skills[:5]])
                        response += f"\n\nSome of the featured skills include: {skill_names}, and more!"
                elif tag == "gallery_models":
                    models = gallery_service.get_all_models()
                    if models:
                        model_names = ", ".join([m['name'] for m in models[:3]])
                        response += f"\n\nCurrently supported models include: {model_names}."
            except Exception as e:
                logger.warning(f"Could not fetch gallery info: {e}")
            
            return tag, response
        else:
            return "unknown", "I'm not quite sure I understand. Could you rephrase?"
    except Exception as e:
        logger.error(f"Error predicting intent: {e}")
        return "error", "Sorry, I encountered an internal error while processing your request."
