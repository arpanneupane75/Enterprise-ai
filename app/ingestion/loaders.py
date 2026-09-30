from pathlib import Path

from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_core.documents import Document


DATA_DIR = Path("data/documents")


def load_documents() -> list[Document]:
    documents: list[Document] = []

    pdf_loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
    )

    documents.extend(pdf_loader.load())

    txt_loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )

    documents.extend(txt_loader.load())

    return documents