from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os

from app.models.schemas import FileMetadata, SearchRequest, SearchResult
from app.models.database import get_db, GalleryFile
from app.services.file_indexer import process_and_store_file, search_files
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/gallery", tags=["gallery"])

# Ensure edge_gallery upload dir exists
UPLOAD_DIR = "backend/data/edge_gallery"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=FileMetadata)
async def upload_file(
    file: UploadFile = File(...),
    tags: str = Form(""),
    db: Session = Depends(get_db)
):
    """Upload a file to the Edge Gallery."""
    logger.info(f"Received file upload: {file.filename}")
    try:
        content = await file.read()
        
        # Save file physically (optional, but good for Edge Gallery)
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(content)
            
        file_type = file.content_type or "unknown"
        
        # Process and extract text/embeddings
        new_db_file = process_and_store_file(
            db=db,
            filename=file.filename,
            file_type=file_type,
            file_content=content,
            tags=tags
        )
        
        return new_db_file
        
    except Exception as e:
        logger.error(f"Failed to upload file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files", response_model=List[FileMetadata])
def list_files(db: Session = Depends(get_db)):
    """List all files in the Edge Gallery."""
    files = db.query(GalleryFile).all()
    return files

@router.post("/search", response_model=List[SearchResult])
def search_gallery(request: SearchRequest, db: Session = Depends(get_db)):
    """Semantic search inside the Edge Gallery."""
    logger.info(f"Searching gallery for: {request.query}")
    results = search_files(db, request.query, top_k=request.top_k)
    return results
