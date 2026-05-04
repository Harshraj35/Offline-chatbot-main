import sys
print(f"Python version: {sys.version}")
try:
    import fastapi
    print(f"FastAPI version: {fastapi.__version__}")
except ImportError:
    print("FastAPI not installed")

try:
    import torch
    print(f"Torch version: {torch.__version__}")
except ImportError:
    print("Torch not installed")

try:
    from sentence_transformers import SentenceTransformer
    print("SentenceTransformers imported successfully")
except ImportError:
    print("SentenceTransformers not installed")
