from langchain_core.documents import Document

from app.ingestion.storage import load_chunks


def expand_context(
    selected_documents: list[tuple[Document, float]],
    window: int = 1,
) -> list[Document]:
    """
    Expand selected chunks with nearby chunks from the
    persisted, ordered chunk store.
    """

    all_chunks = load_chunks()

    chunk_index = {
        document.metadata["chunk_id"]: index
        for index, document in enumerate(all_chunks)
        if "chunk_id" in document.metadata
    }

    expanded_documents = []
    seen_chunk_ids = set()

    for document, _score in selected_documents:

        chunk_id = document.metadata.get("chunk_id")

        if chunk_id not in chunk_index:
            expanded_documents.append(document)
            continue

        index = chunk_index[chunk_id]

        start = max(0, index - window)
        end = min(len(all_chunks), index + window + 1)

        source = document.metadata.get("source")

        for neighbor in all_chunks[start:end]:

            neighbor_source = neighbor.metadata.get("source")

            # Don't expand across different source documents.
            if neighbor_source != source:
                continue

            neighbor_id = neighbor.metadata.get("chunk_id")

            if neighbor_id in seen_chunk_ids:
                continue

            seen_chunk_ids.add(neighbor_id)
            expanded_documents.append(neighbor)

    return expanded_documents