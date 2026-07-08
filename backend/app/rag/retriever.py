from app.rag.vector_store import vector_store


def get_retriever(
    document_type: str = "resume",
    k: int = 4,
):
    return vector_store.as_retriever(
        search_kwargs={
            "k": k,
            "filter": {
                "document_type": document_type
            }
        }
    )