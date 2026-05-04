from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.models.database import init_db
from app.services.nlp_engine import load_model, load_intents
from app.routes import chat, gallery
from app.utils.logger import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    logger.info("Initializing Database...")
    init_db()
    
    logger.info("Loading NLP Engine...")
    load_model()
    load_intents()
    
    logger.info("Backend Startup Complete.")
    yield
    # Shutdown tasks
    logger.info("Shutting down backend...")

app = FastAPI(
    title="Offline Chatbot Backend",
    description="Backend API for local NLP chatbot and Edge Gallery",
    version="1.0.0",
    lifespan=lifespan
)

# Setup CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(gallery.router)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Offline Chatbot Backend is running."}

if __name__ == "__main__":
    import uvicorn
    # Use 10000 to match Render and Frontend expectations
    uvicorn.run(app, host="127.0.0.1", port=10000)
