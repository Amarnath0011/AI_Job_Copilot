from pathlib import Path

# Upload directory
UPLOAD_DIR = Path("app/uploads")

# Chroma persistence directory
VECTOR_DB_DIR = "app/vectorstore"

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Chunk settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100