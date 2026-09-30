from app.ingestion.chunking import split_documents
from app.ingestion.loaders import load_documents
from app.ingestion.storage import save_chunks
from app.retrieval.vectorstore import create_vectorstore


def remove_duplicate_chunks(documents):
    seen = set()
    unique_documents = []

    for document in documents:
        content = document.page_content.strip()

        if not content:
            continue

        if content in seen:
            continue

        seen.add(content)
        unique_documents.append(document)

    return unique_documents


def run_ingestion():
    print("Loading documents...")

    documents = load_documents()

    print(f"Loaded {len(documents)} documents")

    print("Splitting documents...")

    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    print("Removing duplicate chunks...")

    chunks = remove_duplicate_chunks(chunks)

    print(f"Remaining unique chunks: {len(chunks)}")

    print("Saving processed chunks...")

    save_chunks(chunks)

    print("Processed chunks saved successfully.")

    print("Creating vector database...")

    vectorstore = create_vectorstore(chunks)

    print("Vector database created successfully.")

    return vectorstore


if __name__ == "__main__":
    run_ingestion()