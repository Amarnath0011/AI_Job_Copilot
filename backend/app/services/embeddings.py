from langchain_huggingface import HuggingFaceEmbeddings

from app.config import EMBEDDING_MODEL


embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)