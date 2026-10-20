from app.rag.splitter import split_text
from app.rag.vector_store import vector_store


def store_document(
    text: str,
    source: str,
    document_type: str,
    session_id: str,
    user_id: str | None = None,
):
    documents = split_text(text)
    for doc in documents:
        doc.metadata.update({
            "source": source,
            "document_type": document_type,
            "session_id": session_id,
            "user_id": str(user_id) if user_id is not None else "legacy",
        })
    if documents:
        vector_store.add_documents(documents)
    return len(documents)
