from app.rag.vector_store import vector_store


def get_retriever(
    document_type: str = "resume",
    k: int = 2,
    session_id: str | None = None,
    user_id: int | str | None = None,
):
    filters = [{"document_type": document_type}]
    if session_id is not None:
        filters.append({"session_id": session_id})
    if user_id is not None:
        filters.append({"user_id": str(user_id)})
    where = filters[0] if len(filters) == 1 else {"$and": filters}
    return vector_store.as_retriever(search_kwargs={"k": k, "filter": where})
