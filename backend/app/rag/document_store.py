from app.rag.splitter import split_text
from app.rag.vector_store import vector_store


def store_document(
    text: str,
    source: str,
    document_type: str,
    session_id: str,
):
    documents = split_text(text)

    print(f"Number of chunks: {len(documents)}")

    for doc in documents:
        doc.metadata.update({
    "source": source,
    "document_type": document_type,
    "session_id": session_id,
     })

    vector_store.add_documents(documents)

    print("Documents stored successfully!")

    return len(documents)