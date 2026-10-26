from typing import Any
from langchain_core.documents import Document

from app.rag.vector_store import vector_store


def get_retriever(
    document_type: str = "resume",
    k: int = 2,
    session_id: str | None = None,
    user_id: int | str | None = None,
):
    """
    Returns a LangChain retriever filtered by document type and session/user.
    """
    filters = [{"document_type": document_type}]
    if session_id is not None:
        filters.append({"session_id": session_id})
    if user_id is not None:
        filters.append({"user_id": str(user_id)})
    where = filters[0] if len(filters) == 1 else {"$and": filters}
    return vector_store.as_retriever(search_kwargs={"k": k, "filter": where})


def retrieve_requirement_chunks(
    query: str,
    session_id: str,
    k: int = 2,
    store: Any = None,
) -> list[Document]:
    """
    Requirement-specific retrieval filtered strictly to the provided session_id.
    Deduplicates overlapping chunk contents and guarantees session isolation.
    """
    if not session_id or not session_id.strip():
        return []

    target_store = store or vector_store
    where = {
        "$and": [
            {"document_type": "resume"},
            {"session_id": session_id.strip()},
        ]
    }

    try:
        docs = target_store.similarity_search(query, k=k, filter=where)
    except Exception:
        return []

    unique_docs: list[Document] = []
    seen_contents: set[str] = set()

    for doc in docs:
        content_key = doc.page_content.strip()
        if content_key and content_key not in seen_contents:
            seen_contents.add(content_key)
            unique_docs.append(doc)

    return unique_docs
