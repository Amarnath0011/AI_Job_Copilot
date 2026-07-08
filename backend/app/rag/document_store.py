from app.rag.splitter import split_text
from app.rag.vector_store import vector_store


def store_document(text: str, source: str, document_type: str):
    documents = split_text(text)

    print(f"Number of chunks: {len(documents)}")

    for doc in documents:
        doc.metadata.update({
            "source": source,
            "document_type": document_type
        })

    vector_store.add_documents(documents)

    print("Documents stored successfully!")

    return len(documents)