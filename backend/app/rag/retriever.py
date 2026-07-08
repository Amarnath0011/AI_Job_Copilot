from app.rag.vector_store import vector_store


def get_retriever(
    document_type: str | None = None,
    session_id: str | None = None,
    k: int = 4,
):
    """
    Returns a Chroma retriever with optional metadata filters.

    Args:
        document_type: Filter by document type (resume, job_description, etc.)
        session_id: Filter by user/session.
        k: Number of relevant chunks to retrieve.

    Returns:
        LangChain Retriever
    """

    search_kwargs = {
        "k": k
    }

    filters = {}

    if document_type:
        filters["document_type"] = document_type

    if session_id:
        filters["session_id"] = session_id

    if filters:
        search_kwargs["filter"] = filters

    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )