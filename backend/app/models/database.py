import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, LargeBinary
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Base directory of the project (backend folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_DIR = os.path.join(BASE_DIR, "backend", "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "chatbot.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    intent_detected = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class GalleryFile(Base):
    __tablename__ = "gallery_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), index=True, nullable=False)
    file_type = Column(String(50), nullable=False)
    tags = Column(String(255), nullable=True)
    text_content = Column(Text, nullable=True)
    # Storing embeddings as binary blob (NumPy array bytes)
    embedding_blob = Column(LargeBinary, nullable=True)
    upload_time = Column(DateTime, default=datetime.utcnow)

def init_db():
    # Ensure database directory exists
    os.makedirs(os.path.dirname(DATABASE_URL.replace("sqlite:///", "")), exist_ok=True)
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
