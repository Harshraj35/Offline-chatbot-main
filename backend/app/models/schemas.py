from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "en"

class ChatResponse(BaseModel):
    response: str
    intent: Optional[str] = None
    source: Optional[str] = None

class FileMetadata(BaseModel):
    id: int
    filename: str
    file_type: str
    tags: Optional[str] = None
    
    class Config:
        from_attributes = True

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

class SearchResult(BaseModel):
    filename: str
    snippet: str
    score: float
