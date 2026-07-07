from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHUNK_SIZE, CHUNK_OVERLAP


splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)


def split_text(text: str):
    return splitter.create_documents([text])