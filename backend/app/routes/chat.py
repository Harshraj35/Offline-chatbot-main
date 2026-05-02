from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.schemas import ChatRequest, ChatResponse
from app.models.database import get_db, Chat
from app.services.nlp_engine import predict_intent
from app.services.file_indexer import search_files
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
def handle_chat(request: ChatRequest, db: Session = Depends(get_db)):
    user_msg = request.message
    logger.info(f"Received message: {user_msg}")
    
    # First, let's see if this is a query about files (Edge Gallery search)
    # A simple heuristic: if the message contains words like "show", "search", "find", "file", "notes"
    lower_msg = user_msg.lower()
    file_keywords = ["show", "search", "find", "file", "notes", "gallery", "document"]
    
    is_file_query = any(keyword in lower_msg for keyword in file_keywords)
    
    intent = None
    response_text = ""
    source = "nlp_engine"
    
    if is_file_query:
        # Perform Edge Gallery Search
        logger.info("Detected file query intent, searching Edge Gallery...")
        results = search_files(db, user_msg, top_k=1)
        if results and results[0]["score"] > 0.3:
            best_match = results[0]
            response_text = f"I found something relevant in '{best_match['filename']}':\n{best_match['snippet']}"
            intent = "edge_gallery_search"
            source = "edge_gallery"
        else:
            response_text = "I searched your local files but couldn't find anything highly relevant."
            intent = "edge_gallery_not_found"
    
    # If not a file query or file not found, fall back to general intent prediction
    if not response_text or intent == "edge_gallery_not_found":
        intent_tag, reply = predict_intent(user_msg)
        response_text = reply
        intent = intent_tag
    
    # Save to history
    new_chat = Chat(
        user_message=user_msg,
        bot_response=response_text,
        intent_detected=intent
    )
    db.add(new_chat)
    db.commit()
    
    return ChatResponse(
        response=response_text,
        intent=intent,
        source=source
    )
