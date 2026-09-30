from app.retrieval.retriever import get_retriever
from app.retrieval.reranker import rerank_documents


# QUESTIONS = [
#     "What is the maximum number of paid holidays?",
#     "How many paid vacation days can be carried over per year?",
#     "When are employees paid?",
#     "How many paid sick days are provided per year?",
# ]

QUESTIONS = [
    "What is the maximum number of paid holidays?",
]


def inspect(question: str):
    retriever = get_retriever(k=10)
    documents = retriever.invoke(question)

    reranked = rerank_documents(
        question=question,
        documents=documents,
        top_k=10,
    )

    print("\n" + "=" * 80)
    print("QUESTION:", question)
    print("=" * 80)

    for rank, (document, score) in enumerate(reranked, start=1):
        print(f"\nRank {rank}")
        print(f"Chunk: {document.metadata.get('chunk_id')}")
        print(f"Score: {score:.4f}")
        print(f"Page: {document.metadata.get('page')}")
        print("Content:")
        print(document.page_content[:500])


if __name__ == "__main__":
    for question in QUESTIONS:
        inspect(question)