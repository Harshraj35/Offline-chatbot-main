import os
import io
import PyPDF2
from sqlalchemy.orm import Session
from app.models.database import GalleryFile
from app.services.nlp_engine import get_embedding
from app.utils.logger import get_logger
import numpy as np

logger = get_logger(__name__)

def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """Extracts text from supported file types."""
    ext = os.path.splitext(filename)[1].lower()
    text = ""
    
    try:
        if ext == ".txt":
            text = file_content.decode("utf-8")
        elif ext == ".pdf":
            reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        else:
            # For images or unsupported types, we can only rely on filename/tags
            text = ""
    except Exception as e:
        logger.error(f"Error extracting text from {filename}: {e}")
        
    return text.strip()

def process_and_store_file(db: Session, filename: str, file_type: str, file_content: bytes, tags: str = ""):
    """Extracts text, generates embedding, and saves to database."""
    text_content = extract_text_from_file(file_content, filename)
    
    embedding_blob = None
    # We combine text content, filename, and tags for a rich embedding
    content_to_embed = f"{filename} {tags} {text_content}".strip()
    
    if content_to_embed:
        try:
            emb = get_embedding(content_to_embed)
            # Store as bytes to save in SQLite LargeBinary
            embedding_blob = emb.tobytes()
        except Exception as e:
            logger.error(f"Error generating embedding for {filename}: {e}")

    new_file = GalleryFile(
        filename=filename,
        file_type=file_type,
        tags=tags,
        text_content=text_content,
        embedding_blob=embedding_blob
    )
    
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file

def search_files(db: Session, query: str, top_k: int = 3):
    """Searches the database for relevant files using cosine similarity."""
    files = db.query(GalleryFile).filter(GalleryFile.embedding_blob.isnot(None)).all()
    
    if not files:
        return []
        
    query_emb = get_embedding(query).reshape(1, -1)
    
    results = []
    for f in files:
        # Reconstruct numpy array from bytes
        file_emb = np.frombuffer(f.embedding_blob, dtype=np.float32).reshape(1, -1)
        
        from sklearn.metrics.pairwise import cosine_similarity
        score = cosine_similarity(query_emb, file_emb)[0][0]
        
        # Simple snippet generation
        snippet = f.text_content[:200] + "..." if f.text_content and len(f.text_content) > 200 else f.text_content
        if not snippet:
            snippet = f"File: {f.filename} | Tags: {f.tags}"
            
        results.append({
            "id": f.id,
            "filename": f.filename,
            "snippet": snippet,
            "score": float(score)
        })
        
    # Sort by descending score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
