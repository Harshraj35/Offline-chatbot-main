# Offline Chatbot Backend

This is the fully offline backend for the EchoMind Chatbot, featuring a local NLP model for intent classification and an "Edge Gallery" for local file vector search.

## Features
- **FastAPI**: High-performance asynchronous API.
- **SQLite**: Fully local database for storing chat history and file metadata.
- **Sentence-Transformers**: Lightweight local embedding model (`all-MiniLM-L6-v2`) that runs on CPU for intent matching and semantic file search.
- **Edge Gallery**: Upload text or PDF files, extract text, generate embeddings, and search through them via the chatbot interface.

## Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.9+ installed.

### 2. Install Dependencies
Navigate to the `backend/` directory and install the required packages:

```bash
cd backend
pip install -r requirements.txt
```

### 3. Initialize the System & Models
Before running the server, you need to initialize the database and let the system download the local NLP model (this is a one-time download, ~90MB):

```bash
python cli.py --mode setup
```

### 4. Run the Server
Start the FastAPI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 10000 --reload
```

The API will be available at `http://localhost:8000`. You can view the interactive Swagger API docs at `http://localhost:8000/docs`.

### 5. CLI Testing
You can test the chatbot logic and file search directly in the terminal without starting the server:

```bash
python cli.py --mode chat
```

## API Endpoints

### Chat
- `POST /chat/`: Send a message and get an AI response.

### Edge Gallery
- `POST /gallery/upload`: Upload a file (`.txt`, `.pdf`, image).
- `GET /gallery/files`: List all files.
- `POST /gallery/search`: Perform a semantic search on uploaded files.
