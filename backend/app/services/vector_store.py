from langchain_chroma import Chroma

from app.services.embeddings import embedding_model

vector_store = Chroma(
    collection_name="resume",
    embedding_function=embedding_model,
    persist_directory="app/vectorstore"
)