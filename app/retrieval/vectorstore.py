from langchain_chroma import Chroma

from app.config import CHROMA_DIR, COLLECTION_NAME
from app.retrieval.embeddings import get_embeddings


def create_vectorstore(documents):
    embeddings = get_embeddings()

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
    )

    return vectorstore


def get_vectorstore():
    embeddings = get_embeddings()

    return Chroma(
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )