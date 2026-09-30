from langchain_core.documents import Document

from app.retrieval.reranker import get_reranker


def select_evidence(
    documents: list[Document],
    question: str,
    max_sources: int = 3,
) -> list[tuple[Document, float]]:
    """
    Select the most relevant evidence chunks from the
    expanded context using the CrossEncoder.
    """

    if not documents:
        return []

    reranker = get_reranker()

    pairs = [
        (question, document.page_content)
        for document in documents
    ]

    scores = reranker.predict(pairs)

    ranked_documents = sorted(
        zip(documents, scores),
        key=lambda item: item[1],
        reverse=True,
    )

    selected = []
    seen_chunk_ids = set()

    for document, score in ranked_documents:

        chunk_id = document.metadata.get("chunk_id")

        if chunk_id in seen_chunk_ids:
            continue

        seen_chunk_ids.add(chunk_id)

        selected.append(
            (document, float(score))
        )

        if len(selected) >= max_sources:
            break

    return selected