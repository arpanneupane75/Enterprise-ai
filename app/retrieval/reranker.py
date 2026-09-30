from sentence_transformers import CrossEncoder
from langchain_core.documents import Document

RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

_reranker = None


def get_reranker() -> CrossEncoder:
    global _reranker

    if _reranker is None:
        _reranker = CrossEncoder(RERANKER_MODEL)

    return _reranker


def rerank_documents(
    question: str,
    documents: list[Document],
    top_k: int = 3,
) -> list[tuple[Document, float]]:

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

    seen_content = set()

    for document, score in ranked_documents:

        normalized_content = " ".join(
            document.page_content.lower().split()
        )

        if normalized_content in seen_content:
            continue

        seen_content.add(normalized_content)

        selected.append(
            (document, float(score))
        )

        if len(selected) >= top_k:
            break

    return selected