from langchain_chroma import Chroma

from app.config import VECTOR_DB_DIR
from app.services.embeddings import embedding_model


vector_store = Chroma(
    collection_name="job_copilot",
    embedding_function=embedding_model,
    persist_directory=VECTOR_DB_DIR
)