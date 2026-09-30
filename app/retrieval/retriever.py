from app.config import RETRIEVAL_K
from app.retrieval.vectorstore import get_vectorstore


def get_retriever(k: int | None = None):

    vectorstore = get_vectorstore()

    candidate_k = k if k is not None else RETRIEVAL_K

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": candidate_k,
        },
    )