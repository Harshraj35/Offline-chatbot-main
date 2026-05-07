import os
import sys

# Add the backend directory to sys.path so we can import app
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app.models.database import SessionLocal, init_db
from app.services.file_indexer import process_and_store_file
from app.utils.logger import get_logger

logger = get_logger(__name__)

def populate():
    # Ensure DB is initialized
    init_db()
    
    db = SessionLocal()
    docs_dir = os.path.join(current_dir, "data", "initial_docs")
    
    if not os.path.exists(docs_dir):
        logger.error(f"Directory not found: {docs_dir}")
        return

    files = [f for f in os.listdir(docs_dir) if os.path.isfile(os.path.join(docs_dir, f))]
    
    for filename in files:
        file_path = os.path.join(docs_dir, filename)
        logger.info(f"Indexing {filename}...")
        
        with open(file_path, "rb") as f:
            content = f.read()
            
        tags = "initial_setup, " + filename.split(".")[0]
        process_and_store_file(
            db=db,
            filename=filename,
            file_type="text/plain",
            file_content=content,
            tags=tags
        )
        logger.info(f"Successfully indexed {filename}")

    db.close()

if __name__ == "__main__":
    populate()
